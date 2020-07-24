function [out] = GetThroughputPerRB(UsedCQI, SymbolPerSlot)
% GetThroughputPerSlot(UsedCQI, SymbolPerSlot)
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
% 闽CQI table弧
% > code rate(絏瞯)   = 獺ゑ疭计 / (獺ゑ疭计+喷ゑ疭计)
% > efficiency (瞯) = 獺ゑ疭计 / 羆才腹计
% パ獺ゑ疭计+喷ゑ疭计=羆ゑ疭计=羆才腹计*秸籹顶计┮
% 瞯 = 絏瞯*秸籹顶计
% ㄒ,CQI index = 1, QPSK, modulation order2, 絏瞯 = 78/1024 = 0.0762
% 瞯 = 0.1523 = 0.0762 * 2
% 
% ê1024莱赣碞琌ボよ獽

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