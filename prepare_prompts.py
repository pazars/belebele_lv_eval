import os
import jsonlines

PATH_TO_BELEBELE = "C:/Users/dpazars/Documents/Belebele"
LANGUAGE_FLORES_200_CODE = "lvs_Latn"
LLAMA_2_7B_PATH = "C:/Users/dpazars/Documents/llms/models"

file_path = os.path.join(PATH_TO_BELEBELE, LANGUAGE_FLORES_200_CODE + ".jsonl")


dataset = []
correct_answers = []
with jsonlines.open(file_path) as reader:
    for obj in reader:
        dataset.append(obj)

with open("prompts.txt", "w", encoding="utf-8") as prompt_file:
    for num, row in enumerate(dataset):
        prompt = f"""{row["flores_passage"]}
        
{row["question"]}

Atbilžu varianti:

1: {row["mc_answer1"]}
2: {row["mc_answer2"]}
3: {row["mc_answer3"]}
4: {row["mc_answer4"]}

Sniedz atbildi pēc formāta "Pareizā atbilde: <tava atbilde>".
"""

        prompt_file.write(f"Jautājums #{num + 1}\n\n")
        prompt_file.write(prompt)
        prompt_file.write("\n")

        correct_answers.append(row["correct_answer_num"])

with open("correct_answers.txt", "w", encoding="utf-8") as answer_file:
    for answer in correct_answers:
        answer_file.write(answer + "\n")
