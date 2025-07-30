"""
Main evaluation class. 

Responsible for taking a config and running the evaluation. Runs the model file on the inputs and scores the outputs.
If the files are python, execute with python, otherwise just run the file. After every step, append output to a jsonl
output file corresponding to the run. Handle errors nicely. Progress bar. Very simple but nice Rich summary of the output.

Output shape:
| id | step | input | output | score |
|----|------|-------|--------|-------|
| 1  | 1    | "Hey, whats your name?" | "My name is John" | 0.95 |
| 1  | 2    | "What is your favorite color?" | "My favorite color is blue" | 0.95 |
| 1  | 3    | "What is your favorite food?" | "My favorite food is pizza" | 0.95 |
| 2  | 1    | "What is your name?" | "My name is John" | 0.95 |
| 2  | 2    | "Wow great!" | "..." | 0.95 |


Example config:
```yaml
dataset: /data/test.csv
model: /models/test.py
scorer: /scorers/scorer.py
eval_parallelism: 2
hyperband:
  min_examples: 10
  bands: [10, 20, 30, 40, 50]
```
"""

import glob
import json
import os
import random
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pandas as pd
from rich.console import Console
from rich.progress import Progress, TaskID

from .summary import print_summary

console = Console()


def _make_run_name(config: Dict[str, Any]) -> str:
    """Generate a run name for directories and files."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dataset_name = Path(config["dataset"]).stem
    model_name = Path(config["model"]).stem
    scorer_name = Path(config["scorer"]).stem
    return f"eval-{dataset_name}-{model_name}-{scorer_name}-{timestamp}"


def _make_results_filename(config: Dict[str, Any]) -> str:
    """Generate a filename for the output file."""
    return f"{_make_run_name(config)}.jsonl"


class Eval:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        # Create run directory and save results.jsonl inside it
        self.run_dir = self._create_run_directory()
        self.output_file = str(self.run_dir / "results.jsonl")

    def _get_results_base_dir(self) -> Path:
        """Get the base results directory, defaulting to 'results/' if not specified."""
        results_dir = self.config.get("results_dir", "results")
        return Path(results_dir)

    def _create_run_directory(self) -> Path:
        """Create a timestamped run directory within the results folder."""
        run_name = _make_run_name(self.config)
        run_dir = self._get_results_base_dir() / run_name
        run_dir.mkdir(parents=True, exist_ok=True)

        return run_dir

    def _get_prompt_file(self) -> str:
        """Get the first prompt file from the prompts directory, or empty string if none."""
        if "prompts" not in self.config:
            return ""

        prompts_dir = Path(self.config["prompts"])
        if not prompts_dir.exists():
            return ""

        # Get all files in prompts directory
        prompt_files = list(prompts_dir.glob("*"))
        prompt_files = [f for f in prompt_files if f.is_file()]

        if not prompt_files:
            return ""

        # Return the first prompt file (sorted for consistency)
        return str(sorted(prompt_files)[0])

    def _save_result(self, result: Dict[str, Any]):
        """Append result to JSONL file."""
        with open(self.output_file, "a") as f:
            f.write(json.dumps(result) + "\n")

    def run(self):
        """Run the evaluation."""
        # Load dataset
        df = pd.read_csv(self.config["dataset"])
        console.print(f"Loaded {len(df)} examples from {self.config['dataset']}")

        # Apply sorting if specified
        if self.config.get("sort") == "random":
            df = df.sample(frac=1, random_state=42).reset_index(drop=True)
            console.print("Dataset order randomized")

        # Limit number of examples if specified
        num_examples = self.config.get("num_examples")
        if num_examples is not None and num_examples > 0:
            original_len = len(df)
            df = df.head(num_examples)
            console.print(f"Limited to {len(df)} examples (from {original_len} total)")

        console.print(f"Output will be saved to: {self.output_file}")

        # Get prompt file
        prompt_file = self._get_prompt_file()
        if prompt_file:
            console.print(f"Using prompt file: {prompt_file}")
        else:
            console.print("No prompt file found, using empty prompt")

        # Initialize output file
        Path(self.output_file).unlink(missing_ok=True)

        results = []
        consecutive_errors = 0
        max_consecutive_errors = 3

        with Progress() as progress:
            task = progress.add_task("Evaluating...", total=len(df))

            for idx, row in df.iterrows():
                example_id = idx + 1
                input_text = str(row.get("input", ""))
                expected_output = str(row.get("expected", ""))

                # Run model with prompt
                model_output, model_error = run_script(
                    self.config["model"], input_text, prompt_file
                )

                # Surface model errors to console
                if model_error:
                    console.print(
                        f"[red]Model error for example {example_id}: {model_error}[/red]"
                    )

                # Run scorer
                score_output, scorer_error = run_script(
                    self.config["scorer"], input_text, "", model_output, expected_output
                )

                # Surface scorer errors to console
                if scorer_error:
                    console.print(
                        f"[yellow]Scorer error for example {example_id}: {scorer_error}[/yellow]"
                    )

                # Parse score
                try:
                    score = float(score_output) if score_output else 0.0
                except:
                    score = 0.0

                # Collect all errors
                errors = []
                if model_error:
                    errors.append(f"model: {model_error}")
                if scorer_error:
                    errors.append(f"scorer: {scorer_error}")

                # Track consecutive errors
                if errors:
                    consecutive_errors += 1
                else:
                    consecutive_errors = 0

                # Save result
                result = {
                    "id": example_id,
                    "step": 1,
                    "input": input_text,
                    "output": model_output,
                    "expected": expected_output,
                    "score": score,
                    "errors": errors,
                }

                self._save_result(result)
                results.append(result)

                progress.advance(task)

                # Check for early stopping due to consecutive errors
                if consecutive_errors >= max_consecutive_errors:
                    console.print(
                        f"\n[red]Stopping evaluation early: {max_consecutive_errors} consecutive errors detected[/red]"
                    )
                    console.print(
                        "This usually indicates a configuration issue with the model or scorer."
                    )

                    # Save partial results before raising exception
                    print_summary(results, self.output_file)

                    raise RuntimeError(
                        f"Evaluation stopped after {max_consecutive_errors} consecutive errors. "
                        f"Processed {len(results)} examples before stopping. "
                        f"Please check your model ({self.config['model']}) and scorer ({self.config['scorer']}) configuration. "
                        f"Common issues include: missing API keys, incorrect file paths, or script execution permissions."
                    )

        print_summary(results, self.output_file)
        return results


def run_script(
    script_path: str,
    input_text: str,
    prompt_file: str = "",
    model_output: str = "",
    expected_output: str = "",
) -> Tuple[str, str]:
    """Run script and return (output, error_msg)."""
    try:
        cmd_args = []
        if script_path.endswith(".py"):
            cmd_args = [sys.executable, script_path]
        else:
            cmd_args = [script_path]

        # Add prompt parameter if provided
        if prompt_file:
            cmd_args.extend(["--prompt", prompt_file])

        # Add model_output parameter if provided (for scorers)
        if model_output:
            cmd_args.extend(["--model-output", model_output])

        # Add expected_output parameter if provided (for scorers)
        if expected_output:
            cmd_args.extend(["--expected-output", expected_output])

        result = subprocess.run(
            cmd_args,
            input=input_text,
            text=True,
            capture_output=True,
            timeout=30,
        )

        if result.returncode != 0:
            error_msg = f"Script failed with code {result.returncode}: {result.stderr}"
            return result.stdout.strip() if result.stdout else "", error_msg
        return result.stdout.strip(), ""
    except Exception as e:
        error_msg = f"Exception running script: {str(e)}"
        return "", error_msg
