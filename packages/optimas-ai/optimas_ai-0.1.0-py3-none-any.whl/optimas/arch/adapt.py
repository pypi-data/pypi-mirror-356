import dspy
import copy
import json
from typing import Type, Any
from optimas.arch.base import BaseModule
from optimas.utils.logging import setup_logger
from optimas.utils.api import get_llm_output


logger = setup_logger(__name__)

def raw_prompt_dspy(signature: Type[dspy.Signature], **inputs: Any) -> str:
    """
    Gets the raw prompt for a signature and inputs.
    This function retrieves the prompt formatted by the dspy adapter.

    Args:
        signature (Type[dspy.Signature]): A subclass of dspy.Signature.
        inputs (Any): Keyword arguments representing the input fields.

    Returns:
        str: The formatted raw prompt string.
    """
    adapter = dspy.settings.adapter or dspy.ChatAdapter()
    return adapter.format(signature, demos=[], inputs=inputs)


def create_module_from_signature(signature_cls: Type[dspy.Signature]) -> Type[BaseModule]:
    """
    Create a module class from a dspy.Signature subclass.
    The module will accept LLM configuration parameters from the pipeline.

    Args:
        signature_cls (Type[dspy.Signature]): A subclass of dspy.Signature that defines the module's input/output fields.

    Returns:
        Type[BaseModule]: A dynamically created subclass of BaseModule.
    """
    # Extract the description from the signature's docstring
    description = signature_cls.__doc__.strip() if signature_cls.__doc__ else "No description provided."

    # Extract input and output field names by checking for InputField and OutputField attributes
    input_fields = list(signature_cls.input_fields.keys())
    output_fields = list(signature_cls.output_fields.keys())
    
    class DSPyModule(BaseModule):
        def __init__(self, signature_cls: Type[dspy.Signature]):
            """Initialize the generated module with signature"""

            try:
                config = {**dspy.settings.config['lm'].kwargs}
                if hasattr(dspy.settings.config['lm'], 'model'):
                    config['model'] = dspy.settings.config['lm'].model
            except:
                raise ValueError("No LLM config found in dspy.settings.config. If you are using LLM, please ensure that dspy.settings.configure is set.")

            self.signature_cls = signature_cls
            super().__init__(
                description=description, 
                input_fields=input_fields, 
                output_fields=output_fields,
                variable=signature_cls.instructions,
                config=config
            )

        def forward(self, **inputs):
            """
            Forward pass for the module, leveraging the dspy.Signature call.
            Expects LLM config params to be passed directly from the pipeline.
            
            Args:
                **inputs: Module inputs including LLM config parameters (model, temperature, max_tokens)
                
            Returns:
                Dict: Module outputs with processed responses
            """
            # Extract LLM config from inputs
            # Use dspy with the specified model and temperature
            config = copy.deepcopy(vars(self.config))
            config.pop('randomize_search_variable')

            signature_cls = self.signature_cls.with_instructions(self.variable)
            signature = dspy.Predict(signature_cls)
            with dspy.settings.context(lm=dspy.LM(**config, cache=False)):
                outputs = signature(**inputs, dspy_cache=False)
                
                outputs_dict = {key: item for key, item in outputs.items()}
                
                for key in signature.signature.output_fields:
                    prefix = signature.signature.output_fields[key].json_schema_extra['prefix']
                    if key in outputs_dict and isinstance(outputs_dict[key], str) and prefix in outputs_dict[key]:
                        outputs_dict[key] = outputs_dict[key].split(prefix)[-1]
            
            return outputs_dict
        
        def dspy_prompt(self, **inputs) -> str:
            """
            Return the prompt string that dspy would generate for a given signature class
            and a dictionary of input values.
            """
            adapter = dspy.settings.adapter or dspy.ChatAdapter()
            
            prompt_str = adapter.format(self.signature_cls, demos=[], inputs=inputs)
            return prompt_str

        # outdated
        def dspy_prompt_system(self):
            """
            Extract the formatted prompt template that would be used by DSPy for a given signature class.
            
            Args:
                
            Returns:
                str: The formatted prompt template that DSPy would use
            """
            # Get docstring which serves as the instruction
            instruction = self.signature_cls.__doc__ or ""
            
            # Build the input template
            input_fields = []
            for field_name, field in self.signature_cls.__annotations__.items():
                if hasattr(field, 'default') and isinstance(field.default, dspy.InputField):
                    prefix = field.default.json_schema_extra.get('prefix', f"{field_name}: ")
                    desc = field.default.json_schema_extra.get('desc', '')
                    input_fields.append(f"{prefix}{{{{ {field_name} }}}}")
            
            output_fields = []
            for field_name, field in self.signature_cls.__annotations__.items():
                if hasattr(field, 'default') and isinstance(field.default, dspy.OutputField):
                    prefix = field.default.json_schema_extra.get('prefix', f"{field_name}: ")
                    output_fields.append(f"{prefix}")
            
            # Combine everything into the final prompt template
            prompt_template = f"{instruction}\n\n"
            prompt_template += "\n".join(input_fields)
            if output_fields:
                prompt_template += "\n\n" + "\n".join(output_fields)
            
            return prompt_template
        
    # Set the name of the generated class
    DSPyModule.__name__ = f"{signature_cls.__name__}Module"
    DSPyModule.__qualname__ = DSPyModule.__name__

    # Return an instance of the generated module
    return DSPyModule(signature_cls)