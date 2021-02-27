import matlab.engine
import os
# Simulation Independent Variables
MATLAB_ENG = None


def InitializeSimulationContext():
    global MATLAB_ENG
    MATLAB_ENG = matlab.engine.start_matlab()
    MATLAB_ENG.addpath(os.getcwd() + "/matlab/")
    MATLAB_ENG.addpath(os.getcwd() + "/matlab/SelectCQI_bySNR/")
    MATLAB_ENG.addpath(os.getcwd() + "/matlab/PlannerV1/")
    MATLAB_ENG.InitializeSimulationContext(nargout=0)
