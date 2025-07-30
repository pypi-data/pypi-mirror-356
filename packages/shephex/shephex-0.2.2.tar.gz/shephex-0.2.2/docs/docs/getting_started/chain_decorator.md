# Using `shephex.chain`

As an example of using the `shephex.chain`-decorator, consider a simple decorated function 

```python
--8<-- "test_getting_started_1.py:part1"
```
Any valid Python code is allowed in this function, be it other functions defined in the same 
script or imported from other packages. Then we can use Shephex to create and 
queue sets of evaluations of this function.

```python
--8<-- "test_getting_started_1.py:func"
```
The decorated function is then used to create the experiments we want to run. First 
the directory where we want to run and store the experiments is given. Then, we are creating experiments where the `a` and `b` arguments will be paired, like using Python's 
`zip` on the two lists. For each of these two pairs an experiment will be created for 
all three values of `c` - resulting in a total of 6 experiments. Finally,
```python
--8<-- "test_getting_started_1.py:part3"
```
This runs all the experiments, here using the `LocalExecutor` which runs everything in 
serial in the current Python instance. 

Running this script produces a directory `experiments` containing the results of the 
calculations and other information about the experiments and their execution. 
