r"""Command-line tool to validate and pretty-print HTML

    Based on json.tool

Usage::

    $ echo '<html><body>Hello World</body></html>' | python -m html.tool
    <html>
     <body>
      Hello World
     </body>
    </html>

"""
import sys
#from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup

def main():
    if len(sys.argv) == 1:
        infile = sys.stdin
        outfile = sys.stdout
    elif len(sys.argv) == 2:
        infile = open(sys.argv[1], 'rb')
        outfile = sys.stdout
    elif len(sys.argv) == 3:
        infile = open(sys.argv[1], 'rb')
        outfile = open(sys.argv[2], 'wb')
    else:
        raise SystemExit("{0} [infile [outfile]]".format(sys.argv[0]))
    try:
        outfile.write(BeautifulSoup(infile.read()).prettify())
    except ValueError, e:
        raise SystemExit(e)
    outfile.write('\n')


if __name__ == '__main__':
    main()
