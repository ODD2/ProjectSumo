function GP_CONF = CalcOptGpConfPosOfs(GP_CONF)
% CalcOptGpConfPosOfs  Compute solution-vector offsets and sizes for each group.
%
%   GP_CONF = CalcOptGpConfPosOfs(GP_CONF) iterates over all group configs and
%   fills in the following derived fields used to index into the flat solution
%   vector x inside Optimize:
%
%     grp_sol_ofs  - Starting index offset of this group's segment in x.
%     oma_sol_ofs  - Starting index offset of the OMA sub-segment.
%     oma_sol_size - Length of the OMA sub-segment (rb_num × oma_cqi_num).
%     noma_sol_ofs - Starting index offset of the NOMA sub-segment.
%     noma_sol_size- Length of the NOMA sub-segment (rb_num × noma_cqi_num).
%     grp_sol_size - Total length of this group's segment (OMA + NOMA).
%
%   Must be called after any change to oma_cqi_num or noma_cqi_num so that
%   all offset fields remain consistent before Optimize is invoked.
%
%   Input / Output:
%     GP_CONF - Array of group config structs; updated in-place and returned.
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