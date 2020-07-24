function [CQI_out] = Get_BS_CQI_Vector(BS, UE)
    MACRO_BS_NUM = 1;
    N_BS = length(BS);
    CQI_Iter = zeros(N_BS, 1);
    SINR_Iter = zeros(N_BS, 1);
    
    for tx_BS_num = 1:N_BS
        Intf_dist = zeros(1, N_BS);
        Intf_pwr_dBm = zeros(1, N_BS);
        %Confirm settings with 3GPP specs
        if(tx_BS_num == MACRO_BS_NUM)
            tx_p_dBm = 23;
        else
            tx_p_dBm = 10;
        end
        for intf_BS_num = 1:N_BS
            if(intf_BS_num == tx_BS_num)
                continue;
            end
            if(intf_BS_num == MACRO_BS_NUM)
                h_BS = 25;
                h_MS = 0.8;
                CP = 4.69; %us
                bandwidth = 180000; %180 kHz per RB
                Intf_pwr_dBm(intf_BS_num) = 23;
            else
                h_BS = 10;
                h_MS = 0.8;
                CP = 2.34; %us
                bandwidth = 360000; %360 kHz per RB
                Intf_pwr_dBm(intf_BS_num) = 18;
            end
            
            
            CP = CP * 1000; %us to ns
            %SINR Model
            %BS=h_BS;
            %MS=1.5;
            %BS_t=h_BS;
            %MS_t=0.8;
            SF = normrnd(0, 7); %7dB std deviation, random normal, mean 0
            SF = 0;
            DS_Desired = normrnd(0, 4); %up to 4 us
            DS_Desired = DS_Desired * 1000; %us to ns
            fc = 2.0;
            %Locations
            UE_dist = sqrt((BS(tx_BS_num).Loc_x-UE.Loc_x)^2+(BS(tx_BS_num).Loc_y-UE.Loc_y)^2);
            Intf_BS.Loc_x = BS(intf_BS_num).Loc_x;
            Intf_BS.Loc_y = BS(intf_BS_num).Loc_y;
            Intf_dist(intf_BS_num) = sqrt((Intf_BS.Loc_x - UE.Loc_x)^2 + (Intf_BS.Loc_y - UE.Loc_y)^2);
            %Intf_pwr_mW(intf_BS_num) = BS(intf_BS_num).power; %dBm
            [CQI_Iter(tx_BS_num), SINR_Iter(tx_BS_num)] = SINR_Channel_Model( UE_dist, h_BS, h_MS, fc, tx_p_dBm, bandwidth, Intf_dist, Intf_pwr_dBm, DS_Desired, CP);
        end
    end
    CQI_out = CQI_Iter;
end