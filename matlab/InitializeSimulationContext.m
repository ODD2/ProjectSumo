function [] = InitializeSimulationContext(seed)
% InitializeSimulationContext  Seed the MATLAB random-number generator for a
%   simulation run.
%
%   InitializeSimulationContext(SEED) sets the global RNG state to SEED so
%   that stochastic elements (shadow fading, multipath delays, LOS/NLOS
%   selection) are fully reproducible across repeated runs with the same
%   InterestConfig.rng_seed.
%
%   Called once per simulation run from od/engine.py after the MATLAB engine
%   has been started.
%
%   Input:
%     seed - Integer random seed forwarded from InterestConfig.rng_seed.
	rng(seed)
end