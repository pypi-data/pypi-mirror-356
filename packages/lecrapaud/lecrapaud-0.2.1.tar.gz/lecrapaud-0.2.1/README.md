<div align="center">

<div style="font-size:50rem;">🐸</div>

## Welcome to LeCrapaud

**An all-in-one machine learning framework**

</div>

## 🚀 Introduction

LeCrapaud is a high-level Python library for end-to-end machine learning workflows on tabular data, with a focus on financial and stock datasets. It provides a simple API to handle feature engineering, model selection, training, and prediction, all in a reproducible and modular way.

## ✨ Key Features

- 🧩 Modular pipeline: Feature engineering, preprocessing, selection, and modeling as independent steps
- 🤖 Automated model selection and hyperparameter optimization
- 📊 Easy integration with pandas DataFrames
- 🔬 Supports both regression and classification tasks
- 🛠️ Simple API for both full pipeline and step-by-step usage
- 📦 Ready for production and research workflows

## ⚡ Quick Start


### ⚙️ Install the package

```sh
pip install lecrapaud
```

### 🛠️ How it works

This package provides a high-level API to manage experiments for feature engineering, model selection, and prediction on tabular data (e.g. stock data).

### Typical workflow

```python
from lecrapaud import LeCrapaud

# 1. Create the main app
app = LeCrapaud()

# 2. Define your experiment context (see your notebook or api.py for all options)
context = {
    "data": your_dataframe,
    "columns_drop": [...],
    "columns_date": [...],
    # ... other config options
}

# 3. Create an experiment
experiment = app.create_experiment(**context)

# 4. Run the full training pipeline
experiment.train(your_dataframe)

# 5. Make predictions on new data
predictions = experiment.predict(new_data)
```

### Modular usage

You can also use each step independently:

```python
data_eng = experiment.feature_engineering(data)
train, val, test = experiment.preprocess_feature(data_eng)
features = experiment.feature_selection(train)
std_data, reshaped_data = experiment.preprocess_model(train, val, test)
experiment.model_selection(std_data, reshaped_data)
```

## 🤝 Contributing

### Reminders for Github usage

1. Creating Github repository

```sh
$ brew install gh
$ gh auth login
$ gh repo create
```

2. Initializing git and first commit to distant repository

```sh
$ git init
$ git add .
$ git commit -m 'first commit'
$ git remote add origin <YOUR_REPO_URL>
$ git push -u origin master
```

3. Use conventional commits  
https://www.conventionalcommits.org/en/v1.0.0/#summary

4. Create environment

```sh
$ pip install virtualenv
$ python -m venv .venv
$ source .venv/bin/activate
```

5. Install dependencies

```sh
$ make install
```

6. Deactivate virtualenv (if needed)

```sh
$ deactivate
```

---

Pierre Gallet © 2025