from .hotpot_qa import dataset_engine as hotpot_qa_dataset_engine
from .bigcodebench import dataset_engine as bigcodebench_dataset_engine
from .pubmed import dataset_engine as pubmed_dataset_engine
from .session_based_next_item_selection_dataset import dataset_engine as amazon_next_item_selection_dataset_engine
try:
    from .stark_prime import dataset_engine as stark_prime_dataset_engine
except ImportError:
    stark_prime_dataset_engine = None
    print("stark_prime dataset engine not available. Please install the required dependencies.")

registered_dataset = {
    'hotpotqa': hotpot_qa_dataset_engine,
    'bigcodebench': bigcodebench_dataset_engine,
    'pubmed': pubmed_dataset_engine,
    'stark': stark_prime_dataset_engine,
    'amazon': amazon_next_item_selection_dataset_engine
}
