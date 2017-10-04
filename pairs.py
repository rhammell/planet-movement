import dateutil.parser
from shapely.geometry import Polygon
from planet import api

def is_pair(item_1, item_2):
    """ Determine if two Planet Items are a pair

    Valid pairs have equal satellite id's, equal strip id's, 
    equal provider values, acquired times less than two seconds apart, and 
    geometry polyons that intersect. 

    Args:
        item_1 (dict): Planet API Item reference
        item_2 (dict): Planet API Item reference
    """

    # Item properties
    props_1 = item_1['properties']
    props_2 = item_2['properties']
    if (props_1['satellite_id'] != props_2['satellite_id'] or  
       props_1['strip_id'] != props_2['strip_id'] or  
       props_1['provider'] != props_2['provider']):
        return False

    # Time difference
    t1 = dateutil.parser.parse(props_1['acquired'])
    t2 = dateutil.parser.parse(props_2['acquired'])
    t_diff = abs(t1 - t2).total_seconds()
    if t_diff > 2: 
        return False

    # Geometry intersection
    geom_1 = item_1['geometry']
    geom_2 = item_2['geometry']
    if (geom_1['type'] != 'Polygon' or 
        geom_2['type'] != 'Polygon'):
            return False
    poly_1 = Polygon(geom_1['coordinates'][0])
    poly_2 = Polygon(geom_2['coordinates'][0])
    if poly_1.intersects(poly_2):
        return True


def find_pairs(items):
    """ Return list of Planet Item pairs that

    Operates on the result returned from a Planet API search and returns a list 
    of tuples containing pairs of Planet Item references

    Args:
        items(planet.api.models.Items): Planet API search result 
    """

    # Set initial output
    pairs = []

    # List all items
    all_items = [item for item in items.items_iter(None)]

    # Find item pairs
    if len(all_items) > 1: 
        for i, item_1 in enumerate(all_items[:-1]):
            for item_2 in all_items[i+1:]:
                if is_pair(item_1, item_2):
                    pairs.append((item_1, item_2))

    return pairs


if __name__ == '__main__':
    """ Demo code using find_pair() function """

    # Client
    client = api.ClientV1()

    # Sample AOI
    aoi = {
      "type": "Polygon",
      "coordinates": [
        [
          [-122.54, 37.81],
          [-122.38, 37.84],
          [-122.35, 37.71],
          [-122.53, 37.70],
          [-122.54, 37.81]
        ]
      ]
    }

    # Build request
    query = api.filters.and_filter(
      api.filters.geom_filter(aoi)
    )
    item_types = ['PSScene3Band']
    request = api.filters.build_search_request(query, item_types)

    # Quick search
    print("Searching...")
    results = client.quick_search(request)
    print("Images found: ", len([item for item in results.items_iter(None)]))

    # Use search results as input into find_pairs() function
    print('Finding pairs...')
    pairs = find_pairs(results)
    for pair in pairs:
        print(pair[0]['id'], pair[1]['id'])
    print('Pairs found: ', len(pairs))