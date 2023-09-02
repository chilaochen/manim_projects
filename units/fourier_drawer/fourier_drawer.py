from manim import *
from ..mobjects import *

class FourierDrawer(VMobject):
    vector_config = {
        "buff": 0,
        "fill_opacity": 1,
        "tip_length_ratio": 0.1,
        "max_tip_length": 0.16,
        "stroke_width": 1,
    }

    circle_config = {
        "color": BLUE,
        "stroke_width": 1,
        "stroke_opacity": 1,
    }

    drawn_path_config = {
        "stroke_width": 1.5,
        "stroke_color": YELLOW,
    }

    def __init__(self, path, n_vector, n_sample, params=None, vec_cfg=vector_config, circle_cfg=circle_config, drawn_path_cfg=drawn_path_config, **kwargs):
        super().__init__(**kwargs)
        if path is not None:
            self.path = path.copy()
            self.add(self.path)
            params = FourierDrawer.fourier_path(self.path, n_vector, n_sample)
        self._generate(params, vec_cfg, circle_cfg, drawn_path_cfg)

        self._process = 0
        self._drawn_time = 0

    @property
    def drawn_time(self):
        return self._drawn_time

    @drawn_time.setter
    def drawn_time(self, value):
        self._drawn_time = value

    @property
    def process(self):
        return self._process

    @process.setter
    def process(self, value: float):
        self.set_process(value)

    @property
    def pen_point(self):
        return self.vectors[-1].get_end()

    def set_process(self, value):
        self._process = value

        for vector in self.vectors[1:]:
            vector.shift(vector.pre_vec.get_end() - vector.get_start())
            vector.set_angle(vector.phase + self._process * vector.freq * TAU)
            vector.circle.move_to(vector.get_start())

        return self

    def set_process_func(self, func):
        self.process_func = func

    @property
    def animate(self):
        return super().animate(suspend_mobject_updating=False)

    def _generate(self, params, vec_cfg, circle_cfg, drawn_path_cfg):
        vectors, circles, drawn_path = FourierDrawer.generate_drawing_elements(
            params, vec_cfg, circle_cfg, drawn_path_cfg)
        self.vectors = vectors
        self.circles = circles
        self.drawn_path = drawn_path

        self.add(*vectors, *circles, drawn_path)

        self.process_func = lambda t: t / 10
        self.add_updater(FourierDrawer.process_updater)

    @staticmethod
    def process_updater(drawer, dt):
        drawer.drawn_time += dt
        drawer.process = drawer.process_func(drawer.drawn_time)

    @staticmethod
    def generate_drawing_elements(params, vec_cfg={}, circle_cfg={}, drawn_path_cfg={}):
        last_vec = None
        vectors = []
        circles = []

        for freq, coef in params:
            length = abs(coef)

            if length == 0:
                phase = 0
            else:
                phase = np.log(coef).imag

            vector = StretchVector([length, 0],  **vec_cfg).set_angle(phase)
            circle = Circle(length, **circle_cfg)
            vector.set_angle(phase)

            vector.length = length
            vector.freq = freq
            vector.phase = phase

            vector.pre_vec = last_vec
            vector.circle = circle

            if last_vec:
                vector.shift(last_vec.get_end() - vector.get_start())
                circle.move_to(vector.get_start())

            vectors.append(vector)
            circles.append(circle)

            last_vec = vector

        drawn_path = TracedPath(last_vec.get_end, **drawn_path_cfg)

        return vectors, circles, drawn_path

    @staticmethod
    def fourier_path(path, n_vector, n_sample):
        if n_sample is not None:
            dt = 1 / n_sample
            steps = np.arange(0, 1, dt)
            samples = FourierDrawer.sample_path(path, steps)
        else:
            samples = FourierDrawer.sample_path(path)
            dt = 1 / len(samples)
            steps = np.arange(0, 1, dt)

        complex_samples = samples[:, 0] + 1j * samples[:, 1]

        freqs = list(range(n_vector // 2, -n_vector // 2, -1))
        freqs.sort(key=abs)

        coefs = []
        for freq in freqs:
            riemann_sum = np.array([
                np.exp(-TAU * 1j * freq * t) * cs
                for t, cs in zip(steps, complex_samples)
            ]).sum() * dt
            coefs.append(riemann_sum)

        return zip(freqs, coefs)

    @staticmethod
    def sample_path(path, steps, step_size=0.5):
        path.throw_error_if_no_points()

        curves_and_lengths = tuple(path.get_curve_functions_with_lengths())
        total_length = sum(length for _, length in curves_and_lengths)

        if steps is None:
            steps = np.arange(0, 1, step_size / total_length)

        n = len(steps)
        samples = np.ndarray(shape=(n, 2))

        idx = 0
        current_length = 0

        for curve, length in curves_and_lengths:
            if length == 0:
                continue

            next_length = current_length + length
            target_length = steps[idx] * total_length

            while target_length >= current_length and target_length <= next_length:
                samples[idx] = curve(
                    (target_length - current_length) / length)[0:2]

                idx += 1
                if idx < n:
                    target_length = steps[idx] * total_length
                else:
                    return samples

            current_length = next_length

        return samples

