# planet-movement
The `movement.py` Python module enables the searching and processing of [Planet](https://www.planet.com/) imagery to highlight object movement between valid image pairs. Included are functions for filtering Planet API search results to identify image pairs, and for processing images into visual outputs.

## Methodology
Change detection algorithms are commonly used in remote sensing imagery analysis to help identify the differences between two images collected over the same geographic area at different times.

Until recently, the shortest time difference between comparable images for a given geographic area could range from days to weeks due to the limited frequency of satellite collections over the area. This has changed with Planet's constellation of small satellites which image the entire earth every day, making daily change detection now possible for most of the globe.

Additionally, Planet's collection strategy provides an unique opportunity for change detection on a much shorter time scale. Image frames collected during each satellite flight scan contain a small amount of geographic overlap with the previous frame in the scan. Frames are collected only less than two seconds apart, so a comparison of these overlapping regions makes rapid change detection possible. 

<p>
<img src="https://imgur.com/ns5hbzy.png" width="100%">
</p>

On this short time scale, any differences observed in the image regions are largely due to the physical displacement of objects on the ground due to their movement. The `movement.py` module can be used to search and process these overlapping image pairs to highlight this change.

## Setup
```bash
# Clone this repository
git clone https://github.com/rhammell/planet-movement.git

# Go into the repository
cd planet-movement

# Install required modules
pip install -r requirements.txt
```
