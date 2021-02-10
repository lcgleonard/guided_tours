from decimal import Decimal
from math import pi, sqrt, radians, sin, cos, acos


def get_distances_nsew_from_starting_point(starting_latitude, starting_longitude):
    """Get the distances north, south, east and west from a starting latitude and
    longitude based on a diff values.
    """

    # TODO: move the following to the config file
    diff_latitude = Decimal("0.5")
    diff_longitude = Decimal("0.5")

    distance_north = starting_longitude + diff_longitude
    distance_south = starting_longitude - diff_longitude
    distance_east = starting_latitude + diff_latitude
    distance_west = starting_latitude - diff_latitude

    return distance_north, distance_south, distance_east, distance_west


def calculate_distance(
    starting_latitude, starting_longitude, ending_latitude, ending_longitude
):
    """Calculate distance between starting and ending latitude and longitude"""
    starting_latitude = radians(starting_latitude)
    starting_longitude = radians(starting_longitude)
    ending_latitude = radians(ending_latitude)
    ending_longitude = radians(ending_longitude)

    # the following distance calculate is based on this piece of code:
    # https://www.w3resource.com/python-exercises/math/python-math-exercise-27.php
    distance = 6371.01 * acos(
        sin(starting_latitude) * sin(ending_latitude)
        + cos(starting_latitude)
        * cos(ending_latitude)
        * cos(starting_longitude - ending_longitude)
    )
    return distance


def check_coordinates_are_inside_given_km_radius(
    starting_latitude,
    starting_longitude,
    ending_latitude,
    ending_longitude,
    km_radius,
):
    """
    Notes:
    (1)  Longitude and latitude are not valid coordinates in relation to cartesian geometry
         (eg they are not of the form (x,y,z) etc...), as such there must be converted into cartesian format,
         where the centre of the earth is the origin (0, 0, 0).
    (2)  Longitude and latitude are converted directly into three dimensions and not two dimensions,
         as such two dimensional geometry such as lines, squares and circles are redundant and useless.
    (3)  In order to convert longitude and latitude into cartesian format we must first transform them
         from there standard degree format into a radian format,
         -> we express them in terms of pi so that the trigonometric functions used to convert to
            cartesian format are more computationally efficient
         -> doing trigonometric calculations using degrees is very messy
         -> the symbol for radians is rad and uses the irrational number pi which has many applications
            in circles, spheres and curvatures
    (4)  The euclidean distance is used in measuring the distance between the two points, this is at best
         an estimate of the distance and not a 100% accurate.  This is because the surface of the earth is
         curved and not straight.
            To obtain a more precise answer we would use arcs, but arcs are way more complex and cumbersome
         to compute as they involve integration and integral calculus.  However euclidean distance will provide
         very effective answers for two close points with little curvature in between,
         eg any two points lying in Ireland should be accurately calculated.
    (5)  The equation of a cube with radius r and centre (xa, ya, za) is:
            `max(abs(x - xa), abs(y - ya), abs(z - za)) = r`
    (6)  The equation of a sphere with radius r and centre (xa, ya, za) is:
            `(x - xa)**2 + (y - ya)**2 + (z - za)**2 = r*2`
    (7)  The euclidean distance between two points in three dimensions is:
            `sqrt((xb - xa)**2 + (yb - ya)**2 + (zb - za)**2)`
    (8)  r determines the size of our cube and sphere by specifying the radius of that cube and sphere.
         thus a cube and sphere with radius r has diameter 2*r
         hence if we want a cube and sphere with radius 100km we would specify r to 50km
    (9)  point a is our location and point b is the items location
    (10) the earth is not a perfect sphere
    (11) the earth has an expected radius of 6371km, which is where the 6371 comes from in the
         conversion to cartesian space formulas

    References:
        http://papers.cumincad.org/data/works/att/a38d.content.03652.pdf

    """

    # convert to radians
    starting_latitude = radians(starting_latitude)
    starting_longitude = radians(starting_longitude)
    ending_latitude = radians(ending_latitude)
    ending_longitude = radians(ending_longitude)

    # convert to 3D cartesian coordinates
    starting_point_x = 6371 * cos(starting_longitude) * cos(starting_latitude)
    starting_point_y = 6371 * sin(starting_longitude) * cos(starting_latitude)
    starting_point_z = 6371 * sin(starting_latitude)

    ending_point_x = 6371 * cos(ending_longitude) * cos(ending_latitude)
    ending_point_y = 6371 * sin(ending_longitude) * cos(ending_latitude)
    ending_point_z = 6371 * sin(ending_latitude)

    # construction of the cube with
    # centre point a = (starting_point_a, starting_point_y, starting_point_z) and radius r
    if (
        max(
            abs(ending_point_x - starting_point_x),
            abs(ending_point_y - starting_point_y),
            abs(ending_point_z - starting_point_z),
        )
        <= km_radius
    ):

        # construction of the sphere with
        # centre point a = (starting_point_a, starting_point_y, starting_point_z) and radius r
        if (
            (ending_point_x - starting_point_x) ** 2
            + (ending_point_y - starting_point_y) ** 2
            + (ending_point_z - starting_point_z) ** 2
        ) <= km_radius ** 2:
            # Inside the sphere.
            return True
        else:
            # Outside the sphere.
            return False
    else:
        # Outside the cube.
        return False
