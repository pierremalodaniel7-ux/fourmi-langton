from hx import PHASES
def hd(dx, dy): return (abs(dx) + abs(dy) + abs(dx + dy)) // 2
RAD = max(hd(cx, cy) for (h, cs) in PHASES for (cx, cy) in cs)
DMAX = 2 * RAD + 2
