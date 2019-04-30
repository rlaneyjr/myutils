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

def profileDict(dictInput, sKey, sLevel):
    
    if sKey == None:
        # start at top level of dict
        for key, value in dictInput.items():
            print sLevel + key,
            dictNext = dictInput[key]
            if isinstance(dictNext, list):
                print '[' + str(len(dictNext)) + ']'
                sLevel = sLevel + '\t'
                profileDict(dictNext[0], None, sLevel)
                sLevel = ""
            else:
                print
            if isinstance(dictNext, dict):
                sLevel = sLevel + '\t'
                profileDict(dictNext, None, sLevel)
                sLevel = ""
        # end for
    else:
        return profileDict(dictInput['sKey'], None, '')
        
    # end if
    
    return 0

def main(argv):
       
    parser = argparse.ArgumentParser(description='Profile json files')
    parser.add_argument('inputfilespec', help="path to the json file(s) to profile")
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
        print "jprofile.py: reading:", sFile                      
        try:
            f = open(sFile, 'r')
        except Exception, e:
            print "jprofile.py: error opening:", e
            continue
        try:
            jInput = json.load(f)
        except Exception, e:
            print "jprofile.py: error reading:", e
            f.close()
            continue
        
        nFiles = nFiles + 1
        
        # ASSERT: jInput is valid and populated
        
        # success reading
        f.close()
        
        print "jProfile.py: profling:", sFile
        print "jProfile.py: ----------------------------------------"                
        profileDict(jInput, None, '')
        print "jProfile.py: ----------------------------------------"                
                
    # end for
            
    print"jprofile.py: scanned", nFiles, "file(s)"
    print"jprofile.py: done!"

    
# end main 

#############################################    
    
if __name__ == "__main__":
    main(sys.argv)

# end