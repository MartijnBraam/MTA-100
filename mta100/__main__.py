import hmac
import os
import uuid
import math
from hashlib import sha256

from sexpdata import Symbol, dumps

from mta100.shape import Rect, PadRect, Line, Pad, make_connected_lines, make_indexed_rect

add_purpose_labels = True

def make_uuid(name, index):
    h = hmac.new(name.encode(), str(index).encode(), digestmod=sha256)
    return str(uuid.UUID(bytes=h.digest()[:16], version=4))


def make_647050(partno, positions, l, w=None, g=None):
    name = f'mta100_01x{positions}_P2.54_{partno}'
    desc = f'MTA-100 Headers with retention peg, straight angle, {positions} positions. Part code {partno}'
    tags = f'MTA-100 2.54mm header single row'

    footprint = [Symbol('footprint'), name]
    footprint.append([Symbol('version'), Symbol('20240108')])
    footprint.append([Symbol('generator'), Symbol('mta100.py')])
    footprint.append([Symbol('descr'), desc])
    footprint.append([Symbol('tags'), tags])
    footprint.append(
        [Symbol('attr'), Symbol('through_hole')])
    footprint.append(make_id_label('Reference', 'Ref**', 'F.SilkS', (-0.9525, 6.6675)))
    if add_purpose_labels:
        footprint.append(make_purpose_label((l * 0.5, 7.62)))

    cmargin = 0.5
    smargin = 0.1
    ph = 7.62
    moffset = (ph - 6.35)
    sloped_margin = smargin * math.tan(math.pi / 16.0)

    shapes = make_connected_lines(
        'F.Fab', [
            [0, 0],
            [l - 1, 0],
            [l, 1],
            [l, 6.35],
            [0, 6.35],
        ], width=0.1, loop=True
    ) + [
        Rect('F.CrtYd', [-cmargin, -moffset - cmargin], [l + cmargin, ph + cmargin - (moffset / 2)], width=0.05),
    ] + make_connected_lines(
        'F.SilkS', [
            [-smargin, -smargin],
            [l - 1 + sloped_margin, -smargin],
            [l + smargin, 1 - sloped_margin],
            [l + smargin, 6.35 + smargin],
            [-smargin, 6.35 + smargin],
        ], loop=True
    )


    th = 2.87 - 0.64 - (0.64 / 2)
    if g is None:
        # Single tab
        shapes.append(Rect('F.SilkS', [1.27, -smargin], [l - 1.27, th - smargin], filled=True))
    elif w is None:
        # Double tab
        shapes.append(Rect('F.SilkS', [1.27, -smargin], [l / 2 - (g / 2), th - smargin], filled=True))
        shapes.append(Rect('F.SilkS', [l / 2 + (g / 2), -smargin], [l - 1.27, th - smargin], filled=True))

    for pos in range(0, positions):
        pin = positions - pos
        left = 1.27 + (pos * 2.54)
        if add_purpose_labels:
            footprint.append(make_purpose_pin_label(pin, left, -0.3175))
        shapes.append(Pad(pin, [left, 2.87], 1.85, 1.1))

    salt = 0
    for shape in shapes:
        salt += 1
        graphic = shape.graphic(make_uuid(name, salt))
        footprint.append(graphic)

    return name, footprint

def make_purpose_pin_label(pin, left, top):
    return [
        Symbol('fp_text'), Symbol('user'), f'${{Purpose Pin{pin}}}',
        [Symbol('at'), left, top, 90],
        [Symbol('uuid'), make_uuid(f'purpose_pin_{pin}', 42)],
        [Symbol('layer'), 'F.SilkS'],
        [Symbol('effects'),
            [Symbol('font'),
                [Symbol('size'), 1, 1],
                [Symbol('thickness'), 0.15],
            ],
            [Symbol('justify'), Symbol('left')],
        ]
    ]

def make_id_label(key, value, layer, pos):
    return [
        Symbol('property'), key, value,
        [Symbol('at'), pos[0], pos[1], -90],
        [Symbol('uuid'), make_uuid(f'label_{key}_{value}', 42)],
        [Symbol('layer'), layer],
        [Symbol('effects'),
            [Symbol('font'),
                [Symbol('size'), 1, 1],
                [Symbol('thickness'), 0.15],
            ],
            [Symbol('justify'), Symbol('left')],
        ]
    ]

def make_purpose_label(pos):
    return [
        Symbol('fp_text'), Symbol('user'), '${Purpose}',
        [Symbol('at'), pos[0], pos[1], 0],
        [Symbol('uuid'), make_uuid(f'label_purpose', 42)],
        [Symbol('layer'), 'F.SilkS'],
        [Symbol('effects'),
            [Symbol('font'),
                [Symbol('size'), 1.2, 1.2],
                [Symbol('thickness'), 0.2],
            ],
        ]
    ]


def make_640455(partno, positions, l, w=None, g=None):
    name = f'mta100_01x{positions}_P2.54_{partno}'
    desc = f'MTA-100 polarized headers, right angle, {positions} positions. Part code {partno}'
    tags = f'MTA-100 2.54mm header single row polarized'

    footprint = [Symbol('footprint'), name]
    footprint.append([Symbol('version'), Symbol('20240108')])
    footprint.append([Symbol('generator'), Symbol('mta100.py')])
    footprint.append([Symbol('descr'), desc])
    footprint.append([Symbol('tags'), tags])
    footprint.append(
        [Symbol('attr'), Symbol('through_hole')])
    footprint.append(make_id_label('Reference', 'Ref**', 'F.SilkS', (-2.2225, 9.525)))

    cmargin = 0.5
    smargin = 0.1
    ph = 7.62
    moffset = (ph - 6.35)
    origin = [0, 0]
    sloped_margin = smargin * math.tan(math.pi / 16.0)
    shapes = make_connected_lines(
        'F.Fab', [
            [0, 0], [l-1, 0], [l, 1], [l, 6.35], [0, 6.35]
        ], width=0.1, loop=True
    ) + [
        Rect('F.CrtYd', [-cmargin, -moffset - cmargin], [l + cmargin, ph + cmargin - (moffset / 2)], width=0.05),
    ] + make_connected_lines(
        'F.SilkS', [
            [-smargin, -smargin],
            [l - 1 + sloped_margin, -smargin],
            [l + smargin, 1 - sloped_margin],
            [l + smargin, 6.35 + smargin],
            [-smargin, 6.35 + smargin],
        ], loop=True
    )

    th = 2.87 - 0.64 - (0.64 / 2)
    if g is None:
        # Single tab
        shapes.append(Rect('F.SilkS', [1.27, -smargin], [l - 1.27, th - smargin], filled=True))
    elif w is None:
        # Double tab
        shapes.append(Rect('F.SilkS', [1.27, -smargin], [l / 2 - (g / 2), th - smargin], filled=True))
        shapes.append(Rect('F.SilkS', [l / 2 + (g / 2), -smargin], [l - 1.27, th - smargin], filled=True))

    for pos in range(0, positions):
        pin = positions - pos
        left = 1.27 + (pos * 2.54)
        shapes.append(Pad(pin, [left, -2.985], 1.85, 1.1))
        if pos == 0:
            origin = shapes[-1].center
        if add_purpose_labels:
            footprint.append(make_purpose_pin_label(pin, left - origin[0], -0.9525))
        shapes.append(Line('F.SilkS', [left, -1.8], [left, 0]))
    if add_purpose_labels:
        footprint.append(make_purpose_label((l * 0.5 - origin[0], 10.4775)))

    salt = 0
    for shape in shapes:
        salt += 1
        shape.origin = origin
        graphic = shape.graphic(make_uuid(name, salt))
        footprint.append(graphic)

    return name, footprint


def main():
    parts = [
        {'partno': '647050-2', 'positions': 2, 'l': 5.08},
        {'partno': '647050-3', 'positions': 3, 'l': 7.62},
        {'partno': '647050-4', 'positions': 4, 'l': 10.16},
        {'partno': '647050-5', 'positions': 5, 'l': 12.7},
        {'partno': '647050-6', 'positions': 6, 'l': 15.24},
        {'partno': '647050-7', 'positions': 7, 'l': 17.78},
        {'partno': '647050-8', 'positions': 8, 'l': 20.32, 'g': 2.54},
        {'partno': '647050-9', 'positions': 9, 'l': 22.86, 'g': 5.08},
        {'partno': '647050-9', 'positions': 9, 'l': 22.86, 'g': 5.08},
        {'partno': '640455-2', 'positions': 2, 'l': 5.08},
        {'partno': '640455-3', 'positions': 3, 'l': 7.62},
        {'partno': '640455-4', 'positions': 4, 'l': 10.16},
        {'partno': '640455-5', 'positions': 5, 'l': 12.7},
        {'partno': '640455-6', 'positions': 6, 'l': 15.24},
        {'partno': '640455-7', 'positions': 7, 'l': 17.78},
        {'partno': '640455-8', 'positions': 8, 'l': 20.32},
        {'partno': '640455-9', 'positions': 9, 'l': 22.86},
        {'partno': '640455-9', 'positions': 9, 'l': 22.86},
    ]
    libname = 'Connector_MTA-100.pretty'
    os.makedirs(libname, exist_ok=True)
    for p in parts:
        if '647050' in p['partno']:
            name, fp = make_647050(**p)
        elif '640455' in p['partno']:
            name, fp = make_640455(**p)
        sexpr = dumps(fp, pretty_print=True)
        with open(f'{libname}/{name}.kicad_mod', 'w') as handle:
            handle.write(sexpr)


if __name__ == '__main__':
    main()
