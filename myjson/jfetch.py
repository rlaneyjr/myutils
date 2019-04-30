#!/usr/local/bin/python2.7
# encoding: utf-8
'''
@author:     Sid Probstein
@contact:    sidprobstein@gmail.com
'''

import sys
import argparse
import json
import requests

#############################################    

def main(argv):
       
    parser = argparse.ArgumentParser(description='Fetch json from a RESTful web service, and serialize it')
    parser.add_argument('-o', '--outputfile', help="filename for serialization")
    parser.add_argument('uri', help="uri to the web service")
    args = parser.parse_args()

    # assert: args.uri is a uri
    
    url = args.uri
    res = requests.get(url)
    
    if(res.ok):
        
        jData = json.loads(res.content)
        
        # debug
        # print json.dumps(jData, sort_keys=True, indent=4, separators=(',', ': '))
        
        # if requested, write the file out
        if args.outputfile:
            
            try:
                f = open(args.outputfile, 'wb')
            except Exception, e:                
                f.close()
                sys.exit(e)
    
            print "jfetch.py: writing:", args.outputfile
            try:
                json.dump(jData, f, sort_keys=True, indent=4, separators=(',', ': '))
            except Exception, e:
                sys.exit(e)
                
            f.close()

    else:
        # to do: add durability (see proc_sdwis_json.py)
        res.raise_for_status()
    
    # success reading
    res.close()

    print "jfetch.py: done!"

    
# end main 

#############################################    
    
if __name__ == "__main__":
    main(sys.argv)

# end