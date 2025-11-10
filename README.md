# Reproduce and Replicate of "Evaluating Superhuman Models with Consistency Checks - LLMs forecasting future events"

## Introduction

This study (“Evaluating Superhuman Models with Consistency Checks”, 2023) proposed a set of logical self-consistency tests for LLM forecasts: Negation, Paraphrasing, Monotonicity, Bayes’ rule.

I focus on reproducing the Monotonicity experiment (50 forecasting questions × 5 years).
This is the easiest part that can be reproduced directly from the publicly released dataset.

The original paper reports (GPT-4-0314, temp=0) Monotonicity violation:
| Model                       | Mean violation | >0.2 strong violation % |
| --------------------------- | -------------: | ----------------------: |
| GPT-3.5-turbo-0301(3 times) |      **0.229** |              **42.0 %** |
| GPT-3.5-turbo-0301(6 times) |      **0.136** |              **26.0 %** |
| GPT-4-0314(3 times)         |      **0.105** |              **16.0 %** |
| GPT-4-0314(6 times)         |      **0.089** |              **12.0 %** |


My goal:

1. Reproduce the original reported 0.105 / 16% on the public raw log

2. Replicate the experiment with a different LLM (via OpenRouter) to see if consistency holds

## Reproducibility

### How to Reproduce the Results

1. **Requirements**  

   | Component | Version |
   | --------- | ------- |
   | Python    | 3.11    |
   | numpy     | 1.26.4  |
   | scipy     | 1.11.4  |
   | requests  | 2.31.0  |

   - List dependencies and their versions (e.g., Python, R, libraries, etc.).
   - Specify any system requirements.

3. **Setting Up the Environment**  

   - Provide instructions for using the Dockerfile to create a reproducible environment:  

     ```bash
     docker build -t reproducible-project .
     docker run -it reproducible-project
     ```

4. **Reproducing Results**  

   - Describe how to run the automated scripts or notebooks to reproduce data and analyze results:

     ```bash
     bash scripts/run_analysis.sh
     ```

   - Mention Jupyter notebooks (if applicable):  
     Open `notebooks/reproduce_results.ipynb` to execute the analysis step-by-step.

5. **Automation (Bonus)**  

   - Explain the included GitHub Action that produces or analyzes data automatically.  

### Encountered Issues and Improvements

- Report any challenges, errors, or deviations from the original study.
- Describe how these issues were resolved or improved, if applicable.

### Is the Original Study Reproducible?

- Summarize the success or failure of reproducing the study.
- Include supporting evidence, such as comparison tables, plots, or metrics.

## Replicability

### Variability Factors

- **List of Factors**: Identify all potential sources of variability (e.g., dataset splits, random seeds, hardware).  
  Example table:

  | Variability Factor | Possible Values     | Relevance                                   |
  |--------------------|---------------------|--------------------------------------------|
  | Random Seed        | [0, 42, 123]       | Impacts consistency of random processes    |
  | Hardware           | CPU, GPU (NVIDIA)  | May affect computation time and results    |
  | Dataset Version    | v1.0, v1.1         | Ensures comparability across experiments   |

- **Constraints Across Factors**:  
  - Document any constraints or interdependencies among variability factors.  
    For example:
    - Random Seed must align with dataset splits for consistent results.
    - Hardware constraints may limit the choice of GPU-based factors.

- **Exploring Variability Factors via CLI (Bonus)**  

  - Provide instructions to use the command-line interface (CLI) to explore variability factors and their combinations:  

     ```bash
     python explore_variability.py --random-seed 42 --hardware GPU --dataset-version v1.1
     ```

  - Describe the functionality and parameters of the CLI:
    - `--random-seed`: Specify the random seed to use.
    - `--hardware`: Choose between CPU or GPU.
    - `--dataset-version`: Select the dataset version.

### Replication Execution

1. **Instructions**  
   - Provide detailed steps or commands for running the replication(s):  

     ```bash
     bash scripts/replicate_experiment.sh
     ```

2. **Presentation and Analysis of Results**  
   - Include results in text, tables, or figures.
   - Analyze and compare with the original study's findings.

### Does It Confirm the Original Study?

- Summarize the extent to which the replication supports the original study’s conclusions.
- Highlight similarities and differences, if any.

## Conclusion

- Recap findings from the reproducibility and replicability sections.
- Discuss limitations of your
