import os, json
def parseConfig():
    filepath = os.path.join(os.path.dirname(os.path.relpath(__file__)), "config")
    if os.path.exists(filepath):
        config = json.loads(open(filepath).read())
        return config
    else:
        print("no config found")