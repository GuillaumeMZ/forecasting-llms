import json, re
import numpy as np
from scipy.stats import spearmanr

json_path = "raw_openai_gpt41mini_monotonic.json"
json_path2 ="raw_deepseek_monotonic.json"
YEARS = [2025,2028,2032,2036,2040]

answer_re = re.compile(r'\[Answer\]\s*([0-9]*\.?[0-9]+)')

def extract_answer(text):
    m = answer_re.search(text)
    return float(m.group(1)) if m else None

with open(json_path,"r",encoding="utf-8") as f:
    data = json.load(f)

with open(json_path2,"r",encoding="utf-8") as f:
    data2 = json.load(f)

def analyze(data, dataset_name):
    violations = []
    for item in data:
        medians = []
        for year_block in item["responses"]:
            nums = [extract_answer(x) for x in year_block]
            nums = [x for x in nums if x is not None]
            if len(nums) < 2:
                break
            medians.append(np.median(nums))
        if len(medians) != 5: 
            continue
        rho, _ = spearmanr(YEARS, medians)
        if np.isnan(rho): 
            rho = 1.0
        violations.append((1 - rho) / 2)

    violations = np.array(violations)
    
    print(f"\n=== {dataset_name} Analysis Results ===")
    print("Mean violation score:", float(np.mean(violations)))
    print("Percentage with violation > 0.2:", float(np.mean(violations > 0.2)) * 100, "%")
    print("Total questions analyzed:", len(violations))
    
    return violations

viol_gpt = analyze(data, "GPT-4.1-mini")
viol_deepseek = analyze(data2, "DeepSeek")