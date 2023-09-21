from azureml.core import Workspace, Experiment

# Connect to the Azure Machine Learning workspace
ws = Workspace.from_config()

# Create or retrieve an experiment
experiment_name = "TextTranslationPipeline"
exp = Experiment(workspace=ws, name=experiment_name)
