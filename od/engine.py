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
