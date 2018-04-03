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

class SparkSlusterManager():
    def __init__ (self):
        pass

    def isValidIP(self, ip):
        hosts = open('/etc/hosts').read()
        return re.search(ip, hosts) != None

    def deactivateSparkWorker(self, ip):
        if not self.isValidIP(ip):
            return None
        activatedSlaves = getSlaveIPs()
        if ip not in activatedSlaves:
            return False
        cmd = 'ssh ubuntu@' + ip + ' "cd $SPARK_HOME/sbin; ./stop-slave.sh"'
        try:
            subprocess.run(cmd, stdout=subprocess.STDOUT)
            return True
        except Exception:
            return False

    def activateSparkWorker(self, ip):
        if not self.isValidIP(ip):
            return None
        activatedSlaves = getSlaveIPs()
        if ip in activatedSlaves:
            return False
        cmd = 'ssh ubuntu@' + ip + ' "cd $SPARK_HOME/sbin; ./start-slave.sh spark://43.240.97.180:7077"'
        try:
            subprocess.run(cmd, stdout=subprocess.STDOUT)
            return True
        except Exception:
            return False
