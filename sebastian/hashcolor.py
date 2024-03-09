import hashlib
from typing import Tuple


def color(phrase: str) -> str:
    m = hashlib.md5()  # nosec
    m.update(phrase.encode("utf-8"))
    return m.hexdigest()[:6]


def _adjust(v: int | float) -> float:
    v = float(v) / 255.0
    if v <= 0.0398:
        return v / 12.92
    else:
        return ((v + 0.055) / 1.055) ** 2.4


def luminosity(r: int | float, g: int | float, b: int | float) -> float:
    # using formula from http://www.w3.org/TR/WCAG20-GENERAL/G17.html
    [r, g, b] = [_adjust(v) for v in [r, g, b]]
    return (0.2126 * r) + (0.7152 * g) + (0.0722 * b)


def make_contrasting(
    color: str | Tuple[int, int, int]
) -> Tuple[int, int, int]:
    if isinstance(color, str):
        # hex -> triple
        color = color.strip("#")  # in case someone left it on there
        color = (int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16))
    (r, g, b) = color
    lum = luminosity(r, g, b)
    if lum >= 0.5:
        return (0, 0, 0)
    else:
        return (255, 255, 255)


if __name__ == "__main__":
    import random

    words = [line for line in open("/usr/share/dict/words")]
    random.shuffle(words)

    print("<table>")
    for word in words[:1000]:
        word = word.strip()
        hex = color(word)
        print("<tr>")
        bghex = "%02x%02x%02x" % make_contrasting(hex)
        print(
            """<td bgcolor="#%s"><font color="#%s">%s</font></td>"""
            % (hex, bghex, word)
        )
        print("</tr>")
    print("</table>")
