from Catagory import Catagory
import xml.etree.cElementTree as ET
import re


_XMLNS = 'xmlns'

class NVD_XMLParser(object):
    '''Target at "https://nvd.nist.gov/download.cfm#statements",
       NVD data --- Version 1.2.1
       ***.xml'''

    def __init__(self, filename):
        self.file = filename
        self.KEY = self.getNameSpace()
        self.Catagory = Catagory()
        assert self.KEY is not None
        self.parser()

    def getNameSpace(self):
        p = re.compile('(%s=")(.*?)(")'%_XMLNS)
        with open(self.file, 'r') as f:
            count = 0
            while count <= 10:
                line = f.readline()
                if _XMLNS in line:
                    m = re.search(p, line)
                    return '{' + m.group(2) + '}'
            return None

    def parser(self):
        tree = ET.parse(self.file)
        root = tree.getroot()

        for entry in root.findall('%sentry'%self.KEY):
            date, severity = entry.get('published'), entry.get('severity')
            vuln_soft = entry.find('%svuln_soft'%self.KEY)
            if not vuln_soft:
                continue
            vendors = {}
            for prod in vuln_soft.findall('%sprod'%self.KEY):
                c = prod.get('vendor')
                p = prod.get('name')
                vendors[c] = vendors.get(c, set())
                vendors[c].add(p)
            self.Catagory.handler(date, severity, vendors)

    def simpleDataPack_time(self):
        return self.Catagory.simple_data_pack_time()

    def simpleDataPack_company(self):
        return self.Catagory.simple_data_pack_company()

    def get_specific_company(self, name):
        d = self.Catagory.vendor
        assert name in d
        return d[name]

def test():
    T = NVD_XMLParser('nvdcve-2015.xml')
    #T = NVD_XMLParser('test.xml')
    packT = T.simpleDataPack_time()
    for t in packT:
        #print t
        print t.year, t.total, t.severity

    #packF = T.simpleDataPack_company()
    #arr = sorted(packF)
    #for f in arr:
    #    print packF[f]

    #print T.get_specific_company('microsoft')
    

if __name__ == '__main__':
    test()
