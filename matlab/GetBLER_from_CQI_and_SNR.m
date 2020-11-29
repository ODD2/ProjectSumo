function [return_value]=GetBLER_from_CQI_and_SNR(CQI, SNR)
    if nargin < 2
        ME = MException('MyComponent:invalidFormat', sprintf('ERROR INPUT!\n [bler]=GetBLERfrom_CQI_and_SNR(CQI, SNR)\n'));
        throw(ME); %terminate
    end
    load('SNR_BLER_CQI.mat');

    [~, BLER_LEVEL ~] = size(snr_to_bler_with_cqi);
    
    return_value = 1.0;
    for b = 1:BLER_LEVEL
        %the 1st-row is the SNR
        %the 2nd-row is the BLER
        s = snr_to_bler_with_cqi(1, b, CQI);
        bler = snr_to_bler_with_cqi(2, b, CQI);
        if(s < SNR)
            if(bler < return_value)
                return_value = bler;
            end
        else
            break;
        end
    end
end