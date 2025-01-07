import argparse

from seurat.overpass import get_intersections_for_bbox
from seurat.geo import cluster_points
from seurat.map import output_to_kml

parser = argparse.ArgumentParser(
    prog = 'seurat',
    description = 'simple tool to generate dot-maps',
    epilog = 'ex. python seurat.py 40.768402 -73.968350 40.761245 -73.961197 -n 2 -o nyc.kml'
)

parser.add_argument('north_latitude', type = float)
parser.add_argument('west_longitude', type = float)
parser.add_argument('south_latitude', type = float)
parser.add_argument('east_longitude', type = float)

parser.add_argument('-n', '--num_clusters', type = int, default = 7)

parser.add_argument('-o', '--output', default = 'output.kml')

args = parser.parse_args()

bounding_box = (
    (args.north_latitude, args.west_longitude),
    (args.south_latitude, args.east_longitude)
)

intersections = get_intersections_for_bbox(*bounding_box)
clusters = cluster_points(intersections, args.num_clusters)
output_to_kml(clusters, args.output)