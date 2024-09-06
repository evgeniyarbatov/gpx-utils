# GPX Utils

One place for all scripts to extract useful data from GPX files.

### Setup 

```
python3 -m venv ~/.venv/gpx-utils
source ~/.venv/gpx-utils/bin/activate
pip install -r requirements.txt
```

### Scripts

Extract segment from GPX route given start and end coordinates:

```
source ~/.venv/gpx-utils/bin/activate &&
python get-segment.py \
1.309743979078668 \
103.89449080743935 \
1.2850818043059817 \
103.86170047918944 \
~/Downloads/SG200Miles2024.gpx \
~/Downloads/route.gpx
```

Convert KML to GPX:

```
python kml2gpx.py \
~/gitRepo/run-with-ben/data/Smash\ 80km.kml \
~/gitRepo/run-with-ben/data/Smash\ 80km.gpx
```
