import matlab.engine
import os
# Simulation Independent Variables
MATLAB_ENG = matlab.engine.start_matlab()
MATLAB_ENG.addpath(os.getcwd() + "/matlab/")
MATLAB_ENG.addpath(os.getcwd() + "/matlab/SelectCQI_bySNR/")
MATLAB_ENG.addpath(os.getcwd() + "/matlab/NomaPlannerV1/")