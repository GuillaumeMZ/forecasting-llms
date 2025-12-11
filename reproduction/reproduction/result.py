from pathlib import Path

import matplotlib.pyplot as plt
import polars as pl

from .property import Property

def _generate_histograms(results: pl.DataFrame, property_name: str, output_directory: Path) -> None:
    for (model, temperature, violations) in results.rows():
        # remove the model vendor prefix to avoid / in filenames
        model = model.split("/")[-1]

        plt.figure()
        plt.hist(violations, bins=20, range=(0.0, 1.0), edgecolor='white')
        plt.title(f"{model}, T = {temperature}")
        plt.xlabel("Violation")
        plt.ylabel("Frequency")
        plt.grid(axis='y', alpha=0.75)
        plt.savefig(str(output_directory / f"{property_name}_histogram_{model}_temp_{temperature}.png"))
        plt.close()

def _strong_violations_percentage(violations: list[float]) -> float:
    if len(violations) == 0:
        return 0.0

    strong_violations = [v for v in violations if v > 0.2]
    return len(strong_violations) / len(violations) * 100.0

def _mean(violations: list[float]) -> float:
    if len(violations) == 0:
        return 0.0

    return sum(violations) / len(violations)

def serialize_results(property: Property, results: pl.DataFrame, output_directory: Path) -> None:
    # save intermediate results to json (for debugging purposes)
    results.write_json(output_directory / f"{property.name()}_results.json")
    # compute violations from answers
    results = results.with_columns(results["answers"].map_elements(property.violation, return_dtype=pl.Float64).alias("violation"))
    # drop answers column
    results = results.drop("answers")
    # group by model, temperature and question_id and compute mean violation
    results = results.group_by(["model", "temperature", "question_id"]).mean()
    # prepare the data for histogram generation
    results = results.drop("question_id").group_by(["model", "temperature"]).agg(pl.col("violation").alias("violations"))
    # generate histograms
    _generate_histograms(results, property.name(), output_directory)
    # split violations into rows "mean_violation" and "strong_violations_percentage"
    results = results.with_columns([
        results["violations"].map_elements(_mean, return_dtype=pl.Float64).alias("mean_violation"),
        results["violations"].map_elements(_strong_violations_percentage, return_dtype=pl.Float64).alias("strong_violations_percentage"),
    ])
    results = results.drop("violations")
    # save results to csv
    results.write_csv(output_directory / f"{property.name()}_violations.csv")