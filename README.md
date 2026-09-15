# ProjectSumo

A network simulation tool for **Vehicle-to-Everything (V2X)** communication in **5G** networks. It combines Python-based networking logic, [Eclipse SUMO](https://eclipse.dev/sumo/) for road traffic simulation, and MATLAB for 5G channel modeling and resource allocation optimization.

## Overview

ProjectSumo simulates how vehicles communicate with roadside base stations under real traffic conditions, modeling the full stack from physical-layer signal quality (SINR, CQI) to application-layer data delivery, with QoS-differentiated OMA/NOMA scheduling.

**Key capabilities:**

- Realistic vehicle mobility via SUMO road traffic simulation
- 5G channel modeling with 3GPP TR 38.901 path loss models and TDL-C multipath fading
- OMA and NOMA (Non-Orthogonal Multiple Access) resource allocation, with an optimal MATLAB-solved mode and a fast approximation mode
- QoS-aware scheduling for critical and general traffic classes
- Emergency event simulation (earthquake scenario with a 5x critical-traffic surge)
- Parallel multi-scenario execution with configurable seeds and parameters
- Delivery latency and resource utilization statistics

## Architecture

```
ProjectSumo/
├── single.py              # Single simulation entry point
├── multi.py               # Parallel simulation manager
├── od/                    # Core Python package
│   ├── engine.py          # MATLAB engine interface
│   ├── vars.py            # Global simulation state
│   ├── env/
│   │   ├── config.py      # Simulation parameters
│   │   └── station.py     # Base station presets (UMA/UMI)
│   ├── network/
│   │   ├── controller.py  # Base station resource scheduler
│   │   ├── model.py       # Channel estimation & SINR calculation
│   │   ├── allocator.py   # OMA / NOMA allocation algorithms
│   │   ├── application.py # Application data reception
│   │   └── package.py     # Network packet structures
│   ├── vehicle/           # Vehicle simulation entities
│   ├── social/            # Social group management (CRASH, RCWS)
│   ├── event/             # Simulation events (earthquake)
│   └── misc/              # Logging, statistics, utilities
├── matlab/                # MATLAB signal processing modules
│   ├── SINR_Channel_Model.m
│   ├── SelectCQI.m
│   ├── GetThroughputPerRB.m
│   └── PlannerV1/         # Resource planning optimization
├── ntust.sumocfg          # SUMO simulation configuration
├── ntust.net.xml          # Road network topology
└── ntust.rou.xml          # Vehicle routes and departure rates
```


## Requirements

### Software

| Dependency | Purpose |
|---|---|
| Python 3.8 | Core simulation logic |
| [Eclipse SUMO](https://eclipse.dev/sumo/) | Road traffic simulation |
| MATLAB | 5G channel modeling and optimization |
| MATLAB Engine API for Python | Python–MATLAB bridge |

### Python Packages

Install via [Pipenv](https://pipenv.pypa.io/):

```bash
pipenv install
```

Key packages: `numpy`, `traci`, `matplotlib`, `pandas`, `psutil`, `openpyxl`, `jupyter`

## Usage

### Single Simulation

Run one simulation instance with the parameters defined in `od/env/config.py`:

```bash
pipenv run python single.py
```

### Parallel Simulations

Run multiple simulation scenarios concurrently (automatically manages memory and CPU resources):

```bash
pipenv run python multi.py
```

`multi.py` schedules a grid built from two sweeps:

- Allocator × RSU × QoS-reclassification × traffic-scale × seed: `NOMA_OPT`/`NOMA_APR` allocators, with/without UMI base stations, QoS reclassification enabled/disabled, traffic density 1.0x–1.4x, 20 seeds per configuration
- Dynamic social-group behaviour × size: every group-formation strategy at several group-size limits, with allocator/RSU/traffic fixed (`NOMA_APR`, RSU enabled, 1.4x traffic), 20 seeds per configuration

## Configuration

All tunable parameters live in `od/env/config.py`, grouped by subsystem (SUMO timing, network timing, base station RF, vehicle, event, paths):

```python
# SUMO
SUMO_SIM_GUI          = False      # launch sumo-gui instead of headless SUMO
SUMO_SECONDS_PER_STEP = 0.1        # seconds per SUMO simulation step

# Network
NET_SECONDS_PER_TS    = 0.0005     # seconds per network timeslot
NET_RB_SLOT_SYMBOLS   = 14         # OFDM symbols per resource block

# Base station bandwidth / frequency / max transmit power
BS_TOTAL_BAND = {UMA: 10e6, UMI: 5e6}    # Hz
BS_FREQ       = {UMA: 2,    UMI: 3.5}    # GHz
BS_TRANS_PWR  = {UMA: 23,   UMI: 10}     # dBm
```

Base station positions and types (UMA / UMI) are defined in `od/env/station.py`. The default scenario includes 2 UMA macro cells and 5 UMI small cells over the NTUST campus road network.

### Simulation Time Scales

The simulation operates across three interleaved time scales:

| Scale | Interval | Purpose |
|---|---|---|
| SUMO step | 100 ms | Vehicle position updates |
| Network step | 1 ms | Channel estimation, subscriptions |
| Timeslot | 0.5 ms | Resource block allocation, transmission |

## Network Model

### Base Stations

- **UMA (Urban Macro):** 500 m coverage radius, 10 MHz bandwidth
- **UMI (Urban Micro):** 50 m coverage radius, 5 MHz bandwidth

### Channel Estimation

MATLAB computes channel quality for each vehicle–BS pair using:

- 3GPP TR 38.901 path loss models
- TDL-C multipath fading
- SINR → CQI mapping (15 usable CQI levels per TS 36.213)

### Social Groups & QoS

Vehicles are organized into social groups with differentiated QoS:

| Group | Class | Priority | Use Case |
|---|---|---|---|
| `CRASH` | Critical | High | Collision/emergency alerts |
| `RCWS` | General | Normal | Road condition warnings |

Dynamic group creation is supported for large-scale scenarios.

### Resource Allocation

| Mode | Description |
|---|---|
| `OMA` | Orthogonal Multiple Access — exclusive RB assignment |
| `NOMA_OPT` | NOMA with optimal power allocation |
| `NOMA_APR` | NOMA with approximation (faster) |

`OMA` and `NOMA_OPT` are both solved via the MATLAB PlannerV1 optimizer (OMA constrains the solver to orthogonal power allocation); `NOMA_APR` uses a fast in-Python approximation instead.

### Event Simulation

The `EarthQuake` event increases the critical group's network request rate by 5x for the duration of the event, simulating emergency traffic surges.

## Output

Each scenario run writes to `data/<scenario_path>/report.pickle`, where `<scenario_path>` is derived from the `InterestConfig` (allocator type, RSU mode, QoS flag, traffic scale, seed, etc.). Reports include per-packet statistics:

- Application data delivery rate and latency
- Queue wait times and transmission times per base station
- Timeout and drop counts
- Resource allocation failure rates

Scenarios that fail to produce a report are logged to `scheme_fail_report.txt` by `multi.py`.

Use the Jupyter notebooks in `ipynb/graph/` to visualize results.

## License
MIT
