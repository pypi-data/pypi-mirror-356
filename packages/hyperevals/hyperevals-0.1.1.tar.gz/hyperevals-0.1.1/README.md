# HyperEvals

Hyperband-optimized parallelized prompt and model parameter tuning for evaluating LLMs.

## Motivation

Evaluating LLMs is both notoriously challenging and yet critical before confidently deploying in production environments. Seemingly small tweaks in prompts or upgrades to the model can have a significant impact on performance across various tasks, hence the need for carefully crafted evaluations. 

HyperEvals provides hyperband-optimized parallelized prompt and model parameter tuning for evaluating LLMs, inspired by W&B's sweeps combined with hyperband optimization.


<img width="905" alt="Screenshot 2025-06-19 at 9 27 03 AM" src="https://github.com/user-attachments/assets/2535e554-4c8e-4fdd-b84a-4c3e4aca7525" />

<img width="420" alt="image" src="https://github.com/user-attachments/assets/e2d99382-5e7d-40ba-9521-ffc1a5e0a5c3" />



## Installation

```bash
pip install hyperevals
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
dataset: data/diseases.csv
model: models/simple_model.py
scorer: scorers/basic_scorer.py
prompts: prompts
results_dir: results
num_examples: 5
sort: random
hyperband:
  num_trials: 2
  min_examples: 1
```

## TODO
- multi-step scorers for agent evals


Shape of the eval output:
| id | step | input | output | score |
|----|------|-------|--------|-------|
| 1  | 1    | "Hey, whats your name?" | "My name is John" | 0.95 |
| 1  | 2    | "What is your favorite color?" | "My favorite color is blue" | 0.95 |
| 1  | 3    | "What is your favorite food?" | "My favorite food is pizza" | 0.95 |
| 2  | 1    | "What is your name?" | "My name is John" | 0.95 |
| 2  | 2    | "Wow great!" | "..." | 0.95 |
