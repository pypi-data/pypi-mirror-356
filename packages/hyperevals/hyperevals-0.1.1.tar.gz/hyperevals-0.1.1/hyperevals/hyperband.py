"""
Mock Hyperband implementation. Identifies the best and worst performing examples in an eval, then 
uses an LLM to generate a new prompt and model parameters for the next iteration. Uses litellm.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from litellm import completion

from .eval import _make_run_name

ANALYSIS_PROMPT = """You are an expert at analyzing LLM evaluation results and creating better prompts.

I ran an evaluation and got these results. Please analyze the best and worst performing examples:

BEST PERFORMING EXAMPLES:
{best_examples}

WORST PERFORMING EXAMPLES:
{worst_examples}

PREVIOUS PROMPT:
{previous_prompt}

Based on this analysis, please create an improved system prompt that would help the model perform better on the worst cases while maintaining performance on the best cases.

Return ONLY the improved prompt text, no other commentary or explanation."""


class Hyperband:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

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

    def analyze_results(
        self,
        results: List[Dict[str, Any]],
        previous_prompt: str = "You are a helpful assistant.",
    ) -> str:
        """Analyze results and generate an improved prompt."""
        if not results:
            raise ValueError("No results to analyze")

        # Sort results by score
        sorted_results = sorted(results, key=lambda x: x.get("score", 0), reverse=True)

        # Get best and worst examples
        num_examples = min(3, len(sorted_results))
        best_examples = sorted_results[:num_examples]
        worst_examples = sorted_results[-num_examples:]

        # Format examples for analysis
        def format_examples(examples):
            formatted = []
            for ex in examples:
                formatted.append(f"Input: {ex['input']}")
                formatted.append(f"Output: {ex['output']}")
                formatted.append(f"Score: {ex['score']}")
                formatted.append("---")
            return "\n".join(formatted)

        best_formatted = format_examples(best_examples)
        worst_formatted = format_examples(worst_examples)

        # Generate analysis prompt
        analysis_prompt = ANALYSIS_PROMPT.format(
            best_examples=best_formatted,
            worst_examples=worst_formatted,
            previous_prompt=previous_prompt,
        )

        try:
            # Use LLM to analyze and create improved prompt
            response = completion(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": analysis_prompt}],
                max_tokens=300,
            )

            return str(response.choices[0].message.content).strip()
        except Exception as e:
            print(f"Error generating improved prompt: {e}")
            return "You are a helpful assistant."

    def save_new_prompt(self, prompt_text: str, run_dir: Path) -> str:
        """Save new prompt to the run directory and return the path."""
        # Create a timestamped prompt file within the run directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prompt_file = run_dir / f"generated_prompt_{timestamp}.txt"

        with open(prompt_file, "w") as f:
            f.write(prompt_text)

        return str(prompt_file)

    def get_previous_prompt(self) -> str:
        """Get the most recent prompt from existing run directories or original prompts directory."""
        # First check for generated prompts in results directories
        results_base_dir = self._get_results_base_dir()
        if results_base_dir.exists():
            # Find all run directories
            run_dirs = [d for d in results_base_dir.iterdir() if d.is_dir()]

            # Look for generated prompts in run directories
            all_generated_prompts = []
            for run_dir in run_dirs:
                generated_prompts = list(run_dir.glob("generated_prompt_*.txt"))
                all_generated_prompts.extend(generated_prompts)

            if all_generated_prompts:
                # Get the most recent generated prompt
                latest_prompt_file = max(
                    all_generated_prompts, key=lambda f: f.stat().st_mtime
                )
                try:
                    with open(latest_prompt_file, "r") as f:
                        return f.read().strip()
                except Exception as e:
                    print(
                        f"Error reading generated prompt file {latest_prompt_file}: {e}"
                    )

        # Fall back to original prompts directory
        if "prompts" in self.config:
            prompts_dir = Path(self.config["prompts"])
            if prompts_dir.exists():
                prompt_files = list(prompts_dir.glob("*.txt"))
                if prompt_files:
                    latest_prompt_file = max(
                        prompt_files, key=lambda f: f.stat().st_mtime
                    )
                    try:
                        with open(latest_prompt_file, "r") as f:
                            return f.read().strip()
                    except Exception as e:
                        print(f"Error reading prompt file {latest_prompt_file}: {e}")

        return "You are a helpful assistant."

    def run(self, results: List[Dict[str, Any]], run_dir: Optional[Path] = None) -> str:
        """Main hyperband iteration - analyze results and create new prompt."""
        print("Running hyperband analysis...")

        # Use provided run directory or create a new one
        if run_dir is None:
            run_dir = self._create_run_directory()

        # Get the previous prompt
        previous_prompt = self.get_previous_prompt()

        # Analyze results and generate improved prompt
        improved_prompt = self.analyze_results(results, previous_prompt)

        # Save the new prompt in the run directory
        prompt_file = self.save_new_prompt(improved_prompt, run_dir)

        print(f"Generated new prompt: {prompt_file}")
        print(f"Prompt content: {improved_prompt}")

        return prompt_file
