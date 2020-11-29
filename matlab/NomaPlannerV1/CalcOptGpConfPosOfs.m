%   Helper Functions
function GP_CONF = CalcOptGpConfPosOfs(GP_CONF)
    %calculate position/offset for every group in solution
    for i = 1:length(GP_CONF)
        if i == 1
            GP_CONF(i).grp_sol_ofs = 0;
        else
            GP_CONF(i).grp_sol_ofs =  GP_CONF(i-1).grp_sol_ofs + GP_CONF(i-1).grp_sol_size;
        end
        GP_CONF(i).oma_sol_size =  GP_CONF(i).rb_num * GP_CONF(i).oma_cqi_num;
        GP_CONF(i).noma_sol_size = GP_CONF(i).rb_num * GP_CONF(i).noma_cqi_num;
        
        GP_CONF(i).oma_sol_ofs = GP_CONF(i).grp_sol_ofs;
        GP_CONF(i).noma_sol_ofs = GP_CONF(i).grp_sol_ofs + GP_CONF(i).oma_sol_size;
%       calculate the total solution size/offset for OMA & NOMA for each group
        GP_CONF(i).grp_sol_size =  GP_CONF(i).oma_sol_size + GP_CONF(i).noma_sol_size;
    end
end