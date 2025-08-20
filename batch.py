import common
import json
import io
import os
import pandas as pd
from tqdm import tqdm
from pydantic import BaseModel
from typing import Literal
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from openai.lib._parsing._completions import type_to_response_format_param


class Answer(BaseModel):
    answer: Literal["1", "2", "3", "4"]


def submit_openai_batch(model: str, limit: int = None):
    client = OpenAI()
    ds = common.load_belebele_lv()
    data = []

    num = limit if limit else 900
    res_fmt = type_to_response_format_param(Answer)

    for idx, line in tqdm(enumerate(iter(ds)), total=num):
        prompt = common.write_prompt(line)

        data.append(
            {
                "custom_id": f"req-{idx + 1}",
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": model,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt,
                        },
                    ],
                    "response_format": res_fmt,
                },
            }
        )

        if limit and idx + 1 == limit:
            break

    # Create an in-memory text file-like object
    file_object = io.BytesIO()

    # Write each dictionary as a JSON line
    for entry in data:
        json_line = json.dumps(entry)
        file_object.write((json_line + "\n").encode("utf-8"))

    batch_input_file = client.files.create(file=file_object, purpose="batch")

    metadata = client.batches.create(
        input_file_id=batch_input_file.id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={"description": f"{model} belebele eval"},
    )

    return metadata


def process_batch_output(fp: Path, include_reason: bool = False):
    ds = common.load_belebele_lv()

    cols = ["question_number", "model_answer", "correct_answer"]
    if include_reason:
        cols.append("model_reasoning")
    
    df = pd.DataFrame(columns=cols)

    data = []
    with open(str(fp)) as f:
        for line in f:
            data.append(json.loads(line))
    
    for idx, line in tqdm(enumerate(iter(ds)), total=len(data)):

        res = data[idx]
        choice = res['response']['body']['choices'][0]
        content = json.loads(choice['message']['content'])
        ans = int(content['answer'])

        qnum = int(line["question_number"])
        corr = int(line["correct_answer_num"])

        row = [qnum, ans, corr]
        if include_reason:
            row.append(content['reasoning'])
        
        df.loc[idx] = row

        if idx + 1 == len(data):
            break

    return df


if __name__ == "__main__":
    load_dotenv()

    limit = None
    model = os.getenv("MODEL_STRING").split("/")[-1]
    print(f"Model name: {model}")

    # -- Uncomment to submit a batch -- 
    # metadata = submit_openai_batch(model, limit)
    # print(metadata)

    # -- Uncomment to process batch results --
    # fp = Path('/path/to/openai_batch_file.jsonl')
    # df = process_batch_output(fp)
    # common.export_results(df, model)
    # common.print_stats(df)
