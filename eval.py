import instructor
import os
import pandas as pd
from tqdm import tqdm
from datasets import load_dataset
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
LIMIT = None

print("Loading BELEBELE dataset from HuggingFace")
ds = load_dataset("facebook/belebele", "lvs_Latn")
ds = ds["test"]

num_qs = 900
if LIMIT and LIMIT > 0:
    ds[:LIMIT]
    num_qs = LIMIT


# Define what you want
class Answer(BaseModel):
    answer: Literal["1", "2", "3", "4"]
    # reasoning: str


kwargs = {}
if "google/" in MODEL:
    kwargs = {
        "vertexai": True,
        "project": os.getenv("GCP_PROJECT_ID"),
        "location": os.getenv("GCP_LOCATION"),
    }

client = instructor.from_provider(MODEL, **kwargs)

df = pd.DataFrame(
    columns=["question_number", "model_answer", "correct_answer", "model_reasoning"],
)

print(f"Evaluating model: {MODEL.split('/')[-1]}")
for idx, line in tqdm(enumerate(iter(ds)), total=num_qs):
    prompt = "Atbildi uz jautājumu par teksta fragmentu, izvēloties pareizo atbilžu variantu:\n\n"
    prompt += line["flores_passage"] + "\n\n" + line["question"] + "\n\n"
    prompt += f"1) {line['mc_answer1']}.\n"
    prompt += f"2) {line['mc_answer2']}.\n"
    prompt += f"3) {line['mc_answer3']}.\n"
    prompt += f"4) {line['mc_answer4']}.\n"

    res = client.chat.completions.create(
        response_model=Answer,
        messages=[{"role": "user", "content": prompt}],
    )

    qnum = int(line["question_number"])
    corr = int(line["correct_answer_num"])

    df.loc[idx] = [qnum, int(res.answer), corr, None]

    if LIMIT and idx + 1 == LIMIT:
        break

dt = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")
fname = MODEL.split("/")[-1] + f"_{dt}.csv"
export_path = Path(os.getenv("RESULTS_DIR")) / fname
df.to_csv(export_path)


num_ask = (df["question_number"] > 0).sum()
num_ans = (df["model_answer"] > 0).sum()
num_corr = (df["model_answer"] == df["correct_answer"]).sum()

print("Total number of questions: 900")
print(f"Number of questions asked: {num_ask}")
print(f"Number of questions answered: {num_ans}")
print(f"Correct answers: {num_corr}")
print(f"Percentage correct: {(num_corr / num_ask * 100):.1f}%")
