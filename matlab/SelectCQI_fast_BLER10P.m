function [cqi_index]=SelectCQI_fast_BLER10P(SNR_UPPERBOUND)
    SINR_LIM = [-Inf, -6.9, -5.1, -3.1, -1.4, 0.80, 2.60, 4.70, 6.50, 8.40, 10.40, 12.30, 14.10, 15.90, 17.75, 19.70];
    cqi_index = find(SINR_LIM <= SNR_UPPERBOUND, 1, 'last' ) - 1;
    %cqi_index = find(SINR_LIM <= SNR_UPPERBOUND,1,'last');
end