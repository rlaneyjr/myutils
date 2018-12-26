#!/usr/local/bin/python2.7
# encoding: utf-8
'''
@author:     Sid Probstein
@contact:    sidprobstein@gmail.com
'''

import sys
import argparse
import glob
import json

#############################################    

def main(argv):
       
    parser = argparse.ArgumentParser(description='Merge JSON files')
    parser.add_argument('-o', '--outputfile', help="filename to write merged output to")
    parser.add_argument('inputfilespec', help="path to the json file(s) to merge")
    args = parser.parse_args()

    # initialize
    lstFiles = []
    nFiles = 0
    nRecords = 0
    lstMerge = []
       
    if args.inputfilespec:
        lstFiles = glob.glob(args.inputfilespec)
    else:
        sys.exit()
        
    # read input file(s)
    for sFile in lstFiles:
        
        # read the input file   
        print "jscan.py: reading:", sFile                      
        try:
            f = open(sFile, 'r')
        except Exception, e:
            print "jscan.py: error opening:", e
            continue
        try:
            jInput = json.load(f)
        except Exception, e:
            print "jscan.py: error reading:", e
            f.close()
            continue
        
        # success reading
        nFiles = nFiles + 1
        f.close()
        
        # ASSERT: jInput is valid and populated
        lstMerge = lstMerge + jInput
        nRecords = nRecords + len(jInput)

    # end for
 
    print"jscan.py: scanned", nFiles, "file(s)"

    # write jMerge out
    if args.outputfile:
        try:
            fo = open(args.outputfile, 'wb')
        except Exception, e:                
            fo.close()
            sys.exit(e)
        # write the file
        try:
            json.dump(lstMerge, fo, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception, e:
            sys.exit(e)
        fo.close()
    
    print "jscan.py: wrote", nRecords, "records from", nFiles, "file(s) to", args.outputfile
    print "jscan.py: done!"
    
# end main 

#############################################    
    
if __name__ == "__main__":
    main(sys.argv)

# end