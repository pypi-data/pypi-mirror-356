import joblib
import dspy
from dspy.datasets.hotpotqa import HotPotQA
from optimas.utils.example import Example

def dataset_engine(**kwargs):

    dataset = HotPotQA(train_seed=1,
                       train_size=kwargs.get('train_size', 5000),
                       dev_size=250, test_size=0)
    trainset = [Example(question=x.question, gd_answer=x.answer).with_inputs('question') for x in dataset.train]
    valset = [Example(question=x.question, gd_answer=x.answer).with_inputs('question') for x in dataset.dev]

    hotpot_test = joblib.load('examples/data/hotpot-qa-distractor-sample.joblib').reset_index(drop = True)
    testset = [
        Example(question=hotpot_test.iloc[i]['question'], gd_answer=hotpot_test.iloc[i]['answer']).with_inputs("question")
        for i in range(len(hotpot_test))
    ]
    return trainset, valset, testset
