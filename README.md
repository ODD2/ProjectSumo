# ProjectSumo

A network simulation tool for **Vehicle-to-Everything (V2X)** communication in **5G** networks. The project integrates three major components: Python-based networking logic, [Eclipse SUMO](https://eclipse.dev/sumo/) for realistic road traffic simulation, and MATLAB for 5G wireless channel modeling and resource allocation optimization.

---

## Overview

ProjectSumo simulates how vehicles communicate with roadside base stations under real traffic conditions. It models the full stack from physical-layer signal quality (SINR, CQI) to application-layer data delivery, supporting both OMA and NOMA resource allocation schemes with QoS-differentiated scheduling.

**Key capabilities:**

- Realistic vehicle mobility via SUMO road traffic simulation
- 5G channel modeling with 3GPP TR 38.901 path loss models and TDL-C multipath fading
- OMA and NOMA (Non-Orthogonal Multiple Access) resource allocation with optimization and approximation modes
- QoS-aware scheduling for critical and general traffic classes
- Emergency event simulation (earthquake scenario with 5x critical traffic surge)
- Parallel multi-scenario execution with configurable seeds and parameters
- Comprehensive delivery latency and resource utilization statistics

---

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

### Simulation Time Scales

The simulation operates across three interleaved time scales:

| Scale | Interval | Purpose |
|---|---|---|
| SUMO step | 0.1 s | Vehicle position updates |
| Network step | 1 ms | Channel estimation, subscriptions |
| Timeslot | 0.5 ms | Resource block allocation, transmission |

---

## Requirements

### Software

| Dependency | Purpose |
|---|---|
| Python 3.x | Core simulation logic |
| [Eclipse SUMO](https://eclipse.dev/sumo/) | Road traffic simulation |
| MATLAB | 5G channel modeling and optimization |
| MATLAB Engine API for Python | Python–MATLAB bridge |

### Python Packages

Install via [Pipenv](https://pipenv.pypa.io/):

```bash
pipenv install
```

Key packages: `numpy`, `traci`, `matplotlib`, `pandas`, `psutil`, `openpyxl`, `jupyter`

---

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

`multi.py` schedules combinations of:
- Resource allocators: `NOMA_OPT`, `NOMA_APR`
- RSU modes: with/without UMI base stations
- QoS reclassification: enabled/disabled
- Traffic densities: 1.0x – 1.4x
- Multiple random seeds per configuration

---

## Configuration

Edit `od/env/config.py` to adjust simulation parameters:

```python
# SUMO
SUMO_GUI           = False       # Enable SUMO GUI
SUMO_STEP_LENGTH   = 0.1        # Simulation step (seconds)

# Network
TIMESLOT_DURATION  = 0.5e-3     # Timeslot duration (seconds)
NUM_RB_SYMBOLS     = 14         # OFDM symbols per resource block

# Base station (UMA example)
UMA_BANDWIDTH      = 10e6       # 10 MHz
UMA_FREQUENCY      = 2.0e9      # 2 GHz carrier
UMA_TX_POWER       = 46         # dBm
```

Base station positions and types (UMA / UMI) are defined in `od/env/station.py`. The default scenario includes 2 UMA macro cells and 5 UMI small cells over the NTUST campus road network.

---

## Network Model

### Base Stations

- **UMA (Urban Macro):** 500 m coverage radius, 10 MHz bandwidth
- **UMI (Urban Micro):** 50 m coverage radius, 5 MHz bandwidth

### Channel Estimation

MATLAB computes channel quality for each vehicle–BS pair using:
- 3GPP TR 38.901 path loss models
- TDL-C multipath fading
- SINR → CQI mapping (15 CQI levels per TS 36.213)

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

### Event Simulation

The `EarthQuake` event increases the critical group's network request rate by 5x for the duration of the event, simulating emergency traffic surges.

---

## Output

Simulation results are saved to `data/report.pickle` and include per-packet statistics:

- Application data delivery rate and latency
- Queue wait times and transmission times per base station
- Timeout and drop counts
- Resource allocation failure rates

Use the Jupyter notebooks in `ipynb/graph/` to visualize results.

---

## Cleaning Up

Remove generated log and statistics files:

```bash
bash cleanup.sh
```

---

## License
MIT
