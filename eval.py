import os
import common
import instructor
import pandas as pd

from tqdm import tqdm
from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv
from litellm import completion


# API keys and private variables (see .env.example)
load_dotenv()

# Limit number of questions (testing/debugging)
LIMIT = 1

# Return model's reasoning
REASONING = False

client = instructor.from_litellm(completion)

# Instructor's model string
model_name = os.getenv("MODEL_STRING")

print("Loading BELEBELE dataset from HuggingFace")
ds = common.load_belebele_lv()

cols = ["question_number", "model_answer", "correct_answer"]
if REASONING:
    class Answer(BaseModel):
        answer: Literal["1", "2", "3", "4"]
        reasoning: str
    cols.append("model_reasoning")
else:
    class Answer(BaseModel):
        answer: Literal["1", "2", "3", "4"]

df = pd.DataFrame(columns=cols)

print(f"Evaluating model: {model_name.split('/')[-1]}")
for idx, line in tqdm(enumerate(iter(ds)), total=LIMIT):
    prompt = common.write_prompt(line)

    res = client.chat.completions.create(
        model=model_name,
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

# Export results to results dir
common.export_results(df, model_name)

# Show statistics
common.print_stats(df)
