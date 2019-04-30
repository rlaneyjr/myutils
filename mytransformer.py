#!/usr/bin/python

import argparse
import os
import json
import yaml
import dicttoxml
import xmltodict
from xml.dom.minidom import parseString

"""
Detect file type and convert
"""
def convertFile(inputFile, outputFile):
  fileName, fileExtensionInput = os.path.splitext(inputFile)
  fileName, fileExtensionOutput = os.path.splitext(outputFile)

  if fileExtensionInput == ".yaml" and fileExtensionOutput == ".json":
    convertYamlJson (inputFile, outputFile)

  if fileExtensionInput == ".json" and fileExtensionOutput == ".yaml":
    convertJsonYaml (inputFile, outputFile)

  if fileExtensionInput == ".json" and fileExtensionOutput == ".xml":
    convertJsonXml (inputFile, outputFile)

"""
Convert from Json to Yaml
"""
def convertJsonYaml(inputFile, outputFile):
  with open(inputFile, 'r') as stream:
    yamlOutput = yaml.safe_dump(json.load(stream), default_flow_style=False)
    f = open(outputFile,'w')
    f.write(yamlOutput) # python will convert \n to os.linesep
    f.close()

"""
Convert from Json to XML
"""
def convertJsonXml(inputFile, outputFile):
  with open(inputFile, 'r') as stream:
    obj = json.load(stream)
    xml = dicttoxml.dicttoxml(obj)
    dom = parseString(xml)
    f = open(outputFile,'w')
    f.write(dom.toprettyxml())
    f.close()

"""
Convert from Yaml to Json
"""
def convertYamlJson(inputFile, outputFile):
  with open(inputFile, 'r') as stream:
    jsonOutput = json.dumps(yaml.load(stream), indent=4)
    f = open(outputFile,'w')
    f.write(jsonOutput)
    f.close()

parser = argparse.ArgumentParser(description='"The Transformer" is a tool to create files in a set of specific formats based on a common input. Available formats: XML, JSON and Yaml')
parser.add_argument('--input', help='Input file to convert')
parser.add_argument('--output', action='append', help='Multiples output files to convert')
args = parser.parse_args()

for output in args.output:
  convertFile(args.input, output)
