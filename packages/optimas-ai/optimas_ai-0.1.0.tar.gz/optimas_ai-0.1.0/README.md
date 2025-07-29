
### Optimizing Compound Agent System 

#### Note about env:
install from requirements.txt

#### Pipeline usage guide:

```
CompoundAgentPipeline
├── Modes
│   ├── LLM-based Mode
│   │   ├── default_model
│   │   ├── default_temperature
│   │   ├── sample_temperature
│   │   ├── rm (Reward Model)
│   │   ├── intermediate_only
│   │   ├── max_workers
│   │   ├── sample_size
│   │   ├── Execution Flow
│   │   │   ├── call_llm()
│   │   │   │   ├── parallel_sample_and_rank()
│   │   │   │   ├── single_call()
│   │   │   │   └── run_subpipeline()
│   │   └── Output Processing
│   │       ├── evaluate()
│   │       ├── state_dict()
│   │       ├── load_state_dict()
│   │       ├── register_module()
│   │       ├── register_modules()
│   │       └── desc()
│
│   ├── Static-data Mode
│   │   ├── static_data
│   │   ├── random_mode
│   │   ├── Execution Flow
│   │   │   ├── call_static()
│   │   │   │   ├── pick_best_candidate()
│   │   │   │   └── run_subpipeline_static()
│
├── Pipeline Configuration
│   ├── execution_order
│   ├── final_output_fields
│   ├── ground_fields
│   ├── construct_pipeline()
│   └── eval_func
│
├── Subpipeline Execution
│   ├── run_subpipeline()
│   ├── run_subpipeline_llm()
│   └── run_subpipeline_static()
│
└── Internal Methods
    ├── _single_call()
    ├── _parallel_sample_and_rank()
    ├── _call_llm()
    ├── _call_static()
    ├── _run_subpipeline_llm()
    ├── _run_subpipeline_static()
    └── _pick_best_candidate()

```

----
#### Script

```
python -m examples.rag
```

----

### Readings: 
- https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/
- https://openai.com/index/improving-mathematical-reasoning-with-process-supervision/

