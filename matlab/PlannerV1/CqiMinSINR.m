function [min_sinr] = CqiMinSINR(CQI,BLER_UPPERBOUND)
% CqiMinSINR  Return the minimum SINR required for a CQI at a given BLER target.
%
%   MIN_SINR = CqiMinSINR(CQI, BLER_UPPERBOUND) scans the SNR-BLER lookup
%   table (SNR_BLER_CQI.mat) for the CQI entry and returns the lowest SNR
%   value at which BLER <= BLER_UPPERBOUND.  Used by PlannerV1 to compute
%   required receive power for NOMA outer-user allocation.
%
%   Inputs:
%     CQI            - CQI index (1–15).
%     BLER_UPPERBOUND - Maximum tolerable BLER (e.g. 0.1 for 10% BLER target).
%
%   Output:
%     min_sinr - Minimum required SINR (dB).  Returns -7 dB if no table entry
%                satisfies the BLER constraint.

%  persistent CQI_TO_SINR;
%  if isempty(CQI_TO_SINR)
%     CQI_TO_SINR = [-6.7 -4.7 -2.3...
%                     0.2  2.4  4.3...
%                     5.9  8.1 10.3...
%                    11.7 14.1 16.3...
%                    18.7 21.0 22.7 ];
%  end 
%  min_sinr = CQI_TO_SINR(cqi);

    persistent snr_to_bler_with_cqi    %set variable to static variable (faster)
    if isempty(snr_to_bler_with_cqi)
        load('SNR_BLER_CQI.mat');
    end
    
    [~, BLER_LEVEL, ~] = size(snr_to_bler_with_cqi);
    min_sinr = -7;
    for b = BLER_LEVEL:-1:1
        %the 1st-row is the SNR
        %the 2nd-row is the BLER
        %snr = snr_to_bler_with_cqi(1, b, index);
        %bler = snr_to_bler_with_cqi(2, b, index);            
        if( snr_to_bler_with_cqi(2, b, CQI) <= BLER_UPPERBOUND)
            min_sinr = snr_to_bler_with_cqi(1,b,CQI);
        end
    end
end

