import os


# def parse_project(location):
#         for filename in os.listdir(location):
#             with open(os.path.join(location, filename), 'r') as f:
#                 write = False
#                 for line in f:
#                     if()
#     return

def get_content():
    content = """
        @RestController
        @RequestMapping("/")
        public class TestController {


            @GetMapping("/get")
            public TestModel getTest() {
                return new TestModel();
            }
        }

        @Getter
        @Setter
        @NoArgsConstructor
        public class TestModel {
        private String id;
        private TestSubModel testSubModel;
        }

        @Getter
        @Setter
        @NoArgsConstructor
        public class TestSubModel {
            private String name;
        }

        create a contract based on this classes
        """
    return content