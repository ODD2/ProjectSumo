function [a,b] = TestEntry()
%TEST Summary of this function goes here
%   Detailed explanation goes here
    SIM_CONF = struct("rbf_h",50.0,...
                      "rbf_w",2.0,...
                      "max_pwr_dBm",23.0 ...
    ); 

    QoS_GP_CONF = {...
        {...
            struct( "gid",0, ...
                    "rbf_w",1, ...
                    "rbf_h",2, ...
                    "sinr_max",35.603482825755734,...
                    "pwr_req_dBm",23,...
                    "pwr_ext_dBm",0,...
                    "rem_bits",23330.0,...
                    "mem_num",4.0 ...
            )...
        }...
        {...
            struct( "gid",1, ...
                    "rbf_w",2, ...
                    "rbf_h",1, ...
                    "sinr_max",17,...
                    "pwr_req_dBm",23,...
                    "pwr_ext_dBm",0,...
                    "rem_bits",20000,...
                    "mem_num",4.0 ...
            )...
            struct( "gid",2, ...
                    "rbf_w",1, ...
                    "rbf_h",2, ...
                    "sinr_max",30,...
                    "pwr_req_dBm",23,...
                    "pwr_ext_dBm",0,...
                    "rem_bits",30000,...
                    "mem_num",4.0 ...
            )...
        }...
    };
%     QoS_GP_CONF = {};
    [a,b] = NomaPlannerV1(SIM_CONF,QoS_GP_CONF);
end

