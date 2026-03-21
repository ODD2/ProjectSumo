function [SINR_min]=GetMax_CQI_SINR_BLER(BLER_UPPERBOUND)
% GetMax_CQI_SINR_BLER  Return the minimum required SINR for every CQI level.
%
%   SINR_MIN = GetMax_CQI_SINR_BLER(BLER_UPPERBOUND) scans the SNR-BLER lookup
%   table (SNR_BLER_CQI.mat) and returns, for each CQI index (1–15), the
%   lowest SNR at which BLER <= BLER_UPPERBOUND.
%
%   Input:
%     BLER_UPPERBOUND - Maximum tolerable block error rate (0–1, e.g. 0.1).
%
%   Output:
%     SINR_min - 1×15 vector of minimum SINR values (dB) indexed by CQI.
%                Set to 40 dB for any CQI with no qualifying table entry.
%
% SNR<->BLER table follows Table 7.2.3-1 of TS 36.213 v12.3.0
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
% ����CQI table������
% > code rate(�X�v)   = �H����S�� / (�H����S��+�����S��)
% > efficiency (�Ĳv) = �H����S�� / �`�Ÿ���
% �ѩ�H����S��+�����S��=�`��S��=�`�Ÿ���*�ջs���ơA�ҥH
% �Ĳv = �X�v*�ջs����
% �Ҧp,CQI index = 1, QPSK, modulation order��2, �X�v = 78/1024 = 0.07617
% �Ĳv = 0.1523 = 0.07617 * 2
% 
% ����1024���ӴN�O���F���ܪ���K
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