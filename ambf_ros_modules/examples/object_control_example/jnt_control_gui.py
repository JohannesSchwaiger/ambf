#!/usr/bin/env python
# //==============================================================================
# /*
#     Software License Agreement (BSD License)
#     Copyright (c) 2020, AMBF
#     (https://github.com/WPI-AIM/ambf)
#
#     All rights reserved.
#
#     Redistribution and use in source and binary forms, with or without
#     modification, are permitted provided that the following conditions
#     are met:
#
#     * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above
#     copyright notice, this list of conditions and the following
#     disclaimer in the documentation and/or other materials provided
#     with the distribution.
#
#     * Neither the name of authors nor the names of its contributors may
#     be used to endorse or promote products derived from this software
#     without specific prior written permission.
#
#     THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#     "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#     LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#     FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#     COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#     INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#     BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#     LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#     CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#     LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
#     ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#     POSSIBILITY OF SUCH DAMAGE.
#
#     \author    <amunawar@wpi.edu>
#     \author    Adnan Munawar
#     \version   1.0
# */
# //==============================================================================

import functools
import sys
if sys.version_info[0] >= 3:
    from tkinter import *
else:
    from Tkinter import *


class JointGUI:
    def __init__(self, obj_name, num_jnts, jnt_names):
        self.App = Tk()
        self.jnt_cmds = []
        self.jnt_mode = []
        self.cmd_scales = []
        self.resolution = None

        self._cmd_sliders = []

        self.create_gui(self.App, obj_name, num_jnts, jnt_names)

    def get_app_handle(self):
        return self.App

    # Define Callbacks for Tkinter GUI Sliders
    def scale_cb(self, val, idx):
        self.cmd_scales[idx] = float(val)

    # Define Callbacks for Tkinter GUI Sliders
    def slider_cb(self, val, idx):
        self.jnt_cmds[idx] = float(val)

    # Define Callbacks for Tkinter GUI Sliders
    def effort_button_cb(self, idx):
        self.jnt_mode[idx] = 0

    # Define Callbacks for Tkinter GUI Sliders
    def position_button_cb(self, idx):
        self.jnt_mode[idx] = 1

    # Define Callbacks for Tkinter GUI Sliders
    def velocity_button_cb(self, idx):
        self.jnt_mode[idx] = 2

    # Define Callbacks for Tkinter GUI Sliders
    def reset_scale_cb(self):
        for cs in self.cmd_scales:
            cs.set('1.0')

    # Define Callbacks for Tkinter GUI Sliders
    def reset_cmds_cb(self):
        for sl in self._cmd_sliders:
            sl.set(0.0)

    def create_gui(self, app, obj_name, num_jnts, jnt_names):
        _width = 20
        _length = 300
        _resolution = 0.0001
        _min = -1
        _max = 1
        check_buttons = []
        self.jnt_cmds = [0.0] * num_jnts
        self.jnt_mode = [0]*num_jnts
        self.cmd_scales = [0]*num_jnts
        self.resolution = _resolution

        # obj_label = Label(app, text='CONTROLLING OBJECT: ' + obj_name, fg="Red")
        # obj_label.pack(row=0, columnspan=2, pady=5)

        for i in range(2*num_jnts):
            if i % 2 == 0:
                sv = StringVar()
                scale_input = Entry(app, textvariable=sv)
                scale_input.grid(row=i, column=0)
                sv.set("1.0")
                jidx = int(i/2)
                self.cmd_scales[jidx] = sv

                slider = Scale(app, from_=_min, to=_max, resolution=_resolution, orient=HORIZONTAL,
                                 command=functools.partial(self.slider_cb, idx=jidx))
                slider.grid(row=i, column=1)
                self._cmd_sliders.append(slider)

                v = IntVar(value=0)
                eff_cb = Radiobutton(app, text="Effort", variable=v, indicatoron=False, value=0,
                                  command=functools.partial(self.effort_button_cb, idx=jidx))
                eff_cb.grid(row=i, column=2)

                pos_cb = Radiobutton(app, text="Position", variable=v, indicatoron=False, value=1,
                                  command=functools.partial(self.position_button_cb, idx=jidx))
                pos_cb.grid(row=i, column=3)

                vel_cb = Radiobutton(app, text="Velocity", variable=v, indicatoron=False, value=2,
                                  command=functools.partial(self.velocity_button_cb, idx=jidx))
                vel_cb.grid(row=i, column=4)

            else:
                scale_label = Label(app, text='Cmd ('+str(jidx) + ') Scale')
                scale_label.grid(row=i, column=0)

                label = Label(app, text=jnt_names[jidx])
                label.grid(row=i, column=1)

        reset_scale_btn = Button(app, text='Reset Scales', command=self.reset_scale_cb)
        reset_scale_btn.grid(row=num_jnts*2, column=0)

        reset_cmd_btn = Button(app, text='Reset Cmds', command=self.reset_cmds_cb)
        reset_cmd_btn.grid(row=num_jnts*2, column=1)
        self.init_keyboard_control(app)

    def init_keyboard_control(self, app):
        self.key_stack = []
        inputs = [('y', 'Joint1Open'),
                  ('Y', 'Joint1Open'),
                  ('x', 'Joint1Close'),
                  ('X', 'Joint1Close'),
                  ('v', 'Joint2Open'),
                  ('V', 'Joint2Open'),
                  ('c', 'Joint2Close'),
                  ('C', 'Joint2Close'),
                  ('q', 'GrabberClose'),
                  ('Q', 'GrabberClose'),
                  ('e', 'GrabberOpen'),
                  ('E', 'GrabberOpen'),
                  ('Shift_L', 'Slow')]

        for key, direction in inputs:
            app.bind('<KeyPress-' + key + '>', functools.partial(key_down, self, direction))
            app.bind('<KeyRelease-' + key + '>', functools.partial(key_up, self, direction))

        app.bind('<FocusOut>', self.on_focus_out)

    def on_focus_out(self, event):
        self.key_stack = []


def key_down(app, direction, event):
    app.key_stack.append(direction)

def key_up(app, direction, event):
    app.key_stack.remove(direction)
