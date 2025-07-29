import json
import csv
import ast
from pathlib import Path
import dspy
from typing import List, Dict, Any
from optimas.utils.example import Example



def dataset_engine(**kwargs) -> (List[Example], List[Example]):
    """
    Load two session-based recommendation CSVs and split each 80/20,
    then combine into a single train and a single test set.
    """
    data_root = Path("/dfs/project/kgrlm/multiagent_reward/data/multiple_choice")

    # Primary and multilingual files
    primary_fp = data_root / "session_based_next_item_selection_dataset.csv"
    multi_fp   = data_root / "multilingual_session_based_recommendation_dataset.csv"

    def load_rows(fp: Path) -> List[Dict[str, str]]:
        with fp.open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    primary_rows = load_rows(primary_fp)
    multi_rows   = load_rows(multi_fp)

    def split_rows(rows: List[Dict[str, str]], frac: float = 0.8):
        cutoff = int(len(rows) * frac)
        return rows[:cutoff], rows[cutoff:]

    # 80/20 splits for each source
    train_primary, test_primary = split_rows(primary_rows)
    train_multi,   test_multi   = split_rows(multi_rows)

    # Combine
    train_rows = train_primary + train_multi
    test_rows  = test_primary  + test_multi

    print(f"  Primary: {len(primary_rows)} total → {len(train_primary)} train + {len(test_primary)} test")
    print(f"  Multi:   {len(multi_rows)} total → {len(train_multi)} train + {len(test_multi)} test")
    print(f" Combined: {len(train_rows)} train + {len(test_rows)} test")

    def make_example(item: Dict[str, str]) -> Example:
        # extract sequence only (drop the fixed preamble)
        sequence = item["question"].split("Product Sequence:")[-1].strip()
        # parse choices
        try:
            choices = ast.literal_eval(item["choices"])
        except Exception:
            choices = json.loads(item["choices"])
        # build Example
        answer_idx = int(item["answer"])
        return (
            Example(
                sequence=sequence,
                choices=choices,
                gd_answer=str(answer_idx)
            )
            .with_inputs("sequence", "choices")
        )

    train_val_examples = [make_example(r) for r in train_rows]
    test_examples  = [make_example(r) for r in test_rows]

    if len(train_val_examples) < 20:
        train_examples = train_val_examples[:-1]
        val_examples = train_val_examples[-1]
    else:
        train_examples = train_val_examples[:int(len(train_val_examples) * 0.85)]
        val_examples = train_val_examples[int(len(train_val_examples) * 0.85):]

    return train_examples, val_examples, test_examples


if __name__ == "__main__":
    train, val, test = dataset_engine()
    print(f"\nLoaded {len(train)} training and {len(test)} testing examples")
    train_val = train + val
    for i, ex in enumerate(train_val):
        if 'Nicky Elite Carta Igienica' in ex.sequence:
            print(f"\nExample {i}:")
            print(f"  Sequence: {ex.sequence}")
            print(f"  Choices: {ex.choices}")
            print(f"  Answer: {ex.gd_answer}")
            break
