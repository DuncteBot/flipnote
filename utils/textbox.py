from PIL import Image, ImageFont, ImageDraw
import sys


class Point:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def get_xy(self):
        return self.x, self.y


class Rectangle(Point):
    width: float
    height: float

    def __init__(self, x: float, y: float, width: float, height: float):
        super().__init__(x, y)
        self.width = width
        self.height = height

    def get_wh(self):
        return self.width, self.height

    def get_xywh(self):
        return self.get_xy(), self.get_wh()


class TextBox:
    font_size: int
    base_line: float = 0.2
    line_height: float = 1.25
    font_color: str = "Black"
    font: ImageFont
    background_color: str = None
    box: Rectangle = Rectangle(0, 0, 100, 100)

    def __init__(self, img: Image):
        self.img = img
        self.canv = ImageDraw.Draw(img)

    def set_font(self, file_path: str, font_size: int):
        self.font_size = font_size
        self.font = ImageFont.truetype(file_path, font_size)

    def set_box(self, x: int, y: int, width: int, height: int):
        self.box = Rectangle(x, y, width, height)

    def set_background_color(self, color: str):
        self.background_color = color

    def font_size_in_points(self):
        return 0.75 * self.font_size

    def calculate_box(self, text: str):
        bounds = self.font.getbbox(text)

        left = bounds[0]
        top = bounds[1]
        right = bounds[2]
        bottom = bounds[3]

        return Rectangle(
            left,
            top,
            right - left,
            bottom - top
        )

    def draw(self, text: str):
        return self._draw_text(text, True)

    def _draw_text(self, text: str, draw: bool = True):
        if not self.font:
            return None

        lines = self.wrap_text_with_overflow(text)

        line_height_px = self.line_height * self.font_size
        # text_height = len(lines) * line_height_px

        # TODO: alignment
        yAlign = 0
        n = 0
        drawnX = drawnY = sys.maxsize
        drawnH = drawnW = 0

        for line in lines:
            box = self.calculate_box(line)
            # TODO: alignment
            xAlign = 0

            yShift = line_height_px * (1 - self.base_line)
            # current line X and Y position
            xMOD = self.box.x + xAlign
            yMOD = self.box.y + yAlign + yShift + (n * line_height_px) - self.font_size

            if draw:
                if line and self.background_color is not None:
                    background_height = self.font_size
                    bg_shape = (
                        (xMOD, yMOD),
                        (
                            self.box.width + box.width,
                            background_height + yMOD
                        )
                    )
                    self.canv.rectangle(
                        bg_shape,
                        fill=self.background_color
                    )

                self.draw_internal(
                    Point(xMOD, yMOD),
                    self.font_color,
                    line
                )

            drawnX = min(xMOD, drawnX)
            drawnY = min(self.box.y + yAlign + (n * line_height_px), drawnY)
            drawnW = max(drawnW, box.width)
            drawnH += line_height_px

            n += 1

        return Rectangle(drawnX, drawnY, drawnW, drawnH)

    def wrap_text_with_overflow(self, text: str):
        lines = []
        explicit_lines = text.split('\n')  # TODO: split by \r\n and \r as well

        for line in explicit_lines:
            words = line.split(' ')
            inner_line = words[0]
            for i in range(1, len(words)):
                box = self.calculate_box(f"{inner_line} {words[i]}")
                if box.width >= self.box.width:
                    lines.append(inner_line)
                    inner_line = words[i]
                else:
                    inner_line += f" {words[i]}"

            lines.append(inner_line)

        return lines

    def draw_internal(self, position: Point, color: str, text):
        self.canv.text(
            position.get_xy(),
            text,
            font=self.font,
            fill=color,
            spacing=0,
            stroke_fill=None
        )
