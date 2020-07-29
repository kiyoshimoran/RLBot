from rlutilities.linear_algebra import vec3
from math import sqrt
from numpy.linalg import norm

def normalize(vec : vec3) -> float:
	return sqrt(vec.x ** 2 + vec.y ** 2 + vec.z ** 2)

def distance(loc1 : vec3, loc2 : vec3) -> float:
	new = vec3(loc2.x - loc1.x, loc2.y - loc1.y, loc2.z - loc1.z)
    return new.length()

