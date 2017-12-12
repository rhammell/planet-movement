# planet-movement
The `movement.py` Python module enables the searching and processing of [Planet](https://www.planet.com/) imagery to highlight object movement between valid image pairs. Included are functions for filtering Planet API search results to identify image pairs, and for processing images into visual outputs.

## Methodology
Change detection algorithms are commonly used in remote sensing imagery analysis to help identify the differences between two images collected over the same geographic area at different times. 

Planet's constellation of small satellites is able to image the earth every day, making daily change detection possible for most of the globe. This collection strategy also provides an unique opportunity for change detection on a much shorter time scale. 

Image frames collected during each satellite flight scan contain a small amount of geographic overlap with the previous frame in the scan. Frames are collected less than two seconds apart, so a comparison of these overlapping regions makes rapid change detection possible. 

An example of this overlap between Time 1 and Time 2 images is shown below. 

<img src="https://imgur.com/ns5hbzy.png" width="100%">

On this short time scale, any differences observed in this overlap are largely due to the physical displacement of moving objects on the groud. The `movement.py` module can be used to search and process these overlapping image pairs to highlight this change.

## Examples
<p>
  <img src="https://imgur.com/K8Ogqvn.png" width="450px">
  <img src="https://imgur.com/BlQWuIL.png" width="450px">
  <img src="https://imgur.com/vplmgbD.png" width="450px">
  <img src="https://imgur.com/dHozIUB.png" width="450px">
</p>

## Setup
```bash
# Clone this repository
git clone https://github.com/rhammell/planet-movement.git

# Go into the repository
cd planet-movement

# Install required modules
pip install -r requirements.txt
```

## Image Pairs
Images are determined to be a valid pair if they have:
1. Equal `satellite_id` values
2. Equal `strip_id` values
3. Difference in `acquired` values less than 2
4. Overlapping image geometry

The `find_pairs()` function filters Planet API search results to return a list of image pairs. Each pair is contained in a two element tuple, where each image is represented as a Planet API image reference. 

An example of filtering  
```python
# Python 3
from planet import api
import movement

# Planet API client
client = api.ClientV1()

# Point of interest
poi = {
  "type": "Point",
  "coordinates": [-122.38640785217285, 37.61647504351534]
}

# Geometry filter
query = api.filters.and_filter(
  api.filters.geom_filter(poi)
)

# Build search request
item_types = ['PSScene3Band']
request = api.filters.build_search_request(query, item_types)

# Perform quick search
results = client.quick_search(request)

# Find image pairs within search results
pairs = movement.find_pairs(results)
print('Pairs found: ', len(pairs))
for pair in pairs:
    print(pair[0]['id'], pair[1]['id'])
```

Results from this filtering can be downloaded using standard Planet API methods. 

```python
from planet.api import downloader

# Planet API Downloader
dl = downloader.create(client)

# Download first pair
dl.download(iter(pairs[0]), ["visual"], r"C:/destination/folder")
```

## Processing
The `process_pairs()` function takes pairs of images to 
