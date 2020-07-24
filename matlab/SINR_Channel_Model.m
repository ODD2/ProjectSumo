function [ CQI_out, SINR_rx_dB_10 ] = SINR_Channel_Model( D2D_dist, h_BS, h_MS, fc, tx_p_dBm, bandwidth, Intf_dist, Intf_pwr_dBm, DS_Desired, CP)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here

%Per T% 38.901, table 7.7.2-3 (normalized) (Normalized Delay, power in dB)
TDL_C = [0     , -4.4 ; ...
         0.2099, -1.2 ; ...
         0.2219, -3.5 ; ...
         0.2329, -5.2 ; ...
         0.2176, -2.5 ; ...
         0.6366,    0 ; ...
         0.6448, -2.2 ; ...
         0.6560, -3.9 ; ...
         0.6584, -7.4 ; ...
         0.7935, -7.1 ; ...
         0.8213, -10.7; ...
         0.9336, -11.1; ...
         1.2285, -5.1 ; ...
         1.3083, -6.8 ; ...
         2.1704, -8.7 ; ...
         2.7105, -13.2; ...
         4.2589, -13.9; ...
         4.6003, -13.9; ...
         5.4902, -15.9; ...
         5.6077, -17.1; ...
         6.3065, -16  ; ...
         6.6374, -15.7; ...
         7.0427, -21.6; ...
         8.6523, -22.8; ...
         ];
            
TDL_C_SCALED = TDL_C .* [DS_Desired * 10^(-9), 1] ; %DS_Desired (ns) is the Delay Spread as observed by the UE


%Antennas
BS=h_BS;
MS=1.5;
BS_t=h_BS;
MS_t= h_MS;
%model selection distance
d_bp_pl = 4*h_BS.*h_MS.*20/3; %20/3 = 2.0 Ghz / 3.0 * 10^8, footnote 2 in winner+ model, Table 4.1
%Shadow Fading
DS_u = -0.24*log10(1 + fc) - 6.83; %NLOS, table 7.5.6 part 1 TR 38.901
DS_sd = 0.16*log10(1+fc ) + 0.28;
DS = normrnd(DS_u, DS_sd);
SF = normrnd(0, 7); %log10(normrnd(0, 7)); %7dB std deviation, random normal, mean 0
%SF = 0;    
%LOS model (only for 10 meters or more)
PL_B1_sig = 22.7*log10(D2D_dist) + 27.0 + 20*log10(fc) + SF; %sf 3dB
PL_B1_2_sig = 40*log10(D2D_dist) + 7.56-17.3*log10(BS_t)-17.3*log10(MS_t)+2.7*log10(fc)+SF;
%LOS model (only for 10 meters or more)
PL_B1_intf = 22.7*log10(Intf_dist) + 27.0 + 20*log10(fc) + SF; %sf 3dB
PL_B1_2_intf = 40*log10(Intf_dist) + 7.56-17.3*log10(BS_t)-17.3*log10(MS_t)+2.7*log10(fc)+SF;
%http://projects.celtic-initiative.org/winner+/WINNER+%20Deliverables/D5.3_v1.0.pdf

%Path Loss, free space
PL_DB_free_sig = 20*log10(D2D_dist)+ 46.4 + 20*log10(fc/5);
PL_DB_free_intf = 20*log10(Intf_dist)+ 46.4 + 20*log10(fc/5); %Winner-2 model
    
% LOS probability
Prob_Los = min(18./Intf_dist,1).*(1-exp(-Intf_dist/36)) + exp(-Intf_dist/36); % LOS probability

%Model descion (PathLoss to device)
if D2D_dist < d_bp_pl
    PL_b1_matrix_sig = PL_B1_sig; % 10m<d<d_BP': LOS1
else
   PL_b1_matrix_sig = PL_B1_2_sig; % d_BP'<d<5000m: LOS2 
end
% should greater than or equal for free space
PL_tot_sig = max(PL_DB_free_sig, PL_b1_matrix_sig);

%Model decision (Interference)
if Intf_dist < d_bp_pl
    PL_b1_matrix_intf = PL_B1_intf; % 10m<d<d_BP': LOS1
else
   PL_b1_matrix_intf = PL_B1_2_intf; % d_BP'<d<5000m: LOS2 
end
% should greater than or equal for free space
PL_tot_intf = max(PL_DB_free_intf, PL_b1_matrix_intf);
%PL_tot_intf = PL_DB_free; %Assume FreeSpace Path Loss
    
%Assume frequency flat fading
sum_intf_MP_mW = 0; 
%Worst Case attenuation model
for i = 1:length(TDL_C_SCALED)
    DS_Cur = TDL_C_SCALED(i, 1);
    if((DS_Cur > CP)) %Only account for elements which are not filtered out by the CP
        intf_dB_MP = tx_p_dBm -PL_tot_sig + (TDL_C_SCALED(i,2)); %Scaled is negative, so we add
        sum_intf_MP_mW = sum_intf_MP_mW + 10^(intf_dB_MP / 10);
    end
end
%sum_intf_MP = () + sum_intf_dB_MP;
%sum_intf_MP_mW = 10^(sum_intf_MP / 10);


if(Intf_pwr_dBm > PL_tot_intf) %Ensure external direct inerference is lower bounded
    Intf_RX = Intf_pwr_dBm - PL_tot_intf;
else
    Intf_RX = 0;
end
%Noise
N0_W = 10^((-174-30)/10)*bandwidth; % AWGN Noise [Thermal noise density = -174dBm/Hz] 
%SINR Model
%Direct Model
N0_dBm = (10*log10(N0_W) + 30);
N0_mW = 10^(N0_dBm/10);
P_RX_mW = 10^((tx_p_dBm - PL_tot_sig) / 10);%was PL_DB_free_sig
if((Intf_RX) == 0) %lower bound interference
    INTF_P_RX_mW = sum_intf_MP_mW;
else
    INTF_P_RX_mW = sum(10.^((Intf_RX) / 10)) + sum_intf_MP_mW; %10^(sum(Intf_pwr_dBm - PL_DB_free_intf) / 10);
end
SINR_rx_dB_10_new=10*log10( ...
                P_RX_mW / ... %Signal (mW)
                ( ...
                N0_mW ... %Noise
                + ...
                INTF_P_RX_mW ... %Intf
                ) ...
                );

%SINR_rx_dB = 10*log10(SINR_rx)+30;
SINR_rx_dB_10 = SINR_rx_dB_10_new;

%UE_CQI = SelectCQI(SINR_rx_dB, 0.1); %determine CQI for UE %submit r0
CQI_out = SelectCQI(SINR_rx_dB_10, 0.1); %determine CQI for UE %9-25

end

