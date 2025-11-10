# Reproduce and Replicate of "Evaluating Superhuman Models with Consistency Checks - LLMs forecasting future events"

## Introduction

This study (“Evaluating Superhuman Models with Consistency Checks”, 2023) proposed a set of logical self-consistency tests for LLM forecasts: Negation, Paraphrasing, Monotonicity, Bayes’ rule.

I focus on **reproducing the Monotonicity experiment** (50 forecasting questions × 5 years).
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

The original repository provides only the raw JSON dataset, but no code and no procedural description of how the violation metrics were computed.
The paper includes only the mathematical definitions (Spearman–based formula), but not the actual parsing logic or implementation details.
Therefore, in order to reproduce the results, we had to write our own Python scripts to:
(1) extract the numerical forecast answers from the JSON logs and
(2) compute the violation scores exactly following the equations in the paper.

Initially, we attempted to compute the violation metrics directly on the JSON files inside the raw_outputs directory, but our scores did not match the values reported in the paper. We discovered that this was because the dataset contains multiple variants of each run (sorted / only_violations / raw / with_violations), and the paper’s table corresponds specifically to the a version, with a particular filtering logic.(pas sûr.......)
   
- Report any challenges, errors, or deviations from the original study.
- Describe how these issues were resolved or improved, if applicable.

### Is the Original Study Reproducible?

- Summarize the success or failure of reproducing the study.
- Include supporting evidence, such as comparison tables, plots, or metrics.

## Replicability

### Variability Factors

- **List of Factors**: Identify all potential sources of variability (e.g., dataset splits, random seeds, hardware).  
  Example table:

| Factor         | Values                        | relevance                |
| -------------- | ----------------------------- | ------------------------ |
| model          | gpt-4-0314 vs YOUR-MODEL-NAME | main causal factor       |
| temperature    | 0.0, 0.5                      | affects variance         |
| #runs per year | 3,6                           | affects median stability |
| JSON structure | dict vs string                | affects parser           |
......

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

We re-asked the same 50×5 questions using:

model: "openai/gpt-4.1-mini"

temp = 0.0

runs per year = 3

API = OpenRouter

1. **Instructions**  
   - Provide detailed steps or commands for running the replication(s):  

     ```bash
     bash scripts/replicate_experiment.shp
     ```

2. **Presentation and Analysis of Results**
   | Model                          | Mean violation | % strong violation (>0.2) |
   | ------------------------------ | -------------: | ------------------------: |
   | GPT-3.5-turbo-0301(3 times)    |      **0.229** |                **42.0 %** |
   | GPT-3.5-turbo-0301(6 times)    |      **0.136** |                **26.0 %** |
   | GPT-4-0314(3 times)            |      **0.105** |                **16.0 %** |
   | GPT-4-0314(6 times)            |      **0.089** |                **12.0 %** |
   | **openai/gpt-4.1-mini (ours)** |      **0.326** |                 **47.8%** |

Replication confirms the core claim of the paper: weaker models violate logical monotonicity more often.

   - Include results in text, tables, or figures.
   - Analyze and compare with the original study's findings.

### Does It Confirm the Original Study?

Qualitatively — YES.

Replication shows that a weaker model is far more logically inconsistent, exactly as hypothesis predicts: monotonic constraints are broken more frequently by less capable LLMs.

- Summarize the extent to which the replication supports the original study’s conclusions.
- Highlight similarities and differences, if any.

## Conclusion

- Recap findings from the reproducibility and replicability sections.
- Discuss limitations of your
