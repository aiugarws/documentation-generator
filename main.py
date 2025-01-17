import json

import project_parser
from generate_documentation import generate_openapi_documentation, save_json_from_response

# path to project, add up to main so it doesn't parse Test files
path = r"C:\Users\aiuga\workspace\lc-webhook-receiver-service\src\main"
content = project_parser.get_content(path)

# Generate OpenAPI documentation
openapi_documentation = generate_openapi_documentation(content)

# Check if the response is valid and print it for debugging
if openapi_documentation:
    print("Generated OpenAPI documentation:")
    print(json.dumps(openapi_documentation, indent=4))  # Pretty print the JSON
else:
    print("Error: The generated OpenAPI documentation is empty.")

# Save OpenAPI documentation to a JSON file
response = save_json_from_response(openapi_documentation, "openapi_documentation.json")

