import arcpy
import requests

time = 10
mode = 'cycling'

apiKey = 'pk.eyJ1IjoiZGVseW5rbyIsImEiOiJjam11MHY3dTcyc2g2M3FqcGxsOWltZzFpIn0.rfRlgDIEAX44AjnPjrYsjA'

fc = 'Q:\ForTesting\THsAcces.gdb\Trailheads_Access_InJeffco'
targetFc = r'Q:\ForTesting\THsAcces.gdb\Isos'

curs = arcpy.SearchCursor(fc, ['*'])

x = 1
for row in curs:
    lon = row.getValue("POINT_X")
    lat = row.getValue("POINT_Y")
    park = row.getValue("Park_Name")
    print(park)

    isoURL = 'https://api.mapbox.com/isochrone/v1/mapbox/{}/{},{}?contours_minutes={}&contours_colors=04e813&polygons=true&access_token={}'.format(mode, lon, lat, str(time), apiKey)

    r = requests.get(isoURL)
    polys = r.json()

    toArray = []

    for coord in polys["features"][0]["geometry"]["coordinates"][0]:

        toArray.append(arcpy.Point(coord[0], coord[1]))

    array = arcpy.Array(toArray)
    sr = arcpy.SpatialReference(4326)
    polygon = arcpy.Polygon(array, sr)

    arcpy.Append_management(polygon, targetFc, 'NO_TEST')

    fields = ["Park_Name", "Mode", "Time"]

    with arcpy.da.UpdateCursor(targetFc, fields) as upCurs:
        for r in upCurs:
            if r[0] == None:
                r[0] = park
                r[1] = mode
                r[2] = time
                upCurs.updateRow(r)
    print('{} done.'.format(str(x)))
    x += 1
