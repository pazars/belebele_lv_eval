import instructor
import os
import common
import pandas as pd
from tqdm import tqdm
from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timezone

# API keys and private variables (see .env.example)
load_dotenv()

# Instructor's model string
MODEL = os.getenv("MODEL_STRING")

# Limit number of questions (testing/debugging)
LIMIT = 2

# Return model's reasoning
REASONING = False

print("Loading BELEBELE dataset from HuggingFace")
ds, num_qs = common.load_belebele_lv(limit=LIMIT)

if REASONING:
    class Answer(BaseModel):
        answer: Literal["1", "2", "3", "4"]
        reasoning: str

    df = pd.DataFrame(
        columns=["question_number", "model_answer", "correct_answer", "model_reasoning"],
    )
else:
    class Answer(BaseModel):
        answer: Literal["1", "2", "3", "4"]

    df = pd.DataFrame(
        columns=["question_number", "model_answer", "correct_answer"],
    )

kwargs = {}
if "google/" in MODEL:
    kwargs = {
        "vertexai": True,
        "project": os.getenv("GCP_PROJECT_ID"),
        "location": os.getenv("GCP_LOCATION"),
    }

client = instructor.from_provider(MODEL, **kwargs)


print(f"Evaluating model: {MODEL.split('/')[-1]}")
for idx, line in tqdm(enumerate(iter(ds)), total=num_qs):
    prompt = common.write_prompt(line)

    res = client.chat.completions.create(
        response_model=Answer,
        messages=[{"role": "user", "content": prompt}],
    )

    qnum = int(line["question_number"])
    corr = int(line["correct_answer_num"])

    if REASONING:
        row = [qnum, int(res.answer), corr, res.reasoning]
    else:
        row = [qnum, int(res.answer), corr]

    df.loc[idx] = row

    if LIMIT and idx + 1 == LIMIT:
        break

# Export results file
dt = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")
fname = MODEL.split("/")[-1] + f"_{dt}.csv"
export_path = Path(os.getenv("RESULTS_DIR")) / fname
df.to_csv(export_path)

# Show stats
num_ask = (df["question_number"] > 0).sum()
num_ans = (df["model_answer"] > 0).sum()
num_corr = (df["model_answer"] == df["correct_answer"]).sum()

print("Total number of questions: 900")
print(f"Number of questions asked: {num_ask}")
print(f"Number of questions answered: {num_ans}")
print(f"Correct answers: {num_corr}")
print(f"Percentage correct: {(num_corr / num_ask * 100):.1f}%")
