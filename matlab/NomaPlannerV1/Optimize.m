% function [Aeq,beq,A,b] = Optimize(SIM_CONF,GP_CONF)
function [x,fval,exitflag,output] = Optimize(SIM_CONF,OPT_GP_CONF,OMA_LAYER)
%The function that constructs linear/non-linear constraints, objective
%function and runs the optimizer

%   collect required simulation info
%   - size of the solution
    sol_size = OPT_GP_CONF(end).grp_sol_ofs + OPT_GP_CONF(end).grp_sol_size;
%   - fixed group logic index
    fixed_grp_logi = [OPT_GP_CONF.is_fix];
    fixed_grp_index = find(fixed_grp_logi);
    fixed_grp_size = length(fixed_grp_index);
%   - allocation group logic index
    alloc_grp_logi =~[OPT_GP_CONF.is_fix];
    alloc_grp_index = find(alloc_grp_logi);
    alloc_grp_size = length(alloc_grp_index);
    
%   resource block geo to resource block fraction geo mapping
    M_RB_TO_RBF = zeros(SIM_CONF.rbfs,sol_size);
%   initialize mapping from resource block to resource block fractions
    for gp_conf = OPT_GP_CONF
%       loop through all possible resource block positions
        for rb_i = 1:gp_conf.rb_num
            loc_y = mod((rb_i-1),gp_conf.y_max)+1;
            loc_x = floor((rb_i-1)/gp_conf.y_max)+1;
            anchor = loc_y + (loc_x-1) * SIM_CONF.rbf_h;
%           go through all resource block fractions
            for ofs_x = 0:gp_conf.rbf_w-1
                for ofs_y = 0:gp_conf.rbf_h-1
%                   OMA layer
                    for cqi_ofs = 0: gp_conf.oma_cqi_num - 1
                        M_RB_TO_RBF(anchor+ofs_y+ofs_x*SIM_CONF.rbf_h, ...
                                    gp_conf.oma_sol_ofs + cqi_ofs * gp_conf.rb_num + rb_i) = 1;
                    end
                    
%                   NOMA layer
                    for cqi_ofs = 0: gp_conf.noma_cqi_num - 1
                        M_RB_TO_RBF(anchor+ofs_y+ofs_x*SIM_CONF.rbf_h, ...
                                    gp_conf.noma_sol_ofs + cqi_ofs * gp_conf.rb_num + rb_i) = 1;
                    end
                end 
            end
        end
    end



%Equality Constraints:
%	(BOTH LAYER)
%	fix group oma rb required
%	fix group noma rb required
%	(NOMA LAYER ALLOC ONLY)
%	unfix group oma rb required
%
%Inequality Constraints:
%	(BOTH LAYER)
%	resource block fraction maximum allocation constraint for oma layer
%	resource block fraction maximum allocation constraint for noma layer
%	resource block fraction maximum power constraint
%	resource block allocation same group different cqi/layer 
%	redundant resource allocation constraint
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   
%   ================  Equality Constraint  ===============    

%   - required resource block for fix groups in OMA layer
    oma_cqi_req_rb_fix_grp_num = length([OPT_GP_CONF(fixed_grp_logi).oma_cqi_req_rb_list]);
    AEQ_FIX_OMA_REQ_RB = zeros(oma_cqi_req_rb_fix_grp_num,sol_size);
    BEQ_FIX_OMA_REQ_RB = zeros(oma_cqi_req_rb_fix_grp_num,1);
    cpos_fix_oma_req_rb = 1;
    for gp_conf = OPT_GP_CONF(fixed_grp_logi)
%       fix group oma layer - required RB allocation for specific cqi constraint
        if(gp_conf.oma_cqi_num > 0)
            for cqi_i = 1: gp_conf.oma_cqi_num
                AEQ_FIX_OMA_REQ_RB(cpos_fix_oma_req_rb, ...
                       (gp_conf.oma_sol_ofs + (cqi_i-1) * gp_conf.rb_num  + 1) : ...
                       (gp_conf.oma_sol_ofs + (cqi_i  ) * gp_conf.rb_num ) ) = 1;
                BEQ_FIX_OMA_REQ_RB(cpos_fix_oma_req_rb,1) = gp_conf.oma_cqi_req_rb_list(cqi_i);
                cpos_fix_oma_req_rb = cpos_fix_oma_req_rb + 1;
            end
        end
    end
    
%   - required resource block for fix groups in NOMA layer
    noma_cqi_req_rb_fix_grp_num = length([OPT_GP_CONF(fixed_grp_logi).noma_cqi_req_rb_list]);
    AEQ_FIX_NOMA_REQ_RB = zeros(noma_cqi_req_rb_fix_grp_num,sol_size);
    BEQ_FIX_NOMA_REQ_RB = zeros(noma_cqi_req_rb_fix_grp_num,1);
    cpos_fix_noma_req_rb = 1;
    for gp_conf = OPT_GP_CONF(fixed_grp_logi)
%       fix group noma layer - required RB allocation for specific cqi constraint
        if(gp_conf.noma_cqi_num > 0)
            for cqi_i = 1: gp_conf.noma_cqi_num
                AEQ_FIX_NOMA_REQ_RB(cpos_fix_noma_req_rb, ...
                       (gp_conf.noma_sol_ofs + (cqi_i-1) * gp_conf.rb_num  + 1) : ...
                       (gp_conf.noma_sol_ofs + (cqi_i  ) * gp_conf.rb_num ) ) = 1;
                BEQ_FIX_NOMA_REQ_RB(cpos_fix_noma_req_rb,1) = gp_conf.noma_cqi_req_rb_list(cqi_i);
                cpos_fix_noma_req_rb = cpos_fix_noma_req_rb + 1;
            end
        end
    end
    
%   - required resource block for alloc groups in OMA layer    
    if ~OMA_LAYER
        oma_cqi_req_rb_alloc_grp_num = length([OPT_GP_CONF(alloc_grp_logi).oma_cqi_req_rb_list]);
        AEQ_ALLOC_OMA_REQ_RB = zeros(oma_cqi_req_rb_alloc_grp_num,sol_size);
        BEQ_ALLOC_OMA_REQ_RB = zeros(oma_cqi_req_rb_alloc_grp_num,1);
        cpos_alloc_oma_req_rb = 1;
        for gp_conf = OPT_GP_CONF(alloc_grp_logi)
    %       fix group oma layer - required RB allocation for specific cqi constraint
            if(gp_conf.oma_cqi_num > 0)
                for cqi_i = 1: gp_conf.oma_cqi_num
                    AEQ_ALLOC_OMA_REQ_RB(cpos_alloc_oma_req_rb, ...
                           (gp_conf.oma_sol_ofs + (cqi_i-1) * gp_conf.rb_num  + 1) : ...
                           (gp_conf.oma_sol_ofs + (cqi_i  ) * gp_conf.rb_num ) ) = 1;
                    BEQ_ALLOC_OMA_REQ_RB(cpos_alloc_oma_req_rb,1) = gp_conf.oma_cqi_req_rb_list(cqi_i);
                    cpos_alloc_oma_req_rb = cpos_alloc_oma_req_rb + 1;
                end
            end
        end
    else
        AEQ_ALLOC_OMA_REQ_RB = [];
        BEQ_ALLOC_OMA_REQ_RB = [];
    end
    
    
%   construct EQ constraints
    Aeq = [ AEQ_FIX_OMA_REQ_RB;
            AEQ_FIX_NOMA_REQ_RB;
            AEQ_ALLOC_OMA_REQ_RB; ];
        
    beq = [ BEQ_FIX_OMA_REQ_RB;
            BEQ_FIX_NOMA_REQ_RB;
            BEQ_ALLOC_OMA_REQ_RB;];
    
%   ================  Ineqaulity Constraint  ===============
    
%   resource block fraction max allocation limit for oma layer
    ALEQ_OMA_RBF_MAX_ALLOC = zeros(SIM_CONF.rbfs,sol_size);
    BLEQ_OMA_RBF_MAX_ALLOC = ones(SIM_CONF.rbfs,1);
    for gp_conf = OPT_GP_CONF([OPT_GP_CONF.oma_cqi_num] > 0)
        sol_beg = gp_conf.oma_sol_ofs + 1;
        sol_end = gp_conf.oma_sol_ofs + gp_conf.oma_sol_size;
        ALEQ_OMA_RBF_MAX_ALLOC( : , sol_beg : sol_end ) = M_RB_TO_RBF( : , sol_beg : sol_end);
    end
    
%   resource block fraction max allocation limit for noma layer
    ALEQ_NOMA_RBF_MAX_ALLOC = zeros(SIM_CONF.rbfs,sol_size);
    BLEQ_NOMA_RBF_MAX_ALLOC = ones(SIM_CONF.rbfs,1);
    for gp_conf = OPT_GP_CONF([OPT_GP_CONF.noma_cqi_num] > 0)
        sol_beg = gp_conf.noma_sol_ofs + 1;
        sol_end = gp_conf.noma_sol_ofs + gp_conf.noma_sol_size;
        ALEQ_NOMA_RBF_MAX_ALLOC( : , sol_beg : sol_end ) = M_RB_TO_RBF( : , sol_beg : sol_end );
    end

%   resource block reused by same group constraint
%   TODO: could be rewrite to only include alloc group that requires oma
%   cqi RBs.
    ALEQ_GRP_RB_OVERLAP = zeros((fixed_grp_size+alloc_grp_size)*SIM_CONF.rbfs,sol_size);
    BLEQ_GRP_RB_OVERLAP =  ones((fixed_grp_size+alloc_grp_size)*SIM_CONF.rbfs,1);
    cofs_grp_rb_lap = 0;
    for gp_conf = OPT_GP_CONF(fixed_grp_logi)
        sol_beg = gp_conf.grp_sol_ofs + 1;
        sol_end = gp_conf.grp_sol_ofs + gp_conf.grp_sol_size;
        cpos_beg =  1 + cofs_grp_rb_lap  *  SIM_CONF.rbfs;
        cpos_end =( 1 + cofs_grp_rb_lap )*  SIM_CONF.rbfs;
        ALEQ_GRP_RB_OVERLAP( cpos_beg : cpos_end , sol_beg : sol_end ) = ...
                                                M_RB_TO_RBF( : , sol_beg : sol_end );
        cofs_grp_rb_lap = cofs_grp_rb_lap + 1;
    end
    for gp_conf = OPT_GP_CONF(alloc_grp_logi)
        sol_beg = gp_conf.grp_sol_ofs + 1;
        sol_end = gp_conf.grp_sol_ofs + gp_conf.grp_sol_size;
        cpos_beg =  1 + cofs_grp_rb_lap  *  SIM_CONF.rbfs;
        cpos_end =( 1 + cofs_grp_rb_lap )*  SIM_CONF.rbfs;
        ALEQ_GRP_RB_OVERLAP( cpos_beg : cpos_end , sol_beg : sol_end ) = ...
                                                M_RB_TO_RBF( : , sol_beg : sol_end );
        cofs_grp_rb_lap = cofs_grp_rb_lap + 1;
    end

%   resource block fraction max power constraint
    ALEQ_RBF_MAX_PWR = zeros(SIM_CONF.rbfs,sol_size);
    BLEQ_RBF_MAX_PWR = ones(SIM_CONF.rbfs,1) * SIM_CONF.max_pwr;
    for gp_conf = OPT_GP_CONF
%       oma layer resource block
        for oma_cqi_i = 1 : gp_conf.oma_cqi_num
            cqi_min_sinr_pwr = gp_conf.oma_cqi_pwr_list(oma_cqi_i);
            oma_cqi_sol_beg = gp_conf.oma_sol_ofs + (oma_cqi_i - 1) * gp_conf.rb_num + 1;
            oma_cqi_sol_end = gp_conf.oma_sol_ofs + (oma_cqi_i    ) * gp_conf.rb_num    ;                
            ALEQ_RBF_MAX_PWR( : , oma_cqi_sol_beg : oma_cqi_sol_end ) = ...
                 M_RB_TO_RBF( : , oma_cqi_sol_beg : oma_cqi_sol_end ) * cqi_min_sinr_pwr;
        end
%       noma layer resource block
        for noma_cqi_i = 1 : gp_conf.noma_cqi_num
            cqi_min_sinr_pwr = gp_conf.noma_cqi_pwr_list(noma_cqi_i);
            noma_cqi_sol_beg = gp_conf.noma_sol_ofs + (noma_cqi_i - 1) * gp_conf.rb_num + 1;
            noma_cqi_sol_end = gp_conf.noma_sol_ofs + (noma_cqi_i    ) * gp_conf.rb_num    ;                
            ALEQ_RBF_MAX_PWR( : , noma_cqi_sol_beg : noma_cqi_sol_end ) = ...
                 M_RB_TO_RBF( : , noma_cqi_sol_beg : noma_cqi_sol_end ) * cqi_min_sinr_pwr;
        end
    end
    
    
%   prevent group from allocating redundant resource constraint
    ALEQ_GRP_ALLOC_REDU = zeros(alloc_grp_size,sol_size);
    BLEQ_GRP_ALLOC_REDU = zeros(alloc_grp_size,1);
    cpos_grp_alloc_redu = 1;
    for gp_conf = OPT_GP_CONF(alloc_grp_logi)
        min_cqi_rb_size = GetThroughputPerRB(15,14);
        if OMA_LAYER
            for oma_cqi_i = 1:gp_conf.oma_cqi_num
                cqi =  gp_conf.oma_cqi_list(oma_cqi_i);
                rbsize = GetThroughputPerRB(cqi,14);
                ALEQ_GRP_ALLOC_REDU(cpos_grp_alloc_redu , ...
                         gp_conf.oma_sol_ofs + (oma_cqi_i - 1)*gp_conf.rb_num + 1 :...
                         gp_conf.oma_sol_ofs + (oma_cqi_i    )*gp_conf.rb_num     ) = rbsize;
                if rbsize < min_cqi_rb_size
                    min_cqi_rb_size = rbsize;
                end      
            end
        else
            for noma_cqi_i = 1:gp_conf.noma_cqi_num
                cqi =  gp_conf.noma_cqi_list(noma_cqi_i);
                rbsize = GetThroughputPerRB(cqi,14);
                ALEQ_GRP_ALLOC_REDU(cpos_grp_alloc_redu,...
                         gp_conf.noma_sol_ofs + (noma_cqi_i - 1)*gp_conf.rb_num + 1 :...
                         gp_conf.noma_sol_ofs + (noma_cqi_i    )*gp_conf.rb_num     ) = GetThroughputPerRB(cqi,14);
                if rbsize < min_cqi_rb_size
                    min_cqi_rb_size = rbsize;
                end    
            end
        end
        BLEQ_GRP_ALLOC_REDU(cpos_grp_alloc_redu, 1 ) = gp_conf.rem_bits + min_cqi_rb_size;
        cpos_grp_alloc_redu = cpos_grp_alloc_redu + 1;
    end
    
%   construct LEQ constraints
    A = [   ALEQ_OMA_RBF_MAX_ALLOC;
            ALEQ_NOMA_RBF_MAX_ALLOC;
            ALEQ_GRP_RB_OVERLAP;
            ALEQ_RBF_MAX_PWR;
            ALEQ_GRP_ALLOC_REDU;    ];
        
    b = [   BLEQ_OMA_RBF_MAX_ALLOC;
            BLEQ_NOMA_RBF_MAX_ALLOC;
            BLEQ_GRP_RB_OVERLAP;
            BLEQ_RBF_MAX_PWR;
            BLEQ_GRP_ALLOC_REDU;    ];
        
%   create required vectors
    lb = zeros(1,sol_size);
    ub = ones(1,sol_size);
    f = zeros(1,sol_size); 

%   define objective function
    cpos_grp_alloc_redu = 1;
    for gp_conf = OPT_GP_CONF(alloc_grp_logi)
        if(OMA_LAYER)
            grp_oma_sol_beg = gp_conf.oma_sol_ofs + 1;
            grp_oma_sol_end = gp_conf.oma_sol_ofs + gp_conf.oma_sol_size;
            f(grp_oma_sol_beg : grp_oma_sol_end) = ALEQ_GRP_ALLOC_REDU(cpos_grp_alloc_redu,grp_oma_sol_beg : grp_oma_sol_end);
        else
            grp_noma_sol_beg = gp_conf.noma_sol_ofs + 1;
            grp_noma_sol_end = gp_conf.noma_sol_ofs + gp_conf.noma_sol_size;
            f(grp_noma_sol_beg : grp_noma_sol_end) = ALEQ_GRP_ALLOC_REDU(cpos_grp_alloc_redu,grp_noma_sol_beg : grp_noma_sol_end);
        end
        cpos_grp_alloc_redu = cpos_grp_alloc_redu + 1;
    end
        
%   add small difference for each rb per group subframe
%     for gp_conf = OPT_GP_CONF(SIM_CONF.noma_grps)
%         gap = 1/gp_conf.rb_num;
%         diff = 0;
%         for i = gp_conf.grp_sol_size:1
%             if mod(i,gp_conf.rb_num) == 0
%                 diff = 0;
%             else
%                 diff = diff + gap;
%             end
%             f(i+gp_conf.grp_sol_ofs) = f(i+gp_conf.grp_sol_ofs)+diff;
%         end
%     end

%   group prioritization
%   (group having large member has higher prior, group having the same
%   members but required lower bits has higher priority)
    for gp_conf = OPT_GP_CONF(alloc_grp_logi)
        if OMA_LAYER
            grp_sol_beg = gp_conf.oma_sol_ofs+1;
            grp_sol_end = gp_conf.oma_sol_ofs + gp_conf.oma_sol_size;
        else
            grp_sol_beg = gp_conf.noma_sol_ofs+1;
            grp_sol_end = gp_conf.noma_sol_ofs + gp_conf.noma_sol_size;
        end
        if gp_conf.rem_bits > 0
            weight = (gp_conf.mem_num/gp_conf.rem_bits);
        else
            weight = 0;
        end
        f(grp_sol_beg : grp_sol_end) = f(grp_sol_beg : grp_sol_end) * weight;
    end
    
    
    
    intcon = 1:sol_size;
    
    f = f*-1;
    
    options = optimoptions('intlinprog'...
                           ,'IntegerPreprocess','advanced'...
                           ,'CutGeneration','intermediate'...
                           ,'OutputFcn',{@CustomOutputFunction}...
                           ,'Display','none'...
...%                            ,'PlotFcn',@optimplotmilp...
                          );
%                            'MaxTime',10);

    [x,fval,exitflag,output] = intlinprog(f,intcon,A,b,Aeq,beq,lb,ub,[],options);
    
    
    function STOP = CustomOutputFunction(X,OPT_VAL,STATE)
        if OPT_VAL.phase == "branching"
            STOP = true;
        else
            STOP = false;
        end
    end
end

