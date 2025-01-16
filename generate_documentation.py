import os
import javalang
import json
from openai import AzureOpenAI


# Function to scan Java files for @RestController annotation and concatenate their content
def concatenate_rest_controller_content(java_directory):
    concatenated_content = ""

    for root, _, files in os.walk(java_directory):
        for file in files:
            if file.endswith(".java"):  # Only process Java files
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as java_file:
                        java_code = java_file.read()

                        # Parse the Java file
                        try:
                            tree = javalang.parse.parse(java_code)

                            # Extract class declarations
                            for class_decl in tree.types:
                                if isinstance(class_decl, javalang.tree.ClassDeclaration):
                                    annotations = class_decl.annotations or []
                                    for annotation in annotations:
                                        if annotation.name == "RestController":
                                            # Add the full class content to the concatenated content
                                            concatenated_content += f"\nClass: {class_decl.name} (File: {file_path})\n"

                                            # Add the entire class code
                                            concatenated_content += f"{java_code}\n"

                                            # Add a separator between controllers
                                            concatenated_content += "\n"  # Optional: You can add more separators if needed
                        except javalang.parser.JavaSyntaxError as e:
                            print(f"Syntax error in file {file_path}: {e}")
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

    return concatenated_content


# Function to generate OpenAPI 3.0.1 documentation in a single JSON object
# Function to generate OpenAPI 3.0.1 documentation in a single JSON object
def generate_openapi_documentation(concatenated_content):
    # Set up the Azure OpenAI client
    client = AzureOpenAI(
        azure_endpoint="https://trados-openai-dev-sweden.openai.azure.com/",
        api_key="39fa144ca10446018a60b3b9c46c468a",
        api_version="2024-02-01"
    )

    # Specific prompt to request OpenAPI 3.0.1 documentation in JSON format
    prompt = f"""
    Generate OpenAPI 3.0.1 documentation in JSON format for the following Java controller classes. The documentation should include:
    - Paths with operations (GET, PUT, etc.)
    - Parameters with type, description, and required flags
    - Responses with status codes, descriptions, and schema references
    - Reusable schemas for request and response bodies under the components section

    Here are the @RestController classes:
    {concatenated_content}
    """

    # Request completion from Azure OpenAI model
    response = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": prompt,
        }],
        model="gpt-4o-mini",
    )

    # Extract OpenAPI content from the response
    openapi_content = response.choices[0].message.content

    return openapi_content



# Function to save the generated OpenAPI to a JSON file
def save_json_from_response(response: str, file_path: str) -> None:
    """
    Extracts the JSON content from the response string and saves it to a file.

    Args:
    - response (str): The response string containing JSON content.
    - file_path (str): The path to the file where the JSON content should be saved.
    """
    # Find the starting and ending indices for the JSON content
    start_index = response.find("{")
    end_index = response.rfind("}") + 1

    # Extract the JSON content from the response string
    json_content = response[start_index:end_index]

    # Save the extracted JSON content to a file
    with open(file_path, 'w') as file:
        file.write(json_content)


# Function to scan Java files for @RestController annotation and concatenate their content
def concatenate_rest_controller_content(java_directory):
    concatenated_content = ""

    for root, _, files in os.walk(java_directory):
        for file in files:
            if file.endswith(".java"):  # Only process Java files
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as java_file:
                        java_code = java_file.read()

                        # Parse the Java file
                        try:
                            tree = javalang.parse.parse(java_code)

                            # Extract class declarations
                            for class_decl in tree.types:
                                if isinstance(class_decl, javalang.tree.ClassDeclaration):
                                    annotations = class_decl.annotations or []
                                    for annotation in annotations:
                                        if annotation.name == "RestController":
                                            # Add the full class content to the concatenated content
                                            concatenated_content += f"\nClass: {class_decl.name} (File: {file_path})\n"

                                            # Add the entire class code
                                            concatenated_content += f"{java_code}\n"

                                            # Add a separator between controllers
                                            concatenated_content += "\n"  # Optional: You can add more separators if needed
                        except javalang.parser.JavaSyntaxError as e:
                            print(f"Syntax error in file {file_path}: {e}")
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

    return concatenated_content


# Example usage
java_directory = r"C:\Users\aiuga\workspace\lc-public-api-service\src\main\java\com\sdl\lt\lc\publicapi\web\v1"
concatenated_content = concatenate_rest_controller_content(java_directory)

# Generate OpenAPI documentation
openapi_documentation = generate_openapi_documentation(concatenated_content)

# Check if the response is valid and print it for debugging
if openapi_documentation:
    print("Generated OpenAPI documentation:")
    print(json.dumps(openapi_documentation, indent=4))  # Pretty print the JSON
else:
    print("Error: The generated OpenAPI documentation is empty.")

# Save OpenAPI documentation to a JSON file
save_json_from_response(openapi_documentation, "openapi_documentation.json")
