from manim import *

class StretchTip(ArrowTip):
    def __init__(
        self,
        fill_opacity=1,
        stroke_width=1,
        length=DEFAULT_ARROW_TIP_LENGTH,
        start_angle=PI,
        **kwargs,
    ):
        self.start_angle = start_angle
        VMobject.__init__(
            self, fill_opacity=fill_opacity, stroke_width=stroke_width, **kwargs
        )
        self.set_points_as_corners(
            [
                [1, 0, 0],  # tip
                [-0.3, 0.5, 0],
                [0, 0, 0],  # base
                [-0.3, -0.5, 0],
                [1, 0, 0],  # close path, back to tip
            ]
        )
        self.scale(length / self.length)

    @property
    def length(self):
        """The length of the arrow tip.

        In this case, the length is computed as the height of
        the triangle encompassing the stealth tip (otherwise,
        the tip is scaled too large).
        """
        return np.linalg.norm(self.vector)

class StretchVector(Vector):
    def __init__(
            self,
            *args,
            tip_shape=StretchTip,
            tip_length_ratio=0.1,
            max_tip_length=0.15,
            stroke_width=1,
            **kwargs
    ):
        self.tip_length_ratio = tip_length_ratio
        self.max_tip_length = max_tip_length
        self.vec_stroke_width = stroke_width

        super().__init__(*args, tip_shape=tip_shape, **kwargs)

    def get_default_tip_length(self) -> float:
        return min(self.max_tip_length, self.get_length() * self.tip_length_ratio)

    def _set_stroke_width_from_length(self):
        if config.renderer == RendererType.OPENGL:
            self.set_stroke(
                width=self.vec_stroke_width,
                recurse=False,
            )
        else:
            self.set_stroke(
                width=self.vec_stroke_width,
                family=False,
            )
        return self
