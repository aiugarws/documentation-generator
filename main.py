import project_parser
from generate_documentation import generate_controller_documentation, save_json_from_response, generate_documentation

# path to project, add up to main so it doesn't parse Test files
path = r"C:\Users\aiuga\workspace\lc-webhook-receiver-service\src\main\java\com\sdl\lt\lc\webhook\receiver"

classes, controllers = project_parser.get_classes_and_controllers(path)


def main():
    print("Select an option:")
    print("1. Generate new documentation")
    print("2. Analyze existing documentation")
    choice = input("Enter 1 or 2: ")

    if choice == '1':
        print("Generating new documentation...")
        documentation = generate_documentation(openapi_documentation)
        save_json_from_response(documentation, "openapi_documentation.json")
    elif choice == '2':
        print("Analyzing existing documentation...")
        # generate_improved_docs()
    else:
        print("Invalid choice. Please enter 1 or 2.")


i = 1
openapi_documentation = ""
for controller in controllers:
    content = project_parser.get_content_by_controller(classes, controller)
    i += 1
    if content != "":
        rez = generate_controller_documentation(content)
        openapi_documentation = openapi_documentation + rez

if __name__ == "__main__":
    main()
