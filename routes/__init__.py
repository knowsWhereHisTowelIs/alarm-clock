import os


def register_all():
    directory = os.path.dirname(__file__)
    for root, directories, files in os.walk(directory):
        # print({"root": root, "directories": directories, "files": files})
        for f in [f for f in files if f.endswith('.py')]:
            file_path = os.path.join(root, f)
            module_name = file_path.replace(root, 'routes').replace('/', '.')[:-3]
            __import__(module_name)
