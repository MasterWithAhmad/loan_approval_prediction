import papermill as pm

# List of notebooks to execute in order
notebooks = [
    "01_data_understanding.ipynb",
    "02_data_exploration.ipynb",
    "03_data_preprocessing.ipynb",
    "04_model_training.ipynb",
    "05_model_evaluation.ipynb"
]

# Execute each notebook sequentially
for notebook in notebooks:
    print(f"Executing {notebook}...")
    output_notebook = notebook.replace(".ipynb", "_executed.ipynb")
    try:
        pm.execute_notebook(notebook, output_notebook)
        print(f"Finished executing {notebook}. Output saved to {output_notebook}.")
    except Exception as e:
        print(f"Error executing {notebook}: {e}")
        break