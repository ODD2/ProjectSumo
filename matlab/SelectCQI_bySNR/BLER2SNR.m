function [SNR]=BLER2SNR(BLER, CQI)
% [SNR]=BLER2SNR(BLER, CQI)
%Given the used CQI-level and the BLER, output the linearly-approximated
%bler from the SNR-BLER curve
    load('SNR_BLER_CQI.mat');

    [~, BLER_LEVEL ~] = size(snr_to_bler_with_cqi);
    y_bler = snr_to_bler_with_cqi(2, :, CQI);
    x_snr = snr_to_bler_with_cqi(1, :, CQI);
    
    if( BLER >= y_bler(1))
        SNR = x_snr(1);
    elseif( BLER <= y_bler(end) )
        SNR = x_snr(end);
    else
        %Use Linear Interpolation to get snr in the interval
        last = 1.0;
        for b=1:BLER_LEVEL
            if last < 0.0744
                fprintf('');
            end
            if(last >= BLER && BLER >= y_bler(b))
                %found the interval containing the 'BLER'
                break;
            end
            last = y_bler(b);
        end

        %[Linear Interpolation]
        y0 = y_bler(b-1); y1 = y_bler(b);
        x0 = x_snr(b-1);  x1 = x_snr(b);
        y = BLER;
        %   [derivation]
        %   (y - y0)/(x - x0) = (y1-y0)/(x1-x0)
        %    => y-y0 = (y1-y0)/(x1-x0) * x - (y1-y0)/(x1-x0)*x0
        %    => c = (y1-y0)/(x1-x0)
        %    => y-y0 = cx - c*x0 => y-y0+c*x0 = cx
        c = (y1-y0)./(x1-x0);
        SNR = ( y-y0+c*x0 )./ c;
    end
end