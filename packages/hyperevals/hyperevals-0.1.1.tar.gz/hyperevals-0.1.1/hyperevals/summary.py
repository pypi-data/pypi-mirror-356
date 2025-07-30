"""
Summary display functionality for evaluation results.
"""

from pathlib import Path
from typing import Any, Dict, List

from rich.console import Console
from rich.table import Table

console = Console()


def print_summary(results: List[Dict[str, Any]], output_file: str):
    """Print evaluation summary with stats and examples."""
    if not results:
        console.print("No results to summarize.")
        return

    # Determine summary file path
    output_path = Path(output_file)
    summary_file = output_path.parent / "summary.txt"

    scores = [r["score"] for r in results if isinstance(r["score"], (int, float))]
    avg_score = sum(scores) / len(scores) if scores else 0

    # Count errors
    error_count = sum(1 for r in results if r.get("errors"))
    has_errors = error_count > 0

    # Check if any results have expected output
    has_expected = any(r.get("expected") for r in results)

    # Create a file console for saving output
    with open(summary_file, "w") as f:
        file_console = Console(file=f, width=120)

        # Print to both console and file
        _print_summary_content(
            results,
            output_file,
            avg_score,
            error_count,
            has_errors,
            has_expected,
            console,
        )
        _print_summary_content(
            results,
            output_file,
            avg_score,
            error_count,
            has_errors,
            has_expected,
            file_console,
        )

    console.print(f"\nSummary saved to: {summary_file}")


def _print_summary_content(
    results: List[Dict[str, Any]],
    output_file: str,
    avg_score: float,
    error_count: int,
    has_errors: bool,
    has_expected: bool,
    console_output: Console,
):
    """Print summary content to the given console (screen or file)."""
    console_output.print("\n\n")

    # Stats table
    stats_table = Table(title="Evaluation Summary")
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Value", style="green")

    stats_table.add_row("Total Examples", str(len(results)))
    stats_table.add_row("Average Score", f"{avg_score:.3f}")
    stats_table.add_row("Examples with Errors", str(error_count))
    stats_table.add_row("Output File", output_file)

    console_output.print(stats_table)

    # Examples table
    console_output.print("\n")
    examples_table = Table(title="Sample Results")
    examples_table.add_column("ID", style="dim", width=4)
    examples_table.add_column("Input", style="white", width=30)
    examples_table.add_column("Output", style="blue", width=40)

    # Add expected column only if there's expected output
    if has_expected:
        examples_table.add_column("Expected", style="yellow", width=40)

    examples_table.add_column("Score", style="green", width=8)

    # Add errors column only if there are errors
    if has_errors:
        examples_table.add_column("Errors", style="red", width=30)

    # Select examples: mix of high/low scores and errors
    selected_examples = _select_examples(results, max_examples=8)

    for example in selected_examples:
        # Truncate long text
        input_text = _truncate_text(example["input"], 40)
        output_text = _truncate_text(example["output"], 60)

        row_data = [
            str(example["id"]),
            input_text,
            output_text,
        ]

        # Add expected column if needed
        if has_expected:
            expected_text = str(example.get("expected", ""))
            expected_text = _truncate_text(expected_text, 40)
            row_data.append(expected_text)

        # Add score after expected (if present)
        row_data.append(f"{example['score']:.2f}")

        # Add errors column if needed
        if has_errors:
            error_text = (
                "; ".join(example.get("errors", [])) if example.get("errors") else ""
            )
            error_text = _truncate_text(error_text, 40)
            row_data.append(error_text)

        examples_table.add_row(*row_data)

    console_output.print(examples_table)


def _select_examples(
    results: List[Dict[str, Any]], max_examples: int = 8
) -> List[Dict[str, Any]]:
    """Select a mix of high/low scoring examples and error examples."""
    if len(results) <= max_examples:
        return results

    # Sort by score
    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    # Get examples with errors
    error_examples = [r for r in results if r.get("errors")]

    # Get high scoring examples (top half)
    high_scoring = sorted_results[: len(sorted_results) // 2]

    # Get low scoring examples (bottom half)
    low_scoring = sorted_results[len(sorted_results) // 2 :]

    selected = []

    # Add some error examples first (up to 2)
    selected.extend(error_examples[:2])

    # Add high scoring examples
    remaining = max_examples - len(selected)
    high_count = min(remaining // 2, len(high_scoring))
    selected.extend(high_scoring[:high_count])

    # Add low scoring examples
    remaining = max_examples - len(selected)
    low_count = min(remaining, len(low_scoring))
    selected.extend(low_scoring[:low_count])

    # Remove duplicates while preserving order
    seen = set()
    unique_selected = []
    for item in selected:
        if item["id"] not in seen:
            seen.add(item["id"])
            unique_selected.append(item)

    return unique_selected[:max_examples]


def _truncate_text(text: str, max_length: int) -> str:
    """Truncate text to max_length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def print_hyperband_summary(
    initial_results: List[Dict[str, Any]], final_results: List[Dict[str, Any]]
):
    """Print hyperband improvement summary comparing initial vs final results."""
    if not initial_results or not final_results:
        console.print("Insufficient data for hyperband comparison.")
        return

    # Calculate average scores
    initial_scores = [
        r["score"] for r in initial_results if isinstance(r["score"], (int, float))
    ]
    final_scores = [
        r["score"] for r in final_results if isinstance(r["score"], (int, float))
    ]

    initial_avg = sum(initial_scores) / len(initial_scores) if initial_scores else 0
    final_avg = sum(final_scores) / len(final_scores) if final_scores else 0

    improvement = final_avg - initial_avg
    improvement_color = (
        "green" if improvement > 0 else "red" if improvement < 0 else "yellow"
    )

    print("\n\n")

    # Overall improvement table
    improvement_table = Table(title="Hyperband Improvement Summary")
    improvement_table.add_column("Metric", style="cyan")
    improvement_table.add_column("Initial", style="blue")
    improvement_table.add_column("Final", style="blue")
    improvement_table.add_column("Change", style=improvement_color)

    improvement_table.add_row(
        "Average Score", f"{initial_avg:.3f}", f"{final_avg:.3f}", f"{improvement:+.3f}"
    )
    improvement_table.add_row(
        "Total Examples", str(len(initial_results)), str(len(final_results)), ""
    )

    console.print(improvement_table)

    # Example-by-example comparison (show a sample)
    print("\n")
    comparison_table = Table(title="Sample Score Changes")
    comparison_table.add_column("ID", style="dim", width=4)
    comparison_table.add_column("Input", style="white", width=30)
    comparison_table.add_column("Score Change", style="white", width=15)

    # Match examples by ID and show score changes
    initial_by_id = {r["id"]: r for r in initial_results}
    sample_count = 0
    max_samples = 8

    for final_result in final_results:
        if sample_count >= max_samples:
            break

        result_id = final_result["id"]
        if result_id in initial_by_id:
            initial_result = initial_by_id[result_id]
            initial_score = initial_result["score"]
            final_score = final_result["score"]

            if isinstance(initial_score, (int, float)) and isinstance(
                final_score, (int, float)
            ):
                score_change = final_score - initial_score

                # Color code the score change
                if score_change > 0:
                    score_text = f"[green]{initial_score:.1f} → {final_score:.1f} (+{score_change:.1f})[/green]"
                elif score_change < 0:
                    score_text = f"[red]{initial_score:.1f} → {final_score:.1f} ({score_change:.1f})[/red]"
                else:
                    score_text = f"[yellow]{initial_score:.1f} → {final_score:.1f} (0.0)[/yellow]"

                input_text = _truncate_text(final_result["input"], 40)

                comparison_table.add_row(str(result_id), input_text, score_text)
                sample_count += 1

    console.print(comparison_table)
