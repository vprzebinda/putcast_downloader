import xml.etree.ElementTree as ET
import urllib2
import os
import argparse

dir = ''

def get_xml(uri):
  print "loading " + uri
  dlfile = urllib2.urlopen(uri)
  return dlfile.read()

def fetch(uri, filename):
  target_file = os.path.join(dir, os.path.basename(filename))
  if os.path.isfile(target_file):
    return
  
  dlfile = urllib2.urlopen(uri)
  total = 0
  print "downloading " + target_file
  #fd = os.open(target_file, os.O_WRONLY|os.O_CREAT)
  with open(target_file, "w") as local_file:
    block_size = 1024
    while True:
      data = dlfile.read(block_size)
      if not data:
	break
      total = total + len(data)
      #print "tranferred " + str(total/1000000) + " bytes"
      local_file.write(data)
  
def download(item):
  link = ""
  filename = ""
  for child in item:
    if child.tag == "title":
      filename = child.text
      print "title " + child.text
    if child.tag == "link":
      link = child.text
      print "link " + child.text
  if link and filename:
    fetch(link, filename)

def extract(root):
  if root.tag == "item":
    download(root)
    return
  for child in root:
    extract(child)

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('dir', help='target directory')
parser.add_argument('xml', help='uri to xml')
args = parser.parse_args()
dir = args.dir

root = ET.fromstring(get_xml(args.xml))
extract(root)
