import os, json, re, subprocess
from sparkUIScraper import getSlaveIPs
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

class SparkClusterManager():
    def __init__ (self):
        print("Manager created")

    def isValidIP(self, ip):
        hosts = open('/etc/hosts').read()
        if re.search(ip, hosts) == None:
            print(ip + " is not valid")
            return False
        else:
            print(ip + " is valid")
            return True

    def deactivateSparkWorker(self, ip):
        if not self.isValidIP(ip):
            return None
        activatedSlaves = getSlaveIPs()
        if ip not in activatedSlaves:
            return False
        cmd = ['bash', './bin/deactivate.sh', ip] 
        try:
            subprocess.run(cmd)
            print("Slave " + ip + " deactivated")
            return True
        except Exception as e:
            print(e)
            return False

    def activateSparkWorker(self, ip):
        if not self.isValidIP(ip):
            return None
        activatedSlaves = getSlaveIPs()
        if ip in activatedSlaves:
            return False
        cmd = ['bash', './bin/activate.sh', ip]
        try:
            subprocess.run(cmd)
            print("Slave " + ip + " activated") 
            return True
        except Exception as e:
            print(e)
            return False

if __name__ == "__main__":
    manager = SparkClusterManager()
    print(manager.activateSparkWorker("43.240.96.234"))
