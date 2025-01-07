import math
import numpy as np

from scipy.cluster.vq import kmeans2

FORTY_FIVE_DEGREES = math.pi / 4
RADIUS_EARTH = 6_378_000

def center_to_bounding_box(center_lat: float, center_lon: float, radius: int) -> tuple[tuple[float, float], tuple[float, float]]:
    '''
        Takes in a center point `(center_lat, center_lon)` and `radius` and returns
        a tuple `(northwest_coordinate, southeast_coordinate)` where the two coordinates
        are of the form `(lat, lon)` and correspond to their respective corners of the
        inscribed square within the circle formed by the center point and radius.

        https://stackoverflow.com/a/7478827
    '''


    x_offset = radius * math.cos(FORTY_FIVE_DEGREES)
    y_offset = radius * math.sin(FORTY_FIVE_DEGREES)

    northwest_lat = center_lat + ((y_offset / RADIUS_EARTH) * (180 / math.pi))
    northwest_lon = center_lon - ((x_offset / RADIUS_EARTH) * (180 / math.pi) / (math.cos(center_lon * (math.pi / 180))))

    southeast_lat = center_lat - ((y_offset / RADIUS_EARTH) * (180 / math.pi))
    southeast_lon = center_lon + ((x_offset / RADIUS_EARTH) * (180 / math.pi) / (math.cos(center_lon * (math.pi / 180))))

    return (
        (northwest_lat, northwest_lon),
        (southeast_lat, southeast_lon)
    )

def bounding_box_to_str(bounding_box: tuple[tuple[float, float], tuple[float, float]]):
    '''
        Converts a bounding box of the form `((NW_LAT, NW_LON), (SE_LAT, SE_LON))` to a string of form `'S_LAT,W_LON,N_LAT,E_LON'`
        in order to accomodate the [Overpass Bounding Box convention](https://dev.overpass-api.de/overpass-doc/en/full_data/bbox.html).
    '''

    ((nw_lat, nw_lon), (se_lat,se_lon)) = bounding_box

    return f'{se_lat},{nw_lon},{nw_lat},{se_lon}'

def cluster_points(points: list[tuple[float, float]], num_clusters: int):
    observations = np.array([
        np.array(point) for point in points
    ])

    _,label = kmeans2(observations, num_clusters)

    return [
        [(float(lat),float(lon)) for (lat,lon) in observations[label == i]] for i in range(num_clusters) if len(observations[label == i]) > 0
    ]

