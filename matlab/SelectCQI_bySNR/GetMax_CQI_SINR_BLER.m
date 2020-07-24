function [SINR_min]=GetMax_CQI_SINR_BLER(BLER_UPPERBOUND)
%% [cqi_index snr bler]=SelectCQI(SNR_UPPERBOUND, BLER_UPPERBOUND)
% report the highest CQI which can satisfy the following condition:
%   1. Achieving BLER <= BLER_UPPERBOUND
%   2. Required SNR <= SNR_UPPERBOUND
% and this function reports the CQI and correspond Requiring-SNR
%   and BLER to this CQI
%
% SNR<->BLER table is follow the Table 7.2.3-1 of TS 36.213 v12.3.0
% [Table 7.2.3-1]
%-----------------------------------------------------------
%| CQI index | modulation | code rate x 1024 | efficiency |
%|    0     |        out of range                     |
%|    1     |    QPSK    |        78      |   0.1523   |
%|    2     |    QPSK    |       120      |   0.2344   |
%|    3     |    QPSK    |       193      |   0.3770   |
%|    4     |    QPSK    |       308      |   0.6016   |
%|    5     |    QPSK    |       449      |   0.8770   |
%|    6     |    QPSK    |       602      |   1.1758   |
%|    7     |    16QAM   |       378      |   1.4766   |
%|    8     |    16QAM   |       490      |   1.9141   |
%|    9     |    16QAM   |       616      |   2.4063   |
%|    10    |    64QAM   |       466      |   2.7305   |
%|    11    |    64QAM   |       567      |   3.3223   |
%|    12    |    64QAM   |       666      |   3.9023   |
%|    13    |    64QAM   |       772      |   4.5234   |
%|    14    |    64QAM   |       873      |   5.1152   |
%|    15    |    64QAM   |       948      |   5.5547   |
%------------------------------------------------------------
% 闽CQI table弧
% > code rate(絏瞯)   = 獺ゑ疭计 / (獺ゑ疭计+喷ゑ疭计)
% > efficiency (瞯) = 獺ゑ疭计 / 羆才腹计
% パ獺ゑ疭计+喷ゑ疭计=羆ゑ疭计=羆才腹计*秸籹顶计┮
% 瞯 = 絏瞯*秸籹顶计
% ㄒ,CQI index = 1, QPSK, modulation order2, 絏瞯 = 78/1024 = 0.07617
% 瞯 = 0.1523 = 0.07617 * 2
% 
% ê1024莱赣碞琌ボよ獽
    %if nargin < 2
    %    ME = MException('MyComponent:invalidFormat', sprintf('ERROR INPUT!\n [cqi_index]=SelectCQI(snr, BLER_UPPERBOUND)\n'));
    %    throw(ME); %terminate
    %end
    
    persistent snr_to_bler_with_cqi    %set variable to static variable (faster)
    if isempty(snr_to_bler_with_cqi)
        load('SNR_BLER_CQI.mat');
    end
    
    [~, BLER_LEVEL, CQI_LEVEL] = size(snr_to_bler_with_cqi);
    cqi_index = 0;
    for index = CQI_LEVEL:-1:1
        min_SNR = 40; %SINR larger than TX power
        for b = BLER_LEVEL:-1:1
            %the 1st-row is the SNR
            %the 2nd-row is the BLER
            %snr = snr_to_bler_with_cqi(1, b, index);
            %bler = snr_to_bler_with_cqi(2, b, index);
            
            %if( bler <= BLER_UPPERBOUND)
            cur_BLER = snr_to_bler_with_cqi(2, b, index);
            if( cur_BLER <= BLER_UPPERBOUND)
                %if(snr <= SNR_UPPERBOUND)
                %if(snr_to_bler_with_cqi(1, b, index) <= SNR_UPPERBOUND)
                cur_SNR = snr_to_bler_with_cqi(1, b, index);
                if(cur_SNR < min_SNR)
                    min_SNR = cur_SNR;
                end
            end
        end
        SINR_min(index) = min_SNR;
    end
end