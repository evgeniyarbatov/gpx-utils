import sys

import xml.dom.minidom

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring

def parse_kml(file_path):
  with open(file_path, 'r') as file:
    kml = file.read()
  tree = ET.fromstring(kml)
  ns = {'kml': 'http://www.opengis.net/kml/2.2'}
  coordinates = tree.findall('.//kml:coordinates', ns)  
  return coordinates[0].text.strip().split()

def create_gpx(points, output_file):
  gpx = Element('gpx', {
    'creator': 'StravaGPX',
    'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'xsi:schemaLocation': 'http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd',
    'version': '1.1',
    'xmlns': 'http://www.topografix.com/GPX/1/1'
  })
  trk = SubElement(gpx, "trk")
  trkseg = SubElement(trk, "trkseg")
  
  for point in points:
    lon, lat, _ = point.split(',')
    SubElement(trkseg, "trkpt", attrib={"lat": str(lat), "lon": str(lon)})

  gpx_file = xml.dom.minidom.parseString(
    tostring(gpx, encoding="unicode")
  ).toprettyxml()

  with open(output_file, "w") as file:
    file.write(gpx_file)

def main(args):
  input_file = args[0]
  output_file = args[1]
    
  points = parse_kml(input_file)

  create_gpx(points, output_file)
  
if __name__ == "__main__":
  main(sys.argv[1:])