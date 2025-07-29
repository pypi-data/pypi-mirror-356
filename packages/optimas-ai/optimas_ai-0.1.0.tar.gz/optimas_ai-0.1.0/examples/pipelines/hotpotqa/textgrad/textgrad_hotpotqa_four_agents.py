"""Train all TextGrad prompts for HotpotQA and merge them."""
import os, json, time, random, os.path as osp
import torch
from tqdm import tqdm
from dotenv import load_dotenv
import textgrad as tg
from textgrad import TGD
from examples.datasets.hotpot_qa import dataset_engine
from examples.pipelines.hotpotqa.textgrad.textgrad_modules import (
    TextGradQuestionRewriter, TextGradInfoExtractor,
    WikipediaRetriever, TextGradHintGenerator,
    TextGradAnswerGenerator
)

# Create timestamped directory for this run
timestamp = time.strftime("%Y%m%d_%H%M%S")
SCRIPT_DIR = osp.dirname(osp.realpath(__file__))
CKPT_DIR = osp.join(SCRIPT_DIR, "checkpoints", f"run_{timestamp}")
os.makedirs(CKPT_DIR, exist_ok=True)

# Create a directory for metrics
METRICS_DIR = osp.join(CKPT_DIR, "metrics")
os.makedirs(METRICS_DIR, exist_ok=True)

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

def optimize(module, trainset, forward_fn, loss_fn, optimizer, n_epochs=5, batch_size=4, context_modules=None):
    # Tune trainset size for faster/thorough optimization
    valset = trainset[:20]
    trainset = trainset[20:]
    
    best_eval_loss = float('inf')
    best_prompt = module.prompt.value
    eval_frequency = 2  # just eval every other batch
    
    # Initialize metrics tracking
    metrics = {
        "train_losses": [],
        "val_losses": [],
        "best_val_loss": float('inf'),
        "epochs": []
    }
    
    for ep in range(n_epochs):
        random.shuffle(trainset)
        # k for Wikipedia right now will be random for training too
        # k = random.choice([1, 5, 10, 25])
        total_train_loss = 0
        num_batches = 0
        epoch_metrics = {
            "train_losses": [],
            "val_losses": []
        }
        
        for idx in tqdm(range(0, len(trainset), batch_size), desc=f"{module.__class__.__name__} e{ep+1}"):
            batch_ex = trainset[idx:idx+batch_size]
            optimizer.zero_grad()
            losses = []
            
            # Training step
            for ex in batch_ex:
                # k for Wikipedia could be random for training
                # k = random.choice([1, 5, 10, 25])
                k = 1
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
                losses.append(loss)
            
            # Sum losses and do backward pass
            if losses:
                total_loss = tg.sum(losses)
                total_loss.backward()
                optimizer.step()
                
                # Update training loss tracking
                total_train_loss += len(losses)
                num_batches += 1
                epoch_metrics["train_losses"].append(total_train_loss/num_batches)
            
            # Validation step
            if num_batches % eval_frequency == 0:
                val_loss = 0
                for val_ex in valset:
                    # k = random.choice([1, 5, 10, 25])
                    k = 1
                    if forward_fn.__name__ == "rewrite":
                        out = forward_fn(val_ex.question)
                        loss = loss_fn(out, val_ex.question, val_ex.gd_answer)
                    elif forward_fn.__name__ == "extract":
                        rq = context_modules["rewriter"].rewrite(val_ex.question).value
                        out = forward_fn(rq)
                        loss = loss_fn(out, val_ex.question, val_ex.gd_answer)
                    elif forward_fn.__name__ == "generate_hints":
                        rq = context_modules["rewriter"].rewrite(val_ex.question).value
                        kws = context_modules["extractor"].extract(rq).value
                        retriever = WikipediaRetriever(k=k, search_space=[1, 5, 10, 25])
                        content = retriever.forward(search_keywords=kws)["retrieve_content"]
                        out = forward_fn(rq, content)
                        loss = loss_fn(out, val_ex.question, val_ex.gd_answer)
                    else:  # generate_answer
                        rq = context_modules["rewriter"].rewrite(val_ex.question).value
                        kws = context_modules["extractor"].extract(rq).value
                        retriever = WikipediaRetriever(k=k, search_space=[1, 5, 10, 25])
                        content = retriever.forward(search_keywords=kws)["retrieve_content"]
                        hints = context_modules["hint"].generate_hints(rq, content).value
                        out = forward_fn(rq, hints)
                        loss = loss_fn(out, val_ex.question, val_ex.gd_answer)
                    val_loss += 1
                
                avg_val_loss = val_loss / len(valset)
                epoch_metrics["val_losses"].append(avg_val_loss)
                
                print(f"\nEpoch {ep+1}, Batch {num_batches}:")
                print(f"Average training loss: {total_train_loss/num_batches:.4f}")
                print(f"Average validation loss: {avg_val_loss:.4f}")
                
                # Update best prompt IF validation loss improved
                if avg_val_loss < best_eval_loss:
                    best_eval_loss = avg_val_loss
                    best_prompt = module.prompt.value
                    print(f"New best validation loss: {best_eval_loss:.4f}")
                    # Save best prompt checkpoint
                    best_ckpt = osp.join(CKPT_DIR, f"best_{module.__class__.__name__}.json")
                    with open(best_ckpt, "w") as f:
                        json.dump({"prompt": best_prompt, "val_loss": best_eval_loss}, f)
        
        # Save epoch metrics
        metrics["epochs"].append(epoch_metrics)
        metrics["train_losses"].extend(epoch_metrics["train_losses"])
        metrics["val_losses"].extend(epoch_metrics["val_losses"])
        metrics["best_val_loss"] = min(metrics["best_val_loss"], best_eval_loss)
        
        # Save epoch checkpoint
        ckpt = osp.join(CKPT_DIR, f"checkpoint_{module.__class__.__name__}_epoch{ep+1}.json")
        with open(ckpt, "w") as f:
            json.dump({
                "prompt": module.prompt.value,
                "train_loss": total_train_loss/num_batches if num_batches > 0 else 0,
                "val_loss": best_eval_loss
            }, f)
    
    # Save all metrics for this module
    metrics_file = osp.join(METRICS_DIR, f"{module.__class__.__name__}_metrics.json")
    with open(metrics_file, "w") as f:
        json.dump(metrics, f, indent=2)
    
    # Restore best prompt at the end
    module.prompt.value = best_prompt
    return module


if __name__ == "__main__":
    train, _, _ = dataset_engine()

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

    # Train with 5 epochs, batch size of 4
    optimize(rew, train, rew.rewrite, rewriter_loss_fn, opt_rew, n_epochs=5, batch_size=4)
    optimize(ext, train, ext.extract, extractor_loss_fn, opt_ext, context_modules=ctx, n_epochs=5, batch_size=4)
    optimize(hint, train, hint.generate_hints, hint_loss_fn, opt_hint, context_modules=ctx, n_epochs=5, batch_size=4)
    optimize(ans, train, ans.generate_answer, answer_loss_fn, opt_ans, context_modules=ctx, n_epochs=5, batch_size=4)

    # merge prompts
    merged = {
        "rewriter_prompt": rew.prompt.value,
        "extractor_prompt": ext.prompt.value,
        "retriever_k": 1,  # Random default k value
        # "retriever_k": random.choice([1, 5, 10, 25]),  # Random default k value
        "retriever_randomize": False,  # flag to enable randomization
        "hint_prompt": hint.prompt.value,
        "answer_prompt": ans.prompt.value
    }
    torch.save(merged, osp.join(CKPT_DIR, "combined_textgrad_prompts.pth"))
    print(f"textgrad_hotpotqa_four_agents training complete – prompts merged in {CKPT_DIR}")

