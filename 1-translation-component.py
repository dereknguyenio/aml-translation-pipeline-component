
""" Translation Component

This code defines a function translate_text that uses the Azure Text Translation service to translate a given text into multiple languages. The function takes in the Azure key, endpoint, region, text to be translated, and target languages as input parameters. It returns a dictionary containing the translated text for each target language.

The code also includes an argparse command-line interface that allows the user to specify the input parameters for the translate_text function. The user can specify the text to be translated, the target languages, the Azure key, endpoint, and region for the Text Translation service, and the output path for the translated text.

If the user specifies an output path, the translated text is written to a file at the specified location. """

from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError
import argparse
import json

def translate_text(key, endpoint, region, text, target_languages):
    # Create a TranslatorCredential object using the Azure key and region
    credential = TranslatorCredential(key, region)
    # Create a TextTranslationClient object using the Azure endpoint and credential
    text_translator = TextTranslationClient(endpoint=endpoint, credential=credential)

    try:
        # Create a list of InputTextItem objects containing the text to be translated
        input_text_elements = [InputTextItem(text=text)]
        # Call the translate method of the TextTranslationClient object to translate the text to the target languages
        response = text_translator.translate(content=input_text_elements, to=target_languages)

        # Create a dictionary to store the translated text for each target language
        results = {}
        for translation in response:
            for t in translation.translations:
                results[t.to] = t.text

        # Return the dictionary containing the translated text
        return results

    except HttpResponseError as exception:
        # If an error occurs, print the error code and message
        print(f"Error Code: {exception.error.code}")
        print(f"Message: {exception.error.message}")

if __name__ == "__main__":
    # Create an ArgumentParser object to parse the command-line arguments
    parser = argparse.ArgumentParser()
    # Add command-line arguments for the text to be translated, target languages, Azure key, endpoint, region, and output path
    parser.add_argument('--text', type=str, help='Text to be translated')
    parser.add_argument('--target-languages', type=str, help='Languages to translate to')
    parser.add_argument('--key', type=str, help='Azure key for translation')
    parser.add_argument('--endpoint', type=str, help='Azure endpoint for translation')
    parser.add_argument('--region', type=str, help='Azure region for translation')
    parser.add_argument('--output', type=str, help='Output path for the translated text')  # Add this line
    # Parse the command-line arguments
    args = parser.parse_args()

    # Split the target languages string into a list of languages
    target_languages = args.target_languages.split(',')
    # Call the translate_text function to translate the text to the target languages
    translated_text = translate_text(args.key, args.endpoint, args.region, args.text, target_languages)

    # If an output path is specified, write the translated text to a file at the specified location
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(translated_text, f)
    # Otherwise, print the translated text to the console
    else:
        print(json.dumps(translated_text))



