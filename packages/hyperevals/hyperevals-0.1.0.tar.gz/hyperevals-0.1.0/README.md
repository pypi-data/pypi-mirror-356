# HyperEvals

Hyperband-optimized parallelized prompt and model parameter tuning for evaluating LLMs.

## Motivation

Evaluating LLMs is both notoriously challenging and yet critical before confidently deploying in production environments. Seemingly small tweaks in prompts or upgrades to the model can have a significant impact on performance across various tasks, hence the need for carefully crafted evaluations. 

HyperEvals provides hyperband-optimized parallelized prompt and model parameter tuning for evaluating LLMs, inspired by W&B's sweeps combined with hyperband optimization.

## Installation

```bash
pip install hyperevals
```

For development installation:
```bash
git clone https://github.com/griffintarpenning/hyperevals.git
cd hyperevals
pip install -e ".[dev]"
```

## Quick Start

```bash
# Install the package
pip install hyperevals

# Run with a configuration file
hyperevals run config.yaml

# Show version
hyperevals --version
```

## Usage

### MVP Flow
1. Create a CSV dataset
2. Create a prompt template
3. Create an executable Model file
4. Create executable scorers 
5. Create a config file
6. Run the evaluation
7. Iterate on prompt and model parameters
8. Hyperband kills bad optimizations early
9. Final prompt is reported w/ accuracy

### Sample Configuration

```yaml
dataset: /data/test.csv
prompt_template: /prompts/test.txt
model: /models/test.py
scorer: /scorers/scorer.py
max_parallelism: 2  
hyperband:
  min_examples: 10
  bands: [10, 20, 30, 40, 50]
```
