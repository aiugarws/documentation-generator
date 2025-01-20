import os

from openai import AzureOpenAI

# Set up the Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint="",
    api_key="",
    api_version="2024-02-01"
)


# Function to generate OpenAPI 3.0.1 documentation in a single JSON object
def generate_controller_documentation(concatenated_content):
    # Specific prompt to request OpenAPI 3.0.1 documentation in JSON format
    prompt = f"""
    Generate a complete OpenAPI 3.0.1 documentation in JSON format for all the following Java controller classes. The documentation should include details for all provided endpoints, up to 100 endpoints, without omitting any. Ensure the output is concise, accurate, and adheres strictly to the OpenAPI specification.

    The documentation must include:
    - **Paths** :with operations (GET, POST, PUT, DELETE, etc.) and meaningful descriptions for each operation.
        - If a description is missing, provide a placeholder based on the method and resource name, like "Get account" or "Update resource"
        - If multiple operation have the same path should group all related operations (e.g., `GET`, `PUT`, `POST`, `DELETE`) under the same path
        - If multiple same path but different path variables, then create a new path for each of it.
    - Each operation must include a unique `operationId` and a `description`. Use the format `<HTTP method><CamelCase path>` (e.g., `getUsersById`) for operationId. Ensure `operationId` values are unique across all operations in the API and do not contais numbers. For `description` use the operation and the resource name, like "Get account".
    - **Parameters** with type, description, and required flags. For missing descriptions, provide placeholders like "Parameter description not provided."
    - **Responses** with status codes, descriptions, and schema references. If response descriptions are missing, add placeholders like "Response description not provided."
    - **Reusable schemas** for request and response bodies under the components section. If a schema is referenced but not defined, create a placeholder schema with a description like "Placeholder schema for SchemaName."
    - No comments, suggestions, or placeholders like "add your additional endpoints" should be included in the documentation. The output must strictly focus on the provided Java classes and their details.
    - No include health paths 
    
    Document the full set of endpoints, up to 100, based on the provided input. Ensure the resulting JSON is complete and valid according to the OpenAPI 3.0.1 specification.

    Here are the @RestController classes:
    {concatenated_content}
    """

    # Request completion from Azure OpenAI model
    response = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": prompt,
        }],
        model="gpt-4o-dev",
    )

    # Extract OpenAPI content from the response
    openapi_content = response.choices[0].message.content

    return openapi_content


def generate_documentation(openapi_documentation):
    prompt = openapi_documentation + "combine these contracts into 1"

    openapi_response = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": prompt,
        }],
        model="gpt-4o-dev",
    ).choices[0].message.content
    return openapi_response


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
