import json
import os

from openai import AzureOpenAI
import project_parser
from generate_documentation import generate_openapi_documentation, save_json_from_response

# path to project, add up to main so it doesn't parse Test files
path = r"C:\Users\vblajan\Desktop\Work\Public API\lc-public-api-service\src\main"
# content = project_parser.get_content(path)

classes, controllers = project_parser.get_classes_and_controllers(path)

i = 1
openapi_documentation = ""
for controller in controllers:
    content = project_parser.get_content_by_controller(classes, controller)
    print("Controller Number " + str(i))
    i += 1
    print(content)
    if content != "":
        rez = generate_openapi_documentation(content)
        if rez:
            print("Generated OpenAPI documentation:")
            print(json.dumps(rez, indent=4))  # Pretty print the JSON
        else:
            print("Error: The generated OpenAPI documentation is empty.")

        openapi_documentation = openapi_documentation + rez

client = AzureOpenAI(
        azure_endpoint= os.environ["ENDPOINT"],
        api_key= os.environ["API_KEY"],
        api_version="2024-02-01"
    )

prompt = openapi_documentation + "combine these contracts into 1"

openapi_response = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": prompt,
        }],
        model="gpt-4o-mini",
    ).choices[0].message.content
# Generate OpenAPI documentation
# openapi_documentation = generate_openapi_documentation(content)
#
# # Check if the response is valid and print it for debugging
if openapi_response:
    print("Generated OpenAPI documentation:")
    print(json.dumps(openapi_response, indent=4))  # Pretty print the JSON
else:
    print("Error: The generated OpenAPI documentation is empty.")
#
# # Save OpenAPI documentation to a JSON file
response = save_json_from_response(openapi_response, "openapi_documentation.json")

