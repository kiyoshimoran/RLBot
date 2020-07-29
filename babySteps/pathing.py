import math

'''
given location, current vector, and destination returns opimal path and time
max throttle speed is 1410 
velocity vs acc described by line: (0, 1600) to (1400, 160)
boost gives 991.67 uu/s**2 acceleration
kmax v(s) = k(s)

velocity vs curvature (no drift):
    0       0.0069
    500     0.00398
    1000    0.00235
    1500    0.001375
    1750    0.0011
    2300    0.00088
'''
def opt_path(self, loc):
    curvature = 1/r
    best_time = min(turn + straight)
