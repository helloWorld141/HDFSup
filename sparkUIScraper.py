from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

def getSlaveIPs():
    html = urlopen("http://43.240.97.180:8080/")
    dom = BeautifulSoup(html.read(), "html.parser")
    suspects = dom.select('td a')   # dead workers will not be selected
                                    # as they are not in <a> tag
    #print(suspects)
    patt = re.compile(r"[0-9]{1,3}(\.[0-9]{1,3}){3}")
    slaves = [suspect for suspect in suspects if re.search(r"worker", suspect.get_text()) != None]
    ips = []
    for slave in slaves:
        try:
            ips.append(patt.search(slave["href"]).group(0))
        except Exception:
            pass
    print(ips)
    return ips

if __name__ == "__main__":
    print(getSlaveIPs())