import matlab.engine
import os
# Simulation Independent Variables
MATLAB_ENG = None


def InitializeSimulationContext(interest_config):
    global MATLAB_ENG
    if(MATLAB_ENG == None):
        MATLAB_ENG = matlab.engine.start_matlab()
        MATLAB_ENG.addpath(os.getcwd() + "/matlab/")
        MATLAB_ENG.addpath(os.getcwd() + "/matlab/SelectCQI_bySNR/")
        MATLAB_ENG.addpath(os.getcwd() + "/matlab/PlannerV1/")
        MATLAB_ENG.InitializeSimulationContext(int(interest_config.rng_seed), nargout=0)


def TerminateMatlabEngine():
    global MATLAB_ENG
    if(not MATLAB_ENG == None):
        MATLAB_ENG.quit()


CQI_SINR = [
    float("-inf"),
    -6.9,
    -5.1,
    -3.1,
    -1.4,
    0.80,
    2.60,
    4.70,
    6.50,
    8.40,
    10.40,
    12.30,
    14.10,
    15.90,
    17.75,
    19.70
]


def SelectCQI_BLER10P(SINR):
    for i in range(0, len(CQI_SINR), 1):
        if(SINR < CQI_SINR[i]):
            return i - 1
    else:
        return i


RB_EFFICIENCY = [
    0,
    0.1523,
    0.2344,
    0.3770,
    0.6016,
    0.8770,
    1.1758,
    1.4766,
    1.9141,
    2.4063,
    2.7305,
    3.3223,
    3.9023,
    4.5234,
    5.1152,
    5.5547
]


def GetThroughputPerRB(CQI, SymbolPerSlot):
    CQI = int(CQI)
    SymbolPerSlot = int(SymbolPerSlot)
    return round(12.0 * SymbolPerSlot * RB_EFFICIENCY[CQI])
