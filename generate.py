
from PIL import Image, ImageDraw, ImageFont
import math
import os

# --------------------------------------------------
# Canvas and animation
# --------------------------------------------------

WIDTH, HEIGHT = 1200, 400
FRAMES = 30
FRAME_DURATION = 120

os.makedirs("assets", exist_ok=True)

# Muted pastel palette
CREAM = "#F2EBD8"
SKY = "#DCE9E6"
SKY_BLUE = "#C6DCE0"
SAGE = "#A9BE9B"
DARK_SAGE = "#82977B"
SAND = "#D6BFA5"
TERRACOTTA = "#D8B9A9"
TEXT = "#59685A"
WHITE = "#F8F5EA"

# --------------------------------------------------
# Fonts
# --------------------------------------------------

def get_font(size, bold=False):
    paths = [
        "assets/fonts/PixelifySans.ttf"
        if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    ]

    for path in paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)

    return ImageFont.load_default()


title_font = get_font(43, bold=True)
subtitle_font = get_font(19)

NAME = "alison kieselack"
SUBTITLE = "GATHER · BUILD · GROW"

# --------------------------------------------------
# Drawing helpers
# --------------------------------------------------

def draw_cloud(draw, x, y, scale=1):
    """Simple blocky pixel cloud."""
    s = scale
    colour = WHITE

    draw.rectangle(
        [x, y + 8*s, x + 54*s, y + 20*s],
        fill=colour
    )
    draw.rectangle(
        [x + 10*s, y, x + 30*s, y + 18*s],
        fill=colour
    )
    draw.rectangle(
        [x + 28*s, y + 4*s, x + 45*s, y + 18*s],
        fill=colour
    )


def draw_flower(draw, x, y, sway=0):
    """Small pixel flower used as the footer decoration."""
    # Stem
    draw.rectangle(
        [x + 7, y + 12, x + 9, y + 31],
        fill=DARK_SAGE
    )

    # Leaves
    draw.rectangle(
        [x - 1, y + 21, x + 7, y + 24],
        fill=SAGE
    )
    draw.rectangle(
        [x + 9, y + 25, x + 16, y + 28],
        fill=SAGE
    )

    # Flower petals, with a tiny amount of movement
    px = x + sway
    py = y

    draw.rectangle([px + 4, py, px + 10, py + 5], fill=TERRACOTTA)
    draw.rectangle([px - 2, py + 5, px + 4, py + 11], fill=TERRACOTTA)
    draw.rectangle([px + 10, py + 5, px + 16, py + 11], fill=TERRACOTTA)
    draw.rectangle([px + 4, py + 11, px + 10, py + 16], fill=TERRACOTTA)

    # Centre
    draw.rectangle([px + 4, py + 5, px + 10, py + 11], fill=SAND)


def draw_landscape(draw):
    """Quiet landscape along the bottom edge."""
    ground_y = 345

    draw.rectangle(
        [0, ground_y, WIDTH, HEIGHT],
        fill=SAGE
    )

    # Soft second layer of ground
    draw.rectangle(
        [0, ground_y + 15, WIDTH, HEIGHT],
        fill=DARK_SAGE
    )

    # Small grass tufts
    for x in [90, 180, 1020, 1100]:
        draw.rectangle(
            [x, ground_y - 5, x + 3, ground_y + 5],
            fill=DARK_SAGE
        )
        draw.rectangle(
            [x - 4, ground_y, x + 7, ground_y + 3],
            fill=DARK_SAGE
        )

    # Small decorative pixel patches
    for x, y in [
        (260, 365), (290, 372), (900, 360),
        (940, 375), (150, 380), (1060, 370)
    ]:
        draw.rectangle([x, y, x + 5, y + 5], fill=SAND)


# --------------------------------------------------
# Build frames
# --------------------------------------------------

frames = []

for frame_number in range(FRAMES):
    image = Image.new("RGB", (WIDTH, HEIGHT), CREAM)
    draw = ImageDraw.Draw(image)

    # Background
    draw.rectangle([12, 12, WIDTH - 12, HEIGHT - 12], fill=SKY)

    # Thin cream border
    draw.rectangle(
        [12, 12, WIDTH - 13, HEIGHT - 13],
        outline=CREAM,
        width=5
    )

    # Slowly drifting clouds
    cloud_offset = frame_number * 1.2

    cloud1_x = int((100 + cloud_offset) % 1250) - 50
    cloud2_x = int((700 + cloud_offset * 0.65) % 1300) - 50

    draw_cloud(draw, cloud1_x, 75, scale=1)
    draw_cloud(draw, cloud2_x, 115, scale=1)

    # A little distant landscape
    draw.rectangle([0, 315, WIDTH, 345], fill=SKY_BLUE)

    # Main text
    title_box = draw.textbbox((0, 0), NAME, font=title_font)
    title_width = title_box[2] - title_box[0]

    draw.text(
        ((WIDTH - title_width) / 2, 155),
        NAME,
        font=title_font,
        fill=TEXT
    )

    subtitle_box = draw.textbbox((0, 0), SUBTITLE, font=subtitle_font)
    subtitle_width = subtitle_box[2] - subtitle_box[0]

    draw.text(
        ((WIDTH - subtitle_width) / 2, 220),
        SUBTITLE,
        font=subtitle_font,
        fill=DARK_SAGE
    )

    # Landscape and footer decoration
    draw_landscape(draw)

    # Tiny flower near the bottom centre
    sway = round(math.sin(frame_number * 2 * math.pi / FRAMES))
    draw_flower(draw, 594, 330, sway=sway)

    frames.append(image)

# --------------------------------------------------
# Save animated GIF
# --------------------------------------------------

frames[0].save(
    "assets/name-banner.gif",
    save_all=True,
    append_images=frames[1:],
    duration=FRAME_DURATION,
    loop=0,
    optimize=False
)

print("Banner generated: assets/name-banner.gif")
