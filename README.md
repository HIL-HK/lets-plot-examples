# Lets-Plot Examples

### Environment Set Up

Use the [conda](https://docs.conda.io) package manager to install all the necessary packages:

```bash
conda env create -f .binder/environment.yml
```

To activate the environment, use the `conda activate` command:

```bash
conda activate lets-plot-examples
```

If file `binder/environment.yml` has been changed, you need to update the environment. In that case, run:

```bash
conda env update --name lets-plot-examples --file .binder/environment.yml --prune
```

### Examples

Open the terminal, execute `jupyter notebook` and navigate through the directories containing examples.

The main set of demo notebooks is located in the [demo/](demo) and [features/](features) directories. More examples can be found in [plans/](plans) and [remakes/](remakes).