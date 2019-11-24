
def find_zero_points(func):
    zero_points = []
    for line in func.parameters['lines']:
        for x, y in zip(line.get_xdata(), line.get_ydata()):
            if y == 0:
                zero_points.append((x, y))
    return zero_points
