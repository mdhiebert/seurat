import simplekml

def output_to_kml(clusters: list[list[tuple[float, float]]], output_file = 'output.kml'):
    '''
        TODO
    '''

    kml = simplekml.Kml()

    color_palette = [
        (simplekml.Color.red, 'RED'),
        (simplekml.Color.orange, 'ORANGE'),
        (simplekml.Color.yellow, 'YELLOW'),
        (simplekml.Color.green, 'GREEN'),
        (simplekml.Color.blue, 'BLUE'),
        (simplekml.Color.indigo, 'INDIGO'),
        (simplekml.Color.violet, 'VIOLET'),

        (simplekml.Color.orangered, 'ORANGE-RED'),
        (simplekml.Color.greenyellow, 'GREEN-YELLOW'),
        (simplekml.Color.blueviolet, 'BLUE-VIOLET'),
        
        (simplekml.Color.azure, 'AZURE'),
        (simplekml.Color.aliceblue, 'ALICE'),
        (simplekml.Color.aquamarine, 'AQUAMARINE'),
        (simplekml.Color.brown, 'BROWN'),
        (simplekml.Color.cadetblue, 'CADET'),
        (simplekml.Color.chartreuse, 'CHARTREUSE'),
        (simplekml.Color.coral, 'CORAL')
    ]

    if len(clusters) > 7:
        print('Warning: Using more than just the colors of the rainbow to match all clusters. Adjust your cluster tolerance value to avoid similar colors.')
    elif len(clusters) > 10:
        print('Warning: Using more than primary and secondary colors of the rainbow to match all clusters. Adjust your cluster tolerance value to avoid similar colors.')
    elif len(clusters) > len(color_palette):
        print('Not enough colors to appropriately color all clusters. Re-run with a higher cluster tolerance.')
        return

    for ((color, color_label), cluster) in zip(color_palette[:len(clusters)], clusters):
        style = simplekml.Style()
        style.polystyle.color = color
        style.labelstyle.color = color
        style.labelstyle.scale = 1

        style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
        style.iconstyle.color = color

        for i,(lat, lon) in enumerate(cluster):
            pnt = kml.newpoint(name = f'{i}')
            pnt.coords = [(lon,lat)]
            pnt.style = style
    
    kml.save(output_file)