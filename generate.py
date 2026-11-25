
from PIL import Image, ImageDraw, ImageFont
import math
import os

# Canvas and animation
WIDTH, HEIGHT = 1200, 400
FRAMES = 30
FRAME_DURATION = 120

os.makedirs("assets", exist_ok=True)

# Fonts
PIXEL_FONT = "assets/fonts/PixelifySans.ttf"
REGULAR_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

if not os.path.exists(PIXEL_FONT):
    raise FileNotFoundError(f"Font not found: {PIXEL_FONT}")

title_font = ImageFont.truetype(PIXEL_FONT, 48)
subtitle_font = ImageFont.truetype(REGULAR_FONT, 19)

NAME = "alison kieselack"
SUBTITLE = "GATHER · BUILD · GROW"

# Day and night palettes
PALETTES = {
    "day": {
        "background": "#F2EBD8",
        "sky": "#DCE9E6",
        "distant": "#C6DCE0",
        "ground": "#A9BE9B",
        "dark_ground": "#82977B",
        "text": "#59685A",
        "subtitle": "#82977B",
        "white": "#F8F5EA",
        "sand": "#D6BFA5",
        "flower": "#D8B9A9",
    },
    "night": {
        "background": "#DCE9E6",
        "sky": "#536779",
        "distant": "#718895",
        "ground": "#71836F",
        "dark_ground": "#526653",
        "text": "#F2EBD8",
        "subtitle": "#D6BFA5",
        "white": "#F2EBD8",
        "sand": "#A9BE9B",
        "flower": "#D8B9A9",
    }
}


def draw_cloud(draw, x, y, colour):
    draw.rectangle([x, y + 8, x + 54, y + 20], fill=colour)
    draw.rectangle([x + 10, y, x + 30, y + 18], fill=colour)
    draw.rectangle([x + 28, y + 4, x + 45, y + 18], fill=colour)


def draw_stars(draw, frame, palette):
    positions = [
        (160, 80), (300, 120), (460, 65),
        (760, 90), (940, 130), (1080, 65),
        (850, 180), (240, 190)
    ]

    for i, (x, y) in enumerate(positions):
        visible = (frame + i * 4) % 12 < 8
        if visible:
            draw.rectangle(
                [x, y, x + 3, y + 3],
                fill=palette["white"]
            )


def draw_moon(draw, palette):
    draw.ellipse([950, 45, 1000, 95], fill=palette["white"])
    draw.ellipse([965, 35, 1010, 85], fill=palette["sky"])


def draw_flower(draw, x, y, sway, palette):
    px = x + sway

    draw.rectangle(
        [x + 7, y + 12, x + 9, y + 31],
        fill=palette["dark_ground"]
    )
    draw.rectangle(
        [x - 1, y + 21, x + 7, y + 24],
        fill=palette["ground"]
    )
    draw.rectangle(
        [x + 9, y + 25, x + 16, y + 28],
        fill=palette["ground"]
    )

    flower = palette["flower"]
    draw.rectangle([px + 4, y, px + 10, y + 5], fill=flower)
    draw.rectangle([px - 2, y + 5, px + 4, y + 11], fill=flower)
    draw.rectangle([px + 10, y + 5, px + 16, y + 11], fill=flower)
    draw.rectangle([px + 4, y + 11, px + 10, y + 16], fill=flower)
    draw.rectangle([px + 4, y + 5, px + 10, y + 11], fill=palette["sand"])


def draw_landscape(draw, palette):
    ground_y = 345

    draw.rectangle(
        [0, ground_y, WIDTH, HEIGHT],
        fill=palette["ground"]
    )
    draw.rectangle(
        [0, ground_y + 15, WIDTH, HEIGHT],
        fill=palette["dark_ground"]
    )

    for x in [90, 180, 1020, 1100]:
        draw.rectangle(
            [x, ground_y - 5, x + 3, ground_y + 5],
            fill=palette["dark_ground"]
        )
        draw.rectangle(
            [x - 4, ground_y, x + 7, ground_y + 3],
            fill=palette["dark_ground"]
        )

    for x, y in [
        (260, 365), (290, 372), (900, 360),
        (940, 375), (150, 380), (1060, 370)
    ]:
        draw.rectangle(
            [x, y, x + 5, y + 5],
            fill=palette["sand"]
        )


def generate_banner(mode):
    palette = PALETTES[mode]
    frames = []

    for frame_number in range(FRAMES):
        image = Image.new(
            "RGB",
            (WIDTH, HEIGHT),
            palette["background"]
        )
        draw = ImageDraw.Draw(image)

        # Sky and border
        draw.rectangle(
            [12, 12, WIDTH - 12, HEIGHT - 12],
            fill=palette["sky"]
        )
        draw.rectangle(
            [12, 12, WIDTH - 13, HEIGHT - 13],
            outline=palette["background"],
            width=5
        )

        if mode == "day":
            cloud_offset = frame_number * 1.2
            cloud1_x = int((100 + cloud_offset) % 1250) - 50
            cloud2_x = int((700 + cloud_offset * 0.65) % 1300) - 50

            draw_cloud(draw, cloud1_x, 75, palette["white"])
            draw_cloud(draw, cloud2_x, 115, palette["white"])
        else:
            draw_stars(draw, frame_number, palette)
            draw_moon(draw, palette)

        # Distant landscape
        draw.rectangle(
            [0, 315, WIDTH, 345],
            fill=palette["distant"]
        )

        # Name
        title_box = draw.textbbox((0, 0), NAME, font=title_font)
        title_width = title_box[2] - title_box[0]

        draw.text(
            ((WIDTH - title_width) / 2, 155),
            NAME,
            font=title_font,
            fill=palette["text"]
        )

        # Subtitle
        subtitle_box = draw.textbbox(
            (0, 0), SUBTITLE, font=subtitle_font
        )
        subtitle_width = subtitle_box[2] - subtitle_box[0]

        draw.text(
            ((WIDTH - subtitle_width) / 2, 220),
            SUBTITLE,
            font=subtitle_font,
            fill=palette["subtitle"]
        )

        draw_landscape(draw, palette)

        sway = round(
            math.sin(frame_number * 2 * math.pi / FRAMES)
        )
        draw_flower(draw, 594, 330, sway, palette)

        frames.append(image)

    output = f"assets/name-banner-{mode}.gif"

    frames[0].save(
        output,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION,
        loop=0,
        optimize=False
    )

    print(f"Banner generated: {output}")


if __name__ == "__main__":
    generate_banner("day")
    generate_banner("night")
