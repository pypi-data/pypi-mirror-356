# -*- coding:utf-8 -*-
#!/usr/bin/python3
import ctypes

from OpenGL import GL as gl
from PyQt6 import QtCore, QtOpenGLWidgets, QtOpenGL
from PyQt6.QtGui import QSurfaceFormat
import numpy as np

class OpenGLDancingDots(QtOpenGLWidgets.QOpenGLWidget):

    _get_data = False
    _x_numbers = False
    _y_numbers = False
    _r_numbers = False
    _phi_numbers = False
    _vertices = False
    _red = False
    _green = False
    _blue = False
    _timer = False
    _p = 0.0
    _q = 0.0
    _r = []
    _k = []
    _shader_program_id = 0
    _vertex_buffer = None  # VBO
    _vertex_array = None  # VAO
    _vertices = False
    _counter = 0.0
    _M = 0
    _N = 0
    _softmax = 3.0
    _smooth = 0.95
    _running_mean = np.ones(5)
    _viewport = [0.0, 0.0, 0.0, 0.0]
    _update_viewport = False
    _fullscreen = False    # current display
    _toggle_fullscreen = None     # callback for onclick function

    # inside:  red / yellow / blue / orange / green
    # outside: orange / green / red / yellow / blue
    red = np.array([0.8, 0.0, 0.0])
    orange = np.array([1.0, 0.5, 0.0])
    yellow = np.array([0.6, 0.6, 0.0])
    green = np.array([0.0, 0.6, 0.0])
    turquoise = np.array([0.0, 0.6, 0.6])
    blue = np.array([0.0, 0.0, 1.0])
    purple = np.array([0.8, 0.0, 0.4])
    black = np.array([0.0, 0.0, 0.0])
    dark = 0.3
    _data_colours = [[red, dark*green],
                     [yellow, dark*blue],
                     [orange, dark*turquoise],
                     [green, dark*red],
                     [blue, dark*yellow]]
    _rotations = [0, 0, 0, 0, 0]

    def __init__(self, get_data, toggle_fullscreen, settings):
        super().__init__()

        self._get_data = get_data
        self._toggle_fullscreen = toggle_fullscreen

        self._M = 30  # number of circles
        self._N = 200  # points per circle

        # initialise data structures
        self._r_numbers = np.arange(0, self._M * 2.0 * np.pi, 2.0 * np.pi / self._N, dtype=np.float32)
        self._r_numbers = np.mod(self._r_numbers, 2.0 * np.pi)
        self._phi_numbers = np.sin(self._r_numbers, dtype=np.float32)
        self._x_numbers = np.zeros(self._r_numbers.shape, dtype=np.float32)
        self._y_numbers = np.zeros(self._r_numbers.shape, dtype=np.float32)
        self._red = np.zeros(self._r_numbers.shape, dtype=np.float32)
        self._green = np.zeros(self._r_numbers.shape, dtype=np.float32)
        self._blue = np.zeros(self._r_numbers.shape, dtype=np.float32)

        self.set_parameters(settings)


    def set_parameters(self, settings):

        if self._timer:
            self._timer.stop()

        # k direction
        # p in/out movement
        self._p = 0.0
        self._q = 1.0
        self._k = np.array([0.0, 0.0, 0.0, 0.0, 0.0])

        self._softmax = settings['power']
        self._smooth = settings['timesmoothing']
        for n in range(0, 5):

            # colours
            self._data_colours[n][0] = np.array(settings['incolour{}'.format(n)])/255.0
            self._data_colours[n][1] = np.array(settings['outcolour{}'.format(n)])/255.0

            # rotations
            self._rotations[n] = np.array(settings['rotation{}'.format(n)])

        # Create sum of sine waves of different frequencies
        dt = 0.005
        t0 = np.arange(0, 5 * np.pi, dt)
        sp = 1  #settings['shape']
        f = [(abs(np.sin(0.5 * settings['freq0'] * t0))**sp),
             (abs(np.sin(0.5 * settings['freq1'] * t0))**sp),
             (abs(np.sin(0.5 * settings['freq2'] * t0))**sp),
             (abs(np.sin(0.5 * settings['freq3'] * t0))**sp),
             (abs(np.sin(0.5 * settings['freq4'] * t0))**sp),]

        # Create 10 circles of different lengths
        freq_start = 1.0
        freq_step = 0.005
        self._r = [[]] * self._M  # the interpolated circle data, zeros for now, consisting of M*N circles s[M][1..5], all the same length
        s = [[]] * self._M        # the raw circle data, zeros for now, consisting of M*N circles s[M][1..5]
        t = [[]] * self._M        # the base to plot against, will go from 0 to 2pi, t[M]
        for m in range(0, self._M):
            s[m] = [[]] * 5
            freq = freq_start + m * freq_step  # our circle frequency
            for n in range(0, 5):
                s[m][n] = np.zeros(int((2 / freq) * np.pi / dt))
            t[m] = [m for m in np.arange(0, 2 * np.pi, 2 * np.pi / self._N)]

        # Average over all circles - pre-calculate parts of the sum of sines
        for m in range(0, self._M):
            for n in range(0, 5):
                # only plot if you can fill the entire circle
                for i in range(0, (len(f[n]) // len(s[m][n])) * len(s[m][n])):
                    value = f[n][i] - 0.5
                    index = i % len(s[m][n])
                    s[m][n][index] += value  # add to front
                    s[m][n][-(index + 1)] += value  # add to back, so beginning and end match and the circle stays closed

        # downsample so all circles have the same length (N samples)
        for m in range(0, self._M):
            self._r[m] = [[]] * 5
            for n in range(0, 5):
                self._r[m][n] = np.zeros(self._N)
                for i in range(0, self._N - 1):
                    index = int(float(i) * (len(s[m][n]) - 1) / (self._N - 1.0))
                    self._r[m][n][i] = s[m][n][index]
                self._r[m][n][self._N - 1] = s[m][n][0]  # close the circle

        # restart timer again
        if self._timer:
            self._timer.start(30)

    def initializeGL(self):

        print(f"GL_VENDOR: {gl.glGetString(gl.GL_VENDOR)}")
        print(f"GL_RENDERER: {gl.glGetString(gl.GL_RENDERER)}")
        print(f"GL_VERSION: {gl.glGetString(gl.GL_VERSION)}")
        print(f"GL_SHADING_LANGUAGE_VERSION: {gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION)}")

        # the vertex shader
        vertex_shader_id = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        shader_code = (" #version 330 core\n"
                       " layout (location = 0) in vec2 xyCoords; "
                       " layout (location = 1) in vec3 vxColour; "
                       " out vec4 vertColour; "
                       " void main() { "
                       "     gl_Position = vec4(xyCoords, 0.0, 1.0); "
                       "     vertColour = vec4(vxColour, 1.0); "
                       " } ")
        gl.glShaderSource(vertex_shader_id, shader_code)
        gl.glCompileShader(vertex_shader_id)
        if gl.glGetShaderiv(vertex_shader_id, gl.GL_COMPILE_STATUS) == gl.GL_FALSE:
            print("Error creating dancing dots vertex shader.")

        # the fragment shader
        fragment_shader_id = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        shader_code = (" #version 330 core\n"
                       " in vec4 vertColour; "
                       " out vec4 fragColour; "
                       " void main() { "
                       "     vec2 coords = gl_PointCoord * 2.0 - 1.0; "
                       "     float dist = length(coords); "
                       "     if (dist > 1.0) "
                       "         discard; "
                       "     else "
                       "         fragColour = vertColour; "
                       " } ")
        gl.glShaderSource(fragment_shader_id, shader_code)
        gl.glCompileShader(fragment_shader_id)
        if gl.glGetShaderiv(fragment_shader_id, gl.GL_COMPILE_STATUS) == gl.GL_FALSE:
            print("Error creating dancing dots fragment shader.")

        # the shader program, linking both shaders
        self._shader_program_id = gl.glCreateProgram()
        gl.glAttachShader(self._shader_program_id, vertex_shader_id)
        gl.glAttachShader(self._shader_program_id, fragment_shader_id)
        gl.glLinkProgram(self._shader_program_id)
        if gl.glGetProgramiv(self._shader_program_id, gl.GL_LINK_STATUS) == gl.GL_FALSE:
            print("Error linking dancing dots shaders.")
        if not gl.glIsProgram(self._shader_program_id):
            print(f"Error: Shader program {self._shader_program_id} is not valid!")

        # declare the buffer to be a vertex array
        self._vertices = np.column_stack((self._x_numbers, self._y_numbers, self._red, self._green, self._blue)).ravel()

        # create the VAO
        self._vertex_array = QtOpenGL.QOpenGLVertexArrayObject()
        self._vertex_array.create()
        self._vertex_array.bind()

        self._vertex_buffer = QtOpenGL.QOpenGLBuffer()
        self._vertex_buffer.create()
        self._vertex_buffer.bind()
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self._vertices.nbytes, self._vertices, gl.GL_DYNAMIC_DRAW)
        size = self._vertices.itemsize
        gl.glVertexAttribPointer(0, 2, gl.GL_FLOAT, gl.GL_FALSE, 5*size, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 5*size, ctypes.c_void_p(2 * size))
        gl.glEnableVertexAttribArray(1)
        gl.glUseProgram(self._shader_program_id)
        gl.glPointSize(6)

    def paintGL(self):

        # cX - amount of frequency ring fX for each frequency X (out of five)
        freqs = self._get_data()
        freqs -= freqs.min()
        freqs = freqs ** self._softmax
        freqs /= freqs.sum()     # necessary for the colours to add up to 1.0
        self._running_mean = self._smooth * self._running_mean + (1.0-self._smooth) * freqs
        [c1, c2, c3, c4, c5] = self._running_mean
        c6 = 0.1 * (c1 - c2 + c3 - c4 + c5)  # c6 - amount of in/out movement
        print("Frequency bands: {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}".format(c1, c2, c3, c4, c5), end='\r')

        # k[X] - turning speed and direction of each frequency ring
        self._k += 0.5*np.array([self._rotations[0]*c1, self._rotations[1]*c2, self._rotations[2]*c3,
                                 self._rotations[3]*c4, self._rotations[4]*c5])
        kn = np.floor(self._k).astype(int)  # left index into ring
        km = kn + 1  # right index into ring
        kp = km - self._k  # left amount
        kq = self._k - kn  # right amount

        # plot curves
        last_data = []
        for m in range(0, self._M):

            # offset = np.sqrt((M-m))
            offset = 1.3*(self._M - m)
            offset = np.sqrt(np.sqrt(offset * offset * offset)) / self._M # x^(3/4)

            # soft rolling of circles by interpolating between floor(k) and ceil(k)
            data = (c1 * (np.roll(self._r[m][0], kn[0]) * kp[0] + np.roll(self._r[m][0], km[0]) * kq[0])
                    + c2 * (np.roll(self._r[m][1], kn[1]) * kp[1] + np.roll(self._r[m][1], km[1]) * kq[1])
                    + c3 * (np.roll(self._r[m][2], kn[2]) * kp[2] + np.roll(self._r[m][2], km[2]) * kq[2])
                    + c4 * (np.roll(self._r[m][3], kn[3]) * kp[3] + np.roll(self._r[m][3], km[3]) * kq[3])
                    + c5 * (np.roll(self._r[m][4], kn[4]) * kp[4] + np.roll(self._r[m][4], km[4]) * kq[4])
                    + 1)
            data /= data.max()
            data *= offset
            data += offset
            try:
                if len(last_data):
                    fr = m*self._N         # from offset
                    to = (m + 1)*self._N   # to offset
                    self._phi_numbers[fr:to] = self._p * last_data + self._q * data
                    colour_in =   c1 * self._data_colours[0][0] \
                                + c2 * self._data_colours[1][0] \
                                + c3 * self._data_colours[2][0] \
                                + c4 * self._data_colours[3][0] \
                                + c5 * self._data_colours[4][0]
                    colour_out =  c1 * self._data_colours[0][1] \
                                + c2 * self._data_colours[1][1] \
                                + c3 * self._data_colours[2][1] \
                                + c4 * self._data_colours[3][1] \
                                + c5 * self._data_colours[4][1]
                    if m == 1:
                        self._red[fr:to] = colour_out[0] * self._q
                        self._green[fr:to] = colour_out[1] * self._q
                        self._blue[fr:to] = colour_out[2] * self._q
                    elif m == self._M - 1:
                        self._red[fr:to] = colour_in[0] * self._p
                        self._green[fr:to] = colour_in[1] * self._p
                        self._blue[fr:to] = colour_in[2] * self._p
                    else:
                        c_in = m / self._M
                        c_out = 1.0 - c_in
                        colour = c_in * colour_in + c_out * colour_out
                        self._red[fr:to] = colour[0]
                        self._green[fr:to] = colour[1]
                        self._blue[fr:to] = colour[2]
            except BaseException as e:
                print("Plot exception {} for curve n={}".format(e, m))
            last_data = data
        self._p = (self._p + c6) % 1
        self._q = 1.0 - self._p

        # convert to x/y/colour data and push to graphic card
        self._y_numbers = (self._phi_numbers * np.cos(self._r_numbers))
        self._x_numbers = self._phi_numbers * np.sin(self._r_numbers)
        self._vertices = np.column_stack((self._x_numbers, self._y_numbers, self._red, self._green, self._blue)).ravel()

        gl.glUseProgram(self._shader_program_id)
        self._vertex_array.bind()
        self._vertex_buffer.bind()
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, self._vertices.nbytes, self._vertices)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT | gl.GL_STENCIL_BUFFER_BIT)
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)
        if self._update_viewport:
            gl.glViewport(*self._viewport)

        # actual drawing
        gl.glDrawArrays(gl.GL_POINTS, 0, len(self._x_numbers))
        error = gl.glGetError()
        if error != gl.GL_NO_ERROR:
            print(f"glDrawArrays error: {error}")

    def resizeGL(self, width, height):
        size = min(width, height)
        x = (width - size) // 2
        y = (height - size) // 2
        gl.glUseProgram(self._shader_program_id)
        gl.glViewport(x, y, size, size)
        self._viewport = [x, y, size, size]
        self._update_viewport = True
        print(f"glViewport set to x={x}, y={y}, width={size}, height={size}")

    def start(self):
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self.update)
        self._timer.start(30)

    def mouseReleaseEvent(self, dummy):
        self._fullscreen = not self._fullscreen
        self._toggle_fullscreen(self._fullscreen)
