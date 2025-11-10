import os, json, time, requests


API_KEY = os.environ["OPENROUTER_API_KEY"]

model = "openai/gpt-4.1-mini"

YEARS = [2025,2028,2032,2036,2040]
T = 3          # runs per question

# load 50 base templates
with open("base_questions_50.txt",encoding="utf-8") as f:
    base_questions = [l.strip() for l in f if l.strip()]

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type":"application/json"
}

def ask(q):
    payload = {
        "model": model,
        "messages":[
            {"role":"system","content":"Output final numeric estimate only in format [Answer] N"},
            {"role":"user","content":q}
        ],
        "temperature":0.0
    }
    r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                      headers=headers,json=payload)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

results = []

for idx, base in enumerate(base_questions):
    print(f"=== Q{idx} ===")
    item = {
        "id": idx,
        "questions": [],
        "responses": []
    }

    for y in YEARS:
        q = base.replace("{YEAR}",str(y))
        item["questions"].append(q)

        row = []
        for run in range(T):
            print("→", q, "(run",run,")")
            out = ask(q)
            row.append(out)
            time.sleep(1.2)   # polite delay

        item["responses"].append(row)

    results.append(item)

with open("raw_openai_gpt41mini_monotonic.json","w",encoding="utf-8") as f:
    json.dump(results,f,indent=2,ensure_ascii=False)

print("DONE saved: raw_openai_gpt41mini_monotonic.json")
