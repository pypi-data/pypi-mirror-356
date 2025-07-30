# Shephex 
Shephex can help create, run and manage computational experiments. The Shephex 
slurm executor allows you to submit Python functions or script to a Slurm cluster 
directly from Python. 

The example show how easy it is to submit an arbitrary Python function for execution 
on Slurm. The function in this case is a biased-random walk in 2D for which 50 different 
parameterizations are submitted and executed. 
```python
import numpy as np
import shephex

@shephex.hexperiment()
def biased_random_walk_2d(steps: int, bias_x: float, bias_y: float) -> tuple:
    """
    Simulate a 2D biased random walk and return the final position.
    """    
    # Movement choices: (-1, 1) for left/right (x) and down/up (y)
    moves_x = np.random.choice([-1, 1], size=steps, p=[1 - bias_x, bias_x])
    moves_y = np.random.choice([-1, 1], size=steps, p=[1 - bias_y, bias_y])
    
    final_x = np.sum(moves_x)
    final_y = np.sum(moves_y)
    
    return final_x, final_y  # Return final (x, y) position

if __name__ == '__main__':

    experiments = []
    for steps in [10, 100, 250, 500, 1000]:
        for bias_x in [0.5, 0.6]:
            for repeat in range(5):
                experiments += [biased_random_walk_2d(steps=steps, 
                                                    bias_x=bias_x, 
                                                    bias_y=0.5)]

    executor = shephex.SlurmExecutor(ntasks=1, partition='q48', time='00:10:00')
    executor.execute(experiments)
```