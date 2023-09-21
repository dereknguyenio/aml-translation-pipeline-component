from azureml.core import RunConfiguration

# Create PipelineData to hold the output
translated_output = PipelineData("translated_output", datastore=ws.get_default_datastore())

# Pipeline parameters
text_to_translate_param = PipelineParameter(name="text_to_translate", default_value="Hello World")
target_languages_param = PipelineParameter(name="target_languages", default_value="es,fr")

# Configure environment
run_config = RunConfiguration()
run_config.environment.python.user_managed_dependencies = True

# Create pipeline step using the component
translate_step = PythonScriptStep(name="Translate Text",
                                  script_name="1-translation-component.py",
                                  arguments=["--text", text_to_translate_param,
                                             "--target-languages", target_languages_param,
                                             "--subscription-key", "YOUR_SUBSCRIPTION_KEY",
                                             "--endpoint", "YOUR_ENDPOINT",
                                             "--output", translated_output],
                                  inputs=[],
                                  outputs=[translated_output],
                                  compute_target="your-compute-target",
                                  runconfig=run_config)

