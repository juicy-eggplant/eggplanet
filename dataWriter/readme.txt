USAGE:

Target at files from "https://nvd.nist.gov/download.cfm#statements" 
					NVD data --- Version 1.2.1 
						[nvdcve-{Year}.xml...] only.

Put **.xml under the same directory with "dataWriter_general.py\dataWriter_general.py" and initiate it.
	Support fetching data related with 1. the number of soft_vuln
					   2. severity of each soft_vuln
                                           3. time (years, month, day)
                                           4. company
                                           5. product
Data will be written into data\nvdcve-{Year}-month.csv
