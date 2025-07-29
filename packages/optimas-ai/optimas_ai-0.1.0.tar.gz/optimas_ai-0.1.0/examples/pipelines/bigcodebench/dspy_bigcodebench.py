import re
import dspy

from optimas.arch.base import BaseModule
from examples.metrics.pass_rate import pass_rate
from bigcodebench.sanitize import sanitize


class InitialCodeGeneratorSignature(dspy.Signature):
    """Generate a runnable Python solution for a given coding problem."""

    question: str = dspy.InputField(desc="The coding problem.")
    initial_code: str = dspy.OutputField(desc="The generated Python solution.")

class InitialCodeGenerator(BaseModule):
    """Generate a runnable Python solution for a given coding problem."""

    def __init__(self):
        super().__init__(
            description="Generate Python solution for coding problem.",
            input_fields=["question"],
            output_fields=["initial_code"],
        )

        self.dspy_module = dspy.ChainOfThought(InitialCodeGeneratorSignature)


    @property
    def variable(self):
        return {"module": self.dspy_module}
    
    def update(self, variable):
        if "module" in variable:
            self.dspy_module = variable["module"]


    def forward(self, question: str):
        """
        Generate a runnable Python solution for a given coding problem.

        Args:
            question (str): A clear and concise description of the coding problem.
            **inputs: May include model, temperature, max_tokens set by pipeline

        Returns:
            code (str): A complete, executable Python solution that solves the given problem without syntax errors.
        """
        initial_code = self.dspy_module(question=question).initial_code
        initial_code = sanitize(initial_code, entrypoint="task_func")
        initial_code = initial_code.split("```python")[-1].split("```")[0].strip()

        return {"initial_code": initial_code}


class UnitTestGeneratorSignature(dspy.Signature):
    """Generate a set of Python unit tests to validate the correctness of the generated code.

Question: Calculates the average of the sums of absolute differences between each pair of consecutive numbers for all permutations of a given list. Each permutation is shuffled before calculating the differences. Args: - numbers (list): A list of numbers. Default is numbers from 1 to 10.    

Additional Unit Tests:
```python
import unittest

class TestCases(unittest.TestCase):
    def test_default(self):
        # Basic: default list 1‑3 should yield positive float
        result = task_func()
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)

    def test_identical(self):
        # Edge: identical values → all differences zero → average zero
        result = task_func([5, 5, 5])
        self.assertEqual(result, 0.0)

    def test_large_input(self):
        # Large‑scale: longer list should still return finite float
        data = list(range(100))
        result = task_func(data)
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)
```
    """

    question: str = dspy.InputField(desc="The coding problem.")
    additional_unit_tests: str = dspy.OutputField(desc="The generated Python unit tests.")


class UnitTestGenerator(BaseModule):
    """Generate a set of Python unit tests to validate the correctness of the generated code."""

    def __init__(self):
        super().__init__(
            description="Generate a set of Python unit tests to validate the correctness of the generated code.",
            input_fields=["question"],
            output_fields=["additional_unit_tests"],
        )

        self.dspy_module = dspy.ChainOfThought(UnitTestGeneratorSignature)


    @property
    def variable(self):
        return {"module": self.dspy_module}
    

    def update(self, variable):
        if "module" in variable:
            self.dspy_module = variable["module"]


    def forward(self, question):
        """
        Generate a set of Python unit tests to validate the correctness of the generated code.

        Args:
            question (str): A clear and concise description of the coding problem.

        Returns:
            additional_unit_tests (str): A set of Python unit tests to validate the correctness of the generated code.
        """
        unit_tests = self.dspy_module(question=question).additional_unit_tests
        
        match = re.search(r"```python\s*(.*?)\s*```", unit_tests, re.DOTALL)
        if match:
            unit_tests = match.group(1).strip("\n").strip()
        else:
            unit_tests = ""

        return {"additional_unit_tests": unit_tests}


class Executor(BaseModule):
    """Execute the generated code against the generated unit tests and return the results."""

    def __init__(self):
        super().__init__(
            description="Execute the generated Python code using the provided unit tests.",
            input_fields=["initial_code", "additional_unit_tests"],
            output_fields=["execution_result"],
        )


    @property
    def variable(self):
        return {}
    

    def update(self, variable):
        pass


    def forward(self, initial_code, additional_unit_tests):
        initial_code = initial_code.split("```python")[-1].split("```")[0].strip()
        result = pass_rate(initial_code, additional_unit_tests, entry_point="task_func")
        return {"execution_result": result}


class FinalCodeGeneratorSignature(dspy.Signature):
    """Refine code based on test results."""

    question = dspy.InputField(desc="The coding problem.")
    initial_code = dspy.InputField(desc="Initial code solution.")
    additional_unit_tests = dspy.InputField(desc="Unit tests for evaluation.")
    execution_result = dspy.InputField(desc="Test execution results, including errors.")
    code = dspy.OutputField(desc="Improved code solution based on test results.")


class FinalCodeGenerator(BaseModule):
    """Refine code based on test results."""

    def __init__(self):
        super().__init__(
            description="Refine code based on test results.",
            input_fields=["question", "initial_code", "additional_unit_tests", "execution_result"],
            output_fields=["code"],
        )

        self.dspy_module = dspy.ChainOfThought(FinalCodeGeneratorSignature)


    @property
    def variable(self):
        return {"module": self.dspy_module}
    

    def update(self, variable):
        if "module" in variable:
            self.dspy_module = variable["module"]


    def forward(self, question: str, initial_code: str, additional_unit_tests: str, execution_result: str):
        """
        Refine code based on test results.
        """
        code = self.dspy_module(question=question, initial_code=initial_code, additional_unit_tests=additional_unit_tests, execution_result=execution_result).code
        code = sanitize(code, entrypoint="task_func")
        code = code.split("```python")[-1].split("```")[0].strip()
        return {"code": code}
