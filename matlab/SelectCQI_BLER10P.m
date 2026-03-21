function [cqi_index]=SelectCQI_BLER10P(SNR_UPPERBOUND)
% SelectCQI_BLER10P  Return the highest CQI index achievable at a given SINR.
%
%   CQI_INDEX = SelectCQI_BLER10P(SNR_UPPERBOUND) looks up the CQI index
%   (0-15) corresponding to the highest modulation-coding scheme whose
%   minimum required SINR does not exceed SNR_UPPERBOUND.  The thresholds
%   are fixed at the 10 % BLER operating point per 3GPP TS 36.213
%   Table 7.2.3-1.
%
%   The lookup is a simple hard-coded table search (no MAT file required),
%   making it significantly faster than SelectCQI() for use inside the
%   main simulation loop.
%
%   Input:
%     SNR_UPPERBOUND - Received SINR in dB (scalar or vector).
%
%   Output:
%     cqi_index - CQI index in [0, 15].
%                 0 means out-of-range (SINR below the lowest threshold).
%
%   SINR thresholds (dB) for CQI 0-15:
%     [-Inf, -6.9, -5.1, -3.1, -1.4, 0.8, 2.6, 4.7, 6.5, 8.4,
%      10.4, 12.3, 14.1, 15.9, 17.75, 19.7]
    SINR_LIM = [-Inf, -6.9, -5.1, -3.1, -1.4, 0.80, 2.60, 4.70, 6.50, 8.40, 10.40, 12.30, 14.10, 15.90, 17.75, 19.70];
    cqi_index = find(SINR_LIM <= SNR_UPPERBOUND, 1, 'last' ) - 1;
    %cqi_index = find(SINR_LIM <= SNR_UPPERBOUND,1,'last');
end