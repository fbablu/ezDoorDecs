import os
import pandas as pd
import requests
from PIL import Image, ImageDraw
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN


# Clash Royale card rarity colors
CARD_COLORS = {
    # Gray
    'common': {'primary': RGBColor(169, 169, 169), 'secondary': RGBColor(211, 211, 211)},
    # Orange
    'rare': {'primary': RGBColor(255, 140, 0), 'secondary': RGBColor(255, 165, 0)},
    # Purple
    'epic': {'primary': RGBColor(128, 0, 128), 'secondary': RGBColor(153, 50, 204)},
    # Gold/Yellow
    'legendary': {'primary': RGBColor(255, 215, 0), 'secondary': RGBColor(255, 255, 0)},
    # Bright Yellow
    'champion': {'primary': RGBColor(255, 255, 0), 'secondary': RGBColor(255, 215, 0)}
}

# Assign card rarities to residents (cycling through rarities)
CARD_RARITIES = ['common', 'rare', 'epic', 'legendary', 'champion']


def create_gradient_background(width, height, color1, color2):
    """Create a gradient background image"""
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)

    for y in range(height):
        # Calculate the blend ratio
        ratio = y / height

        # Interpolate between the two colors
        r = int(color1.r * (1 - ratio) + color2.r * ratio)
        g = int(color1.g * (1 - ratio) + color2.g * ratio)
        b = int(color1.b * (1 - ratio) + color2.b * ratio)

        draw.line([(0, y), (width, y)], fill=(r, g, b))

    return image


def fetch_and_save_image(image_url, image_filename):
    """Fetch and save card image"""
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))

        # Convert RGBA to RGB if needed
        if image.mode == 'RGBA':
            # Create white background for transparency
            white_bg = Image.new('RGB', image.size, (255, 255, 255))
            white_bg.paste(image, mask=image.split()
                           [-1] if len(image.split()) == 4 else None)
            image = white_bg

        # Save the image locally
        image.save(image_filename)
        return image_filename
    except Exception as e:
        print(f"Error fetching image: {e}")
        return None


def create_clash_royale_presentation(residents_df, image_urls):
    """Create Clash Royale themed presentation"""
    prs = Presentation()
    folder_path = 'clash_royale_images'
    os.makedirs(folder_path, exist_ok=True)

    for i in range(0, len(residents_df), 3):
        slide = prs.slides.add_slide(prs.slide_layouts[5])  # Blank slide

        # Add arena-style background
        main_left = Inches(0.3)
        main_top = Inches(0.3)
        main_width = Inches(9.4)
        main_height = Inches(7)

        # Create arena background with blue gradient
        main_shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            main_left, main_top, main_width, main_height
        )
        main_shape.fill.solid()
        main_shape.fill.fore_color.rgb = RGBColor(30, 144, 255)  # Arena blue
        main_shape.line.color.rgb = RGBColor(25, 25, 112)  # Dark blue border
        main_shape.line.width = Pt(4)

        # Add up to three residents per slide
        for j in range(3):
            index = i + j
            if index < len(residents_df):
                resident = residents_df.iloc[index]
                name = resident['Name']
                room = resident['Room']
                card = resident['Card']

                # Get card rarity for this resident
                rarity = CARD_RARITIES[index % len(CARD_RARITIES)]
                colors = CARD_COLORS[rarity]

                left = Inches(0.8 + j * 3)
                top = Inches(0.8)
                width = Inches(2.6)
                height = Inches(5.8)

                # Create card-style shape with rarity colors
                card_shape = slide.shapes.add_shape(
                    MSO_SHAPE.ROUNDED_RECTANGLE,
                    left, top, width, height
                )
                card_shape.fill.solid()
                card_shape.fill.fore_color.rgb = colors['primary']
                card_shape.line.color.rgb = RGBColor(
                    255, 255, 255)  # White border
                card_shape.line.width = Pt(3)

                # Add inner card area
                inner_left = Inches(left.inches + 0.1)
                inner_top = Inches(top.inches + 0.4)
                inner_width = Inches(width.inches - 0.2)
                inner_height = Inches(2.2)

                inner_shape = slide.shapes.add_shape(
                    MSO_SHAPE.ROUNDED_RECTANGLE,
                    inner_left, inner_top, inner_width, inner_height
                )
                inner_shape.fill.solid()
                inner_shape.fill.fore_color.rgb = RGBColor(
                    240, 240, 240)  # Light gray
                inner_shape.line.color.rgb = RGBColor(
                    200, 200, 200)  # Gray border
                inner_shape.line.width = Pt(2)

                # Add card image if available
                if index < len(image_urls):
                    image_url = image_urls[index]
                    image_filename = os.path.join(folder_path, f'{name}.jpg')

                    if fetch_and_save_image(image_url, image_filename):
                        try:
                            slide.shapes.add_picture(
                                image_filename,
                                Inches(inner_left.inches + 0.15),
                                Inches(inner_top.inches + 0.15),
                                width=Inches(inner_width.inches - 0.3),
                                height=Inches(inner_height.inches - 0.3),
                            )
                        except Exception as e:
                            print(f"Error adding image for {name}: {e}")

                # Add name with Clash Royale style font
                name_top = Inches(top.inches + 3)
                name_textbox = slide.shapes.add_textbox(
                    Inches(
                        left.inches + 0.1), name_top, Inches(width.inches - 0.2), Inches(0.8)
                )
                name_textframe = name_textbox.text_frame
                name_textframe.text = name
                name_textframe.paragraphs[0].alignment = PP_ALIGN.CENTER

                # Clash Royale style font (bold, prominent)
                name_font = name_textframe.paragraphs[0].font
                name_font.name = 'Impact'  # Bold, game-like font
                name_font.size = Pt(18)
                name_font.bold = True
                name_font.color.rgb = RGBColor(255, 255, 255)  # White text

                # Add room number in elixir-style circle
                room_left = Inches(left.inches + 0.3)
                room_top = Inches(top.inches + 4.2)
                room_size = Inches(1.2)

                # Elixir-style circle
                elixir_shape = slide.shapes.add_shape(
                    MSO_SHAPE.OVAL,
                    room_left, room_top, room_size, room_size
                )

                elixir_shape.fill.solid()
                elixir_shape.fill.fore_color.rgb = RGBColor(
                    218, 112, 214)  # Elixir purple
                elixir_shape.line.color.rgb = RGBColor(
                    255, 255, 255)  # White border
                elixir_shape.line.width = Pt(3)

                # Room number text
                room_textbox = slide.shapes.add_textbox(
                    room_left, Inches(room_top.inches +
                                      0.25), room_size, Inches(0.7)
                )
                room_textframe = room_textbox.text_frame
                room_textframe.text = str(room)
                room_textframe.paragraphs[0].alignment = PP_ALIGN.CENTER

                room_font = room_textframe.paragraphs[0].font
                room_font.name = 'Impact'
                room_font.size = Pt(14)
                room_font.bold = True
                room_font.color.rgb = RGBColor(255, 255, 255)  # White text

                # Add rarity indicator
                rarity_textbox = slide.shapes.add_textbox(
                    Inches(left.inches + 0.1), Inches(top.inches +
                                                      5.2), Inches(width.inches - 0.2), Inches(0.4)
                )

                rarity_textframe = rarity_textbox.text_frame
                rarity_textframe.text = rarity.upper()
                rarity_textframe.paragraphs[0].alignment = PP_ALIGN.CENTER

                rarity_font = rarity_textframe.paragraphs[0].font
                rarity_font.name = 'Impact'
                rarity_font.size = Pt(10)
                rarity_font.bold = True
                rarity_font.color.rgb = colors['secondary']

    # Save the presentation
    save_path = 'Clash_Royale_Door_Decks.pptx'
    prs.save(save_path)
    print(f"Clash Royale presentation created: {save_path}")

    # Save image paths to CSV
    paths_df = pd.DataFrame({
        'Name': [resident['Name'] for _, resident in residents_df.iterrows()],
        'Path': [os.path.join(folder_path, f'{resident["Name"]}.jpg') for _, resident in residents_df.iterrows()],
        'Rarity': [CARD_RARITIES[i % len(CARD_RARITIES)] for i in range(len(residents_df))]
    })
    paths_df.to_csv('clash_royale_image_paths.csv', index=False)
    print("Image paths saved to clash_royale_image_paths.csv")


if __name__ == "__main__":
    # Load residents and card URLs
    residents_df = pd.read_csv('residents_moore.csv')

    try:
        with open('clash_royale_card_urls.json', 'r') as f:
            import json
            image_urls = json.load(f)
    except FileNotFoundError:
        print("Please run get_clash_royale_cards.py first to generate card URLs")
        image_urls = []

    # Create the presentation
    create_clash_royale_presentation(residents_df, image_urls)
