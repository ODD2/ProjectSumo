function [return_value]=GetBLER_from_CQI_and_SNR(CQI, SNR)
% GetBLER_from_CQI_and_SNR  Return the lowest achievable BLER for a CQI/SNR pair.
%
%   BLER = GetBLER_from_CQI_and_SNR(CQI, SNR) searches the SNR-BLER lookup
%   table (SNR_BLER_CQI.mat) for all entries at the given CQI whose SNR is
%   strictly less than the supplied SNR value, and returns the minimum BLER
%   found.  Returns 1.0 if no such entry exists (SNR is below the table range).
%
%   Inputs:
%     CQI - CQI index (1–15).
%     SNR - Received SINR (dB).
%
%   Output:
%     return_value - Minimum achievable BLER (0–1) at the given CQI and SNR.
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