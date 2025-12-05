"""
Main orchestrator for GraphQL vs REST experiment.
- Runs data collection
- Runs analysis and generates plots
- Logs the pipeline steps
"""
import src.analyzers.analyze_results as analysis
import logging
import os
import sys

# Ensure project paths on sys.path
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
for p in (ROOT, SRC):
    if p not in sys.path:
        sys.path.insert(0, p)


# ROOT already set above


def setup_logging():
    os.makedirs(os.path.join(ROOT, "logs"), exist_ok=True)
    log_file = os.path.join(ROOT, "logs", "pipeline.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ],
    )
    logging.info("Pipeline logging initialized")


def run_pipeline():
    setup_logging()
    logging.info("Starting experiment pipeline")

    # 1) Run experiment (collection)
    logging.info("Step 1/3: Running experiment (collection)")
    from src.collectors.collector import run_experiment
    csv_path = run_experiment()
    logging.info(f"Experiment completed. CSV: {csv_path}")

    # 2) Run analysis (stats + plots)
    logging.info("Step 2/3: Running analysis")
    # Analyzer loads latest CSV automatically; but we can pass path if needed
    try:
        analysis.main() if hasattr(analysis, "main") else analysis.run()
    except Exception:
        # Fallback: execute via module function names likely present
        if hasattr(analysis, "analyze"):
            analysis.analyze()
        elif hasattr(analysis, "__main__"):
            pass
    logging.info(
        "Analysis completed. See analyzers/analysis_report.md and results/plots/")

    logging.info("Step 3/3: Pipeline finished")


if __name__ == "__main__":
    run_pipeline()
