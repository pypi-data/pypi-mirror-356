# Shephex with Slurm

## `SlurmExecutor`

Using Shephex to submit experiments to Slurm is just a matter of using the `SlurmExecutor`
rather than the `LocalExecutor` shown in previous examples. For example, 

```python
import shephex

@shephex.hexperiment()
def my_function(a, b, c):
    with open('hello_world.txt', 'w') as f: 
        print("Hello world", file=f)
    return a + b + c

if __name__ == '__main__':

    experiments = [my_function(a=a, b=2, c=2) for a in [1, 2, 3, 4, 5]]
    executor = shephex.SlurmExecutor(
        partition='q48',
        ntasks=1,
        nodes=1, 
        time='00:10:00',
    )
    results = executor.execute(experiments)
```

The Shephex Slurm executor supports all the options of `sbatch` using either their short or long option 
names. Shephex will create a slurm submission script and submit all the given experiments as a 
single array job. 

Just as with the `LocalExecutor` a new directory `experiments/` will have been created 
containing the experiments and eventually the results once the jobs have finished running on
the Slurm cluster. An additional directory, by default, called `slurm/` will also have been 
created containing the submission script (e.g. `submit_0.sh`) and Shephex slurm configuration file (`config_0.json`). The Slurm output files for each experiment can be found in their respective directories under `experiments/`.

## Slurm configuration files and profiles

Rather than writing all the slurm settings each time a `SlurmExecutor` is made Shephex 
offers two ways of simplifying this. 

- Configuration files: The SlurmExecutor can be instanstiated from a configuration file, this is a `json` file 
that contains the slurm settings you want to use. 
- From a Shephex Slurm profile name. 

The configuration file corresponding to the settings used above looks like so

```json
{
    "partition": "q48",
    "ntasks": 1,
    "nodes": 1,
    "time": "00:10:00",
    "scratch": false,
    "ulimit": 8000,
    "move_output_file": true,
    "commands_pre_execution": [],
    "commands_post_execution": []
}
```
This file was actually written to the `slurm/` directory when the code above was run. 
To use it to instantiate a `SlurmExecutor` we simply do, 

```python
executor = shephex.SlurmExecutor.from_config("<path_to_config_file>")
```
You can also overwrite any options from the config file, e.g. we can increase 
the time limit while keeping the rest of the options from the config file
```python
executor = shephex.SlurmExecutor.from_config("<path_to_config_file>", 
                                            time="01:00:00")
```
Rather than remembering the path to or moving around a config file Shephex 
also supports making profiles. These are setup through Shephex's CLI specifically 
with `hex slurm profile`. To make add a profile use 

```
hex slurm profile add `basic.json`
```
Where `basic.json` is a configuration, like the one discussed above. This will add 
new Shephex Slurm profile, you can see all your profiles with 
```
hex slurm profile list
```
Which after adding the `basic`-profile will output something like;
```
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Name      ┃ Full Path                                           ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ basic     │ /home/user/.shephex/slurm_profiles/basic.json       │
└───────────┴─────────────────────────────────────────────────────┘
```
Also listing where the configuration for each profile is located in case you 
want to update it. An executor with the `basic`-profile can be created with

```python
executor = shephex.SlurmExecutor.from_profile('basic')
```
Again any of the options specified by the profile can be overwritten, like with the 
configuration files

```python
executor = shephex.SlurmExecutor.from_profile('basic', time="01:00:00")
```

