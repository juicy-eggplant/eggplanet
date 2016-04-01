from NVD_XMLParser import NVD_XMLParser as NXParser
import csv, sys, os, re

def setYear(name):
    p = re.compile('[0-9]{4}')
    m = re.search(p, name)
    if m:
        return str(m.group())

def main():
    xmlfiles = [xml for xml in os.listdir('.') if xml.endswith('.xml')]
    xmlfiles.sort()
    assert xmlfiles
    for xmlfile in xmlfiles:
        filename = xmlfile.replace('.xml', '-months.csv')
        print 'processing %s...'%xmlfile
        YEAR = setYear(xmlfile)
        P = NXParser(xmlfile)
        packTime = P.simpleDataPack_time()

        with open(filename, 'w') as csvfile:
            fieldnames = ['Month', 'Number_of_Soft_Vuln',\
                            'Low', 'Medium', 'High']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for y in packTime:
                if y.year != YEAR:
                    continue
                mon = y.month
                arr = sorted(mon)
                for m in arr:
                    m = mon[m]
                    s = m.severity
                    writer.writerow({fieldnames[0] : m.month, fieldnames[1]: m.total,\
                                     fieldnames[2] : s[0], fieldnames[3] : s[1],\
                                     fieldnames[4] : s[2]})
                

if __name__ == '__main__':
    main()
    print '\ndone...'
    input()
