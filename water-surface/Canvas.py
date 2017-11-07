
from vispy import app
from vispy import gloo
from vispy import io
import numpy as np

import shaders
from surface.Sun import Sun
from surface.Bed import Bed


class Canvas(app.Canvas):

    def __init__(self, surface, sky="img\clouds.png", bed="img\seabed.png", size=(600, 600)):
        # app window dimensions
        self.width = size[0]
        self.height = size[1]

        # initial time to count heights of points
        self.time = 0

        app.Canvas.__init__(self, size=(self.width, self.height), title='Circular Waves Surface Simulator')

        self.surface = surface
        self.sky = io.read_png(sky)
        self.bed = io.read_png(bed)
        self.triangles = gloo.IndexBuffer(self.surface.triangulation())
        self.sun = Sun(np.asarray([0, 1, 0.1], dtype=np.float32))
        self.bed_resolver = Bed()

        position = self.surface.position()

        self.program = gloo.Program(shaders.vert_shader, shaders.frag_shader_triangle)
        self.program['a_position'] = position
        self.program['u_sky_texture'] = gloo.Texture2D(self.sky, wrapping='repeat', interpolation='linear')
        self.program['u_bed_texture'] = gloo.Texture2D(self.bed, wrapping='repeat', interpolation='linear')
        self.program['u_eye_height'] = 3
        self.program['u_alpha'] = 0.9
    #    self.program['u_bed_depth'] = 1
        self.program["a_bed_depth"] = self.bed_resolver.bed_depths("beach")
        self.program['u_sun_direction'] = self.sun.normalized_direction()
        self.program['u_sun_diffused_color'] = self.sun.diffused_color()
        self.program['u_sun_reflected_color'] = self.sun.reflected_color()

        self.program_point = gloo.Program(shaders.vert_shader, shaders.frag_shader_point)
        self.program_point['a_position'] = position
        self.program_point['u_eye_height'] = 3

        # GUI set up
        self.camera = np.array([0, 0, 1])
        self.up = np.array([0, 1, 0])
        self.set_camera()

        self.are_points_visible = False
        self.drag_start = None
        self.diffused_flag = True
        self.reflected_flag = True
        self.bed_flag = True
        self.depth_flag = True
        self.sky_flag = True
        self.bed_type = "beach"
        self.stop_flag = False
        self.apply_flags()

        self.timer = app.Timer('auto', connect=self.on_timer, start=True)
        self.activate_zoom()
        self.show()

    def set_camera(self):
        rotation = np.zeros((4, 4), dtype=np.float32)
        rotation[3, 3] = 1
        rotation[0, :3] = np.cross(self.up, self.camera)
        rotation[1, :3] = self.up
        rotation[2, :3] = self.camera
        world_view = rotation
        self.program['u_world_view'] = world_view.T
        self.program_point['u_world_view'] = world_view.T

    def rotate_camera(self, shift):
        right = np.cross(self.up, self.camera)
        new_camera = self.camera - right * shift[0] + self.up * shift[1]
        new_up = self.up - self.camera * shift[0]
        self.camera = Canvas.normalize(new_camera)
        self.up = Canvas.normalize(new_up)
        self.up = np.cross(self.camera, np.cross(self.up, self.camera))

    def apply_flags(self):
        self.program["u_diffused_mult"] = 0.5 if self.diffused_flag else 0
        self.program["u_reflected_mult"] = 1.0 if self.reflected_flag else 0
        self.program["u_bed_mult"] = 1 if self.bed_flag else 0
        self.program["u_depth_mult"] = 1 if self.depth_flag else 0
        self.program["u_sky_mult"] = 1 if self.sky_flag else 0
        self.program["a_bed_depth"] = self.bed_resolver.bed_depths(self.bed_type)

    def activate_zoom(self):
        self.width, self.height = self.size
        gloo.set_viewport(0, 0, *self.physical_size)

    def on_draw(self, event):
        gloo.set_state(clear_color=(0, 0, 0, 1), blend=False)
        gloo.clear()
        height = self.surface.height(self.time)
        normal = self.surface.normal(self.time)
        self.program['a_height'] = height
        self.program['a_normal'] = normal

        # draw triangles
        gloo.set_state(depth_test=True)
        self.program.draw('triangles', self.triangles)

        # draw points
        if self.are_points_visible:
            self.program_point['a_height'] = height
            gloo.set_state(depth_test=False)
            self.program_point.draw('points')

    def on_timer(self, event):
        if not self.stop_flag:
            self.time += 0.01
            # calls on_draw
            self.update()

    def on_resize(self, event):
        self.activate_zoom()

    def on_key_press(self, event):
        if event.key == 'Escape':
            self.close()

        elif event.key == ' ':
            self.are_points_visible = not self.are_points_visible
            print("Show lattice vertices:", self.are_points_visible)

        elif event.key == '1':
            self.diffused_flag = not self.diffused_flag
            print("Show sun diffused light:", self.diffused_flag)
            self.apply_flags()

        elif event.key == '2':
            self.bed_flag = not self.bed_flag
            print("Show refracted image of seabed:", self.bed_flag)

        elif event.key == '3':
            self.depth_flag = not self.depth_flag
            print("Show ambient light in water:", self.depth_flag)

        elif event.key == '4':
            self.sky_flag = not self.sky_flag
            print("Show reflected image of sky:", self.sky_flag)

        elif event.key == '5':
            self.reflected_flag = not self.reflected_flag
            print("Show reflected image of sun:", self.reflected_flag)

        elif event.key == 'b':
            if self.bed_type == "linspace":
                self.bed_type = "beach"
            elif self.bed_type == "beach":
                self.bed_type = "random"
            elif self.bed_type == "random":
                self.bed_type = "linspace"
            print("Bed type:", self.bed_type)

        elif event.key == 'r':
            self.bed_resolver.new_random_surface()

        elif event.key == 'p':
            self.stop_flag = not self.stop_flag
            print("Pause:", self.stop_flag)

        self.apply_flags()

    def on_mouse_press(self, event):
        self.drag_start = self.screen_to_gl_coordinates(event.pos)

    def on_mouse_release(self, event):
        self.drag_start = None

    def on_mouse_move(self, event):
        if not self.drag_start is None:
            pos = self.screen_to_gl_coordinates(event.pos)
            self.rotate_camera(pos - self.drag_start)
            self.drag_start = pos
            self.set_camera()
            self.update()

    def on_mouse_wheel(self, event):
        if event.delta[1] > 0:
            if self.program['u_eye_height'] > 0.5:
                self.program['u_eye_height'] -= event.delta[1] * 0.2
        else:
            if self.program['u_eye_height'] < 5:
                self.program['u_eye_height'] -= event.delta[1] * 0.2

    def screen_to_gl_coordinates(self, pos):
        return 2 * np.array(pos) / np.array(self.size) - 1


    @staticmethod
    def normalize(vec):
        vec = np.asanyarray(vec, dtype=np.float32)
        return vec / np.sqrt(np.sum(vec * vec, axis=-1))[..., None]