from Catagory import Catagory
import re
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


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

    def dataPack_time(self):
        return self.Catagory.simple_data_pack_time()

    def dataPack_company(self):
        return self.Catagory.simple_data_pack_company()

    def dataPack_specific_company(self, c):
        return self.Catagory.simple_data_pack_specific_company(c)

    def dataPack_specific_product(self, c, p):
        return self.Catagory.simple_data_pack_specific_product(c, p)

    def dataPack_Time_Oriented_company(self, c):
        return self.Catagory.simple_data_pack_timeO_company(c)

    def dataPack_Time_Oriented_company_allProduct(self, c):
        v = self.dataPack_specific_company(c)
        return [self.dataPack_Time_Oriented_product(c, p) for p in v.prod]

    def dataPack_Time_Oriented_product(self, c, p):
        return self.Catagory.simple_data_pack_timeO_product(c, p)
    
2
def test():
    T = NVD_XMLParser('nvdcve-2015.xml')
    #T = NVD_XMLParser('test.xml')

    ### General Time related Info
    
    #packT = T.dataPack_time()
    #for t in packT:
        #print t
        #print t.year, t.total, t.severity

    ### General Company related Info

    #packF = T.dataPack_company()
    #arr = sorted(packF)
    #for f in arr:
    #    print packF[f]

    ### Specific Company/Products related Info

    #print T.dataPack_specific_company('microsoft')
    #print T.dataPack_specific_product('microsoft', 'windows_8.1')
    
    ### Time oriented Info of Company/Products

    #packTC = T.dataPack_Time_Oriented_company('microsoft')
    #for t in packTC:
    #    print t

    #packTC = T.dataPack_Time_Oriented_company_allProduct('microsoft')
    #for tc in packTC:
    #    for t in tc:
    #        print t

    packTC = T.dataPack_Time_Oriented_product('microsoft', 'windows_7')
    for t in packTC:
        print t
    
if __name__ == '__main__':
    test()
