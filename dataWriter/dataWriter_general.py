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
    filename = 'data.csv'
    with open(filename, 'w') as csvfile:
        fieldnames = ['Year', 'Total_Number_of_Soft_Vuln',\
                      'Low', 'Medium', 'High', 'Number_of_Companies_Reporting_Soft_Vuln']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for xmlfile in xmlfiles:
            print 'processing %s...'%xmlfile
            YEAR = setYear(xmlfile)
            P = NXParser(xmlfile)
            packTime = P.simpleDataPack_time()
            packCompany = P.simpleDataPack_company()

            
            for y in packTime:
                if y.year != YEAR:
                    continue
                s = y.severity
                writer.writerow({fieldnames[0] : y.year, fieldnames[1]: y.total,\
                                 fieldnames[2] : s[0], fieldnames[3] : s[1], fieldnames[4] : s[2],\
                                 fieldnames[5] : len(packCompany)})
                

if __name__ == '__main__':
    main()
    print '\ndone...'
    input()
