from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError
from azure.storage.blob import BlobServiceClient
import argparse
import json

# Utility function to read content from blob as a string
def read_blob_to_str(blob_service_client, container_name, blob_name):
    # Get blob client for the given container and blob name
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    
    # Download and decode the blob content
    blob_text = blob_client.download_blob().readall().decode('utf-8')
    return blob_text

# Utility function to write a string back to a blob
def write_str_to_blob(blob_service_client, container_name, blob_name, content):
    # Get blob client for the given container and blob name
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    
    # Upload content to blob, overwrite if it already exists
    blob_client.upload_blob(content, overwrite=True)

# Main function that performs the translation
def translate_text(blob_service_client, input_container, input_blob, output_container, output_blob, key, endpoint, region, target_languages):
    # Read text from blob
    text = read_blob_to_str(blob_service_client, input_container, input_blob)
    
    # Initialize Azure Text Translation Client
    credential = TranslatorCredential(key, region)
    text_translator = TextTranslationClient(endpoint=endpoint, credential=credential)
    
    # Set the text content and target languages for translation
    input_text_elements = [InputTextItem(text=text)]
    
    # Perform translation
    response = text_translator.translate(content=input_text_elements, to=target_languages)
    
    # Parse and save the translated text
    results = {}
    for translation in response:
        for t in translation.translations:
            results[t.to] = t.text
            
    # Write translated text back to blob
    write_str_to_blob(blob_service_client, output_container, output_blob, json.dumps(results))
    
    return results

# Entry point of the script
if __name__ == "__main__":
    # Initialize Azure Blob Service Client with your connection string
    connection_str = "your_connection_string_here"
    blob_service_client = BlobServiceClient.from_connection_string(connection_str)
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-container', type=str, help='Blob container name for input text')
    parser.add_argument('--input-blob', type=str, help='Blob name for input text')
    parser.add_argument('--output-container', type=str, help='Blob container name for storing output')
    parser.add_argument('--output-blob', type=str, help='Blob name for storing output')
    parser.add_argument('--key', type=str, help='Azure subscription key for text translation')
    parser.add_argument('--endpoint', type=str, help='Azure endpoint for text translation service')
    parser.add_argument('--region', type=str, help='Azure region for translation service')
    parser.add_argument('--target-languages', type=str, help='Target languages separated by commas')
    args = parser.parse_args()
    
    # Convert comma-separated languages to list
    target_languages = args.target_languages.split(',')
    
    # Perform the translation and write the results back to a blob
    translated_text = translate_text(blob_service_client, args.input_container, args.input_blob, args.output_container, args.output_blob, args.key, args.endpoint, args.region, target_languages)
    
    # Print completion message
    print("Translation complete. Translated text written to output blob.")
