# Replace the generic leaf with the actual 5-leaflet cannabis fan.
import base64, math, re, sys

PATH = "index.html"
raw = open(PATH, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in raw else "\n"
src = raw.replace("\r\n", "\n")

def leaflet(base, angle_deg, length, halfw, teeth=5):
    a = math.radians(angle_deg)
    d = (math.sin(a), -math.cos(a))
    p = (math.cos(a), math.sin(a))
    L, R = [], []
    for i in range(teeth*2 + 1):
        t = 0.06 + 0.90 * i / (teeth*2)
        w = halfw * (math.sin(math.pi * (t ** 1.25)) ** 0.9)
        ser = 1.0 if i % 2 == 0 else 0.80
        L.append((base[0] + d[0]*length*t + p[0]*w*ser, base[1] + d[1]*length*t + p[1]*w*ser))
        R.append((base[0] + d[0]*length*t - p[0]*w*ser, base[1] + d[1]*length*t - p[1]*w*ser))
    tip = (base[0] + d[0]*length*1.02, base[1] + d[1]*length*1.02)
    return L + [tip] + R[::-1]

def weed_group(fill, opacity=1.0, transform=""):
    base = (50, 84)
    polys = []
    for ang, ln, hw in [(62, 50, 5.8), (33, 68, 7.4)]:
        polys.append(leaflet(base, -ang, ln, hw))
        polys.append(leaflet(base, ang, ln, hw))
    polys.append(leaflet(base, 0, 80, 8.6))
    polys.append([(48.7, 78), (51.3, 78), (51.0, 99), (49.0, 99)])   # stem
    d = "".join(
        "M" + " L".join("%.2f %.2f" % (x, y) for x, y in poly) + "Z" for poly in polys
    )
    tr = f' transform="{transform}"' if transform else ""
    return f'<path d="{d}" fill="{fill}" fill-opacity="{opacity}"{tr}/>'

def uri(svg):
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()

# background tile — two leaves, one big one small
tile = ('<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">'
        + weed_group("#ffffff", 0.085, "translate(6 4) scale(0.92) rotate(-8 100 100)")
        + weed_group("#ffffff", 0.06, "translate(118 118) scale(0.5) rotate(24 100 100)")
        + '</svg>')

# card texture — fainter and smaller so text stays calm
card = ('<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">'
        + weed_group("#ffffff", 0.045, "translate(14 10) scale(0.8) rotate(-10 100 100)")
        + '</svg>')

# watermark on the log button
mark = ('<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">'
        + weed_group("#ffffff", 0.55)
        + '</svg>')

# particle
part = ('<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">'
        + weed_group("#8ed46a", 0.95)
        + '</svg>')

new_uris = [uri(tile), uri(card), uri(mark), uri(part)]

# swap the four existing base64 SVGs, in CSS order: body tile, card tile, button leaf, particle
found = list(re.finditer(r'data:image/svg\+xml;base64,[A-Za-z0-9+/=]+', src))
print("data URIs present:", len(found))
icons = [m for m in found if m.start() < src.index("APPEARANCE")]
leaf_uris = [m for m in found if m.start() > src.index("APPEARANCE")]
print("appearance URIs:", len(leaf_uris))
if len(leaf_uris) != 4:
    print("FAIL: expected 4 appearance URIs"); sys.exit(1)

out = []
last = 0
for m, new in zip(leaf_uris, new_uris):
    out.append(src[last:m.start()])
    out.append(new)
    last = m.end()
out.append(src[last:])
src = "".join(out)

# the new tile is square 200; keep the sizing sensible
src = src.replace("background-size: 190px 190px, auto, auto, cover;", "background-size: 200px 200px, auto, auto, cover;")
src = src.replace("background-size:170px 170px, auto;", "background-size:200px 200px, auto;")

open(PATH, "w", encoding="utf-8", newline="").write(src.replace("\n", nl))
print("replaced with cannabis silhouette")
