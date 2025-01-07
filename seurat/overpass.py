from seurat.geo import center_to_bounding_box, bounding_box_to_str

import overpy

def get_intersections_in_radius(center_lat: float, center_lon: float, radius: int):
    '''
        Returns all intersections within `radius` meters of a given coordinate `(center_lat, center_lon)`
        in the form of a list of tuple `(lat, lon)` for each intersection.

        [Source to OverpassQL Query](https://stackoverflow.com/a/77239570)
    '''

    bbox_str = bounding_box_to_str(center_to_bounding_box(center_lat, center_lon, radius))

    return get_intersections_for_bbox_str(bbox_str)

def get_intersections_for_bbox(northwest_coordinate: tuple[float, float], southeast_coordinate: tuple[float, float]):
    return get_intersections_for_bbox_str(bounding_box_to_str((northwest_coordinate, southeast_coordinate)))

def get_intersections_for_bbox_str(bbox_str: str):

    query = f'''[out:json][timeout:25][bbox:{bbox_str}];

                // The public street network
                way["highway"~"^(trunk|primary|secondary|tertiary|unclassified|residential)$"]->.streets;

                // Get nodes that connect between three or more street segments
                node(way_link.streets:3-)->.connections;

                // Get intersections between distinct streets
                foreach .connections->.connection(
                // Get adjacent streets
                way(bn.connection);
                // If the names don't all match, add the node to the set of intersections
                if (u(t["name"]) == "< multiple values found >")''' + '''{
                    (.connection; .intersections;)->.intersections;
                }
                );

                .intersections out geom;
            '''

    api = overpy.Overpass()
    result = api.query(query)

    return [
        (float(node.lat), float(node.lon)) for node in result.nodes
    ]