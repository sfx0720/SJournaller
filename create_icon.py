"""
Generate application icon files (.ico, .png) for the build process.

Requires: pip install Pillow
Run:     python create_icon.py
Output:  assets/icon.ico, assets/icon.png
"""

import os
from PIL import Image, ImageDraw


def create_icon_image(size: int = 256) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    s = size / 64.0

    # Left page (blue)
    draw.rounded_rectangle(
        [int(4*s), int(8*s), int(30*s), int(56*s)],
        radius=int(3*s), fill=(137, 180, 250, 255),
    )
    # Right page (purple)
    draw.rounded_rectangle(
        [int(34*s), int(8*s), int(60*s), int(56*s)],
        radius=int(3*s), fill=(203, 166, 247, 255),
    )
    # Spine
    draw.rectangle(
        [int(28*s), int(6*s), int(36*s), int(58*s)],
        fill=(69, 71, 90, 255),
    )
    # Text lines
    for i in range(6):
        y = int(16*s + i * 7*s)
        w = max(1, int(0.8*s))
        draw.line([int(8*s), y, int(25*s), y], fill=(30, 30, 46, 180), width=w)
        draw.line([int(38*s), y, int(55*s), y], fill=(30, 30, 46, 180), width=w)

    return img


def main():
    os.makedirs("assets", exist_ok=True)

    img = create_icon_image(256)

    # Save PNG
    img.save("assets/icon.png", "PNG")
    print("Created assets/icon.png")

    # Save ICO with multiple sizes
    ico_sizes = [16, 24, 32, 48, 64, 128, 256]
    images = []
    for sz in ico_sizes:
        resized = img.resize((sz, sz), Image.LANCZOS)
        images.append(resized)

    # Pillow ICO save
    images[0].save(
        "assets/icon.ico",
        format="ICO",
        sizes=[(sz, sz) for sz in ico_sizes],
        append_images=images[1:],
    )
    print("Created assets/icon.ico")

    # Also create a small 16x16 for window icon
    small = img.resize((16, 16), Image.LANCZOS)
    small.save("assets/icon_16.png", "PNG")
    print("Created assets/icon_16.png")


if __name__ == "__main__":
    main()