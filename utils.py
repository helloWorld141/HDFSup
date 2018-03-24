import os, json
def parseConfig():
    filepath = os.path.join(os.path.dirname(os.path.relpath(__file__)), "config")
    if os.path.exists(filepath):
        config = json.loads(open(filepath).read())
        return config
    else:
        print("no config found")

class persistFilename():
    def __init__(self):
        self.filepath = os.path.join(os.path.dirname(os.path.relpath(__file__)), "filenames")
        if os.path.exists(self.filepath):
            f = open(self.filepath).read()
            if f != "":
                self.files = json.loads(f)
                return
        self.files = {}
    
    def fileExist(self, filename):
        return filename in self.files.keys()

    def addFilename(self, filename, hdfspath):
        self.files[filename] = hdfspath
        self.persist()

    def persist(self):
        with open(self.filepath, "w") as f:
            f.write(json.dumps(self.files))

    def getHDFSpath(self, filename):
        if self.files.get(filename) != None:
            return self.files.get(filename)
        else:
            print("file not exist")
            return None
