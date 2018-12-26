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
       
    parser = argparse.ArgumentParser(description='Scan json files, or files of json arrays, for specific keys, and print them')
    parser.add_argument('-k', '--keytoscan', help="key to scan for")
    parser.add_argument('inputfilespec', help="path to the json file(s) to parse")
    args = parser.parse_args()

    # initialize
    lstFiles = []
    nFiles = 0
       
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
        nFiles = nFiles + 1
        f.close()
        
        # ASSERT: jInput is valid and populated
                
        jSelected = {}
        
        # make it a list, if it is not
        if not isinstance(jInput, list):
            lstTmp = []
            lstTmp.append(jInput)
            jInput = lstTmp        
        
        for jRec in jInput:
            if jRec.has_key(args.keytoscan):
                print str(args.keytoscan) + ":", jRec[args.keytoscan]

    # end for
 
    print"jscan.py: scanned", nFiles, "file(s)"
    print"jscan.py: done!"

    
# end main 

#############################################    
    
if __name__ == "__main__":
    main(sys.argv)

# end