import torch
import subprocess
import numpy as np
import pdb
import logging
import os



def get_gpu_memory_map():
    '''Get the current gpu usage.'''
    result = subprocess.check_output(
        [
            'nvidia-smi', '--query-gpu=memory.used',
            '--format=csv,nounits,noheader'
        ], encoding='utf-8')
    gpu_memory = np.array([int(x) for x in result.strip().split('\n')])
    return gpu_memory


def auto_select_device(device='auto', memory_max=8000, memory_bias=200, strategy='random', seed=42, cuda_visible=[]):
    '''Auto select GPU device'''

    if device != 'cpu' and torch.cuda.is_available():
        if device == 'auto':
            try:
                memory_raw = get_gpu_memory_map()
            except subprocess.CalledProcessError:
                memory_raw = np.ones(torch.cuda.device_count())
            if len(cuda_visible):
                if isinstance(cuda_visible, list):
                    cuda_visible = cuda_visible
                elif isinstance(cuda_visible, str):
                    cuda_visible = eval(cuda_visible)
                else:
                    raise ValueError
            else:
                cuda_visible = [i for i in range(len(memory_raw))]
            invisible_device = torch.ones(len(memory_raw)).bool()
            invisible_device[cuda_visible] = False
            memory_raw[invisible_device] = 1e6
            if strategy == 'greedy' or np.all(memory_raw > memory_max):
                cuda = np.argmin(memory_raw)
                print('GPU Mem: {}'.format(memory_raw))
                print(
                    'Greedy select GPU, select GPU {} with mem: {}'.format(
                        cuda, memory_raw[cuda]))
            elif strategy == 'random':
                memory = 1 / (memory_raw + memory_bias)
                memory[memory_raw > memory_max] = 0
                memory[invisible_device] = 0
                gpu_prob = memory / memory.sum()
                np.random.seed()
                cuda = np.random.choice(len(gpu_prob), p=gpu_prob)
                np.random.seed(seed)
                print('GPU Mem: {}'.format(memory_raw))
                print('GPU Prob: {}'.format(gpu_prob.round(2)))
                print(
                    'Random select GPU, select GPU {} with mem: {}'.format(
                        cuda, memory_raw[cuda]))

            device = 'cuda:{}'.format(cuda)

    else:
        device = 'cpu'

    return device