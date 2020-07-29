from rlutilities.linear_algebra import vec3
from rlutilities.linear_algebra import angle_between

from math import pi
from math import atan2

def main(vecs):
    t1 = vec3(620, -117, 0)
    t2 = vec3(-155, 360, 0)

    car_dir = vecs[0]
    car_pos = vecs[1]
    ball_pos = vecs[2]
    car_to_ball = ball_pos - car_pos
    print(car_to_ball)
    real = atan2(car_to_ball[1], car_to_ball[0]) * 180 / pi
    rot = atan2(car_dir[1], car_dir[0]) * 180 / pi

    angle = real - rot
    text = "car dir: {}, car to ball: {}, diff = {}, other diff = {}".format(rot, real, rot - real, real - rot)
    print(text)
    steering_angle = steeringMagic(angle)
    print(steering_angle)



def steeringMagic(angle):
    drift_angle = 37
    if angle > 180:
        angle = 360 - angle
    elif angle < -180:
        angle = -360 - angle
    print("corrected angle: {}".format(angle))
    if angle > drift_angle:
        angle = drift_angle - (angle * 37 / 180)
    elif angle < -drift_angle:
        angle = -drift_angle + (angle * 37 / 180)
    return angle

a = [vec3(-5, 10, 0), vec3(-10, -10, 0), vec3(-10, -20, 0)]
b = [vec3(620, -117, 0), vec3(10, 400, 0), vec3(-155, 360, 0)]
c = [vec3(-556, -1178, 0), vec3(3977, 3552, 0), vec3(2439, 3845, 0)]

main(a)
main(b)
main(c)