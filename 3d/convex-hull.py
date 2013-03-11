import Image, ImageDraw
from random import randint

CCW, STRAIGHT, CW = (1, 0, -1)
POINT_NUM = 10

POINTS_FILENAME = "points.png"
HULL_FILENAME = "convex-hull.png"

MAX_X=100
MAX_Y=100

class Plane(object):
    """The plane with the points.
    """

    def __init__(self, point_num=POINT_NUM, points=None, max_x=MAX_X, max_y = MAX_Y):
        """Generate a random number of points.
        """
        if points is None:
            self.points = [(randint(0,max_x), randint(0,max_y)) for i in range(point_num)]
        else:
            self.points = points

        self.min_p = min(self.points, key=lambda ((x,y)):y)

    def edges(self):
        for si,start in enumerate(self.points):
            for end in self.points[si+1:]:
                yield (start, end)

    def ccw(self, (p, q), r):
        return cmp((q[0] - p[0])*(r[1] - p[1]) - (r[0] - p[0])*(q[1] - p[1]), 0)

    def edge_in_hull(self, edge):
        """Test if edge is in hull."""
        side = STRAIGHT

        for i in self.points:
            if self.ccw(edge, i) in [side, STRAIGHT] or side == STRAIGHT:
                if side == STRAIGHT:
                    side = self.ccw(edge, i)
            else:
                return False

        return True

    def dumb_convex_hull(self):
        """Return an unsorted convex hull."""
        ret = set()
        for edge in self.edges():
            if self.edge_in_hull(edge):
                ret.update(edge)

        return list(ret)

    def angle_key(self, p):
        """Return the tangent of the vector to the lowest point."""
        x,y = tuple(map(lambda x1,x2:x1-x2, p, self.min_p)) # p - min_p

        if y == 0:
            return -float('Inf')

        return y/x

    def convex_hull(self):
        hull = self.dumb_convex_hull()
        return sorted(hull, key=self.angle_key)


class Visualize(object):
    """Show the object
    """

    def __init__(self, plane):
        """
        """
        self.plane = plane

    def add_point(self, coord, image):
        draw.point(coord)

    def points_image(self, image_filename=POINTS_FILENAME, image=None):
        """Draw points of plane on image."""

        if image is None:
            image = Image.open(image_filename, 0x777)

        draw = ImageDraw.Draw(image)
        draw.point(self.plane.points)

        return image

    def geometry(self):
        return max(self.plane.points, key=lambda (x,y): x)[0], max(self.plane.points, key=lambda (x,y): y)[1]

    def convex_hull_image(self, hull_filename=HULL_FILENAME, hull_image=None):
        if hull_image is None:
            hull_image = Image.new("RGB", self.geometry())

        draw = ImageDraw.Draw(hull_image)
        draw.polygon(self.plane.convex_hull())

        return hull_image


if __name__ == "__main__":
    p = Plane(10)
    s = Visualize(p)
    s.convex_hull_image().show()
