
from vispy import app
from vispy import gloo

import shaders
from Surface import Surface
from Sun import Sun


class Canvas(app.Canvas):

    def __init__(self, size=(600, 600)):
        # app window dimensions
        self.width = size[0]
        self.height = size[1]

        # initial time to count heights of points
        self.time = 0

        app.Canvas.__init__(self, size=(self.width, self.height), title='Water surface simulator')

        gloo.set_state(clear_color=(0, 0, 0, 1), depth_test=True, blend=False)

        self.surface = Surface()
        self.triangles = gloo.IndexBuffer(self.surface.triangulation())
        self.sun = Sun()
        self.are_points_visible = False

        self.program = gloo.Program(shaders.vert_shader, shaders.frag_shader_triangle)
        self.program['a_position'] = self.surface.position()
        self.program['u_sun_color'] = self.sun.color
        self.program['u_ambient_color'] = Surface.ambient_color()
        self.program['u_sun_direction'] = self.sun.direction(self.time)

        self.program_point = gloo.Program(shaders.vert_shader, shaders.frag_shader_point)
        self.program_point["a_position"] = self.surface.position()

        self.timer = app.Timer('auto', connect=self.on_timer, start=True)
        self.activate_zoom()
        self.show()

    def activate_zoom(self):
        self.width, self.height = self.size
        gloo.set_viewport(0, 0, *self.physical_size)

    def on_draw(self, event):
        gloo.set_state(clear_color=(0, 0, 0, 1), blend=False)
        gloo.clear()
        height = self.surface.height(self.time)
        self.program['a_height'] = height
        self.program['a_normal'] = self.surface.normal(self.time)

        # draw triangles
        gloo.set_state(depth_test=True)
        self.program.draw('triangles', self.triangles)

        # get glares
        if self.are_points_visible:
            self.program_point['a_height'] = height
            gloo.set_state(depth_test=False)
            self.program_point.draw('points')

    def on_timer(self, event):
        self.time += 0.01
        self.program['u_sun_direction'] = self.sun.direction(self.time)
        # calls on_draw
        self.update()

    def on_resize(self, event):
        self.activate_zoom()
