import os
import re

def compile_content(location):
    classes = []
    controllers = ""
    models = []
    for folder in os.walk(location):
        for filename in os.listdir(folder[0]):
            if '.java' in filename:
                classes.append(os.path.join(folder[0], filename))
                if 'Controller' in filename:
                    with open(os.path.join(folder[0], filename), 'r') as f:
                        write = False
                        for line in f:
                            if '@RestController' in line:
                                write = True
                            if write:
                                models = add_models(models, line, "\\(*\\).{")[0]
                                controllers = controllers +  line

    return controllers + get_models(models, classes)

def add_models(models, line, terminal):
    modified = False
    if "extends" in line:
        modified = True
        models.append(re.split("(extends | {)", line)[2])
    if re.match("^((private|public|protected)?\\s+)?.*\\s+(\\w+)" + terminal, line):
        value = None
        if '<' in line:
            value = re.split('(<|>)', line)[2]
        else:
            if line.split()[0][0].isupper():
                value = line.split()[0]
            if line.split()[1][0].isupper():
                value = line.split()[1]
        if value and value not in models:
            models.append(value)
            modified = True
    return models, modified

def get_models(models, classes):
    values = ""
    models_history = models.copy()
    while models:
        model = models.pop()
        for clas in classes:
            if model + ".java" in clas:
                with open(clas, 'r') as f:
                        write = False
                        for line in f:
                            if 'class ' + model in line:
                                write = True
                            if write:
                                models_history, modified = add_models(models_history, line, "(;| =)")
                                if modified:
                                    models.append(models_history[-1])
                                values = values + line
    return values

def get_content(path):
    content = compile_content(path)
    return content