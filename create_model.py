import argparse
import os

def get_python_file_content(model_name):
    txt = f"from base.models import Document\n\n"
    txt += f"class {model_name}(Document):\n\tpass"
    return txt

def get_json_file_content(model_name):
    txt =  f'{{\n\t"name": "{model_name}",\n\t"fields": {{}}\n}}'
    return txt

def create_model(model_name):
    base_dir = os.path.join(os.path.dirname(__file__), 'models')
    model_dir = os.path.join(base_dir, model_name)
    os.makedirs(model_dir, exist_ok=True)
    
    model_python_file = get_python_file_content(model_name)
    
    # Define the content for the JSON model definition file
    json_content = get_json_file_content(model_name)
    
    # Write the Python model file
    with open(os.path.join(model_dir, f"{model_name}.py"), 'w') as f:
        f.write(model_python_file)
    
    # Write the JSON model definition file
    with open(os.path.join(model_dir, f"{model_name}.json"), 'w') as f:
        f.write(json_content)
    
    print(f"Model {model_name} created successfully.")

def main():
    parser = argparse.ArgumentParser(description='Create a new model in the database.')
    parser.add_argument('model_name', type=str, help='The name of the model to create.')
    
    args = parser.parse_args()
    
    create_model(args.model_name)

if __name__ == '__main__':
    main()