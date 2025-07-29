import json
from typing import Dict


def apply_reward_template(input_dict, output_dict, desc):

        def format_io_dict(io_dict: Dict) -> str:
            """
            Format multiple inputs/outputs into a readable string.

            Args:
                io_dict (Dict): Dictionary containing input/output key-value pairs.

            Returns:
                str: Formatted string with each key-value pair on a new line.
            """
            formatted = []
            for key, value in io_dict.items():
                # Handle nested dictionaries or complex objects
                if isinstance(value, (dict, list)):
                    try:
                        value = json.dumps(value, indent=2)
                    except:
                        value = str(value)
                formatted.append(f"- {key}: {value}")
            return "\n".join(formatted)

        user_prompt_template = (
            "Inputs:\n"
            "{inputs}\n\n"
            "Outputs:\n"
            "{outputs}\n\n"
            "Reward:"
        )
        user_prompt = user_prompt_template.format(
            inputs=format_io_dict(input_dict), 
            outputs=format_io_dict(output_dict)
            )

        return f"You are an evaluator for a module. Module task: {desc}\n" + \
            f"Given the inputs: {format_io_dict(input_dict)}\n" + \
            f"Evaluate its outputs: {format_io_dict(output_dict)}"
        


if __name__ == '__main__':
    input_dict = {
        "input1": "value1",
        "input2": "value2"
    }
    output_dict = {
        "output1": "value1",
        "output2": {
            "output2_1": "value1",
            "output2_2": "value2"
        }
    }
    desc = "Do something"
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct", trust_remote_code=True)
    print(reward_ds_template(input_dict, output_dict, desc, tokenizer))