function [GID_REQ_RES,ExitFlag] = NomaPlannerV1(SIM_CONF,QoS_GP_CONF)

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
    SOL_GP_CONF = [];
    x = [];
    exitflag = -2;
    
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
            sinr_max = qos_gp_conf.sinr_max;
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
            sinr_max_noise = 1/(OPT_GP_CONF(index).sinr_max_sdn / SIM_CONF.max_pwr);
            oma_cqi = OPT_GP_CONF(index).cqi_max;
            oma_cqi_req_sdn = 10 ^ (CqiMinSINR(oma_cqi,0.1)/10);
            oma_cqi_pwr =(oma_cqi_req_sdn)*(sinr_max_noise + SIM_CONF.max_pwr)/(1+oma_cqi_req_sdn);
%           if the power required for noma will decrease the cqi, then
%           don't provide noma.
            oma_cqi_pwr = min(oma_cqi_pwr,SIM_CONF.max_pwr);
            OPT_GP_CONF(index).oma_cqi_list = [ oma_cqi ];
            OPT_GP_CONF(index).oma_cqi_pwr_list = [ oma_cqi_pwr ];
            OPT_GP_CONF(index).oma_cqi_num = 1;
        end
        
%       calculate position and offset info
        OPT_GP_CONF = CalcOptGpConfPosOfs(OPT_GP_CONF);
        
%       optimize allocation in OMA layer
        [x,~,exitflag,~] = Optimize(SIM_CONF,OPT_GP_CONF,true);
        
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
        
%       calculate position and offset info
        OPT_GP_CONF = CalcOptGpConfPosOfs(OPT_GP_CONF);
    end
    
    if(isempty(x))
%       find feasible solution
        [x,fval,exitflag,output] = Optimize(SIM_CONF,OPT_GP_CONF,false);
    end
    
%   result info
    PrintSolutionResult(SOL_GP_CONF,x);
    
%   return values
    GID_REQ_RES = struct();
    ExitFlag = exitflag;
    
%   fillin optimization result
    for gp_conf = SOL_GP_CONF
        gname = "g"+gp_conf.gid;
        GID_REQ_RES.(gname) = struct();
%       collect oma layer resource blocks
        for ts = 0: (gp_conf.x_max-1)
            ts_name  = "t"+ts;
            GID_REQ_RES.(gname).(ts_name) = struct();
            for layer = ["oma" "noma"]
                for cqi_i = 1:gp_conf.(layer + "_cqi_num")
                    cqi = gp_conf.(layer+"_cqi_list")(cqi_i);
                    sol_beg = gp_conf.(layer+"_sol_ofs") + (cqi_i - 1) * gp_conf.rb_num + (ts  ) * gp_conf.y_max + 1;
                    sol_end = gp_conf.(layer+"_sol_ofs") + (cqi_i - 1) * gp_conf.rb_num + (ts+1) * gp_conf.y_max;
%                   collect resource blocks allocated at this timeslot
                    ts_rb_num = int16(sum(x(sol_beg:sol_end)));
                    cqi_name = "c" + cqi;
%                   skip if no resource block was allocated
                    if ts_rb_num == 0
                        continue
                    end
%                   check if this group has the same cqi resource block
%                   allocation during this timeslot.
                    if ~isfield(GID_REQ_RES.(gname).(ts_name),cqi_name)
                        GID_REQ_RES.(gname).(ts_name).(cqi_name) = ts_rb_num;
                    else
                        GID_REQ_RES.(gname).(ts_name).(cqi_name) = ts_rb_num + GID_REQ_RES.(gname).(ts_name).(cqi_name);
                    end
                end
            end
        end
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

    function [] = PrintSolutionResult(SOL_GP_CONF,x)
%       print the final allocation result        
        for gpc = SOL_GP_CONF
            fprintf('===== QoS:%d, Gid:%d, Geo:(%d,%d) =====\n',...
            		[gpc.qos gpc.gid gpc.rbf_h gpc.rbf_w]);
            fprintf('{\n');
            for layer_ = ["oma" "noma"]
            	fprintf(" --- %s Layer ---\n", [ upper(layer_) ] );
	            for cqi_i_ = 1:gpc.(layer_+"_cqi_num")
	                g_cqi = gpc.(layer_+"_cqi_list")(cqi_i_);
	                beg_sol_ofs = gpc.(layer_+"_sol_ofs")+gpc.rb_num*(cqi_i_-1) + 1;
	                end_sol_ofs = gpc.(layer_+"_sol_ofs")+gpc.rb_num*(cqi_i_);
	                sol_pos = (find(x(beg_sol_ofs:end_sol_ofs))-1)';

	                if(isempty(sol_pos))
	                    continue
	                end

	                fprintf(' cqi:%d(x%d), pwr:%d , rbs:[',g_cqi,length(sol_pos),gpc.(layer_+"_cqi_pwr_list")(cqi_i_));
	                for pos = sol_pos
	                    fprintf('(%d,%d)', [(mod(pos,gpc.y_max)+1) (floor(pos/gpc.y_max)+1)]);
	                end
	                fprintf(']\n');
	            end
	         end
             fprintf('}\n');
        end
    end
end



