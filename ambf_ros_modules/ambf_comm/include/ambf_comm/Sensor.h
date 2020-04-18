//==============================================================================
/*
    Software License Agreement (BSD License)
    Copyright (c) 2019, AMBF
    (www.aimlab.wpi.edu)

    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions
    are met:

    * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above
    copyright notice, this list of conditions and the following
    disclaimer in the documentation and/or other materials provided
    with the distribution.

    * Neither the name of authors nor the names of its contributors may
    be used to endorse or promote products derived from this software
    without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
    FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
    COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
    BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
    LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
    ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.

    \author    <http://www.aimlab.wpi.edu>
    \author    <amunawar@wpi.edu>
    \author    Adnan Munawar
    \version   $
*/
//==============================================================================

#ifndef SENSOR_H
#define SENSOR_H

#include <string>
#include "ambf_comm/SensorRosCom.h"

// This struct is almost identical to the data in SensorCmd ros_msg
// but is explicitly defined to removed ros_msgs from AMBF and a
// layer of abstraction in between
struct SensorCommand{
    SensorCommand(){
    }
    // Call this update method to assign all the fields from ros_msg
    // to this struct
    void update(const ambf_msgs::SensorCmd* cmd){

    }
};

namespace ambf_comm{
class Sensor: public SensorRosCom{
public:
    Sensor(std::string a_name, std::string a_namespace, int a_freq_min, int a_freq_max, double time_out);
    inline void set_name(std::string name){m_State.name.data = name;}
    void cur_position(double px, double py, double pz);
    void cur_orientation(double roll, double pitch, double yaw);
    void cur_orientation(double qx, double qy, double qz, double qw);
    void cur_force(double fx, double fy, double fz);
    void cur_torque(double nx, double ny, double nz);
    void update_af_cmd();
    void set_wall_time(double a_sec);
    inline void set_sim_time(double a_sec){ m_State.sim_time = a_sec;}
    inline void increment_sim_step(){m_State.sim_step++;}
    inline void set_sim_step(uint step){m_State.sim_step = step;}
    // This method is to set any additional data that could for debugging purposes or future use
    void set_userdata(float a_data);
    // This method is to set any additional data that could for debugging purposes or future use
    void set_userdata(std::vector<float> &a_data);
    void set_children_names(std::vector<std::string> children_names);
    void set_joint_names(std::vector<std::string> joint_names);
    void set_joint_positions(std::vector<float> joint_positions);
    SensorCommand m_SensorCommand;
};
}

#endif