import os

from openai import AzureOpenAI


# Function to generate OpenAPI 3.0.1 documentation in a single JSON object
def generate_openapi_documentation(concatenated_content):
    # Set up the Azure OpenAI client
    client = AzureOpenAI(
        azure_endpoint=os.environ["ENDPOINT"],
        api_key=os.environ["API_KEY"],
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
