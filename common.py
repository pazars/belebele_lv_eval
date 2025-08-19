from datasets import load_dataset


def load_belebele_lv(lang: str = "lvs_Latn", limit: int = None):
    ds = load_dataset("facebook/belebele", lang)
    ds = ds["test"]

    num_qs = 900
    if limit and limit > 0:
        ds[:limit]
        num_qs = limit

    return (ds, num_qs)


def write_prompt(row):
    prompt = "Atbildi uz jautājumu par teksta fragmentu, izvēloties pareizo atbilžu variantu:\n\n"
    prompt += row["flores_passage"] + "\n\n" + row["question"] + "\n\n"
    prompt += f"1) {row['mc_answer1']}.\n"
    prompt += f"2) {row['mc_answer2']}.\n"
    prompt += f"3) {row['mc_answer3']}.\n"
    prompt += f"4) {row['mc_answer4']}.\n"
    return prompt
