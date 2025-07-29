from .hotpotqa.four_agents import pipeline_engine as hotpotqa_four_agents_pipeline
from .bigcodebench.three_agents import pipeline_engine as bigcodebench_three_agents_pipeline
from .pubmed.pubmed_agents import pipeline_engine as pubmed_pipeline
from .amazon_product.amazon_next_item_selection_local import pipeline_engine as amazon_next_item_selection_local_pipeline
try:
    from .stark.bio_agent import pipeline_engine as stark_prime_pipeline
except ImportError:
    stark_prime_pipeline = None
    # print("stark_prime pipeline not available. Please install the required dependencies.")

registered_pipeline = {
    'hotpotqa_four_agents_pipeline': hotpotqa_four_agents_pipeline,
    'bigcodebench_three_agents_pipeline': bigcodebench_three_agents_pipeline,
    'pubmed_pipeline': pubmed_pipeline,
    'amazon_next_item_selection_local_pipeline': amazon_next_item_selection_local_pipeline,
    'stark_prime_pipeline': stark_prime_pipeline
}