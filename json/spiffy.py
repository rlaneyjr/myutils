import click
import json
import sys
 	 

@click.command()
@click.option('--file',help='JSON file.')
@click.option('--n', default = 1, help='Number of lines')


def spiffy(file, n):
	f = open('file', 'r')

	n = 1
	for line in f:
		if n == lines:
			break
		else:
			self.json(line)
			n += 1

def json(line):
	infile = line
	outfile = sys.stdout

	with infile:
		try:
			obj = json.load(infile)
		except ValueError, e:
			raise SystemExit(e)
	with outfile:
		json.dump(obj, outfile, sort_keys=True, indent=4, seperators=(',',': '))
		outfile.write('\n')
		print outfile