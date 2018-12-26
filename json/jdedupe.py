#!/usr/local/bin/python2.7
# encoding: utf-8
'''
@author:     Sid Probstein
@contact:    sidprobstein@gmail.com
'''

#############################################    
# dedupe json file(s)

import sys
import argparse
import json
import operator
import csv
import requests
import time

#############################################    

def main(argv):
       
    parser = argparse.ArgumentParser(description="Process json and report on/remove duplicates")
    parser.add_argument('-o', '--outputfile', help="filename to write de-duped output to, in json format")
    parser.add_argument('-k', '--key', required=True, help="key to use for duplicate detection")
    parser.add_argument('inputfile', help="path to input file in json format")
    args = parser.parse_args()
        
    #############################################    
    # read the input file
    
    print "jdedupe.py: reading", args.inputfile
        
    try:
        fi = open(args.inputfile, 'r')
    except Exception, e:
        print "jdedupe.py: error opening:", e
        sys.exit(e)
    
    lstInput = []
        
    try:
        lstInput = json.load(fi)
    except Exception, e:
        print "jdedupe.py: error reading:", e
        fi.close()
        
    fi.close()
    
    dictRecords = {}
    for jRecord in lstInput:
        if dictRecords.has_key(jRecord[args.key]):
            dictRecords[jRecord[args.key]] = dictRecords[jRecord[args.key]] + 1
        else:
            dictRecords[jRecord[args.key]] = 1
                
    nDupes = 0
    # report
    for key, value in dictRecords.items():
        if value > 1:
            nDupes = nDupes + value
            print "jdedupe.py: duplicate:", key, "(" + str(value) + ")"
    
    print "jdedupe.py:", len(lstInput), "records contain", nDupes, "duplicates",
    if nDupes == 0:
        print ":-)"
    else:
        print ":-\\"
    
    if args.outputfile:
        print "jdedupe.py: removing duplicates..."
        lstDeduped = []
        for jRecord in lstInput:
            if dictRecords[jRecord[args.key]] > 1: 
                if dictRecords[jRecord[args.key]] == 9999:
                    # skip
                    continue
                # emit this first one, no more
                lstDeduped.append(jRecord)
                dictRecords[jRecord[args.key]] = 9999
            else:
                # no dupes detected
                lstDeduped.append(jRecord)
        print "jdedupe.py:", len(lstDeduped), "records retained"
        try:
            fo = open(args.outputfile, 'wb')
        except Exception, e:                
            fo.close()
            sys.exit(e)
        # write the file
        try:
            json.dump(lstDeduped, fo, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception, e:
            sys.exit(e)
        fo.close()
        
# end main 

#############################################    
    
if __name__ == "__main__":
    main(sys.argv)

# end
