function [min_sinr] = CqiMinSINR(CQI,BLER_UPPERBOUND)
%CQI_MIN_SINR Summary of this function goes here
%   Detailed explanation goes here

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

