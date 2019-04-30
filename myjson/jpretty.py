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
       
    parser = argparse.ArgumentParser(description='Pretty print json file(s)')
    parser.add_argument('inputfilespec', help="path to the json file(s) to pretty print")
    args = parser.parse_args()

    # initialize
    lstFiles = []
       
    if args.inputfilespec:
        lstFiles = glob.glob(args.inputfilespec)
    else:
        sys.exit()
        
    # read input file(s)
    for sFile in lstFiles:
        
        # read the input file   
        print "jpretty.py: reading:", sFile                      
        try:
            f = open(sFile, 'r')
        except Exception, e:
            print "jpretty.py: error opening:", e
            continue
        try:
            jInput = json.load(f)
        except Exception, e:
            print "jpretty.py: error reading:", e
            f.close()
            continue
                
        # ASSERT: jInput is valid and populated
        
        # success reading
        f.close()
        
        print "jpretty.py:", sFile
        print json.dumps(jInput, sort_keys=True, indent=4, separators=(',', ': '))

    print"jpretty.py: done!"

    
# end main 

#############################################    
    
if __name__ == "__main__":
    main(sys.argv)

# end