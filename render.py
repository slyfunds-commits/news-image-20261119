from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


SIZE = 1024
PAPER = "#FFFFFF"
INK = "#171717"
MUTED = "#555555"
RULE = "#D9D9D6"
PANEL = "#FAFAF8"
ACCENT = "#B3362D"

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SANS = FONT_DIR / "DejaVuSans.ttf"
SANS_BOLD = FONT_DIR / "DejaVuSans-Bold.ttf"
SERIF_BOLD = FONT_DIR / "DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(str(path), size)


def lines_for(draw, text, face, width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if draw.textbbox((0, 0), candidate, font=face)[2] <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, text, xy, face, fill, width, leading):
    x, y = xy
    lines = lines_for(draw, text, face, width)
    for line in lines:
        draw.text((x, y), line, font=face, fill=fill)
        y += leading
    return y


def draw_lead(draw):
    x, y, w, h = 52, 164, 920, 212
    draw.rounded_rectangle((x, y, x + w, y + h), radius=8, fill=PANEL, outline=RULE, width=2)
    draw.rectangle((x, y, x + 8, y + h), fill=ACCENT)
    draw.text((x + 30, y + 20), "LEAD", font=font(SANS_BOLD, 16), fill=ACCENT)

    title = "World court rules Myanmar committed genocide"
    title_face = font(SERIF_BOLD, 36)
    title_bottom = draw_wrapped(draw, title, (x + 30, y + 48), title_face, INK, 850, 44)
    body = (
        "The International Court of Justice ruled Myanmar committed genocide against "
        "the Rohingya, the first such ruling against a state."
    )
    draw_wrapped(draw, body, (x + 30, title_bottom + 5), font(SANS, 19), MUTED, 850, 26)

    # A restrained globe-and-courthouse emblem, drawn entirely from vector shapes.
    cx, cy = x + w - 76, y + h - 43
    draw.ellipse((cx - 21, cy - 21, cx + 21, cy + 21), outline=ACCENT, width=2)
    draw.arc((cx - 10, cy - 21, cx + 10, cy + 21), 80, 280, fill=ACCENT, width=2)
    draw.arc((cx - 10, cy - 21, cx + 10, cy + 21), 260, 100, fill=ACCENT, width=2)
    draw.line((cx - 19, cy, cx + 19, cy), fill=ACCENT, width=2)


STORIES = [
    (
        "Trump, Xi and Putin issue joint declaration",
        "The three leaders held their first three-way summit in Shenzhen and issued a four-point 'Declaration toward Peace'.",
    ),
    (
        "Anthropic prices record $81bn IPO",
        "The AI developer priced its IPO at $83 a share, raising a record $81.34 billion.",
    ),
    (
        "Denmark approves Greenland-US security pact",
        "Denmark's parliament unanimously approved a defence pact with Greenland and the US.",
    ),
    (
        "Mongolia's president resigns",
        "Mongolia's parliament accepted President Khurelsukh's resignation after a railway-project scandal.",
    ),
    (
        "Israel's Gaza ground operation ends",
        "Israel's military ended its ground operation in central Gaza's Nuseirat camp, a day after it began.",
    ),
    (
        "47,000 evacuated ahead of Cyclone Akvan",
        "More than 47,000 people were evacuated in India ahead of Cyclone Akvan.",
    ),
]


def draw_story(draw, x, y, w, h, number, title, body):
    draw.rounded_rectangle((x, y, x + w, y + h), radius=7, fill=PANEL, outline=RULE, width=2)
    draw.rectangle((x, y, x + w, y + 5), fill=ACCENT)
    draw.text((x + 18, y + 15), f"{number:02d}", font=font(SANS_BOLD, 14), fill=ACCENT)

    title_face = font(SERIF_BOLD, 21)
    title_bottom = draw_wrapped(draw, title, (x + 18, y + 38), title_face, INK, w - 36, 27)
    draw_wrapped(
        draw,
        body,
        (x + 18, title_bottom + 8),
        font(SANS, 16),
        MUTED,
        w - 36,
        21,
    )


def main():
    image = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(image)

    draw.text((52, 30), "THE WORLD IN ONE PAGE", font=font(SERIF_BOLD, 48), fill=INK)
    draw.text(
        (55, 91),
        "THURSDAY, 19 NOVEMBER 2026",
        font=font(SANS_BOLD, 19),
        fill=INK,
    )
    draw.line((52, 133, 972, 133), fill=INK, width=2)

    draw_lead(draw)

    left, right = 52, 524
    card_w, card_h, gap_y = 448, 172, 14
    first_y = 394
    for index, (title, body) in enumerate(STORIES):
        col = index % 2
        row = index // 2
        draw_story(
            draw,
            left if col == 0 else right,
            first_y + row * (card_h + gap_y),
            card_w,
            card_h,
            index + 1,
            title,
            body,
        )

    draw.line((52, 958, 972, 958), fill=RULE, width=2)
    footer = "All stories as reported on 19 November 2026."
    footer_face = font(SANS, 16)
    footer_width = draw.textbbox((0, 0), footer, font=footer_face)[2]
    draw.text(((SIZE - footer_width) // 2, 972), footer, font=footer_face, fill=MUTED)

    image.save(Path(__file__).with_name("entry.png"), format="PNG", optimize=True)


if __name__ == "__main__":
    main()
