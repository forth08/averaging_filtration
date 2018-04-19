import matplotlib.pyplot as plt
import numpy as np
import matplotlib.tri as tri
import matplotlib

def delaunay_edges(x, y):
    # Create Delaunay triangulation and return all edges

    triang = tri.Triangulation(x, y)
    edges = triang.edges
    return edges

def edges_of_points(edges):
    # Find all neighbors points for points

    n_edges = edges.shape[0]
    n_points = np.max(edges)
    pointS_edges = []
    print('Number of points: ', n_points)

    for i in range(n_points + 1):
        point_edges = []

        for k in range(n_edges):
            if edges[k,0] == i:
                point_edges.append(edges[k,1])

        for k in range(n_edges):
            if edges[k,1] == i:
                point_edges.append(edges[k, 0])

        pointS_edges.append(np.array(point_edges))
        show_percent = i % (n_points//10) == 0
        if show_percent:
           print('Calculate -', str(i * 100 // n_points + 1), '%')

    return np.array(pointS_edges)

def calculate_distances(x, y, edges_of_points):
    # Calculate distances for all neighbours points

    n_points = edges_of_points.size
    distances = []
    for i in range(n_points):
        neighbours = edges_of_points[i]
        point_distances = []
        for k in neighbours:
            dx = x[i] - x[k]
            dy = y[i] - y[k]
            r = (dx ** 2 + dy ** 2) ** .5
            point_distances.append(r)
        distances.append(np.array(point_distances))
    return np.array(distances)

def average_filtration(h, edges_of_points, distances):
    # Average filtration for 3D cloud points

    n_points = h.size
    h_average = []
    weights = 1 / distances
    error_points = 0

    for i in range(n_points):
        try:
            i_heights = h[edges_of_points[i]]
            i_weights = weights[i]
            kernel = i_heights * i_weights
            h_filtered = kernel.sum()
            h_filtered = h_filtered / i_weights.sum()
            h_average.append(h_filtered)
        except BaseException:
            error_points += 1
            h_average.append(h[i])
            print("----- Warning! Can't calculate height of point №", i, '-----')

    print('Number of no colculated heights of points is :', error_points)

    return h_average

def vv(h, h_average):
    vv = (h - h_average) ** 2
    print('Number of points is ', str(h.size))
    return vv, vv.sum()/h.size

def open_XYH_file(file):
    # Open txt file and convert from string to float

    text_file = open(file, 'r', encoding='utf-8')
    xyh = text_file.read()

    x_yh = np.array(xyh.split('\n'))

    x_y_h_string = []
    for i in range(x_yh.size):
        x_y_h_string.append(x_yh[i].split(' '))
    x_y_h = []

    for i in range(x_yh.size):
        x_y_h_1point = []
        for k in range(3):
            x_y_h_1point.append(float(x_y_h_string[i][k]))
        x_y_h.append(x_y_h_1point)

    text_file.close()

    x_y_h = np.array(x_y_h)
    x = x_y_h[:, 0]
    y = x_y_h[:, 1]
    h = x_y_h[:, 2]
    return x, y, h

def plotting(x, y, h, h_filtered, pvv, sum_pvv):

    plt.figure()

    plt.subplot(311)
    cmap = plt.cm.rainbow
    rounding = 1000
    step = (h.max() - h.min()) / 10
    step = round(step * rounding) / rounding
    min_round = round(h.min() * rounding) / rounding
    max_round = round(h.max() * rounding) / rounding
    points_size = 10

    norm = matplotlib.colors.BoundaryNorm(np.arange(min_round, max_round, step), cmap.N)
    plt.scatter(x, y, c=h, cmap=cmap, norm=norm, s=points_size, edgecolor='none')
    plt.colorbar(ticks=np.linspace(h.min(), h.max(), 10))
    plt.title('Original 3D Cloud')

    plt.subplot(312)
    plt.scatter(x, y, c=h_filtered, cmap=cmap, norm=norm, s=points_size, edgecolor='none', )
    plt.colorbar(ticks=np.linspace(h.min(), h.max(), 10))
    plt.title('FIltered 3D Cloud')

    plt.subplot(313)
    cmap = plt.cm.rainbow
    norm = matplotlib.colors.BoundaryNorm(np.arange(pvv.min(), pvv.max(), (pvv.max() - pvv.min()) / 10), cmap.N)
    plt.scatter(x, y, c=pvv, cmap=cmap, norm=norm, s=points_size, edgecolor='none') # 50 - is a scaling for good viewing
    plt.colorbar(ticks=np.linspace(pvv.min(), pvv.max(), 10))
    title = '[PVV]=' + str(sum_pvv)
    plt.title(title)
    plt.show()
