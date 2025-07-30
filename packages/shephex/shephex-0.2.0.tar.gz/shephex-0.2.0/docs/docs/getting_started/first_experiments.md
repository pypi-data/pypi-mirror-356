# First experiments

## A single experiment

Below a simple Python function is defined, with the only difference being it is 
decorated by the `shephex.hexperiment`-decorator.

```python
import shephex

@shephex.hexperiment()
def my_function(a, b, c):
    with open('hello_world.txt') as f: 
        print("Hello world", file=f)

    return a + b + c
```

The decorator changes the function, so calling it will not execute the function 
but rather create an `Experiment` that can be executed by one of Shephex's executors. 
For example, this code
```python
experiment = my_function(a=1, b=1, c=1)
```
Does not return `3` but rather an `Experiment` parameterized with the arguments we gave. 
In order to perform the actual computation we need to give the experiment to an 
executor. 
```python
executor = shephex.LocalExecutor()
result = executor.run(experiment)
print(result)
```
The output from this will be something like; 
```
[ExperimentResult(result=3, status='completed', name='result', extension='pkl', info=None)]
```
If we are only interested in the actual result of the computation, then we can do
```
print(result.result) # Prints 3
```
This might seem like a bit of a round-about way of running what is otherwise a very 
simple Python function. However, behind the scenes Shephex has done quite helpful things! 
Specifically, Shephex has created a directory where we executed the script called `experiments`[^1]. 
The structure of this directory will look something like this
```
├── experiments
│   ├── FSHNjL76SafH3C9NtGE3nq-exp
│   │   ├── hello_world.txt
│   │   └── shephex
│   │       ├── meta.json
│   │       ├── options.json
│   │       ├── procedure.pkl
│   │       ├── procedure.py
│   │       └── result.pkl
```
Shephex has automatically created a directory with a unique name, here `FSHNjL76SafH3C9NtGE3nq-exp`[^2], 
this is the directory where `Shephex` ran our function and the resulting file `hello_world.txt` was created 
in this directory. 

In the `shephex` directory number of files detailing the computation that was done are located, these are

- `meta.json`: Contains information about the status of an experiment and a timestamp. 
- `options.json`: Contains the arguments we set for the experiment.
- `procedure.pkl`: This is a pickle file that can be used to execute the experiment. 
- `procedure.py`: Contains the script we ran, so we can go back and inspect the code. 
- `result.pkl`: Contains the result of the experiment, again in a pickle format, which is anything returned by the decorated function `my_function` in this case just the returned value of `3`. 

With the exception of the `.pkl`-files all of these are easy to read, for example the contents 
of the `options.json` file are

```json
{
    "kwargs": {
        "a": 1,
        "b": 1,
        "c": 1
    },
    "args": []
}
```

## Multiple experiments

Often we want to execute some function with multiple sets of inputs, Shephex 
makes this very simple. With the same defintion of `my_function` as above we can 
for example do; 

```python
experiments = [my_function(a=a, b=2, c=2) for a in [1, 2, 3, 4, 5]]
executor = shephex.LocalExecutor()
results = executor.execute(experiments)
```

Now the `experiments/` directory will contain five sub directories, so looking through the 
`options.json`-files manually would be rather inconvenient, but Shephex provides a CLI 
to help with that, running

```
hex report experiments/
```
will produce about like this
```bash
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━┳━━━┳━━━┓
┃       Identifier       ┃  Status   ┃ a ┃ b ┃ c ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━╇━━━╇━━━┩
│ h4bSqWJ9Vt3Mwvos7kuP3B │ Completed │ 1 │ 2 │ 2 │
│ 7ggmoyFt74Kvn8HEYt3Akv │ Completed │ 2 │ 2 │ 2 │
│ mLng7ryzUgHHrxLJGs32xQ │ Completed │ 3 │ 2 │ 2 │
│ AGyioJs3YxfdqF5WqxGeDi │ Completed │ 4 │ 2 │ 2 │
│ SDdpsNR5nYTRHcK8snyPot │ Completed │ 5 │ 2 │ 2 │
└────────────────────────┴───────────┴───┴───┴───┘
```
Which tells us about the status and options for all of the individual experiments. 
The return value of `executor.execute(experiments)` is a list of results[^3], so we can use that 
but we often it is more convenient to run the experiments and then analyze the results seperately. 
To facilitate this Shephex provides ways of extracting computed results, for example 

```python
from shephex import result_where

results, options = result_where(directory='experiments/', 
                                a=lambda x: x % 2 == 0)

for result, option in zip(results, options):
    print(f"Result: {result}, Option: {option}")
```
Which prints

```
Result: 8, Option: ExperimentOptions(args=[], kwargs={'a': 4, 'b': 2, 'c': 2})
Result: 6, Option: ExperimentOptions(args=[], kwargs={'a': 2, 'b': 2, 'c': 2})
```

[^1]: This is a default name that can be changed, it can be specified when the experiment is 
created e.g. `experiment = my_function(a=1, b=1, c=1, directory='my_directory)` or 
on the decoratored function `@hexperiment(hex_directory='my_directory)`. 
[^2]: This can also be changed through specifying the identifier when creating the experiment e.g. 
`experiment = my_function(a=1, b=1, c=1, identifier="my_func_a1b1c1")` but the default naming 
scheme makes doing so optional and gaurantees a unique identifier. 
[^3]: When using the `LocalExecutor`, with other executors it may instead be a list of `FutureResult`. 