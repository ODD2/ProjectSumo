function [ CQI_out,  SINR_rx_dB_10] = SINR_Channel_Model_5G( D2D_dist, h_BS, h_MS, fc, tx_p_dBm, bandwidth, Intf_h_BS, Intf_h_MS, Intf_dist, Intf_pwr_dBm, DS_Desired, CP, UMA_notUMI_Model)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here

%Per TR 38.901, table 7.7.2-3 (normalized) (Normalized Delay, power in dB)
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
CP = CP * 10^-9;

%Path Loss model per TR 38.901

%Antennas
BS=h_BS; %Per TR 38.901, h_BS=25m
MS=1.5;  %Per TR 38.901, h_UT=1.5m --> 22.5m
BS_t=h_BS;
MS_t= h_MS;
Intf_BS_t = Intf_h_BS;
Intf_MS_t = Intf_h_MS;
%model 3D distance

%model selection distance
d_bp_pl = 4*h_BS.*h_MS.*20/3; %20/3 = 2.0 Ghz / 3.0 * 10^8, footnote 2 in winner+ model, Table 4.1, see TR 38.901 table 7.4.1.-1 note 1
%Shadow Fading
DS_u = -0.24*log10(1 + fc) - 6.83; %NLOS, table 7.5.6 part 1 TR 38.901
DS_sd = 0.16*log10(1+fc ) + 0.28;
DS = normrnd(DS_u, DS_sd);

if(UMA_notUMI_Model)
    D3D_dist = sqrt(D2D_dist^2 + (MS_t - BS_t)^2); %Since we are outside, always, we consider D2D_dist = D2D_dist_out
    [Prob_LOS_sig] = PrLOS(D2D_dist,MS_t,UMA_notUMI_Model);
    [PL_tot_sig] = UMA_Model(fc, D3D_dist, BS_t, MS_t, d_bp_pl, Prob_LOS_sig);
    %[Prob_LOS_sig] = PrLOS(D2D_dist_out,MS_t,UMA_notUMi)
    
    % LOS probability
    D3D_Intf_dist = sqrt(Intf_dist.*Intf_dist + (Intf_MS_t - Intf_BS_t).*(Intf_MS_t - Intf_BS_t)); %Since we are outside, always, we consider D2D_dist = D2D_dist_out
    %Prob_Los_Intf = min(18./Intf_dist,1).*(1-exp(-Intf_dist/36)) + exp(-Intf_dist/36); % LOS probability
    [Prob_LOS_intf] = PrLOS(Intf_dist,MS_t,UMA_notUMI_Model);
    [PL_tot_intf] = UMA_Model(fc, D3D_Intf_dist, Intf_BS_t, Intf_MS_t, d_bp_pl, Prob_LOS_intf);
else
    D3D_dist = sqrt(D2D_dist^2 + (MS_t - BS_t)^2); %Since we are outside, always, we consider D2D_dist = D2D_dist_out
    [Prob_LOS_sig] = PrLOS(D2D_dist,MS_t,UMA_notUMI_Model);
    [PL_tot_sig] = UMI_Model(fc, D3D_dist, BS_t, MS_t, d_bp_pl, Prob_LOS_sig);
    
    D3D_Intf_dist = sqrt(Intf_dist.^2 + (Intf_MS_t - Intf_BS_t).^2); %Since we are outside, always, we consider D2D_dist = D2D_dist_out
    %Prob_Los_Intf = min(18./Intf_dist,1).*(1-exp(-Intf_dist/36)) + exp(-Intf_dist/36); % LOS probability
    [Prob_LOS_intf] = PrLOS(Intf_dist,MS_t,UMA_notUMI_Model);
    [PL_tot_intf] = UMA_Model(fc, D3D_Intf_dist, Intf_BS_t, Intf_MS_t, d_bp_pl, Prob_LOS_intf);
end
    

    
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
CQI_out = max(SelectCQI_fast_BLER10P(SINR_rx_dB_10),1); %determine CQI for UE %9-25

end

function [sig] = UMA_Model(fc, D3D_dist, BS_t, MS_t, d_bp_pl, pLOS)
    
    SF_UMA_LOS = normrnd(0, 4, size(D3D_dist)); %log10(normrnd(0, 7)); %7dB std deviation, random normal, mean 0
    %SF = 0;    
    %Per TR 38.901, Table 7.4.1-1
    
    %LOS model (only for 10 meters or more)
    %PL1
    PL_UMA_LOS_sig   = 28.0 + 22*log10(D3D_dist) + 20*log10(fc) + SF_UMA_LOS; %TR 38.901
    %PL2
    PL_UMA_LOS_dBP_sig = 28.0 + 40.*log10(D3D_dist) + 20*log10(fc) - 9*log10((d_bp_pl)^2+(BS_t-MS_t).^2) +SF_UMA_LOS; %TR 38.901
    %Path Loss, free space
    SF_FS = normrnd(0,7.8);
    PL_UMA_free_sig = 32.4 + 20*log10(fc)+ 30.*log10(D3D_dist) + SF_FS; %%%%%%%%%%%%%%%%%%%%%%%%
    %Model descion (PathLoss to device)
    if D3D_dist <= d_bp_pl
        PL_UMa_matrix_sig = PL_UMA_LOS_sig; % 10m<d<d_BP': LOS1
    else
       PL_UMa_matrix_sig = PL_UMA_LOS_dBP_sig; % d_BP'<d<5000m: LOS2 
    end
    % should greater than or equal for free space
    PL_tot_sig_LOS = max(PL_UMA_free_sig, PL_UMa_matrix_sig);
    %NLOS
    SF_UMa_NLOS = normrnd(0,6, size(D3D_dist));
    PL_UMA_NLOS_sig = 13.54 + 39.08*log10(D3D_dist)+20*log10(fc)-0.6*(MS_t-1.5) + SF_UMa_NLOS;
    PL_tot_sig_NLOS = max(PL_tot_sig_LOS,PL_UMA_NLOS_sig);
    
    x = rand;
    if(x <= pLOS)
        PL_tot_sig = PL_tot_sig_LOS;
    else
        PL_tot_sig = PL_tot_sig_NLOS;
    end
    
    sig = PL_tot_sig;

end

function [sig] = UMI_Model(fc, D3D_dist, BS_t, MS_t, d_bp_pl, pLOS)
    
    SF_UMi_LOS = normrnd(0, 4, size(D3D_dist)); %log10(normrnd(0, 7)); %7dB std deviation, random normal, mean 0
    %SF = 0;    
    %Per TR 38.901, Table 7.4.1-1
    
    %LOS model (only for 10 meters or more)
    %PL1
    PL_UMI_LOS_sig   = 32.4 + 21*log10(D3D_dist) + 20*log10(fc) + SF_UMi_LOS; %TR 38.901
    %PL2
    PL_UMI_LOS_dBP_sig = 32.4 + 40*log10(D3D_dist) + 20*log10(fc) - 9.5*log10((d_bp_pl)^2+(BS_t-MS_t)^2) +SF_UMi_LOS; %TR 38.901
    %Path Loss, free space
    SF_FS = normrnd(0,8.2);
    PL_UMI_free_sig = 32.4 + 20*log10(fc)+ 31.9*log10(D3D_dist) + SF_FS; %%%%%%%%%%%%%%%%%%%%%%%%
    %Model descion (PathLoss to device)
    if D3D_dist <= d_bp_pl
        PL_UMI_matrix_sig = PL_UMI_LOS_sig; % 10m<d<d_BP': LOS1
    else
       PL_UMI_matrix_sig = PL_UMI_LOS_dBP_sig; % d_BP'<d<5000m: LOS2 
    end
    % should greater than or equal for free space
    PL_tot_sig_LOS = max(PL_UMI_free_sig, PL_UMI_matrix_sig);
    %NLOS
    SF_UMI_NLOS = normrnd(0,7.82, size(D3D_dist));
    PL_UMI_NLOS_sig = 22.4 + 35.3*log10(D3D_dist)+21.3*log10(fc)-0.3*(MS_t-1.5) + SF_UMI_NLOS;
    PL_tot_sig_NLOS = max(PL_tot_sig_LOS,PL_UMI_NLOS_sig);
    
    x = rand;
    if(x <= pLOS)
        PL_tot_sig = PL_tot_sig_LOS;
    else
        PL_tot_sig = PL_tot_sig_NLOS;
    end
    
    sig = PL_tot_sig;

end


function [Prob_LOS_sig] = PrLOS(D2D_dist_out,MS_t,UMA_notUMi)
    if(UMA_notUMi)
        if(D2D_dist_out <= 18)
            Pr_LOS_sig = 1;
        else
            if(MS_t <= 13)
                C = 0;
            else %should not exceed 23m
                C = ((MS_t - 13)/10)^1.5;
            end
            Pr_LOS_sig = (18 ./ D2D_dist_out + exp(-D2D_dist_out ./ 63).*(1-18./D2D_dist_out)) .* ...
                         (1 + ((C*5/4*(D2D_dist_out./100).^3) .* exp(-D2D_dist_out./150) )); 
        end
    else
        if(D2D_dist_out <= 18)
            Pr_LOS_sig = 1;
        else
            Pr_LOS_sig = (18 ./ D2D_dist_out + exp(-D2D_dist_out ./ 36).*(1-18./D2D_dist_out));
        end
    end
    Prob_LOS_sig = Pr_LOS_sig;
end