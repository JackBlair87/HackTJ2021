from shapely.geometry import Polygon, Point


polygon = Polygon([(0, 0), (1, 0), (1, 1), (0,1)])


print(polygon.distance(Point(2, 2)))

print(len(list(polygon.exterior.coords)))
print(polygon.geom_type)