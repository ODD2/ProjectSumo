function [GID_REQ_BITS,ExitFlag] = NomaPlannerV1(SIM_CONF,QoS_GP_CONF)

    for qos = 1:length(QoS_GP_CONF)
        QoS_GP_CONF{qos} = [QoS_GP_CONF{qos}{:}];
    end
%The entry point for optimization
%     SIM_CONF = struct("rbf_h",4,...
%                       "rbf_w",2,...
%                       "rbfs",0,...
%                       "max_pwr",10 ...
%     ); 

%   Pended QoS group allocation configs.
%   (arranged by qos order, the smaller index the higher priority)
%     QoS_GP_CONF = {...
%         struct( "gid",{0}, ...
%                 "rbf_w",{2}, ...
%                 "rbf_h",{1}, ...
%                 "sinr_max",{15},...
%                 "rem_bits",{14368},...
%                 "mem_num",{1}...
%         )...
%         struct( "gid",{3,4}, ...
%                 "rbf_w",{2,1}, ...
%                 "rbf_h",{1,2}, ...
%                 "sinr_max",{5,20},...
%                 "rem_bits",{700,384590},...
%                 "mem_num",{20,5}...
%         )...

 
%         struct( "gid",{1,2,3}, ...
%                 "rbf_w",{2,1,2}, ...
%                 "rbf_h",{1,2,1}, ...
%                 "sinr_max",{20,8.5,15.7},...
%                 "rem_bits",{3000000,200000,3000000},...
%                 "mem_num",{50,8,15}...
%         )...
        
%         struct( "gid",{1,2}, ...
%                 "rbf_w",{1,2}, ...
%                 "rbf_h",{2,1}, ...
%                 "sinr_max",{8.5,15.7},...
%                 "rem_bits",{50000,70000},...
%                 "mem_num",{100,15}...
%         )...
%     };

%   Group configs for the optimizer
    OPT_GP_CONF_TEMPLATE = struct(...
                         "gid",0, ...
                         "qos",0, ...
                         "rbf_w",0, ...
                         "rbf_h",0, ...
                         "x_max",0,...
                         "y_max",0,...
                         "sinr_max",0,...
                         "sinr_max_sdn",0,... % signal / noise
                         "cqi_max",0,...
                         "rem_bits",0,...
                         "req_bits",0,...
                         "mem_num",0,...
                         "rb_num",0,...
                         "grp_sol_size",0,...
                         "grp_sol_ofs",0,...
                         ...%Optimization settings
                         "is_fix",false,...
                         ...%OMA settings
                         "oma_cqi_num",0,...
                         "oma_cqi_list",[],...
                         "oma_cqi_pwr_list",[],...
                         "oma_cqi_req_rb_list",[],...
                         "oma_sol_ofs",0,...
                         "oma_sol_size",0,...
                         ...%NOMA settings
                         "noma_cqi_num",0,...
                         "noma_cqi_list",[],...
                         "noma_cqi_pwr_list",[],...
                         "noma_cqi_req_rb_list",[],...
                         "noma_sol_ofs",0,...              
                         "noma_sol_size",0 ...
    );

%   initialization
    SIM_CONF.rbfs = SIM_CONF.rbf_w* SIM_CONF.rbf_h;

    OPT_GP_CONF = [];    
    
%   optimization
    for qos = 1:length(QoS_GP_CONF)
        if(isempty(QoS_GP_CONF{qos}))
            continue;
        end
        
%       configure and add basic group settings from new QoS level.
        for qos_gp_conf = QoS_GP_CONF{qos}
%           calculate the maximum possible resource block in x/y axis
            y_max = SIM_CONF.rbf_h - (qos_gp_conf.rbf_h - 1);
            x_max = SIM_CONF.rbf_w - (qos_gp_conf.rbf_w - 1);  
%           calculate the max cqi's required minimum power(dbm)
            cqi_max = SelectCQI(qos_gp_conf.sinr_max,0.1);
%           problem: higher cqi given even when the sinr_max doesn't reach the
%           minimum sinr requirement.
            sinr_max = max(qos_gp_conf.sinr_max,CqiMinSINR(cqi_max,0.1));
            sinr_max_sdn = 10 ^(sinr_max/10); 
            
%           create a new solution group config
            new_gp_conf  = OPT_GP_CONF_TEMPLATE;            
            
%           data copy from origin
            new_gp_conf.gid = qos_gp_conf.gid;
            new_gp_conf.qos = qos;
            new_gp_conf.rbf_w = qos_gp_conf.rbf_w;
            new_gp_conf.rbf_h = qos_gp_conf.rbf_h;
            new_gp_conf.rem_bits = qos_gp_conf.rem_bits;
            new_gp_conf.mem_num = qos_gp_conf.mem_num;
            
%           max cqi & max  sinr
            new_gp_conf.cqi_max = cqi_max;
            new_gp_conf.sinr_max = sinr_max;
            new_gp_conf.sinr_max_sdn = sinr_max_sdn;
            
%           newly joined groups will try to allocate both in oma&noma layer
            new_gp_conf.is_fix = false;
            
%           number of possible RB positions
            new_gp_conf.y_max = y_max;
            new_gp_conf.x_max = x_max;
            new_gp_conf.rb_num = y_max * x_max;
            
%           add new group configs
            OPT_GP_CONF = [OPT_GP_CONF new_gp_conf];
        end
        
%       record the group indices require allocation.
        alloc_grp_index = find(~[OPT_GP_CONF.is_fix]);
        
%       configure oma layer allocation prerequisites.
        for index = alloc_grp_index
            oma_cqi = OPT_GP_CONF(index).cqi_max;
            oma_cqi_pwr = (10 ^ (CqiMinSINR(oma_cqi,0.1)/10)) /...
                          (OPT_GP_CONF(index).sinr_max_sdn / SIM_CONF.max_pwr);
            OPT_GP_CONF(index).oma_cqi_list = [ oma_cqi ];
            OPT_GP_CONF(index).oma_cqi_pwr_list = [ oma_cqi_pwr ];
            OPT_GP_CONF(index).oma_cqi_num = 1;
        end
        
%       calculate position and offset info
        OPT_GP_CONF = CalcOptGpConfPosOfs(OPT_GP_CONF);
        
%       optimize allocation in OMA layer
        [x,fval,exitflag,output] = Optimize(SIM_CONF,OPT_GP_CONF,true);
        
%       update information from the last optimize allocation.
        OPT_GP_CONF = UpdateOptimizeResult(alloc_grp_index,OPT_GP_CONF,x,exitflag,true);
        
%       remove group index if group has been satisfied.
        alloc_grp_index([OPT_GP_CONF(alloc_grp_index).rem_bits] == 0) = [];
        
        
%       find the possible max/min remaining power lefted for NOMA resource block allocations
        oma_max_rem_pwr = SIM_CONF.max_pwr - min([OPT_GP_CONF.oma_cqi_pwr_list SIM_CONF.max_pwr]);
        oma_min_rem_pwr = SIM_CONF.max_pwr - max([OPT_GP_CONF.oma_cqi_pwr_list  0]);
        if(oma_min_rem_pwr > oma_max_rem_pwr)
            oma_min_rem_pwr = oma_max_rem_pwr;
        end
        for index = alloc_grp_index
%           sufficient resource groups are ignored from noma layer
%           optimize allocation process
            if( OPT_GP_CONF(index).rem_bits <=0 )
                continue
            end
            noise_reciprocal = OPT_GP_CONF(index).sinr_max_sdn / SIM_CONF.max_pwr;
            noma_cqi_max =  SelectCQI(10 *log10( oma_max_rem_pwr * noise_reciprocal), 0.1);
            noma_cqi_min =  max( SelectCQI(10 *log10( oma_min_rem_pwr * noise_reciprocal), 0.1) , 1);
            
%           unable to provide suitable power for noma layer allocation
            if(noma_cqi_max < noma_cqi_min)
                continue
            end
            
%           configure cqi settings for noma layer allocation
            noma_cqi_list = [];
            noma_cqi_pwr_list = [];
            for cqi = noma_cqi_min:noma_cqi_max
                noma_cqi_list = [noma_cqi_list cqi];
                noma_cqi_pwr_list = [noma_cqi_pwr_list (10 ^ (CqiMinSINR(cqi,0.1)/10))/...
                                                       (OPT_GP_CONF(index).sinr_max_sdn / SIM_CONF.max_pwr);];
            end
            OPT_GP_CONF(index).noma_cqi_list = noma_cqi_list;
            OPT_GP_CONF(index).noma_cqi_pwr_list = noma_cqi_pwr_list;
            OPT_GP_CONF(index).noma_cqi_num = length(OPT_GP_CONF(index).noma_cqi_list);
        end
        
%       calculate position and offset info
        OPT_GP_CONF = CalcOptGpConfPosOfs(OPT_GP_CONF);
        
        [x,fval,exitflag,output] = Optimize(SIM_CONF,OPT_GP_CONF,false);
        
%       save solution config for result display
        SOL_GP_CONF = OPT_GP_CONF;
        
%       update information from the last optimize allocation.
        OPT_GP_CONF = UpdateOptimizeResult(alloc_grp_index,OPT_GP_CONF,x,exitflag,false);
    end
    
    
%   print the final allocation result
    fprintf('==== OMA ====\n');
    for gp_conf = SOL_GP_CONF([SOL_GP_CONF.oma_cqi_num] > 0)
        fprintf('qos:%d, gid:%d, geo:(%d,%d)\n', [gp_conf.qos gp_conf.gid gp_conf.rbf_h gp_conf.rbf_w]);
        fprintf('{\n');
        for cqi_i = 1:gp_conf.oma_cqi_num
            cqi = gp_conf.oma_cqi_list(cqi_i);
            beg_sol_ofs = gp_conf.oma_sol_ofs+gp_conf.rb_num*(cqi_i-1) + 1;
            end_sol_ofs = gp_conf.oma_sol_ofs+gp_conf.rb_num*(cqi_i);
            sol_pos = (find(x(beg_sol_ofs:end_sol_ofs))-1)';
            
            if(isempty(sol_pos))
                continue
            end
            
            fprintf(' cqi:%d(x%d), pwr:%d , rbs:[',cqi,length(sol_pos),gp_conf.oma_cqi_pwr_list(cqi_i));
            for pos = sol_pos
                fprintf('(%d,%d)', [(mod(pos,gp_conf.y_max)+1) (floor(pos/gp_conf.y_max)+1)]);
            end
            fprintf(']\n');
        end
         fprintf('}\n');
    end
    
    fprintf('==== NOMA ====\n');
    for gp_conf = SOL_GP_CONF([SOL_GP_CONF.noma_cqi_num] > 0)
        fprintf('qos:%d, gid:%d, geo:(%d,%d)\n', [gp_conf.qos gp_conf.gid gp_conf.rbf_h gp_conf.rbf_w]);
        fprintf('{\n');
        for cqi_i = 1:gp_conf.noma_cqi_num
            cqi = gp_conf.noma_cqi_list(cqi_i);
            beg_sol_ofs = gp_conf.noma_sol_ofs+gp_conf.rb_num*(cqi_i-1) + 1;
            end_sol_ofs = gp_conf.noma_sol_ofs+gp_conf.rb_num*(cqi_i);
            sol_pos = (find(x(beg_sol_ofs:end_sol_ofs))-1)';
            
            if(isempty(sol_pos))
                continue
            end
            
            fprintf(' cqi:%d(x%d), pwr:%d , rbs:[',cqi,length(sol_pos),gp_conf.noma_cqi_pwr_list(cqi_i));
            for pos = sol_pos
                fprintf('(%d,%d)', [(mod(pos,gp_conf.y_max)+1) (floor(pos/gp_conf.y_max)+1)]);
            end
            fprintf(']\n');
        end
         fprintf('}\n');
    end
    
    
%   return values...
    GID_REQ_BITS = struct();
    ExitFlag = exitflag;
%   create result vector
    for qos = 1:length(QoS_GP_CONF)
        gid_list = [QoS_GP_CONF{qos}.gid];
        for gid = gid_list
            GID_REQ_BITS.("g"+gid) = 0;
        end
    end
%   fillin optimal allocation result
    for gp_conf = OPT_GP_CONF
        GID_REQ_BITS.("g"+gp_conf.gid) = gp_conf.req_bits;
    end
    
    
%   Helper Functions
    function NEW_GP_CONF = UpdateOptimizeResult(alloc_gidx,GP_CONF,x,extflg,OMA_LAYER)
%       error condition
        if(~( extflg==1 || extflg == -1 || extflg == 2 ))
            x = zeros(1,GP_CONF(end).grp_sol_ofs + GP_CONF(end).grp_sol_size);
        end
        
        if OMA_LAYER
            ln = "oma";
        else
            ln = "noma";
        end
%       update group status according to optimized allocation in NOMA layer
        for idx = alloc_gidx
            new_cqi_list = [];
            new_cqi_req_rb_list = [];
            new_cqi_pwr_list = [];
            rem_bits = GP_CONF(idx).rem_bits;
            req_bits = GP_CONF(idx).req_bits;
            for uor_cqi_i = 1: GP_CONF(idx).(ln+"_cqi_num")
                cqi_sol_beg = GP_CONF(idx).(ln+"_sol_ofs") + (uor_cqi_i - 1) * GP_CONF(idx).rb_num + 1;
                cqi_sol_end = GP_CONF(idx).(ln+"_sol_ofs") + (uor_cqi_i    ) * GP_CONF(idx).rb_num;
                rb_alloc = sum(x(cqi_sol_beg:cqi_sol_end));
                uor_cqi = GP_CONF(idx).(ln+"_cqi_list")(uor_cqi_i);
                pwr = GP_CONF(idx).(ln+"_cqi_pwr_list")(uor_cqi_i);
                bit_alloc =  rb_alloc * GetThroughputPerRB(uor_cqi,14);
                if( rb_alloc > 0 )
                    rem_bits = rem_bits - bit_alloc;
                    req_bits = req_bits + bit_alloc;
                    new_cqi_list = [new_cqi_list uor_cqi];
                    new_cqi_req_rb_list = [new_cqi_req_rb_list rb_alloc];
                    new_cqi_pwr_list = [new_cqi_pwr_list pwr];
                end
            end
            GP_CONF(idx).rem_bits = max(rem_bits ,0);
            GP_CONF(idx).req_bits = req_bits;
            GP_CONF(idx).(ln+"_cqi_list") = new_cqi_list;
            GP_CONF(idx).(ln+"_cqi_req_rb_list") = new_cqi_req_rb_list;
            GP_CONF(idx).(ln+"_cqi_pwr_list") = new_cqi_pwr_list;
            GP_CONF(idx).(ln+"_cqi_num") = length(GP_CONF(idx).(ln+"_cqi_list"));
            
            if OMA_LAYER && (GP_CONF(idx).rem_bits == 0)
%           satisfied group should be removed from allocation process
                GP_CONF(idx).is_fix = true;
            elseif ~OMA_LAYER
%           both OMA & NOMA layer allocation done, the group has reached its maximum resource.
                GP_CONF(idx).is_fix = true;
            end
        end
        
        NEW_GP_CONF = GP_CONF;
    end
end



