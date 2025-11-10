import json

json_path = "sorted_violations/monotonic_sequence_gpt-4-0314_method_1shot_climbers_T_0.0_times_3_mt_400.json"

with open(json_path,encoding="utf-8") as f:
    data = json.load(f)

YEARS = [2025,2028,2032,2036,2040]

questions_50 = []

for item in data:
    # take the 2025 version (index=0)
    q0 = item["questions"][0]   # e.g., "... by the year 2025?"

    # make generic: replace "2025" with {YEAR}
    base = q0.replace("2025","{YEAR}")  
    questions_50.append(base)

# save file
with open("base_questions_50.txt","w",encoding="utf-8") as f:
    for q in questions_50:
        f.write(q+"\n")