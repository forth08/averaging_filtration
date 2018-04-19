import averaging_filtration as af

print('Open txt file of XYH')
x,y,h = af.open_XYH_file('test2.txt')

print('Create edges')
edges = af.delaunay_edges(x, y)

print('Finding neighbours points')
points = af.edges_of_points(edges)

print('Calculate distances')
distances = af.calculate_distances(x, y, points)

print('Filtration')
h_filtered = af.average_filtration(h, points, distances)

print('Calculate PVV')
pvv, sum_pvv = af.vv(h, h_filtered)

print('Plotting')
af.plotting(x, y, h, h_filtered, pvv, sum_pvv)
