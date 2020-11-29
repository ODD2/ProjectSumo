function [bler] = SNR_to_BLER(cqi, snr_bound)
%Given the used CQI and SNR of the UE, report the achieving BLER
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