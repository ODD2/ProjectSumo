function [out] = GetThroughputPerRB(UsedCQI, SymbolPerSlot)
% GetThroughputPerRB  Compute the number of bits carried by one resource block.
%
%   OUT = GetThroughputPerRB(USEDCQI, SYMBOLPERSLOT) returns the bit
%   capacity of one resource block (RB) for the given CQI index and number
%   of OFDM symbols per slot.
%
%   Formula:
%     bits = 12 subcarriers × SymbolPerSlot × efficiency(UsedCQI)
%
%   Spectral efficiency values follow 3GPP TS 36.213 Table 7.2.3-1.
%   CQI = 0 (out of range) is mapped to index 16, which has zero efficiency,
%   returning 0 bits.
%
%   Inputs:
%     UsedCQI       - CQI index (0-15, scalar or array).
%                     CQI 0 is treated as unusable and returns 0 bits.
%     SymbolPerSlot - Number of OFDM symbols per slot (typically 14 for
%                     normal cyclic prefix, or 12 for extended CP).
%
%   Output:
%     out - Number of bits per resource block (scalar or array matching
%           the shape of UsedCQI).
%
% return the Throughput per slot in bit (including the length of CRC)
% RB: one slot(in time)
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
% ����CQI table������
% > code rate(�X�v)   = �H����S�� / (�H����S��+�����S��)
% > efficiency (�Ĳv) = �H����S�� / �`�Ÿ���
% �ѩ�H����S��+�����S��=�`��S��=�`�Ÿ���*�ջs���ơA�ҥH
% �Ĳv = �X�v*�ջs����
% �Ҧp,CQI index = 1, QPSK, modulation order��2, �X�v = 78/1024 = 0.0762
% �Ĳv = 0.1523 = 0.0762 * 2
% 
% ����1024���ӴN�O���F���ܪ���K

    %if CQI == 0 then set CQI to 16
    UsedCQI(UsedCQI == 0) = 16; %16 is an unexpected value to avoid being selected as Group's CQI
    
    persistent efficiency;
    if isempty(efficiency)
        efficiency = [0.1523 0.2344 0.3770 0.6016 0.8770 1.1758 1.4766 1.9141 2.4063 2.7305 3.3223 3.9023 4.5234 5.1152 5.5547  0];
    end    
    out = 12 * SymbolPerSlot .* efficiency(UsedCQI);
    % 12 subcarrier * (6 or 7 symbols per slot) * efficiency
    % = bits / RB
end