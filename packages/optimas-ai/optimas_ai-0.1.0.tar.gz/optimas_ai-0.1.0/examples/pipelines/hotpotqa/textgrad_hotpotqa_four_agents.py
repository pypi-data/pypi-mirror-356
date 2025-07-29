"""Train all TextGrad prompts for HotpotQA and merge them."""
import os, json, time, random, os.path as osp
import torch
from tqdm import tqdm
from dotenv import load_dotenv
import textgrad as tg
from textgrad import TGD
from examples.datasets.hotpot_qa import dataset_engine
from examples.pipelines.hotpotqa.modules import (
    TextGradQuestionRewriter, TextGradInfoExtractor,
    WikipediaRetriever, TextGradHintGenerator,
    TextGradAnswerGenerator
)

SCRIPT_DIR = osp.dirname(osp.realpath(__file__))
CKPT_DIR   = osp.join(SCRIPT_DIR, "checkpoints")
os.makedirs(CKPT_DIR, exist_ok=True)

load_dotenv()
tg.set_backward_engine("gpt-4o-mini", override=True)  # No prefix for OpenAI models

from textgrad.loss import TextLoss
from textgrad import Variable


def make_loss_fn(role_desc):
    def _f(var: Variable, question: str, gd: str):
        prompt = (
            f"Evaluate the quality of the {role_desc} relative to the ground truth.\n"
            f"Question: {question}\nGround Truth Answer: {gd}\n"
            "Provide concise feedback to improve it."
        )
        eval_var = Variable(
            prompt,
            requires_grad=False,
            role_description=f"{role_desc} evaluation"
        )
        return TextLoss(eval_var)(var)
    return _f

rewriter_loss_fn = make_loss_fn("rewritten question")
extractor_loss_fn = make_loss_fn("search keywords")
hint_loss_fn = make_loss_fn("hints")
answer_loss_fn = make_loss_fn("answer")

# generic optimizer loop
def optimize(module, trainset, forward_fn, loss_fn, optimizer, n_epochs=1, batch=4, context_modules=None):
    # Tune trainset size for faster/thorough optimization
    # trainset = trainset[:20]
    
    for ep in range(n_epochs):
        random.shuffle(trainset)
        # k for Wikipedia right now will be random for training too
        # k = random.choice([1, 5, 10, 25])
        
        for idx in tqdm(range(0, len(trainset), batch), desc=f"{module.__class__.__name__} e{ep+1}"):
            batch_ex = trainset[idx:idx+batch]
            optimizer.zero_grad()
            loss_total = None
            for ex in batch_ex:
                # k for Wikipedia will be random for training
                k = random.choice([1, 5, 10, 25])
                if forward_fn.__name__ == "rewrite":
                    out = forward_fn(ex.question)
                    loss = loss_fn(out, ex.question, ex.gd_answer)
                elif forward_fn.__name__ == "extract":
                    rq = context_modules["rewriter"].rewrite(ex.question).value
                    out = forward_fn(rq)
                    loss = loss_fn(out, ex.question, ex.gd_answer)
                elif forward_fn.__name__ == "generate_hints":
                    rq = context_modules["rewriter"].rewrite(ex.question).value
                    kws = context_modules["extractor"].extract(rq).value
                    retriever = WikipediaRetriever(k=k, search_space=[1, 5, 10, 25])  # can tune k
                    content = retriever.forward(search_keywords=kws)["retrieve_content"]
                    out = forward_fn(rq, content)
                    loss = loss_fn(out, ex.question, ex.gd_answer)
                else:  # generate_answer
                    rq = context_modules["rewriter"].rewrite(ex.question).value
                    kws = context_modules["extractor"].extract(rq).value
                    retriever = WikipediaRetriever(k=k, search_space=[1, 5, 10, 25])  # can tune k
                    content = retriever.forward(search_keywords=kws)["retrieve_content"]
                    hints = context_modules["hint"].generate_hints(rq, content).value
                    out = forward_fn(rq, hints)
                    loss = loss_fn(out, ex.question, ex.gd_answer)
                loss_total = loss if loss_total is None else (loss_total + loss)
            loss_total.backward()
            optimizer.step()
        # save prompt each epoch
        ckpt = osp.join(CKPT_DIR, f"checkpoint_{module.__class__.__name__}_epoch{ep+1}.json")
        with open(ckpt, "w") as f: json.dump({"prompt": module.prompt.value}, f)


if __name__ == "__main__":
    train, _ = dataset_engine()

    # instantiate modules
    rew = TextGradQuestionRewriter()
    ext = TextGradInfoExtractor()
    hint = TextGradHintGenerator()
    ans = TextGradAnswerGenerator()

    ctx = {"rewriter": rew, "extractor": ext, "hint": hint}

    # optimizers
    opt_rew = TGD([rew.prompt])
    opt_ext = TGD([ext.prompt])
    opt_hint = TGD([hint.prompt])
    opt_ans = TGD([ans.prompt])

    optimize(rew, train, rew.rewrite, rewriter_loss_fn, opt_rew)
    optimize(ext, train, ext.extract, extractor_loss_fn, opt_ext, context_modules=ctx)
    optimize(hint, train, hint.generate_hints, hint_loss_fn, opt_hint, context_modules=ctx)
    optimize(ans, train, ans.generate_answer, answer_loss_fn, opt_ans, context_modules=ctx)

    # merge prompts
    merged = {
        "rewriter_prompt": rew.prompt.value,
        "extractor_prompt": ext.prompt.value,
        "retriever_k": random.choice([1, 5, 10, 25]),  # Random default k value
        "retriever_randomize": True,  # flag to enable randomization
        "hint_prompt": hint.prompt.value,
        "answer_prompt": ans.prompt.value
    }
    torch.save(merged, osp.join(CKPT_DIR, "combined_textgrad_prompts.pth"))
    print("[train_hotpotqa_textgrad] training complete – prompts merged.")

