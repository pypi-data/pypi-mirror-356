from typing import Dict, Any


def get_context_from_traj(traj: Dict[str, Any]) -> Dict[str, Any]:
    module_names = traj.keys()
    context = {}
    
    # Process inputs if they exist
    for m in module_names:
        if 'input' in traj[m]:
            for k, v in traj[m]['input'].items():
                context[k] = v
    
    # Process outputs if they exist
    for m in module_names:
        if 'output' in traj[m]:
            for k, v in traj[m]['output'].items():
                context[k] = v
    
    return context