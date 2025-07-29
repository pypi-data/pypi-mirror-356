# CLI tool to save relevance_connect integrations

import argparse
import json
from relevance_connect.core.relevance_code import RelevanceCode

def read_file_to_string(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def read_json_to_dict(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def main():
    parser = argparse.ArgumentParser(description='Save a Relevance Connect integration')
    parser.add_argument('-m', '--main', help='Path to the main.py file containing the integration code. defaults to main.py. Note: for submission it will need to be main.py', default='main.py')
    parser.add_argument('-mt', '--metadata', help='Path to the metadata.json file containing the integration metadata. defaults to metadata.json. Note: for submission it will need to be metadata.json', default='metadata.json')
    parser.add_argument('-id', '--id', help='Optional ID for the integration. If not provided, a random UUID will be generated.', default=None)

    args = parser.parse_args()
    code = read_file_to_string(args.main)
    metadata = read_json_to_dict(args.metadata)    

    # Create a RelevanceCode instance to save the code
    requirements = [] if "requirements" not in metadata else metadata["requirements"]
    long_output_mode = False if "long_output_mode" not in metadata else metadata["long_output_mode"]
    timeout = 300 if "timeout" not in metadata else metadata["timeout"]
    required = [] if "required" not in metadata else metadata["required"]
    inputs = [] if "inputs" not in metadata else metadata["inputs"]
    icon = None if "icon" not in metadata else metadata["icon"]

    integration = RelevanceCode(
        code=code,
        name=metadata["name"],
        requirements=requirements,
        required=required,
        description=metadata["description"],
        inputs=inputs,
        long_output_mode=long_output_mode,
        timeout=timeout,
        id=args.id,
        icon=icon
    )
    
    # Save the integration
    saved_id = integration.save()
    print(f"Integration saved successfully with ID: {saved_id}")

if __name__ == "__main__":
    main()