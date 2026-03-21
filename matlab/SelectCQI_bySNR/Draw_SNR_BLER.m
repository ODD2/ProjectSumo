% Draw_SNR_BLER  Plot the SNR-BLER curves for all 15 CQI levels.
%
%   Loads SNR_BLER_CQI.mat and produces a single figure with 15 line plots
%   (one per CQI index, colour-coded) showing BLER as a function of SNR.
%
%   Run as a script (no inputs or outputs).  Requires SNR_BLER_CQI.mat to be
%   on the MATLAB path.
load('SNR_BLER_CQI.mat');
color = 'rgbcmykrgbcmykrgbcmyk';
figure;
hold on;
[dummy LEVEL CQI_LEVEL] = size(snr_to_bler_with_cqi);
for cqi=1:CQI_LEVEL
    snr = snr_to_bler_with_cqi(1, :, cqi);
    bler = snr_to_bler_with_cqi(2, :, cqi);
    plot(snr, bler, sprintf('%c-', color(cqi)));
end
hold off;
clear dummy bler snr cqi;
title('SNR to BLER');
xlabel('SNR');
ylabel('BLER');
legend('CQI=1', 'CQI=2', 'CQI=3', 'CQI=4', 'CQI=5', 'CQI=6', 'CQI=7', ...
    'CQI=8', 'CQI=9', 'CQI=10', 'CQI=11', 'CQI=12', 'CQI=13', 'CQI=14', ...
    'CQI=15', 'Location', 'BestOutside');