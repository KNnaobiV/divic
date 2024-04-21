### Create Models

Creates a model which subclasses document.
It creates a model folder if none exists and generates the following files:
- models/<model_name>.py: This file holds logic for the model.
- models/<model_name>.json: Generates a json file which will describe model fields.

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch task_dev
bench install-app task_manager
```

### Usage

```bash
python create_models.py <model_name>
```