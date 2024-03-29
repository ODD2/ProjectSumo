%5G SINR Channel Model
% This file implements a Tapped Delay Line (TDL-C) SINR_model for both UMa and
% UMi scenarios, per TR 38.901

% Use: Main BS vars: D2D_dist, h_BS, h_MS, fc, tx_p_dBm, bandwidth, min_tx_pwr_dBm
%      Intefrence BS: Intf_h_BS, Intf_h_MS, Intf_dist, Intf_pwr_dBm
%      Common Params: DS_Desired, CP, 
%      Main BS SINR_model: UMA_notUMI_Model, tx_delta_dBm, SINR_model

%      Set UMA_notUMI_Model == 1 (UMA), 0 (UMI)
%      Set SINR_model:
%      1 (DS impacts signal power)  
%      0 (DS impacts interference)
%
%     NOMA_Dir:
%     0 (Signal power decrease does not become interference)
%     1 (Signal power decrease becomes interference)

%      Notes:  DS refers to the state of all signals incoming to the RXs
%      (This is considered worst case).

% Revision history:
%  Dec 28, 2020)  Changed SF from normrnd to lognrnd, per text, UMA to UMI
%  for PL_intf, updated dp to make clear Hz
%  Dec 29, 2020)  Seperated out DS interference, moved to attenuation
%  portion of SINR, from interference
%  Dec 30, 2020) Verified log-normal definition, lognrnd changed to
%  normrnd.  Modified DS SINR_model to seperate Main BS from interference BS.
%  Updated Multi-path SINR_model to reduce impact with tx power scaling.  While
%  DS is modeled as being the same (desired) for both main and interfering
%  BS.
%  Jan 1, 2021)  Added min SINR, min DS
%  Jan 12, 2021) Added NOMA direction, NOMA_Dir (Signal decrease,
%  interference increase

function [ CQI_out,  Max_SINR_rx_dB_10, min_tx_p_dBm, PL_dB, INTF_dBm, DS_intf_dBm, Min_SINR_rx_dB_10, Min_INTF_dBm, Min_Spare_dBm] = SINR_Channel_Model_5G( D2D_dist, h_BS, h_MS, fc, tx_p_dBm, bandwidth, Intf_h_BS, Intf_h_MS, Intf_dist, Intf_pwr_dBm, DS_Desired, CP, UMA_notUMI_Model, tx_delta_dBm, min_tx_pwr_dBm, SINR_model, NOMA_Dir)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
CQI_out = 0;
Max_SINR_rx_dB_10 = -100;
min_tx_p_dBm = -100;
PL_dB = -100;
INTF_dBm = -100;
DS_intf_dBm = -100;
Min_SINR_rx_dB_10 = -100;
Min_INTF_dBm= -100;
Min_Spare_dBm= -100;
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
            
     %DS_Desired is in us
TDL_C_SCALED = bsxfun(@times,TDL_C ,[DS_Desired, 1]) ; %DS_Desired (ns) is the Delay Spread as observed by the UE
%CP = CP * 1e3; %10^-9;

%Path Loss SINR_model per TR 38.901

%Antennas
%BS=h_BS; %Per TR 38.901, h_BS=25m
%MS=1.5;  %Per TR 38.901, h_UT=1.5m --> 22.5m
BS_t=h_BS;
MS_t= h_MS;
Intf_BS_t = Intf_h_BS;
Intf_MS_t = Intf_h_MS;
%SINR_model 3D distance

%Shadow Fading
%DS_u = -0.24*log10(1 + fc) - 6.83; %NLOS, table 7.5.6 part 1 TR 38.901
%DS_sd = 0.16*log10(1+fc ) + 0.28;
%DS = normrnd(DS_u, DS_sd);

if(UMA_notUMI_Model)
    %SINR_model selection distance
    %fc is in GHZ, so c = 3.0 * 10^8
    c = 0.3; %3.0 * 10^8;
    d_bp_pl = 4*h_BS.*h_MS.*fc/c; %20/3 = 2.0 Ghz / 3.0 * 10^8, footnote 2 in winner+ SINR_model, Table 4.1, see TR 38.901 table 7.4.1.-1 note 1
    
    D3D_dist = sqrt(D2D_dist.^2 + (MS_t - BS_t)^2); %Since we are outside, always, we consider D2D_dist = D2D_dist_out
    [Prob_LOS_sig] = PrLOS(D2D_dist,MS_t,UMA_notUMI_Model);
    [PL_tot_sig] = UMA_Model(fc, D3D_dist, BS_t, MS_t, d_bp_pl, Prob_LOS_sig);
    %[Prob_LOS_sig] = PrLOS(D2D_dist_out,MS_t,UMA_notUMi)
    
    % LOS probability
    D3D_Intf_dist = sqrt(Intf_dist.*Intf_dist + (Intf_MS_t - Intf_BS_t).*(Intf_MS_t - Intf_BS_t)); %Since we are outside, always, we consider D2D_dist = D2D_dist_out
    %Prob_Los_Intf = min(18./Intf_dist,1).*(1-exp(-Intf_dist/36)) + exp(-Intf_dist/36); % LOS probability
    [Prob_LOS_intf] = PrLOS(Intf_dist,MS_t,UMA_notUMI_Model);
    [PL_tot_intf] = UMA_Model(fc, D3D_Intf_dist, Intf_BS_t, Intf_MS_t, d_bp_pl, Prob_LOS_intf);
else
    %SINR_model selection distance
    %fc is in GsHZ, so c = 3.0 * 10^8
    c = 0.3; %3.0 * 10^8;    
    d_bp_pl = 4*h_BS.*h_MS.*fc/c; %20/3 = 2.0 Ghz / 3.0 * 10^8, footnote 2 in winner+ SINR_model, Table 4.1, see TR 38.901 table 7.4.1.-1 note 1

    D3D_dist = sqrt(D2D_dist.^2 + (MS_t - BS_t).^2); %Since we are outside, always, we consider D2D_dist = D2D_dist_out
    [Prob_LOS_sig] = PrLOS(D2D_dist,MS_t,UMA_notUMI_Model);
    [PL_tot_sig] = UMI_Model(fc, D3D_dist, BS_t, MS_t, d_bp_pl, Prob_LOS_sig);
    
    D3D_Intf_dist = sqrt(Intf_dist.^2 + (Intf_MS_t - Intf_BS_t).^2); %Since we are outside, always, we consider D2D_dist = D2D_dist_out
    %Prob_Los_Intf = min(18./Intf_dist,1).*(1-exp(-Intf_dist/36)) + exp(-Intf_dist/36); % LOS probability
    [Prob_LOS_intf] = PrLOS(Intf_dist,MS_t,UMA_notUMI_Model);
    [PL_tot_intf] = UMI_Model(fc, D3D_Intf_dist, Intf_BS_t, Intf_MS_t, d_bp_pl, Prob_LOS_intf);
    if(PL_tot_intf < 0) %Handle case where we are too close to the Base Station, NOMA
        PL_tot_intf = 0;
    end
end
    

    
%Assume frequency flat fading
%sum_intf_MP_mW = 0;
%sum_intf_self_MP_mW = 0;
%Worst Case attenuation SINR_model
%for h = 1:length(Intf_pwr_dBm)
%    for i = 1:length(TDL_C_SCALED)
%        DS_Cur = TDL_C_SCALED(i, 1); %Always positive DS scaled
%        SR = abs(TDL_C_SCALED(i,2)); %Act as attenutation, negative gain
%        if((DS_Cur > CP)) %Only account for elements which are not filtered out by the CP
%            if(h == 1)
%                intf_dB_MP = tx_p_dBm -PL_tot_sig - SR; %Scaled is negative, so we add
%                sum_intf_self_MP_mW = sum_intf_self_MP_mW(h) + 10^(intf_dB_MP / 10);
%            end
%            intf_NOMA_dB = Intf_pwr_dBm(h) - PL_tot_intf(h) - SR; %Assume interference also undergoes delay spread interference
%            sum_intf_MP_mW = sum_intf_MP_mW + 10^(intf_NOMA_dB / 10);
%        end
%    end
%end
%sum_intf_MP = () + sum_intf_dB_MP;
%sum_intf_MP_mW = 10^(sum_intf_MP / 10);

%Delay Spread Model

%Caculate multiple other BS Multi-Path loss
[sum_intf_MP_mW_Orig] = Calc_DS_Inteference(Intf_pwr_dBm, TDL_C_SCALED, CP, PL_tot_intf);

%Caclulate Main BS Multi-Path loss
[sum_intf_self_MP_mW] = Calc_DS_Inteference(tx_p_dBm, TDL_C_SCALED, CP, PL_tot_sig);

INTF_impact_mw = 10.^(Intf_pwr_dBm./10) - 10.^(PL_tot_intf./10);
if(INTF_impact_mw > 0) %Ensure external direct inerference is lower bounded
    Intf_RX = 10*log10(INTF_impact_mw);
else
    Intf_RX = 0;
end
%Noise
N0_W = 10.^((-174-30)/10)*bandwidth; % AWGN Noise [Thermal noise density = -174dBm/Hz] 
%SINR Model
%Direct Model
N0_dBm = (10*log10(N0_W) + 30);
N0_mW = 10.^(N0_dBm/10);
if(1 == SINR_model)
    %Here we remove the cancelled signal power
    P_RX_mW = 10.^((tx_p_dBm - PL_tot_sig) / 10) - sum_intf_self_MP_mW;%was PL_DB_free_sig, cancellation
    sum_intf_MP_mW = sum_intf_MP_mW_Orig;
else
    P_RX_mW = 10.^((tx_p_dBm - PL_tot_sig) / 10);
    sum_intf_MP_mW = sum_intf_MP_mW_Orig + sum_intf_self_MP_mW;
end
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
Max_SINR_rx_dB_10 = SINR_rx_dB_10_new;
DS_intf_dBm = 10 * log10(sum_intf_self_MP_mW); %mW to dBm

%UE_CQI = SelectCQI(SINR_rx_dB, 0.1); %determine CQI for UE %submit r0
CQI_out = SelectCQI_BLER10P(Max_SINR_rx_dB_10); %determine CQI for UE %9-25
%CQI_out == 0 (outage)

%Determine minimum tx_power, used for NOMA
cur_CQI = CQI_out;
%min_tx_p_dBm = -9999; %Loop has not run
if(nargin < 14)
%if(~exist('tx_delta_dBm','var'))
    tx_delta_dBm = 0.10; %0.05
end
if(nargin < 15)
%if(~exist('min_tx_pwr_dBm','var'))
    tx_pwr_min_mW = 10; %minimum tx power, 200mW ~ 23 dBm is max, 0.2 mw is min
    min_tx_pwr_dBm = 10 * log10(tx_pwr_min_mW / 1);
end 
if(tx_p_dBm < min_tx_pwr_dBm)
    min_tx_p_dBm = -140;
else
    min_tx_p_dBm = min_tx_pwr_dBm; %Set to default
end

PL_dB = PL_tot_sig;
INTF_dBm = 10 * log10((N0_mW + INTF_P_RX_mW)/1); %interference dBm
Min_SINR_rx_dB_10 = SINR_rx_dB_10_new;
Min_INTF_dBm = INTF_P_RX_mW;

for cur_tx_p_dBm = tx_p_dBm:-tx_delta_dBm:min_tx_pwr_dBm %Set minimum    
    [sum_intf_self_MP_mW] = Calc_DS_Inteference(cur_tx_p_dBm, TDL_C_SCALED, CP, PL_tot_sig);
    
    if(1 == SINR_model)
        %Here we remove the cancelled signal power
        P_RX_mW_cur = 10.^((cur_tx_p_dBm - PL_tot_sig) / 10) - sum_intf_self_MP_mW;%was PL_DB_free_sig, cancellation
        sum_intf_MP_mW = sum_intf_MP_mW_Orig;
    else
        P_RX_mW_cur = 10.^((cur_tx_p_dBm - PL_tot_sig) / 10);
        sum_intf_MP_mW = sum_intf_MP_mW_Orig + sum_intf_self_MP_mW;
    end            

    %Calculate the spare power in dBm.
    cur_spare_pwr_dBm = 10*log10(10.^((tx_p_dBm) /10) - 10.^(cur_tx_p_dBm / 10));
    %Prevent restrict the lower bound of cur_spare_pwr_dBm 
    %to -100 to prevent -Inf dBm.
    cur_spare_pwr_dBm = max(cur_spare_pwr_dBm,-100);
    
    if(0 == NOMA_Dir)
        %Signal decrease does not cause interference
        sum_intf_MP_mW_2 = sum_intf_MP_mW;
    else
        %Signal decrease causes interference
        [sum_intf_other_MP_mW] = Calc_DS_Inteference(cur_spare_pwr_dBm, TDL_C_SCALED, CP, PL_tot_sig);
        INTF_add_RX_mw_cur =  10.^((cur_spare_pwr_dBm - PL_tot_sig) / 10);
        sum_intf_MP_mW_2 = INTF_add_RX_mw_cur + sum_intf_MP_mW + sum_intf_other_MP_mW;
    end
        
    if((Intf_RX) == 0) %lower bound interference
        INTF_P_RX_mW = sum_intf_MP_mW_2;
    else
        INTF_P_RX_mW = sum(10.^((Intf_RX) / 10)) + sum_intf_MP_mW_2; %10^(sum(Intf_pwr_dBm - PL_DB_free_intf) / 10);
    end
    

    SINR_rx_dB_10_cur = 10*log10( P_RX_mW_cur / (N0_mW + INTF_P_RX_mW ));
    CQI_out_cur = SelectCQI_BLER10P(SINR_rx_dB_10_cur);
    
    if(CQI_out_cur ~= cur_CQI)
       break;
    end
    
    min_tx_p_dBm = cur_tx_p_dBm;
    Min_SINR_rx_dB_10 = SINR_rx_dB_10_cur;
    Min_INTF_dBm = 10*log10(INTF_P_RX_mW);
    Min_Spare_dBm = cur_spare_pwr_dBm;
    
    if(CQI_out_cur == 0)
        break;
    end
end
%min_tx_dB = 


end

function [sum_DS_intf_MP_mW] = Calc_DS_Inteference(tx_p_dBm, TDL_C_SCALED, CP, PL_tot_sig)
%This function determine the multipath loss experienced by a single.
%This loss is modeled as interference
%Assume frequency flat fading
 
    list_DS_intf_MP_mW = zeros(1,length(tx_p_dBm));
    %Worst Case attenuation SINR_model   
    for i = 1:length(TDL_C_SCALED)
        DS_Cur = TDL_C_SCALED(i, 1); %Always positive DS scaled
        SR = abs(TDL_C_SCALED(i,2)); %Act as attenutation, negative gain
        if((DS_Cur > CP)) %Only account for elements which are not filtered out by the CP
            intf_dB_MP = tx_p_dBm -PL_tot_sig - SR; %Scaled is negative, so we add
            list_DS_intf_MP_mW = list_DS_intf_MP_mW + 10.^(intf_dB_MP / 10);
        end
    end
    sum_DS_intf_MP_mW = sum(list_DS_intf_MP_mW);
end


function [sig] = UMA_Model(fc, D3D_dist, BS_t, MS_t, d_bp_pl, pLOS)
    
    SF_UMA_LOS = normrnd(0, 4, size(D3D_dist)); %log10(normrnd(0, 7)); %7dB std deviation, random normal, mean 0
    %SF = 0;    
    %Per TR 38.901, Table 7.4.1-1
    
    %LOS SINR_model (only for 10 meters or more)
    %PL1
    PL_UMA_LOS_sig   = 28.0 + 22*log10(D3D_dist) + 20*log10(fc) + SF_UMA_LOS; %TR 38.901
    %PL2
    PL_UMA_LOS_dBP_sig = 28.0 + 40.*log10(D3D_dist) + 20*log10(fc) - 9*log10((d_bp_pl).^2+(BS_t-MS_t).^2) +SF_UMA_LOS; %TR 38.901
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
    
    %LOS SINR_model (only for 10 meters or more)
    %PL1
    PL_UMI_LOS_sig   = 32.4 + 21*log10(D3D_dist) + 20*log10(fc) + SF_UMi_LOS; %TR 38.901
    %PL2
    PL_UMI_LOS_dBP_sig = 32.4 + 40*log10(D3D_dist) + 20*log10(fc) - 9.5*log10((d_bp_pl).^2+(BS_t-MS_t).^2) +SF_UMi_LOS; %TR 38.901
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
                C = ((MS_t - 13)/10).^1.5;
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