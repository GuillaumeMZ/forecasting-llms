import json, re
import numpy as np
from scipy.stats import spearmanr

json_path = "raw_outputs/monotonic_sequence_gpt-4-0314_method_1shot_climbers_T_0.0_times_3_mt_400.json"

YEARS = [2025, 2028, 2032, 2036, 2040]

answer_re = re.compile(r'\[Answer\]\s*([0-9]*\.?[0-9]+)')

def extract_answer(text):
    m = answer_re.findall(text)
    return float(m[-1]) if m else None

with open(json_path,"r",encoding="utf-8") as f:
    data = json.load(f)

violations = []
N_kept = 0
N_dropped = 0

for item in data:
    medians = []
    valid_item = True

    for year_responses in item["responses"]:
        vals=[]
        for run in year_responses:
            try:
                content = run["choices"][0]["message"]["content"]
            except:
                continue
            num = extract_answer(content)
            if num is not None:
                vals.append(num)

        if len(vals) < 2:
            valid_item = False
            break
        medians.append(np.median(vals))

    if not valid_item:
        N_dropped += 1
        continue

    N_kept += 1

    rho,_ = spearmanr(YEARS, medians)

    if np.isnan(rho):
        rho = 1.0

    viol = (1-rho)/2
    violations.append(viol)

violations = np.array(violations)

print("Total items:", len(data))
print("Kept:", N_kept, " Dropped:", N_dropped)
print("mean violation:", float(np.mean(violations)))
print(">0.2 proportion:", float(np.mean(violations > 0.2)))
print(len(data))
