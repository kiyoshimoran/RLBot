from rlbot.utils.rendering.rendering_manager import RenderingManager
from rlbot.utils.rendering.rendering_manager import Color
from rlbot.utils.structures.game_data_struct import Vector3
from rlbot.utils.structures.struct import Struct
from util.vec import Vec3

from math import pi 
from math import cos
from math import sin

class DrawingTool():
    artist: RenderingManager
    def __init__(self, artist : RenderingManager):
        self.artist = artist


    def draw_circle(self, center, size=25, num_points=60):
        points = []
        x = center[0]
        y = center[1]
        dt = 2 * pi / num_points
        for i in range(num_points):
            points.append((x + cos(i * dt), y + sin(i * dt), 10) * size)

        points.append(points[0])
        top = center + Vec3(0, 0, 200)
        self.artist.begin_rendering("circle")
        self.artist.draw_polyline_3d(points, self.artist.green())
        self.artist.draw_line_3d(center, top, self.artist.white())
        self.artist.end_rendering()


    def draw_path(self, points):
        color = self.artist.red()
        self.artist.begin_rendering("path")
        self.artist.draw_polyline_3d(points, color)
        self.artist.end_rendering()

    def draw_challenge_loc(self, loc):
        self.draw_circle(loc)