import Image, ImageDraw
from random import randint

SLOW_ALGORITHM = False

CCW, STRAIGHT, CW = (1, 0, -1)
POINT_NUM = 10

IMAGE_PADDING = (10,10)

IMAGE_FILENAME = "hull.png"

POINT_COLOR = (255,0,0)
SHAPE_COLOR = (255, 255, 255)

MAX_X = 1000
MAX_Y = 500

def vadd(p,q):
    """Vector addition."""
    return tuple(map(lambda x1,x2:x1+x2, p, q))

def vsub(p,q):
    """Vector subtravtion."""
    return tuple(map(lambda x1,x2:x1-x2, p, q))

def vdot(p,q):
    return p[0]*q[0] + p[1]*q[1]

def vcross(p, q):
    """Cross product"""
    return p[0]*q[1] - p[1]*q[0]

def tarea(p1, p2, p3):
    """Area of p triangle. This may be used to compare distance point from
    line.

    """
    return vcross(vsub(p1,p2), vsub(p2,p3))


class Plane(object):
    """The plane with the points.
    """

    def __init__(self, point_num=POINT_NUM, points=None, max_x=MAX_X, max_y = MAX_Y):
        """Generate a random number of points. You may want to provide the
        points themselves too.

        """
        if points is None:
            self.points = [(randint(0,max_x), randint(0,max_y)) for i in range(point_num)]
        else:
            self.points = points

        self.min_p = max(self.points, key=lambda ((x,y)):y)

    def edges(self):
        """Generate all the edges one by one."""

        for si,start in enumerate(self.points):
            for end in self.points[si+1:]:
                yield (start, end)

    def ccw(self, (p,q), r):
        """Return the side of pq that r is found."""
        # CW, STRAIGHT or CCW
        return cmp(tarea(p,q,r),0)

    def edge_in_hull(self, edge):
        """Test if edge is in the convex hull."""
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

    def _qhull(self, min_p, max_p, candidates):
        """The qhull recursion. Return min_p + the candidates in the hull."""

        # Filter candidates to only the ones left from the line.
        candidates = filter(lambda q:tarea(min_p, max_p, q) > 0, candidates)

        if len(candidates) <= 1:
            return [min_p] + candidates

        # Find the furthest candidate
        new_p = max(candidates, key=lambda x:tarea(min_p, max_p, x))

        return self._qhull(min_p, new_p, candidates) + self._qhull(new_p, max_p, candidates)

    def quickhull(self):
        """The quickhull algorithm."""
        min_p = min(self.points)
        max_p = max(self.points)

        return self._qhull(min_p, max_p, self.points) + self._qhull(max_p, min_p, self.points)

    def dumb_convex_hull(self):
        """Return an unsorted convex hull. This is a slow and stupid
        bruteforcer.

        """
        ret = set()
        for edge in self.edges():
            if self.edge_in_hull(edge):
                ret.update(edge)

        return list(ret)

    def angle_key(self, p):
        """Return the tangent of the vector from the lowest point."""

        x,y = vsub(p, self.min_p) # p - min_p

        if x == 0:
            return 0

        return float(y)/float(x)

    def convex_hull(self, slow=SLOW_ALGORITHM):
        """This is the stable way to get the convex hull. You may want to do
        it really really slowly using the bruteforcer. Otherwise this
        uses quickhull.

        """
        if slow == True:
            hull = self.dumb_convex_hull()
            return sorted(hull, key=self.angle_key, reverse=True)

        return self.quickhull()


class VisualizePlane(object):
    """Show the object
    """

    def __init__(self, plane):
        """
        """
        self.plane = plane

    def add_point(self, coord, image):
        draw.point(coord)

    def points_image(self, points=None, image=None, color=POINT_COLOR):
        """Draw all the points on an image. """

        if image is None:
            image = Image.new("RGB", self.geometry())

        draw = ImageDraw.Draw(image)

        if points is None:
            points = self.plane.points

        draw.point(points, fill=color)

        return image

    def geometry(self, padding=IMAGE_PADDING):
        """Get the default geometry of the image at hand."""
        min_geo = max(self.plane.points, key=lambda (x,y): x)[0], max(self.plane.points, key=lambda (x,y): y)[1]

        return vadd(min_geo, padding)

    def hull_image(self, points=None, image=None, color=SHAPE_COLOR, slow=SLOW_ALGORITHM):
        """Show the image of th convex hull. This does not show the points.

        """
        if image is None:
            image = Image.new("RGB", self.geometry())

        if points is None:
            points = self.plane.convex_hull(slow)

        draw = ImageDraw.Draw(image)

        draw.polygon(points, fill=color)

        return image


if __name__ == "__main__":
    from sys import argv

    slow = False
    if "--slow" in argv:
        slow = True

    p = Plane( int(argv[1]) )
    s = VisualizePlane(p)

    hull_img = s.hull_image(slow=slow)
    s.points_image(image=hull_img)

    hull_img.show()
    hull_img.save(IMAGE_FILENAME)
