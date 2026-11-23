"""
GLYPH OUTLINE EXTRACTION AND CURVE FLATTENING
Purpose:
    Convert a FontTools glyph outline into contours made from straight-line points.

Algorithm steps:
    1. Ask FontTools to draw the glyph into a custom BasePen.
    2. Start a new contour whenever the pen receives moveTo.
    3. Append straight-line endpoints when lineTo is received.
    4. For a quadratic curve, sample t from 0 to 1 and evaluate quadratic_bezier.
    5. For a cubic curve, sample t from 0 to 1 and evaluate cubic_bezier.
    6. Close closed contours and return all contours as coordinate lists.

FontTools' BasePen resolves TrueType's implied on-curve points and decomposes
composite glyph components before the custom curve methods are called.
"""

from fontTools.pens.basePen import BasePen

from .bezier import quadratic_bezier, cubic_bezier


class FlatteningPen(BasePen):
    def __init__(self, glyph_set, steps=16):
        if steps < 1:
            raise ValueError("steps must be at least 1")

        super().__init__(glyph_set)
        self.steps = steps
        self.contours = []
        self.current_contour = None

    def _moveTo(self, point):
        if self.current_contour:
            self._store_open_contour()
        self.current_contour = [(float(point[0]), float(point[1]))]

    def _lineTo(self, point):
        self._ensure_contour()
        self.current_contour.append((float(point[0]), float(point[1])))

    def _qCurveToOne(self, control_point, end_point):
        start_point = self._getCurrentPoint()
        for step in range(1, self.steps + 1):
            t = step / self.steps
            point = quadratic_bezier(start_point, control_point, end_point, t)
            self.current_contour.append(point)

    def _curveToOne(self, control1, control2, end_point):
        start_point = self._getCurrentPoint()
        for step in range(1, self.steps + 1):
            t = step / self.steps
            point = cubic_bezier(start_point, control1, control2, end_point, t)
            self.current_contour.append(point)

    def _closePath(self):
        if self.current_contour:
            first = self.current_contour[0]
            last = self.current_contour[-1]
            if last != first:
                self.current_contour.append(first)
            self._store_open_contour()

    def _endPath(self):
        self._store_open_contour()

    def _ensure_contour(self):
        if self.current_contour is None:
            self.current_contour = []

    def _store_open_contour(self):
        if self.current_contour and len(self.current_contour) >= 2:
            self.contours.append(self.current_contour)
        self.current_contour = None


def flatten_glyph(glyph_name, glyph_set, steps=16):
    """Return a list of flattened contours for the requested glyph."""
    pen = FlatteningPen(glyph_set, steps=steps)
    glyph_set[glyph_name].draw(pen)

    if pen.current_contour:
        pen._store_open_contour()

    return pen.contours
