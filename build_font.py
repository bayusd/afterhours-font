#!/usr/bin/env python3
"""Afterhours — original Gothic x cyberpunk display font.
Built from scratch with fontTools: pointed-arch stems, neon inline slits,
circuit-node counters. No existing typeface traced or used as a base.
UPM 1000. Charset: A-Z a-z 0-9 . , ! ? - ' : ; & space
"""
import math, os
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

OUT = os.path.dirname(os.path.abspath(__file__))
UPM = 1000
CAP, XH, DESC, ASC = 720, 500, -240, 760
STEM, THIN, PEAK, SLIT = 150, 55, 55, 24

# ---------------------------------------------------------------- helpers
# TrueType: outer contours clockwise, holes counter-clockwise (y-up space).

def stem(pen, x, y0, y1, w=STEM, peak=PEAK, slit=True):
    """Vertical stem, pointed-arch top. x = left edge."""
    pen.moveTo((x, y0))
    pen.lineTo((x, y1))
    if peak:
        pen.lineTo((x + w / 2, y1 + peak))
    pen.lineTo((x + w, y1))
    pen.lineTo((x + w, y0))
    pen.closePath()
    if slit:
        sx = x + w / 2
        top = y1 - 28
        pen.moveTo((sx - SLIT / 2, y0 + 45))          # hole: CCW
        pen.lineTo((sx + SLIT / 2, y0 + 45))
        pen.lineTo((sx + SLIT / 2, top))
        if peak:
            pen.lineTo((sx, top + peak - 18))
        pen.lineTo((sx - SLIT / 2, top))
        pen.closePath()

def node(pen, cx, cy, s=34):
    """Small square circuit-node hole."""
    h = s / 2
    pen.moveTo((cx - h, cy - h))
    pen.lineTo((cx + h, cy - h))
    pen.lineTo((cx + h, cy + h))
    pen.lineTo((cx - h, cy + h))
    pen.closePath()

def hbar(pen, x0, x1, y, h=THIN):
    pen.moveTo((x0, y))
    pen.lineTo((x0, y + h))
    pen.lineTo((x1, y + h))
    pen.lineTo((x1, y))
    pen.closePath()

def diag(pen, x0, y0, x1, y1, w=THIN, slit=True):
    """Diagonal stem from (x0,y0) to (x1,y1), width w (perp)."""
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    nx, ny = -dy / L * w / 2, dx / L * w / 2
    # outer CW: start at p0-n, p1-n, p1+n, p0+n (y-up CW check done visually)
    pen.moveTo((x0 - nx, y0 - ny))
    pen.lineTo((x1 - nx, y1 - ny))
    pen.lineTo((x1 + nx, y1 + ny))
    pen.lineTo((x0 + nx, y0 + ny))
    pen.closePath()
    if slit:
        inset = 42
        t0, t1 = inset / L, 1 - inset / L
        ax, ay = x0 + dx * t0, y0 + dy * t0
        bx, by = x0 + dx * t1, y0 + dy * t1
        sx, sy = -dy / L * SLIT / 2, dx / L * SLIT / 2
        pen.moveTo((ax - sx, ay - sy))
        pen.lineTo((bx - sx, by - sy))
        pen.lineTo((bx + sx, by + sy))
        pen.lineTo((ax + sx, ay + sy))
        pen.closePath()

def vesica(pen, x0, x1, y0, y1, w=THIN, peak=PEAK):
    """Pointed-arch ring (gothic O). x0/x1 outer edges, y0 bottom, y1 top."""
    cx = (x0 + x1) / 2
    mid = (y0 + y1) / 2
    # outer CW: bottom point -> left curve up to peak -> right curve down
    pen.moveTo((cx, y0))
    pen.qCurveTo((x0, mid), (cx, y1 + peak))
    pen.qCurveTo((x1, mid), (cx, y0))
    pen.closePath()
    # inner counter CCW
    ix0, ix1 = x0 + w, x1 - w
    iy0, iy1 = y0 + w, y1 - w
    icx = (ix0 + ix1) / 2
    imid = (iy0 + iy1) / 2
    pen.moveTo((icx, iy0))
    pen.qCurveTo((ix1, imid), (icx, iy1 + peak - 18))
    pen.qCurveTo((ix0, imid), (icx, iy0))
    pen.closePath()

def half_bowl(pen, x, x1, y0, y1, w=THIN, peak=PEAK):
    """Right half-bowl (D/P/B): flat left edge at x, arch bulge to x1."""
    mid = (y0 + y1) / 2
    pen.moveTo((x, y0))
    pen.lineTo((x, y1))
    pen.qCurveTo((x1, mid + (y1 - y0) * 0.18), (x1, mid))
    pen.qCurveTo((x1, mid - (y1 - y0) * 0.18), (x, y0))
    pen.closePath()
    ix, ix1 = x + w, x1 - w
    iy0, iy1 = y0 + w, y1 - w
    imid = (iy0 + iy1) / 2
    pen.moveTo((ix, iy0))
    pen.qCurveTo((ix1, imid - (iy1 - iy0) * 0.18), (ix1, imid))
    pen.qCurveTo((ix1, imid + (iy1 - iy0) * 0.18), (ix, iy1))
    pen.lineTo((ix, iy0))
    pen.closePath()

def arch_c(pen, x0, x1, y0, y1, w=THIN, peak=PEAK):
    """C shape open to the right: one stroked contour."""
    mid = (y0 + y1) / 2
    ix0, ix1, iy0, iy1 = x0 + w, x1 - w, y0 + w, y1 - w
    imid = (iy0 + iy1) / 2
    pen.moveTo((x1, y1))                       # outer top-right end
    pen.qCurveTo((x0, y1), (x0, mid))          # outer left, top half
    pen.qCurveTo((x0, y0), (x1, y0))           # outer left, bottom half
    pen.lineTo((ix1, iy0))                     # inner bottom-right end
    pen.qCurveTo((ix0, iy0), (ix0, imid))      # inner left, bottom half
    pen.qCurveTo((ix0, iy1), (ix1, iy1))       # inner left, top half
    pen.closePath()

def diamond(pen, cx, cy, s=46):
    pen.moveTo((cx, cy - s))
    pen.lineTo((cx + s, cy))
    pen.lineTo((cx, cy + s))
    pen.lineTo((cx - s, cy))
    pen.closePath()

# ---------------------------------------------------------------- glyphs
G = {}   # name -> (advance, draw_fn)
def glyph(name, adv):
    def deco(fn):
        G[name] = (adv, fn)
        return fn
    return deco

W = 640   # default cap advance
# ---- CAPS ----
@glyph('A', 660)
def _A(p):
    diag(p, 60, 0, 330, CAP, w=STEM)
    diag(p, 600, 0, 330, CAP, w=STEM)
    hbar(p, 175, 485, 250)
    node(p, 330, 560)

@glyph('B', 620)
def _B(p):
    stem(p, 40, 0, CAP)
    half_bowl(p, 40, 580, 380, CAP)
    half_bowl(p, 40, 560, 0, 380)

@glyph('C', 620)
def _C(p):
    arch_c(p, 60, 580, 0, CAP)
    node(p, 320, 360)

@glyph('D', 640)
def _D(p):
    stem(p, 40, 0, CAP)
    half_bowl(p, 40, 600, 0, CAP)

@glyph('E', 580)
def _E(p):
    stem(p, 40, 0, CAP)
    hbar(p, 40, 540, CAP - THIN, THIN)
    hbar(p, 40, 480, 330)
    hbar(p, 40, 540, 0, THIN)

@glyph('F', 540)
def _F(p):
    stem(p, 40, 0, CAP)
    hbar(p, 40, 520, CAP - THIN, THIN)
    hbar(p, 40, 460, 330)

@glyph('G', 640)
def _G(p):
    arch_c(p, 60, 580, 0, CAP)
    hbar(p, 330, 580, 300)
    stem(p, 480, 0, 340, w=100, peak=0, slit=False)

@glyph('H', 660)
def _H(p):
    stem(p, 40, 0, CAP)
    stem(p, 470, 0, CAP)
    hbar(p, 40, 620, 330)

@glyph('I', 380)
def _I(p):
    stem(p, 115, 0, CAP)
    hbar(p, 40, 340, CAP - THIN, THIN)
    hbar(p, 40, 340, 0, THIN)

@glyph('J', 560)
def _J(p):
    stem(p, 380, 140, CAP, peak=PEAK)
    # hook: curve at bottom left
    p.moveTo((380, 140))
    p.qCurveTo((380, -40), (210, -40))
    p.qCurveTo((90, -40), (90, 120))
    p.lineTo((90, 200))
    p.qCurveTo((90, 60), (210, 60))
    p.qCurveTo((290, 60), (290, 140))
    p.closePath()

@glyph('K', 640)
def _K(p):
    stem(p, 40, 0, CAP)
    diag(p, 480, CAP, 230, 360, w=STEM)
    diag(p, 240, 330, 540, 0, w=STEM)

@glyph('L', 560)
def _L(p):
    stem(p, 40, 0, CAP)
    hbar(p, 40, 520, 0, THIN)

@glyph('M', 820)
def _M(p):
    stem(p, 40, 0, CAP)
    stem(p, 630, 0, CAP)
    diag(p, 190, CAP, 410, 300, w=STEM)
    diag(p, 630, CAP, 410, 300, w=STEM)

@glyph('N', 680)
def _N(p):
    stem(p, 40, 0, CAP)
    stem(p, 490, 0, CAP)
    diag(p, 190, CAP, 490, 0, w=STEM)

@glyph('O', 680)
def _O(p):
    vesica(p, 50, 630, 0, CAP)
    node(p, 340, 360)

@glyph('P', 600)
def _P(p):
    stem(p, 40, 0, CAP)
    half_bowl(p, 40, 580, 360, CAP)

@glyph('Q', 680)
def _Q(p):
    vesica(p, 50, 630, 0, CAP)
    diag(p, 420, 200, 620, -60, w=90, slit=False)

@glyph('R', 620)
def _R(p):
    stem(p, 40, 0, CAP)
    half_bowl(p, 40, 580, 360, CAP)
    diag(p, 250, 360, 520, 0, w=110, slit=False)

@glyph('S', 600)
def _S(p):
    # top arch opens bottom-right, bottom arch opens top-left
    arch_c(p, 60, 560, 360, CAP)
    # bottom: mirrored C (open left) built from arch_c rotated via transform:
    # draw a C open to the left manually
    mid = 180
    p.moveTo((60, 0))
    p.qCurveTo((560, 0), (560, 180))
    p.qCurveTo((560, 360), (60, 360))
    p.lineTo((115, 305))
    p.qCurveTo((505, 305), (505, 180))
    p.qCurveTo((505, 55), (60, 55))
    p.closePath()

@glyph('T', 620)
def _T(p):
    hbar(p, 30, 590, CAP - THIN, THIN)
    stem(p, 235, 0, CAP - THIN, peak=0)

@glyph('U', 680)
def _U(p):
    # stroked U: outer down left, bottom curve, up right; inner back
    p.moveTo((50, CAP + PEAK))
    p.lineTo((50, 120))
    p.qCurveTo((50, -30), (340, -30))
    p.qCurveTo((630, -30), (630, 120))
    p.lineTo((630, CAP + PEAK))
    p.lineTo((630, CAP))
    p.lineTo((575, CAP))
    p.lineTo((575, 140))
    p.qCurveTo((575, 60), (340, 60))
    p.qCurveTo((105, 60), (105, 140))
    p.lineTo((105, CAP))
    p.lineTo((50, CAP))
    p.closePath()

@glyph('V', 680)
def _V(p):
    diag(p, 60, CAP, 340, 0, w=STEM)
    diag(p, 620, CAP, 340, 0, w=STEM)

@glyph('W', 900)
def _W(p):
    diag(p, 60, CAP, 240, 0, w=STEM)
    diag(p, 420, CAP, 240, 0, w=STEM)
    diag(p, 480, CAP, 660, 0, w=STEM)
    diag(p, 840, CAP, 660, 0, w=STEM)

@glyph('X', 680)
def _X(p):
    diag(p, 60, CAP, 620, 0, w=STEM)
    diag(p, 620, CAP, 60, 0, w=STEM)

@glyph('Y', 640)
def _Y(p):
    diag(p, 60, CAP, 320, 330, w=STEM)
    diag(p, 580, CAP, 320, 330, w=STEM)
    stem(p, 245, 0, 360, peak=0)

@glyph('Z', 600)
def _Z(p):
    hbar(p, 40, 560, CAP - THIN, THIN)
    hbar(p, 40, 560, 0, THIN)
    diag(p, 520, CAP - THIN, 80, THIN, w=STEM)

# ---- lowercase (x-height 500) ----
@glyph('a', 560)
def _a(p):
    vesica(p, 50, 510, 0, XH, peak=40)
    stem(p, 400, 0, XH, w=110, peak=0, slit=False)

@glyph('b', 560)
def _b(p):
    stem(p, 40, 0, ASC)
    half_bowl(p, 40, 520, 0, XH)

@glyph('c', 520)
def _c(p):
    arch_c(p, 50, 500, 0, XH, peak=40)

@glyph('d', 560)
def _d(p):
    vesica(p, 50, 510, 0, XH, peak=40)
    stem(p, 400, 0, ASC, w=110, peak=PEAK, slit=False)

@glyph('e', 540)
def _e(p):
    arch_c(p, 50, 510, 0, XH, peak=40)
    hbar(p, 50, 510, 210)

@glyph('f', 420)
def _f(p):
    p.moveTo((150, 0))
    p.lineTo((150, 640))
    p.qCurveTo((150, 760), (300, 760))
    p.lineTo((300, 705))
    p.qCurveTo((230, 705), (230, 640))
    p.lineTo((230, 0))
    p.closePath()
    hbar(p, 90, 360, 480)

@glyph('g', 560)
def _g(p):
    vesica(p, 50, 510, 0, XH, peak=40)
    stem(p, 400, -200, XH, w=110, peak=0, slit=False)
    p.moveTo((400, -200))
    p.qCurveTo((400, -280), (280, -280))
    p.qCurveTo((160, -280), (160, -160))
    p.lineTo((160, -110))
    p.qCurveTo((160, -200), (280, -200))
    p.qCurveTo((330, -200), (330, -150))
    p.closePath()

@glyph('h', 580)
def _h(p):
    stem(p, 40, 0, ASC)
    p.moveTo((190, 0))
    p.lineTo((190, 420))
    p.qCurveTo((190, 540), (330, 540))
    p.qCurveTo((470, 540), (470, 420))
    p.lineTo((470, 0))
    p.lineTo((470, 60))
    p.lineTo((390, 60))
    p.lineTo((390, 400))
    p.qCurveTo((390, 460), (330, 460))
    p.qCurveTo((270, 460), (270, 400))
    p.lineTo((270, 0))
    p.closePath()

@glyph('i', 300)
def _i(p):
    stem(p, 75, 0, XH, w=130, peak=0, slit=False)
    diamond(p, 140, 620, 42)

@glyph('j', 340)
def _j(p):
    stem(p, 150, -160, XH, w=130, peak=0, slit=False)
    p.moveTo((150, -160))
    p.qCurveTo((150, -240), (60, -240))
    p.qCurveTo((10, -240), (10, -140))
    p.lineTo((10, -90))
    p.qCurveTo((10, -160), (80, -160))
    p.qCurveTo((110, -160), (110, -120))
    p.closePath()
    diamond(p, 215, 620, 42)

@glyph('k', 560)
def _k(p):
    stem(p, 40, 0, ASC)
    diag(p, 440, XH, 220, 240, w=110, slit=False)
    diag(p, 230, 220, 500, 0, w=110, slit=False)

@glyph('l', 300)
def _l(p):
    stem(p, 75, 0, ASC, w=130)

@glyph('m', 820)
def _m(p):
    stem(p, 40, 0, XH, w=120, peak=40)
    for x in (160, 440):
        p.moveTo((x, 0))
        p.lineTo((x, 420))
        p.qCurveTo((x, 540), (x + 140, 540))
        p.qCurveTo((x + 280, 540), (x + 280, 420))
        p.lineTo((x + 280, 0))
        p.lineTo((x + 280, 60))
        p.lineTo((x + 200, 60))
        p.lineTo((x + 200, 400))
        p.qCurveTo((x + 200, 460), (x + 140, 460))
        p.qCurveTo((x + 80, 460), (x + 80, 400))
        p.lineTo((x + 80, 0))
        p.closePath()

@glyph('n', 580)
def _n(p):
    stem(p, 40, 0, XH, w=120, peak=40)
    p.moveTo((160, 0))
    p.lineTo((160, 420))
    p.qCurveTo((160, 540), (300, 540))
    p.qCurveTo((440, 540), (440, 420))
    p.lineTo((440, 0))
    p.lineTo((440, 60))
    p.lineTo((360, 60))
    p.lineTo((360, 400))
    p.qCurveTo((360, 460), (300, 460))
    p.qCurveTo((240, 460), (240, 400))
    p.lineTo((240, 0))
    p.closePath()

@glyph('o', 540)
def _o(p):
    vesica(p, 50, 500, 0, XH, peak=40)

@glyph('p', 560)
def _p(p):
    stem(p, 40, DESC, XH, w=120, peak=40)
    half_bowl(p, 40, 520, 0, XH)

@glyph('q', 560)
def _q(p):
    vesica(p, 50, 510, 0, XH, peak=40)
    stem(p, 400, DESC, XH, w=110, peak=0, slit=False)

@glyph('r', 420)
def _r(p):
    stem(p, 40, 0, XH, w=120, peak=40)
    p.moveTo((160, 300))
    p.qCurveTo((160, 540), (380, 540))
    p.lineTo((380, 460))
    p.qCurveTo((250, 460), (240, 300))
    p.closePath()

@glyph('s', 520)
def _s(p):
    arch_c(p, 50, 480, 250, XH, peak=35)
    mid = 125
    p.moveTo((50, 0))
    p.qCurveTo((480, 0), (480, 125))
    p.qCurveTo((480, 250), (50, 250))
    p.lineTo((105, 195))
    p.qCurveTo((425, 195), (425, 125))
    p.qCurveTo((425, 55), (50, 55))
    p.closePath()

@glyph('t', 420)
def _t(p):
    stem(p, 110, 0, 620, w=130, peak=0, slit=False)
    p.moveTo((110, 0))
    p.qCurveTo((110, -60), (210, -60))
    p.qCurveTo((290, -60), (290, 20))
    p.lineTo((290, 60))
    p.qCurveTo((290, 20), (210, 20))
    p.qCurveTo((190, 20), (190, 60))
    p.closePath()
    hbar(p, 50, 330, 380)

@glyph('u', 580)
def _u(p):
    p.moveTo((50, XH))
    p.lineTo((50, 120))
    p.qCurveTo((50, -20), (290, -20))
    p.qCurveTo((530, -20), (530, 120))
    p.lineTo((530, XH))
    p.lineTo((530, 460))
    p.lineTo((450, 460))
    p.lineTo((450, 140))
    p.qCurveTo((450, 60), (290, 60))
    p.qCurveTo((130, 60), (130, 140))
    p.lineTo((130, XH))
    p.lineTo((50, XH))
    p.closePath()

@glyph('v', 560)
def _v(p):
    diag(p, 50, XH, 280, 0, w=110, slit=False)
    diag(p, 510, XH, 280, 0, w=110, slit=False)

@glyph('w', 820)
def _w(p):
    diag(p, 50, XH, 210, 0, w=110, slit=False)
    diag(p, 370, XH, 210, 0, w=110, slit=False)
    diag(p, 450, XH, 610, 0, w=110, slit=False)
    diag(p, 770, XH, 610, 0, w=110, slit=False)

@glyph('x', 560)
def _x(p):
    diag(p, 50, XH, 510, 0, w=110, slit=False)
    diag(p, 510, XH, 50, 0, w=110, slit=False)

@glyph('y', 560)
def _y(p):
    diag(p, 50, XH, 280, 60, w=110, slit=False)
    diag(p, 510, XH, 280, 60, w=110, slit=False)
    diag(p, 280, 60, 180, DESC, w=110, slit=False)

@glyph('z', 520)
def _z(p):
    hbar(p, 40, 480, XH - THIN, THIN)
    hbar(p, 40, 480, 0, THIN)
    diag(p, 440, XH - THIN, 80, THIN, w=110, slit=False)

# ---- digits ----
@glyph('zero', 680)
def _zero(p):
    vesica(p, 50, 630, 0, CAP)
    diag(p, 240, 560, 440, 160, w=40, slit=False)

@glyph('one', 420)
def _one(p):
    diag(p, 260, CAP, 130, 520, w=90, slit=False)
    stem(p, 170, 0, CAP, w=130, peak=0, slit=False)
    hbar(p, 60, 360, 0, THIN)

@glyph('two', 620)
def _two(p):
    arch_c(p, 60, 560, 360, CAP)
    diag(p, 520, 360, 80, 60, w=110, slit=False)
    hbar(p, 60, 560, 0, THIN)

@glyph('three', 600)
def _three(p):
    half_bowl(p, 60, 560, 360, CAP)
    half_bowl(p, 60, 540, 0, 360)

@glyph('four', 620)
def _four(p):
    diag(p, 460, CAP, 120, 180, w=110, slit=False)
    hbar(p, 60, 560, 180)
    stem(p, 400, 0, CAP, w=120, peak=0, slit=False)

@glyph('five', 600)
def _five(p):
    hbar(p, 60, 540, CAP - THIN, THIN)
    stem(p, 60, 330, CAP - THIN, w=120, peak=0, slit=False)
    half_bowl(p, 60, 560, 0, 360)

@glyph('six', 620)
def _six(p):
    vesica(p, 60, 560, 0, 420)
    p.moveTo((60, 360))
    p.qCurveTo((60, 720), (330, 720))
    p.lineTo((330, 640))
    p.qCurveTo((150, 640), (140, 420))
    p.closePath()

@glyph('seven', 560)
def _seven(p):
    hbar(p, 60, 520, CAP - THIN, THIN)
    diag(p, 480, CAP - THIN, 180, 0, w=110, slit=False)

@glyph('eight', 620)
def _eight(p):
    vesica(p, 70, 550, 360, CAP, peak=40)
    vesica(p, 60, 560, 0, 360, peak=40)

@glyph('nine', 620)
def _nine(p):
    vesica(p, 60, 560, 300, CAP, peak=40)
    p.moveTo((560, 360))
    p.qCurveTo((560, 0), (290, 0))
    p.lineTo((290, 80))
    p.qCurveTo((470, 80), (480, 300))
    p.closePath()

# ---- punctuation ----
@glyph('period', 300)
def _period(p):
    diamond(p, 150, 60, 52)

@glyph('comma', 300)
def _comma(p):
    diamond(p, 150, 60, 52)
    diag(p, 190, 40, 120, -180, w=70, slit=False)

@glyph('exclam', 320)
def _exclam(p):
    stem(p, 95, 220, CAP, w=130, peak=PEAK, slit=False)
    diamond(p, 160, 60, 52)

@glyph('question', 600)
def _question(p):
    arch_c(p, 60, 540, 380, CAP)
    diag(p, 300, 380, 300, 240, w=90, slit=False)
    diamond(p, 300, 90, 52)

@glyph('hyphen', 400)
def _hyphen(p):
    hbar(p, 60, 340, 300)

@glyph('quotesingle', 280)
def _quotesingle(p):
    diag(p, 200, 700, 130, 480, w=70, slit=False)

@glyph('colon', 320)
def _colon(p):
    diamond(p, 160, 430, 48)
    diamond(p, 160, 90, 48)

@glyph('semicolon', 320)
def _semicolon(p):
    diamond(p, 160, 430, 48)
    diamond(p, 160, 60, 48)
    diag(p, 200, 40, 130, -170, w=60, slit=False)

@glyph('ampersand', 700)
def _amp(p):
    # upper loop (small vesica), lower loop (wider vesica), one cross stroke
    vesica(p, 150, 450, 330, CAP, peak=35)
    vesica(p, 80, 520, 0, 330, peak=35)
    diag(p, 480, 640, 120, 40, w=70, slit=False)

@glyph('space', 300)
def _space(p):
    pass

# ---------------------------------------------------------------- assembly
CMAP = {}
for ch in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    CMAP[ord(ch)] = ch
for ch in 'abcdefghijklmnopqrstuvwxyz':
    CMAP[ord(ch)] = ch
for ch, nm in zip('0123456789', ['zero','one','two','three','four','five','six','seven','eight','nine']):
    CMAP[ord(ch)] = nm
CMAP.update({ord('.'): 'period', ord(','): 'comma', ord('!'): 'exclam',
             ord('?'): 'question', ord('-'): 'hyphen', ord("'"): 'quotesingle',
             ord(':'): 'colon', ord(';'): 'semicolon', ord('&'): 'ampersand',
             ord(' '): 'space'})

def build():
    order = ['.notdef', 'space'] + sorted(
        set(G) - {'space'},
        key=lambda n: (len(n), n))
    fb = FontBuilder(UPM, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(CMAP)
    glyphs = {}
    hmtx = {}
    for name in order:
        pen = TTGlyphPen(None)
        if name == '.notdef':
            pen.moveTo((0, 0)); pen.lineTo((0, CAP)); pen.lineTo((500, CAP))
            pen.lineTo((500, 0)); pen.closePath()
            adv = 500
        else:
            adv, fn = G[name]
            fn(pen)
        glyphs[name] = pen.glyph()
        hmtx[name] = (adv, 0)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(hmtx)
    fb.setupHorizontalHeader(ascent=ASC + 60, descent=DESC - 40)
    fb.setupNameTable({
        'familyName': 'Afterhours',
        'styleName': 'Regular',
        'uniqueFontIdentifier': 'Afterhours-Regular-1.0',
        'fullName': 'Afterhours Regular',
        'version': 'Version 1.000',
        'psName': 'Afterhours-Regular',
        'description': 'Afterhours: a Gothic manuscript hacked by a future city. '
                       'Pointed-arch blackletter bones, neon inline slits and '
                       'circuit-node counters. Original work, drawn from scratch.',
        'manufacturer': 'bayusd',
        'designer': 'bayusd',
        'licenseDescription': 'Free for personal use. '
                              'Submitted for the Taskmarket font bounty TSK-1ZQ87Q8M.',
    })
    fb.setupOS2(sTypoAscender=ASC + 60, sTypoDescender=DESC - 40,
                usWinAscent=ASC + 60, usWinDescent=-(DESC - 40))
    fb.setupPost()
    fb.setupMaxp()
    path = os.path.join(OUT, 'Afterhours-Regular.otf')
    fb.save(path)
    print('saved', path, os.path.getsize(path), 'bytes; glyphs:', len(order))
    return path

if __name__ == '__main__':
    build()
