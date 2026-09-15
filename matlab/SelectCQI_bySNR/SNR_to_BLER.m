function [bler] = SNR_to_BLER(cqi, snr_bound)
% SNR_to_BLER  Look up the achievable BLER for a given CQI and received SNR.
%
%   BLER = SNR_to_BLER(CQI, SNR_BOUND) walks the SNR-BLER curve for the
%   specified CQI index (from the highest SNR entry downward) and returns
%   the BLER at the first table entry whose SNR does not exceed SNR_BOUND.
%   If no entry qualifies, returns the BLER of the lowest-SNR table entry
%   (typically close to 1.0, the worst case).
%
%   Inputs:
%     cqi       - CQI index (1–15).
%     snr_bound - Received SINR (dB).
%
%   Output:
%     bler - Block error rate (0–1) at the given operating point.
    load('SNR_BLER_CQI.mat');
    [d BLER_LEVEL CQI_LEVEL] = size(snr_to_bler_with_cqi);
    
    bler = 1.0; %<- the worst case
    for b = BLER_LEVEL:-1:1
        %the 1st-row is the SNR
        %the 2nd-row is the BLER
        snr = snr_to_bler_with_cqi(1, b, cqi);
        bler = snr_to_bler_with_cqi(2, b, cqi);
        if(snr <= snr_bound) 
            %if it found an available (snr, bler) then report this bler
            return;
        end
    end
end