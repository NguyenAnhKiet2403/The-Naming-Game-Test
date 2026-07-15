# The Naming Game (MATLAB -> Python Port)

This repository is a Python port of a Naming Game implementation originally developed in MATLAB at VUB.  
The main goal of this port is long-term compatibility and easier extension in Python workflows (analysis, ML, reproducibility, HPC scripting).

Reference explanation of the model:  
[The Naming Game (VUB PDF)](https://ai.vub.ac.be/sites/default/files/naming-game_0.pdf)

## What This Project Implements

### Core simulation loop
- `NamingGame.py` defines the abstract simulation skeleton:
  - `pick -> produce -> interpret -> success/failure/adopt`
  - simulation/iteration orchestration
  - pluggable pairing strategy
  - pluggable export hooks
  - multi-threshold consensus handling

### Naming Game variants
- `variants/BaselineNG.py`
  - baseline one-topic Naming Game
  - random 7-character token invention
  - failure updates listener topic association
- `variants/Imitation.py`
  - `Imitation`: topic-level replacement on adoption (listener drops older names for that topic)
  - `Imitationv2`: allows multiple names per topic; prunes alternatives only on success
- `variants/ABNG.py`
  - A/B binary naming specialization (invents only `A` or `B`)
  - built on `Imitationv2`

### Agent pairing algorithms
- `namingGameTools/AgentPairs.py`
  - `generateVillatoro`: Villatoro-style pairing baseline
  - `generate`: unique speaker-listener pairing by sampling existing edges and removing reused agents
  - `generateWeighted`: weighted edge sampling (probability proportional to edge weight) with random direction

### Pair-selection strategies
- `namingGameTools/Strategy.py`
  - `multi`: all generated pairs play
  - `mono`: one random pair plays
  - `halfPopular` / `halfUnpopular`
  - `nPopular(n)` / `nUnpopular(n)`

### Network generation algorithms
- `namingGameTools/MatrixFactory.py`
  - ring-lattice generation (`makeLatticeMatrix`)
  - scale-free generation via preferential attachment-style edge sampling (`makeScaleFreeMatrix`)
  - small-world generation (lattice + random shortcuts) (`makeSmallWorldMatrix`)
  - synthetic small-world population sampler (`generateSmallWorldPopulation`)
  - weighted edge generation via injectable `generateWeight`

### Export/metric hooks
- `exports/possibleExports.py` implements:
  - `namesInvented`
  - `namesInCirculation`
  - `preferredAction` (per-agent per-iteration action matrix)
  - `namePopularity`
  - `consensusIteration` (supports multiple consensus thresholds)
  - `actionsPerformed`
  - `agentMemory`
  - `consensusPercentageEvolution`

### Graph/clinical analysis workflows
- `graphAnalysis/` scripts compute:
  - characteristic path length
  - global efficiency
  - local efficiency
  - degree/strength distributions
  - clustering/transitivity
  - small-worldness (`mean clustering / mean shortest path`)
- `graph/patient/` scripts add:
  - convergence histograms/scatters/boxplots
  - ECDF and grouped behavioral comparisons
  - t-tests and quartile analyses
  - Kaplan-Meier survival curves
  - animated preferred-action overlays on patient connectivity graphs

### Synthetic neural predictors
- `SyntheticNN/` contains two-layer PyTorch MLP scripts for predicting convergence-related outcomes from patient/network features.

## Repository Inventory (File-by-File)

### Root
- `NamingGame.py`: abstract base class and runtime loop.
- `convergenceScript.py`: Ray-distributed convergence extraction over HCP patient matrices.
- `preferredActionScript.py`: Ray-distributed preferred-action extraction for BRUMEG data.
- `namingGame.pbs`: SLURM + Ray cluster launch script for HPC runs.
- `requirements.txt`: dependency pinning.
- `README.md`: project documentation.
- `LICENSE`: project license.

### `variants/`
- `variants/BaselineNG.py`: baseline Naming Game behavior.
- `variants/Imitation.py`: imitation variants (`Imitation`, `Imitationv2`).
- `variants/ABNG.py`: A/B token specialization.

### `namingGameTools/`
- `namingGameTools/AgentPairs.py`: pair generation methods (including weighted).
- `namingGameTools/MatrixFactory.py`: lattice/scale-free/small-world generators.
- `namingGameTools/Strategy.py`: strategy functions for selecting active pairs.

### `exports/`
- `exports/export.py`: export hook interface.
- `exports/possibleExports.py`: concrete export implementations and registry.

### `tests/`
- `tests/NamingGameTest.py`: lifecycle and consensus-loop tests.
- `tests/BaselineNGTest.py`: baseline memory/adoption checks.
- `tests/ImitationTest.py`: imitation and v2 behavior checks.
- `tests/AgentPairsTest.py`: pair uniqueness/connectivity/weighting checks.
- `tests/MatrixFactoryTest.py`: matrix generation shape/connectivity/reproducibility checks.

### `MATLAB Legacy Port/`
- `MATLAB Legacy Port/makeLatticeMatrix.py`: direct legacy translation.
- `MATLAB Legacy Port/makeScaleFreeMatrix.py`: direct legacy translation.
- `MATLAB Legacy Port/makeSmallWorldMatrix.py`: direct legacy translation.
- `MATLAB Legacy Port/pairAgents.py`: original pairing translation.
- `MATLAB Legacy Port/pairAgentsImproved.py`: optimized pairing translation.
- `MATLAB Legacy Port/pairAgentsVillatoroWise.py`: Villatoro-style pairing translation.

### `SyntheticNN/`
- `SyntheticNN/NamingGamePredictor.py`: MLP predictor script.
- `SyntheticNN/PredictAverageConversion.py`: MLP predictor on average convergence.
- `SyntheticNN/MSPredictor.py`: MLP predictor for MS-related target.

### `graphAnalysis/`
- `graphAnalysis/characteristicPathLength.py`
- `graphAnalysis/localEfficiency.py`
- `graphAnalysis/degreeDistribution.py`
- `graphAnalysis/Clustering.py`
- `graphAnalysis/smallWorldNess.py`
- `graphAnalysis/smallWorldNessGraph.py`

### `graph/generated/`
- `graph/generated/namesPerIteration.py`: mean invented names per iteration plots.
- `graph/generated/namesInCirculation.py`: popularity trajectory plots.
- `graph/generated/preferredAction.py`: preferred-action heatmaps.
- `graph/generated/preferredActionTimelapse.py`: preferred-action animation export.
- `graph/generated/consensusTimePerNeighbour.py`: consensus-vs-neighborhood boxplots.
- `graph/generated/consensusTimePerEstablishingLinks.py`: consensus-vs-scale-free-link plots.
- `graph/generated/CTPN small World.py`: small-world neighborhood/random-link consensus plots.
- `graph/generated/CTPN violinplot.py`: violin version of consensus-time visualization.

### `graph/patient/Individual/`
- `graph/patient/Individual/AIMSPlotter.py`: BRUMEG behavioral + convergence exploratory plots.
- `graph/patient/Individual/AIMSPlotterGrouped.py`: grouped HCP behavioral/convergence analyses.
- `graph/patient/Individual/SurvivalPlots.py`: Kaplan-Meier survival plotting.

### `graph/patient/Individual/csv_results/`
- `graph/patient/Individual/csv_results/consensusTime.py`: patient-group consensus-time boxplots.
- `graph/patient/Individual/csv_results/graphCircleAnalysisCSV.py`: preferred-action video from CSV exports.
- `graph/patient/Individual/csv_results/histogram.py`: convergence histogram.
- `graph/patient/Individual/csv_results/meanConvergence.py`: mean convergence trend per patient group.
- `graph/patient/Individual/csv_results/scatterPlot.py`: convergence scatter plotting.
- `graph/patient/Individual/csv_results/videos/agent_choices_graph_100206.mp4`: generated visualization.

### `graph/patient/Individual/regular/`
- `graph/patient/Individual/regular/CTPN patientData.py`: direct per-patient consensus boxplots from matrices.
- `graph/patient/Individual/regular/SDMTchart.py`: SDMT line charts by group.
- `graph/patient/Individual/regular/graphCircleAnalysis.py`: preferred-action video directly from simulation output.
- `graph/patient/Individual/regular/meanPlotConvergence95.py`: average convergence (95%) per patient.
- `graph/patient/Individual/regular/preferredActionPatient.py`: single-patient preferred-action heatmap.
- `graph/patient/Individual/regular/scatterPlotConvergence95.py`: convergence scatter at 95% threshold.
- `graph/patient/Individual/regular/videos/agent_choices_graph_102513.mp4`: generated visualization.

### `graph/patient/Misc/`
- `graph/patient/Misc/visualizeSC.py`: structural connectivity heatmaps.
- `graph/patient/Misc/weightDistribution.py`: global weight distribution and distribution fitting.

### `patients/`
- `patients/patientData.py`: shared patient I/O/transforms + global dataset bindings.
- `patients/graphMetadata.py`: network metadata extraction and merge utilities.
- `patients/output/convergenceBRUMEG_AAL2_abs_50.csv`: convergence export sample.

### `patients/HCP/`
- `patients/HCP/behavioral.csv`: raw HCP behavioral data.
- `patients/HCP/subjects.txt`: subject IDs.
- `patients/HCP/lowesthighestpatients.txt`: predefined high/low processing-speed cohorts.
- `patients/HCP/loadBehavioralInfo.py`: behavioral subset extraction script.
- `patients/HCP/loadHCPData.py`: netmats TXT -> CSV conversion script.

### `patients/BRUMEG_functional/`
- `patients/BRUMEG_functional/loadBrumegData.py`: BRUMEG source conversion script.

### Additional artifacts
- `output/exampleConvergence.csv`: sample convergence summary output.
- `plots/Kaplan-Meier.png`: exported survival plot.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Minimal Usage Example

```python
from variants.ABNG import ABNG
from namingGameTools import Strategy, MatrixFactory as mf

matrix = mf.MatrixFactory(triangular=True).makeLatticeMatrix(numberOfAgents=40, numberOfNeighbors=4)

ng = ABNG(
    simulations=5,
    maxIterations=1000,
    strategy=Strategy.multi,
    output=["popularity", "consensus"],
    consensusScore=[0.8, 0.9, 0.95, 1.0],
    display=False,
)

results = ng.start(matrix)
print(results["consensus"])
```

## Current Caveats
This version works on data which was present in the clusters at the AIMS laboratory. So many of the proposed games do not work with real-life data due to the data not being found. Please change the directories of data accordingly to work on real-life adjacency matrices.

## Why This Port Exists

This codebase preserves the original MATLAB research logic while moving execution, analysis, and extensibility into Python.  
That gives better compatibility with modern data science tooling, easier HPC/cluster orchestration, and a clearer path for future maintenance.
