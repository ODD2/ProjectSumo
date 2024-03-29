function [a,b] = TestEntry()
%TEST Summary of this function goes here
%   Detailed explanation goes here
    SIM_CONF = struct("rbf_h",50.0,...
                      "rbf_w",2.0,...
                      "max_pwr_dBm",23.0 ...
    ); 
    QoS_GP_CONF = {
        {...
            struct('gid', 0.0, 'qos', 0.0, 'rbf_w', 1.0, 'rbf_h', 2.0, 'sinr_max', 23.712045618855058, 'pwr_req_dBm', 22.973, 'pwr_ext_dBm', 0.9223015226843518, 'rem_bits', 4712.0, 'mem_num', 71.0, 'eager_rate', 36.63437309374906)...
             struct('gid', 1.0, 'qos', 0.0, 'rbf_w', 1.0, 'rbf_h', 2.0, 'sinr_max', 23.712045618855058, 'pwr_req_dBm', 22.973, 'pwr_ext_dBm', 0.9223015226843518, 'rem_bits', 5012.0, 'mem_num', 20.0, 'eager_rate', 52.63437309374906)...
        },...
        {...
            struct('gid', 5.0, 'qos', 1.0, 'rbf_w', 2.0, 'rbf_h', 1.0, 'sinr_max', 35.174129219912174, 'pwr_req_dBm', 22.956, 'pwr_ext_dBm', 3.034702226027002, 'rem_bits', 10712.0, 'mem_num', 17.0, 'eager_rate', 55.13946065977497)...
            struct('gid', 4.0, 'qos', 1.0, 'rbf_w', 2.0, 'rbf_h', 1.0, 'sinr_max', 29.93949825941053, 'pwr_req_dBm', 22.959, 'pwr_ext_dBm', 2.729511581869497, 'rem_bits', 14792.0, 'mem_num', 10.0, 'eager_rate', 30.285257579987405)...
            struct('gid', 7.0, 'qos', 1.0, 'rbf_w', 2.0, 'rbf_h', 1.0, 'sinr_max', 38.548690819308135, 'pwr_req_dBm', 22.955, 'pwr_ext_dBm', 3.1318014527925526, 'rem_bits', 3688.0, 'mem_num', 9.0, 'eager_rate', 87.80345203054216)...
            struct('gid', 2.0, 'qos', 1.0, 'rbf_w', 2.0, 'rbf_h', 1.0, 'sinr_max', 24.740863098677366, 'pwr_req_dBm', 22.969, 'pwr_ext_dBm', 1.5202830452677776, 'rem_bits', 5640.0, 'mem_num', 9.0, 'eager_rate', 85.85339640344525)...
            struct('gid', 6.0, 'qos', 1.0, 'rbf_w', 2.0, 'rbf_h', 1.0, 'sinr_max', 38.8170972756655, 'pwr_req_dBm', 22.955, 'pwr_ext_dBm', 3.1318014527925526, 'rem_bits', 7240.0, 'mem_num', 10.0, 'eager_rate', 36.47458385930194)...
            struct('gid', 8.0, 'qos', 1.0, 'rbf_w', 2.0, 'rbf_h', 1.0, 'sinr_max', 28.355397019502817, 'pwr_req_dBm', 22.961, 'pwr_ext_dBm', 2.51331754988261, 'rem_bits', 216978.0, 'mem_num', 4.0, 'eager_rate', 0.605619464349728)...
        }...
    };

%     QoS_GP_CONF = {...
%         {...
%             struct( "gid",0.0, ...
%                     "rbf_w",2.0, ...
%                     "rbf_h",1.0, ...
%                     "sinr_max",15.917700322259982,...
%                     "pwr_req_dBm",23.0,...
%                     "pwr_ext_dBm",-100.0,...
%                     "rem_bits",123456789.0,...
%                     "mem_num",39.0, ...
%                     "eager_rate",1.0 ...
%             )...
%         }...
%         {...
%             struct( "gid",1.0, ...
%                     "rbf_w",2.0, ...
%                     "rbf_h",1.0, ...
%                     "sinr_max",100,...
%                     "pwr_req_dBm",23,...
%                     "pwr_ext_dBm",-100,...
%                     "rem_bits",59864.0,...
%                     "mem_num",39.0, ...
%                     "eager_rate",1.0 ...
%             )...
%              struct( "gid",2.0, ...
%                     "rbf_w",2.0, ...
%                     "rbf_h",1.0, ...
%                     "sinr_max",100,...
%                     "pwr_req_dBm",23,...
%                     "pwr_ext_dBm",-100,...
%                     "rem_bits",59864.0,...
%                     "mem_num",39.0, ...
%                     "eager_rate",1.0 ...
%             )...
%              struct( "gid",3.0, ...
%                     "rbf_w",2.0, ...
%                     "rbf_h",1.0, ...
%                     "sinr_max",100,...
%                     "pwr_req_dBm",23,...
%                     "pwr_ext_dBm",-100,...
%                     "rem_bits",59864.0,...
%                     "mem_num",39.0, ...
%                     "eager_rate",1.0 ...
%             )...
%              struct( "gid",4.0, ...
%                     "rbf_w",2.0, ...
%                     "rbf_h",1.0, ...
%                     "sinr_max",100,...
%                     "pwr_req_dBm",23,...
%                     "pwr_ext_dBm",-100,...
%                     "rem_bits",59864.0,...
%                     "mem_num",39.0, ...
%                     "eager_rate",1.0 ...
%             )...
%              struct( "gid",5.0, ...
%                     "rbf_w",2.0, ...
%                     "rbf_h",1.0, ...
%                     "sinr_max",100,...
%                     "pwr_req_dBm",23,...
%                     "pwr_ext_dBm",-100,...
%                     "rem_bits",59864.0,...
%                     "mem_num",39.0, ...
%                     "eager_rate",1.0 ...
%             )...
%              struct( "gid",6.0, ...
%                     "rbf_w",2.0, ...
%                     "rbf_h",1.0, ...
%                     "sinr_max",100,...
%                     "pwr_req_dBm",23,...
%                     "pwr_ext_dBm",-100,...
%                     "rem_bits",59864.0,...
%                     "mem_num",39.0, ...
%                     "eager_rate",1.0 ...
%             )...
%              struct( "gid",7.0, ...
%                     "rbf_w",2.0, ...
%                     "rbf_h",1.0, ...
%                     "sinr_max",100,...
%                     "pwr_req_dBm",23,...
%                     "pwr_ext_dBm",-100,...
%                     "rem_bits",59864.0,...
%                     "mem_num",39.0, ...
%                     "eager_rate",1.0 ...
%             )...
%              struct( "gid",8.0, ...
%                     "rbf_w",2.0, ...
%                     "rbf_h",1.0, ...
%                     "sinr_max",100,...
%                     "pwr_req_dBm",23,...
%                     "pwr_ext_dBm",-100,...
%                     "rem_bits",59864.0,...
%                     "mem_num",39.0, ...
%                     "eager_rate",1.0 ...
%             )...
%              struct( "gid",9.0, ...
%                     "rbf_w",2.0, ...
%                     "rbf_h",1.0, ...
%                     "sinr_max",100,...
%                     "pwr_req_dBm",23,...
%                     "pwr_ext_dBm",-100,...
%                     "rem_bits",59864.0,...
%                     "mem_num",39.0, ...
%                     "eager_rate",1.0 ...
%             )...
%              struct( "gid",10.0, ...
%                     "rbf_w",2.0, ...
%                     "rbf_h",1.0, ...
%                     "sinr_max",100,...
%                     "pwr_req_dBm",23,...
%                     "pwr_ext_dBm",-100,...
%                     "rem_bits",59864.0,...
%                     "mem_num",39.0, ...
%                     "eager_rate",1.0 ...
%             )...
%             struct( "gid",2, ...
%                     "rbf_w",1, ...
%                     "rbf_h",2, ...
%                     "sinr_max",30,...
%                     "pwr_req_dBm",22.964,...
%                     "pwr_ext_dBm",2.1671,...
%                     "rem_bits",3015460,...
%                     "mem_num",37, ...
%                     "eager_rate",1.0 ...
%             )...
%         }...
%     };
%     QoS_GP_CONF = {};
    [a,b] = PlannerV1(SIM_CONF,QoS_GP_CONF);
end

