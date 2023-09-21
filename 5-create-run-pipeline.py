# Create pipeline
pipeline = Pipeline(workspace=ws, steps=[translate_step])

# Submit pipeline run
pipeline_run = exp.submit(pipeline)
pipeline_run.wait_for_completion()

