import Image, ImageDraw
from random import randint

CCW, STRAIGHT, CW = (1, 0, -1)
POINT_NUM = 10

POINTS_FILENAME = "points.png"
HULL_FILENAME = "convex-hull.png"

IMAGE_PADDING = (10,10)

POINT_COLOR = (255,0,0)

MAX_X = 1000
MAX_Y = 500

def vsub(p,q):
    return tuple(map(lambda x1,x2:x1-x2, p, q))

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

        self.min_p = max(self.points, key=lambda ((x,y)):y)

    def edges(self):
        for si,start in enumerate(self.points):
            for end in self.points[si+1:]:
                yield (start, end)

    def ccw(self, (p,q), r):
        """Return the side of pq that r is found."""
        x1, y1 = vsub(p, q)
        x2, y2 = vsub(p, r)
        return cmp(x1*y2 - x2*y1,0)

    def edge_in_hull(self, edge):
        """Test if edge is in hull."""
        side = STRAIGHT

        for i in self.points:
            # If on the correct side or straight or if the side is not determined
            if self.ccw(edge, i) in [side, STRAIGHT] or side == STRAIGHT:
                # Update side if not locked
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
        x,y = vsub(p, self.min_p) # p - min_p

        if x == 0:
            return 0

        return float(y)/float(x)

    def convex_hull(self):
        """This is the stable way to get the convex hull."""
        hull = self.dumb_convex_hull()
        print "Sorting %d points" % len(hull)
        return sorted(hull, key=self.angle_key, reverse=True)


class Visualize(object):
    """Show the object
    """

    def __init__(self, plane):
        """
        """
        self.plane = plane

    def add_point(self, coord, image):
        draw.point(coord)

    def points_image(self, image_filename=POINTS_FILENAME, image=None, color=POINT_COLOR):
        """Draw points of plane on image."""

        if image is None:
            image = Image.new("RGB", self.geometry())

        draw = ImageDraw.Draw(image)
        draw.point(self.plane.points, fill=color)

        return image

    def geometry(self, padding=IMAGE_PADDING):
        min_geo = max(self.plane.points, key=lambda (x,y): x)[0], max(self.plane.points, key=lambda (x,y): y)[1]

        return tuple(map(lambda x,y:x+y,min_geo, padding))

    def convex_hull_image(self, hull_filename=HULL_FILENAME, image=None):
        if image is None:
            image = Image.new("RGB", self.geometry())

        draw = ImageDraw.Draw(image)

        chull = self.plane.convex_hull()

        draw.polygon(chull)

        return image


if __name__ == "__main__":
    from sys import argv

    p = Plane( int(argv[1]) )
    s = Visualize(p)
    points = s.points_image()
    hull = s.convex_hull_image(image=points)
    points.show()
