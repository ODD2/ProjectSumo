function [a,b] = TestEntry()
%TEST Summary of this function goes here
%   Detailed explanation goes here
    SIM_CONF = struct("rbf_h",100.0,...
                      "rbf_w",2.0,...
                      "max_pwr_dBm",23.0 ...
    ); 

    QoS_GP_CONF = {...
        {...
            struct( "gid",0.0, ...
                    "rbf_w",2.0, ...
                    "rbf_h",1.0, ...
                    "sinr_max",15.917700322259982,...
                    "pwr_req_dBm",23.0,...
                    "pwr_ext_dBm",-100.0,...
                    "rem_bits",13440.0,...
                    "mem_num",39.0 ...
            )...
        }...
        {...
            struct( "gid",1.0, ...
                    "rbf_w",2.0, ...
                    "rbf_h",1.0, ...
                    "sinr_max",15.067238406151144,...
                    "pwr_req_dBm",22.968,...
                    "pwr_ext_dBm",1.657666494551771,...
                    "rem_bits",59864.0,...
                    "mem_num",39.0 ...
            )...
%             struct( "gid",2, ...
%                     "rbf_w",1, ...
%                     "rbf_h",2, ...
%                     "sinr_max",30,...
%                     "pwr_req_dBm",22.964,...
%                     "pwr_ext_dBm",2.1671,...
%                     "rem_bits",3015460,...
%                     "mem_num",37 ...
%             )...
        }...
    };
%     QoS_GP_CONF = {};
    [a,b] = PlannerV1(SIM_CONF,QoS_GP_CONF);
end

