from sexpdata import Symbol


class Shape:
    def __init__(self):
        self.origin = [0, 0]

    def pos(self, a):
        return [a[0] - self.origin[0], a[1] - self.origin[1]]

    def graphic(self, uuid):
        return ()


class Line(Shape):
    def __init__(self, layer, start, end, width=0.2):
        super().__init__()
        self.layer = layer
        self.start = start
        self.end = end
        self.width = width

    def graphic(self, uuid):
        return (
            Symbol('fp_line'),
            (Symbol('start'), *self.pos(self.start)),
            (Symbol('end'), *self.pos(self.end)),
            (Symbol('stroke'),
             (Symbol('width'), self.width),
             (Symbol('type'), Symbol('default')),
             ),
            (Symbol('layer'), self.layer),
            (Symbol('uuid'), uuid),
        )


class Circle(Shape):
    def __init__(self, layer, center, end, style=None):
        super().__init__()
        self.layer = layer
        self.center = center
        self.end = end
        self.style = style or 'default'

    def graphic(self, uuid):
        return (
            Symbol('fp_circle'),
            (Symbol('center'), *self.pos(self.center)),
            (Symbol('end'), *self.pos(self.end)),
            (Symbol('stroke'),
             (Symbol('width'), 0.2),
             (Symbol('type'), Symbol(self.style)),
             ),
            (Symbol('fill'), Symbol('none')),
            (Symbol('layer'), self.layer),
            (Symbol('uuid'), uuid),
        )


class Arc(Shape):
    def __init__(self, layer, start, end, middle):
        super().__init__()
        self.layer = layer
        self.start = start
        self.middle = middle
        self.end = end

    def graphic(self, uuid):
        return (
            Symbol('fp_arc'),
            (Symbol('start'), *self.pos(self.start)),
            (Symbol('mid'), *self.pos(self.middle)),
            (Symbol('end'), *self.pos(self.end)),
            (Symbol('stroke'),
             (Symbol('width'), 0.2),
             (Symbol('type'), Symbol('default')),
             ),
            (Symbol('layer'), self.layer),
            (Symbol('uuid'), uuid),
        )


class Rect(Shape):
    def __init__(self, layer, start, end, width=0.2, filled=False):
        super().__init__()
        self.layer = layer
        self.start = start
        self.end = end
        self.width = width
        self.fill = 'solid' if filled else 'none'

    def graphic(self, uuid):
        return (
            Symbol('fp_rect'),
            (Symbol('start'), *self.pos(self.start)),
            (Symbol('end'), *self.pos(self.end)),
            (Symbol('stroke'),
             (Symbol('width'), self.width),
             (Symbol('type'), Symbol('default')),
             ),
            (Symbol('fill'), Symbol(self.fill)),
            (Symbol('layer'), self.layer),
            (Symbol('uuid'), uuid),
        )


class Text(Shape):
    def __init__(self, layer, position, text, size=1, thickness=0.1, justify_h=None, justify_v=None):
        super().__init__()
        self.layer = layer
        self.position = position
        self.text = text
        self.size = size
        self.thickness = thickness
        self.justify_h = justify_h or 'left'
        self.justify_v = justify_v or 'bottom'

    def graphic(self, uuid):

        justify = []
        if self.justify_h not in ['middle', 'center']:
            justify.append(Symbol(self.justify_h))
        if self.justify_v not in ['middle', 'center']:
            justify.append(Symbol(self.justify_v))

        return (
            Symbol('fp_text'),
            Symbol('user'),
            self.text,
            (Symbol('at'), *self.pos(self.position)),
            (Symbol('effects'),
             (Symbol('font'),
              (Symbol('size'), self.size, self.size),
              (Symbol('thickness'), self.thickness),
              ),
             (Symbol('justify'), *justify),
             ),
            (Symbol('layer'), self.layer),
            (Symbol('uuid'), uuid),
        )


class Pad(Shape):
    def __init__(self, num, center, size, drill):
        super().__init__()
        self.num = num
        self.center = center
        self.size = size
        self.drill = drill

    def graphic(self, uuid):
        return (
            Symbol('pad'),
            str(self.num),
            Symbol('thru_hole'),
            Symbol('circle'),
            (Symbol('at'), *self.pos(self.center)),
            (Symbol('size'), self.size, self.size),
            (Symbol('drill'), self.drill),
            (Symbol('layers'), "*.Cu", "*.Mask"),
            (Symbol('remove_unused_layers'), Symbol('no')),
            (Symbol('uuid'), uuid),
        )


class PadRect(Shape):
    def __init__(self, num, center, size, drill):
        super().__init__()
        self.num = num
        self.center = center
        self.size = size
        self.drill = drill

    def graphic(self, uuid):
        return (
            Symbol('pad'),
            str(self.num),
            Symbol('thru_hole'),
            Symbol('rect'),
            (Symbol('at'), *self.pos(self.center)),
            (Symbol('size'), *self.size),
            (Symbol('drill'), self.drill),
            (Symbol('layers'), "*.Cu", "*.Mask"),
            (Symbol('remove_unused_layers'), Symbol('no')),
            (Symbol('uuid'), uuid),
        )
