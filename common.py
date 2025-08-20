import os
import pandas as pd

from pathlib import Path
from typing import Literal
from pydantic import BaseModel
from datetime import datetime, timezone
from datasets import load_dataset


class AnswerReasoning(BaseModel):
    answer: Literal["1", "2", "3", "4"]
    reasoning: str


class Answer(BaseModel):
    answer: Literal["1", "2", "3", "4"]


def load_belebele_lv(lang: str = "lvs_Latn"):
    ds = load_dataset("facebook/belebele", lang)
    return ds["test"]


def write_prompt(row):
    prompt = "Atbildi uz jautājumu par teksta fragmentu, izvēloties pareizo atbilžu variantu:\n\n"
    prompt += row["flores_passage"] + "\n\n" + row["question"] + "\n\n"
    prompt += f"1) {row['mc_answer1']}.\n"
    prompt += f"2) {row['mc_answer2']}.\n"
    prompt += f"3) {row['mc_answer3']}.\n"
    prompt += f"4) {row['mc_answer4']}.\n"
    return prompt


def export_results(df: pd.DataFrame, model: str):
    # Export results file
    dt = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")
    fname = model.split("/")[-1] + f"_{dt}.csv"
    export_path = Path(os.getenv("RESULTS_DIR")) / fname
    df.to_csv(export_path)


def print_stats(df: pd.DataFrame):
    num_ask = (df["question_number"] > 0).sum()
    num_ans = (df["model_answer"] > 0).sum()
    num_corr = (df["model_answer"] == df["correct_answer"]).sum()

    print("Total number of questions: 900")
    print(f"Number of questions asked: {num_ask}")
    print(f"Number of questions answered: {num_ans}")
    print(f"Correct answers: {num_corr}")
    print(f"Percentage correct: {(num_corr / num_ask * 100):.1f}%")


if __name__ == "__main__":
    a, b = load_belebele_lv(limit=10)
