import json, re
import numpy as np
from scipy.stats import spearmanr

json_path = "raw_openai_gpt41mini_monotonic.json"

YEARS = [2025,2028,2032,2036,2040]

answer_re = re.compile(r'\[Answer\]\s*([0-9]*\.?[0-9]+)')

def extract_answer(text):
    m = answer_re.search(text)
    return float(m.group(1)) if m else None

with open(json_path,"r",encoding="utf-8") as f:
    data = json.load(f)

viol=[]
for item in data:
    meds=[]
    for year_block in item["responses"]:
        nums=[extract_answer(x) for x in year_block]
        nums=[x for x in nums if x is not None]
        if len(nums)<2:
            break
        meds.append(np.median(nums))
    if len(meds)!=5: continue
    rho,_ = spearmanr(YEARS,meds)
    if np.isnan(rho): rho=1.0
    viol.append((1-rho)/2)

viol=np.array(viol)
print("Mean violation:",float(np.mean(viol)))
print("Percentage >0.2:",float(np.mean(viol>0.2))*100,"%")