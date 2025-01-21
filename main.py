import project_parser
from generate_documentation import generate_controller_documentation, save_json_from_response, generate_documentation, \
    generate_contract_update

# path to project, add up to main so it doesn't parse Test files
path = r"C:\Users\vblajan\Desktop\Work\Public API\lc-webhook-delivery-service\src\main"
contract_path = r"C:\Users\vblajan\Desktop\Work\Public API\webhook-delivery\Webhook Delivery API.oas2.yml"
controller_path = r"C:\Users\vblajan\Desktop\Work\Public API\lc-webhook-delivery-service\src\main\java\com\sdl\lt\lc\webhook\delivery\web\WebhookDeliveryController.java"


def main():
    classes, controllers = project_parser.get_classes_and_controllers(path)
    print("Select an option:")
    print("1. Generate new documentation")
    print("2. Update existing documentation")
    choice = input("Enter 1 or 2: ")

    if choice == '1':
        print("Generating new documentation...")

        openapi_documentation = ""
        for controller in controllers:
            content = project_parser.get_content_by_controller(classes, controller)
            if content != "":
                rez =  generate_controller_documentation(content)
                openapi_documentation = openapi_documentation + rez

        documentation = generate_documentation(openapi_documentation)
        save_json_from_response(documentation, "openapi_documentation.json")
    elif choice == '2':
        print("Updating existing documentation...")

        controller_content = project_parser.get_content_by_controller(classes, controller_path)
        contract_documentation = project_parser.add_previous_contract(contract_path)

        documentation = generate_contract_update(controller_content, contract_documentation)
        save_json_from_response(documentation, "openapi_documentation.json")
    else:
        print("Invalid choice. Please enter 1 or 2.")
    print("Operation Finished")

if __name__ == "__main__":
    main()
