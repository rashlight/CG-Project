
import world
import camera
import shader
import matrix
import pyglet.gl as gl
import math
import ctypes
import pyglet

pyglet.options["shadow_window"] = False
pyglet.options["debug_gl"] = False


class Window(pyglet.window.Window):
    def __init__(self, **args):
        super().__init__(**args)

        self.speed = 10
        self.sensitivity = 0.002

        # create world
        self.world = world.World()

        # create shader
        self.shader = shader.Shader("vert.glsl", "frag.glsl")
        self.shader_sampler_location = self.shader.find_uniform(
            b"texture_array_sampler")
        self.shader.use()

        # pyglet stuff
        # set the update interval as small as possible
        pyglet.clock.schedule_interval(self.update, 1.0 / 10000)
        self.mouse_captured = False

        # camera stuff
        self.camera = camera.Camera(self.shader, self.width, self.height)

    def update(self, delta_time):
        if not self.mouse_captured:
            self.camera.input = [0, 0, 0]

        self.camera.update_camera(self.speed, delta_time)

    def on_draw(self):
        self.camera.update_matrices()

        # bind textures
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY,
                         self.world.texture_manager.texture_array)
        gl.glUniform1i(self.shader_sampler_location, 0)

        # draw stuff
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_CULL_FACE)

        gl.glClearColor(0.0, 0.0, 0.0, 1.0)
        self.clear()
        self.world.draw()

        gl.glFinish()  # there seems to be a bit of a bug in Pyglet which makes this call necessary

    # input functions

    def on_resize(self, width, height):
        print(f"Resize {width} * {height}")
        gl.glViewport(0, 0, width, height)

        self.camera.width = width
        self.camera.height = height

    def on_mouse_press(self, x, y, button, modifiers):
        self.mouse_captured = True
        self.set_exclusive_mouse(self.mouse_captured)

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        if self.mouse_captured:
            self.camera.rotation[0] -= delta_x * self.sensitivity
            self.camera.rotation[1] += delta_y * self.sensitivity

            self.camera.rotation[1] = max(
                -math.tau / 4,
                min(math.tau / 4, self.camera.rotation[1])
            )

    def on_key_press(self, key, modifiers):
        if not self.mouse_captured:
             return

        print(self.camera.input[2]);

        if key == pyglet.window.key.D:
            self.camera.input[0] += 1
        elif key == pyglet.window.key.A:
            self.camera.input[0] -= 1
        elif key == pyglet.window.key.W:
            self.camera.input[2] += 1
        elif key == pyglet.window.key.S: 
            self.camera.input[2] -= 1
        elif key == pyglet.window.key.SPACE:
            self.camera.input[1] += 1
        elif key == pyglet.window.key.LSHIFT: 
            self.camera.input[1] -= 1

    def on_key_release(self, key, modifiers):
        if not self.mouse_captured:
            return

        if key == pyglet.window.key.D:
            self.camera.input[0] -= 1
        elif key == pyglet.window.key.A: 
            self.camera.input[0] += 1
        elif key == pyglet.window.key.W:
            self.camera.input[2] -= 1
        elif key == pyglet.window.key.S: 
            self.camera.input[2] += 1
        elif key == pyglet.window.key.SPACE:
            self.camera.input[1] -= 1
        elif key == pyglet.window.key.LSHIFT: self.camera.input[1] += 1


class Game:
    def __init__(self):
        self.config = gl.Config(double_buffer = True, major_version = 3, minor_version = 3, depth_size = 16) # add depth_size = 16 because pyglet makes a 24 bit depth buffer by default, which isn't supported on some hardware
        self.window = Window(config = self.config, width = 1024, height = 768, caption = "CG Project - Group ?", resizable = True, vsync = False)

    def run(self):
        pyglet.app.run()


if __name__ == "__main__":
    game = Game()
    game.run()
