import gpxpy
import sys

from geopy.distance import geodesic

import xml.dom.minidom
from xml.etree.ElementTree import Element, SubElement, tostring

def find_closest_point(
  gpx,
  point_lat,
  point_lng,
):
  closest_point = None
  min_distance = float('inf')
  for track in gpx.tracks:
    for segment in track.segments:
      for point in segment.points:
        distance = geodesic((point.latitude, point.longitude), (point_lat, point_lng)).meters
        if distance < min_distance:
          min_distance = distance
          closest_point = point
  return str(closest_point.latitude), str(closest_point.longitude)

def reverse_gpx(gpx):
  for track in gpx.tracks:
    for segment in track.segments:
        segment.points.reverse()
  return gpx

def create_gpx():
  gpx = Element('gpx', {
      'creator': 'StravaGPX',
      'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
      'xsi:schemaLocation': 'http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd',
      'version': '1.1',
      'xmlns': 'http://www.topografix.com/GPX/1/1'
  })
  trk = SubElement(gpx, "trk")
  trkseg = SubElement(trk, "trkseg")
  return gpx, trkseg

def save_gpx(gpx, output_file):
  gpx_file = xml.dom.minidom.parseString(
    tostring(gpx, encoding="unicode")
  ).toprettyxml()

  print('Saving:', output_file)
  with open(output_file, "w") as file:
    file.write(gpx_file)

def main(args):
  start_lat = args[0]
  start_lng = args[1]

  stop_lat = args[2]
  stop_lng = args[3]

  input_file = args[4]
  output_file = args[5]

  gpx_file = open(input_file, 'r')
  gpx = gpxpy.parse(gpx_file)

  gpx = reverse_gpx(gpx)
  print("GPX is reversed")

  start_lat, start_lng = find_closest_point(gpx, start_lat, start_lng)
  print(f"Start: ({start_lat}, {start_lng})")

  stop_lat, stop_lng = find_closest_point(gpx, stop_lat, stop_lng)
  print(f"Stop: ({stop_lat}, {stop_lng})")

  gpx_out, trkseg_out = create_gpx()
  segment_begun, segment_ended = False, False

  for track in gpx.tracks:
    for segment in track.segments:
      for point in segment.points:
        lat, lng = str(point.latitude), str(point.longitude)

        if lat == start_lat and lng == start_lng:
          segment_begun = True

        if lat == stop_lat and lng == stop_lng:
          segment_ended = True

        if segment_begun and not segment_ended:
          SubElement(trkseg_out, "trkpt", attrib={"lat": lat, "lon": lng})

  save_gpx(gpx_out, output_file)

if __name__ == "__main__":
  main(sys.argv[1:])