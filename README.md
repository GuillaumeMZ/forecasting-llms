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

The project uses the Dockerfile to create a reproducible environment ( Please replace “yourkey” with your API key ) :
     ```bash
     docker build -t forecasting-repro .
     docker run -it -e OPENROUTER_API_KEY="yourkey" -v [yourPath\forecast_results:\app\results] --entrypoint bash forecasting-repro
     ```

4. **Reproducing Results**  

For convenience, the project includes a shell script that runs the entire reproduction pipeline — parsing model outputs, computing monotonicity violations, and generating summary statistics:

     ```bash
     bash reproduce.sh
     exit # to exit
     ```
This script executes:

- replicate.py – queries the model and saves raw outputs

- replicate_analyse.py – extracts numeric answers and computes monotonicity metrics


   - Mention Jupyter notebooks (if applicable):  
     Open `notebooks/reproduce_results.ipynb` to execute the analysis step-by-step.

5. **Automation (Bonus)**  

The project includes a GitHub Action workflow that automates the process of generating and analyzing forecasting data. This workflow allows the scripts in the repository—namely replicate.py and replicate_analyse.py—to run automatically without manual intervention, ensuring reproducibility and timely updates.

- Running the Forecast Script ( As it cost a big amount of time to run, we put it in comment )
The workflow executes replicate.py, which generates raw forecasting outputs. These outputs are stored in the results/ directory within the workflow environment.

- Running the Analysis Script
Once the raw outputs are produced, the workflow runs replicate_analyse.py to process the data. This generates summarized analysis reports in the same results/ directory.

- Security Considerations
Sensitive information, such as the OPENROUTER_API_KEY, is stored securely in GitHub Secrets and passed to the workflow at runtime. This ensures the key is never exposed in the repository or logs.

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
     bash replicate.sh
     ```

2. **Presentation and Analysis of Results**
   | Model                          | Mean violation | % strong violation (>0.2) |
   | ------------------------------ | -------------: | ------------------------: |
   | GPT-3.5-turbo-0301(3 times)    |      **0.229** |                **42.0 %** |
   | GPT-3.5-turbo-0301(6 times)    |      **0.136** |                **26.0 %** |
   | GPT-4-0314(3 times)            |      **0.105** |                **16.0 %** |
   | GPT-4-0314(6 times)            |      **0.089** |                **12.0 %** |
   | **openai/gpt-4.1-mini (ours)** |      **0.326** |                 **47.8%** |

1. Mean Violation

Definition: Mean violation measures the average degree to which a model’s predictions violate a given constraint. Lower values indicate better adherence.

Observations:

The GPT-4 series has significantly lower mean violations than GPT-3.5, indicating more consistent adherence to constraints.

Increasing the number of repetitions (from 3 to 6) reduces mean violation for both GPT-3.5 and GPT-4. For example:

GPT-3.5-turbo-0301 drops from 0.229 → 0.136

GPT-4-0314 drops from 0.105 → 0.089

Our gpt-4.1-mini has the highest mean violation (0.326), suggesting it is more prone to constraint violations.

2. Strong Violation Percentage (% >0.2)

Definition: The percentage of predictions exceeding a violation threshold of 0.2. Lower values are better.

Observations:

GPT-4 models have the lowest strong violation rates (12–16%), while GPT-3.5 is higher (26–42%).

Running multiple repetitions reduces strong violation rates for all models.

gpt-4.1-mini has the highest strong violation rate (47.8%), consistent with its high mean violation.

3. Trends

Model improvements: GPT-4 outperforms GPT-3.5 in both mean and strong violations.

Effect of repetition: More sampling repetitions improve stability and reduce violations.

Characteristics of gpt-4.1-mini: This model is more likely to produce larger violations, which may be due to differences in training, fine-tuning, or inference strategy.

4. Potential Improvements

For gpt-4.1-mini, possible improvements include:

Increasing the number of predictions and averaging or using majority voting.

Adding constraint-focused prompt instructions.

Fine-tuning or calibrating the model to reduce high-violation outputs.

! Caution on Model Comparison

While we present the results of our gpt-4.1-mini model alongside GPT-3.5 and GPT-4 baselines, it is important to note that our results may not be fully comparable to those reported in the original papers.

- We were unable to exactly reproduce the numerical values reported in the original studies.

- This discrepancy suggests that the original papers may have used their own calculation methods or evaluation procedures, which were not fully disclosed.

- For example, metrics like the Spearman rank correlation coefficient could have been computed differently at that time.

As a result, any direct comparison with the published numbers should be interpreted with caution, and the absolute values reported here may not reflect the original benchmarks accurately.

### Does It Confirm the Original Study?

Qualitatively — YES.

Replication shows that a weaker model is far more logically inconsistent, exactly as hypothesis predicts: monotonic constraints are broken more frequently by less capable LLMs.

- Summarize the extent to which the replication supports the original study’s conclusions.
- Highlight similarities and differences, if any.

## Conclusion

- Recap findings from the reproducibility and replicability sections.
- Discuss limitations of your
- 

## Appendix: Generate 50 questions (base_questions_50.txt)

In the official monotonicity raw JSON, each item contains 5 versions of the same question (2025 / 2028 / 2032 / 2036 / 2040).
The first question in the list (questions[0]) is always the 2025 formulation.
We therefore extract that base form and replace 2025 with the placeholder {YEAR}.
   ```bash
   import json
   
   src = "raw_outputs/monotonic_sequence_gpt-4-0314_method_1shot_climbers_T_0.0_times_3_mt_400.json"
   YE="2025"
   
   out=[]
   for item in json.load(open(src,encoding="utf-8")):
       base=item["questions"][0]
       base=base.replace(YE,"{YEAR}")
       out.append(base)
   
   with open("base_questions_50.txt","w",encoding="utf-8") as f:
       for q in out:
           f.write(q+"\n")
   ```
The resulting text file contains exactly 50 lines — one template per monotonicity item.
