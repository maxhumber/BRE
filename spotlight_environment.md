####Spotlight

Install conda kernels (in your main environment)

```
conda install nb_conda_kernels
```

Create a 3.6 environment with Anaconda:

```
conda create -n spot python=3.6
conda activate spot
conda install -c anaconda jupyter ipykernel pandas nb_conda_kernels
conda install -c maciejkula -c pytorch spotlight
```

To get out:

```
conda deactivate
```