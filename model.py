import irit


def create_point(x, y, z):
    ctlpt = irit.ctlpt(irit.E3, x, y, z)
    irit.interact(ctlpt)
    return 


def create_ctlpt_list(points):
    return irit.list(*[create_point(point[0], point[1], point[2]) for point in points])


def create_curve(points):
    ctlpts_list = create_ctlpt_list(points)
    crv = irit.cbspline(3, ctlpts_list, irit.list(irit.KV_OPEN))
    return crv


def update_viz(data):
    irit.interact(data)



def main():
    for i in range(1, 10, 1):
        spline = create_curve([(0, 0, 0), (0.5, float(i), 0.5), (1, 1, 1)])
        update_viz(spline)


if __name__ == '__main__':
    main()