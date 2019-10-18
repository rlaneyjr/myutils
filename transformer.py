#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noai:et:tw=80:ts=4:ss=4:sts=4:sw=4:ft=python

import argparse
import dicttoxml
import json
import os
import sys
import xml.dom.minidom
import xmltodict
import yaml


USAGE="""
MyTransformer: convert and prettyprint different filetypes

USAGE:
Long: ./mytransformer.py --input <filename> --output <filename>
Short: ./mytransformer.py -i <filename> -o <filename>

EXAMPLES:
Convert yaml to json:
  ./mytransformer.py --input myfile.yaml --output converted.json
Convert file to multiple output types:
  ./mytransformer.py --input myfile.xml --output converted.json converted.yaml
PrettyPrint file
  ./mytransformer.py --input unformatted.xml

NOTE: Please ensure the file extension is present and correct
      This is how we identify the conversion formats
"""


def json_to_yaml(file_in, file_out):
    """
    Convert from Json to Yaml
    """
    with open(file_in, 'r') as i, open(file_out, 'w') as o:
        o.write(yaml.safe_dump(json.load(i), default_flow_style=False))


def json_to_xml(file_in, file_out):
    """
    Convert from Json to XML
    """
    with open(file_in, 'r') as i, open(file_out, 'w') as o:
        dom = dicttoxml.dicttoxml(json.load(i))
        o.write(xml.dom.minidom.parseString(dom).toprettyxml())


def xml_to_json(file_in, file_out):
    """
    Convert from XML to Json
    """
    with open(file_in, 'r') as i, open(file_out, 'w') as o:
        xml = xmltodict.parse(i.read())
        o.write(json.dumps(xml, indent=2))


def xml_to_yaml(file_in, file_out):
    """
    Convert from XML to Yaml
    """
    with open(file_in, 'r') as i, open(file_out, 'w') as o:
        xml = xmltodict.parse(i.read())
        o.write(yaml.safe_dump(xml, default_flow_style=False))


def yaml_to_xml(file_in, file_out):
    """
    Convert from Yaml  to Xml
    """
    with open(file_in, 'r') as i, open(file_out, 'w') as o:
        dom = dicttoxml.dicttoxml(yaml.load(i))
        o.write(xml.dom.minidom.parseString(dom).toprettyxml())


def yaml_to_json(file_in, file_out):
    """
    Convert from Yaml to Json
    """
    with open(file_in, 'r') as i, open(file_out, 'w') as o:
        o.write(json.dumps(yaml.load(i), indent=2))


def prettyprinter(file_in):
    """
    Detect file type and print
    """
    _, file_ext_in = os.path.splitext(file_in)
    file_type = file_ext_in.lstrip('.')
    if file_type not in ['xml', 'json', 'yaml', 'yml']:
        sys.exit(f"Sorry, {file_type} is NOT supported...yet!")
    with open(file_in) as i:
        if file_type in ['yaml', 'yml']:
            print(yaml.safe_dump(i.read()))
        elif file_type is 'xml':
            dom = xml.dom.minidom.parse(i.read())
            print(dom.toprettyxml())
        elif file_type is 'json':
            print(json.dumps(i.read(), indent=2))


def transform(file_in, file_out):
    """
    Detect file type and convert
    """
    _, file_ext_in = os.path.splitext(file_in)
    _, file_ext_out = os.path.splitext(file_out)
    if file_ext_in in [".yaml", ".yml"] and file_ext_out == ".json":
        yaml_to_json(file_in, file_out)
    elif file_ext_in == ".json" and file_ext_out == ".yaml":
        json_to_yaml(file_in, file_out)
    elif file_ext_in == ".json" and file_ext_out == ".xml":
        json_to_xml(file_in, file_out)
    elif file_ext_in == ".xml" and file_ext_out == ".json":
        xml_to_json(file_in, file_out)
    else:
        sys.exit(print(USAGE))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='"The Transformer" is a tool to create files in a set of specific formats based on a common input. Available formats: XML, JSON and Yaml')
    parser.add_argument('-i', '--input', help='Input file to convert')
    parser.add_argument('-o', '--output', action='append', help='Multiples output files to convert')
    args = parser.parse_args()

    if not args.output:
        print(f"Printing results from {args.input}")
        prettyprinter(args.input)
    else:
        for output in args.output:
            print(f"Writing results from {args.input} to {args.output}")
            transform(args.input, output)

