import os
import common
import litellm
import instructor
import pandas as pd

from tqdm import tqdm
from dotenv import load_dotenv
from litellm import completion
from instructor.exceptions import InstructorRetryException
from tenacity import (
    retry_if_exception_type,
    wait_exponential,
    stop_after_attempt,
    retry,
)


# litellm._turn_on_debug()
litellm.drop_params = True

# API keys and other variables (see .env.example)
load_dotenv()

model_name = os.getenv("MODEL_STRING")
reasoning = bool(int(os.getenv("REASONING", 0)))
limit = int(os.getenv("LIMIT", 900))

client = instructor.from_litellm(completion)

print("Loading BELEBELE dataset from HuggingFace")
ds = common.load_belebele_lv()

cols = ["question_number", "model_answer", "correct_answer"]
cols.append("model_reasoning") if reasoning else None
df = pd.DataFrame(columns=cols)


@retry(
    retry=retry_if_exception_type(InstructorRetryException),
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=2, min=5, max=120),
    before_sleep=lambda retry_state: print(
        f"Retry exception. Maybe structure or rate limit (attempt {retry_state.attempt_number})"
    ),
)
def rate_limit_safe_extraction(prompt: str):
    """Handle rate limits with longer delays."""
    return client.chat.completions.create(
        model=model_name,
        response_model=common.AnswerReasoning if reasoning else common.Answer,
        messages=[{"role": "user", "content": prompt}],
    )


print(f"Evaluating model: {model_name.split('/')[-1]}")
for idx, line in tqdm(enumerate(iter(ds)), total=limit):
    prompt = common.write_prompt(line)
    res = rate_limit_safe_extraction(prompt)

    qnum = int(line["question_number"])
    corr = int(line["correct_answer_num"])

    row = [qnum, int(res.answer), corr]
    row.append(res.reasoning) if reasoning else None

    df.loc[idx] = row

    if idx + 1 >= limit:
        break

# Export results to results dir
common.export_results(df, model_name)

# Show statistics
common.print_stats(df)
