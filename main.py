import os
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE


def fetch_and_save_image(image_url, image_filename):
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an error for bad HTTP responses
        image = Image.open(BytesIO(response.content))

        # Convert RGBA to RGB if needed
        if image.mode == 'RGBA':
            image = image.convert('RGB')

        # Save the image locally
        image.save(image_filename)
    except Exception as e:
        print(f"An error occurred while fetching or saving image: {e}")
        return None
    return image_filename


def create_presentation(residents_df, image_urls):
    prs = Presentation()
    folder_path = 'images'
    os.makedirs(folder_path, exist_ok=True)

    for i in range(0, len(residents_df), 3):
        slide = prs.slides.add_slide(
            prs.slide_layouts[5])  # Adding a blank slide

        # Add the main rectangle
        main_left = Inches(0.5)
        main_top = Inches(0.5)
        main_width = Inches(9)
        main_height = Inches(6.5)

        main_shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            main_left, main_top, main_width, main_height
        )
        main_shape.fill.solid()
        main_shape.fill.fore_color.rgb = RGBColor(255, 255, 255)  # White fill
        main_shape.line.color.rgb = RGBColor(0, 0, 0)  # Black border

        # Add up to three residents per slide
        for j in range(3):
            index = i + j
            if index < len(residents_df):
                resident = residents_df.iloc[index]
                name = resident['Name']
                room = resident['Room']

                left = Inches(1 + j * 3)
                top = Inches(1)
                width = Inches(2.5)
                height = Inches(5.5)

                shape = slide.shapes.add_shape(
                    MSO_SHAPE.RECTANGLE,
                    left, top, width, height
                )
                shape.fill.solid()
                shape.fill.fore_color.rgb = RGBColor(
                    200, 200, 200)  # Light gray fill
                shape.line.color.rgb = RGBColor(0, 0, 0)  # Black border

                # Fetch and add image
                image_url = image_urls.iloc[index]
                image_filename = os.path.join(folder_path, f'{name}.jpg')
                fetch_and_save_image(image_url, image_filename)

                # Add image to the slide
                slide.shapes.add_picture(
                    image_filename, left + Inches(0.25), top + Inches(0.25), width=Inches(2), height=Inches(2))

                # Add name and room number below the image
                text_box = slide.shapes.add_textbox(
                    left, top + Inches(4.5), width, Inches(1))
                text_frame = text_box.text_frame
                text_frame.text = f"{name}\nRoom: {room}"
                for paragraph in text_frame.paragraphs:
                    paragraph.font.size = Pt(14)
                    paragraph.font.color.rgb = RGBColor(0, 0, 0)  # Black text

    # Save the presentation
    save_path = 'Residents_Presentation.pptx'
    prs.save(save_path)
    print(f"Presentation created and saved as {save_path}")

    # Save the paths to a CSV file
    paths_df = pd.DataFrame({
        'Name': [resident['Name'] for index, resident in residents_df.iterrows()],
        'Path': [os.path.join(folder_path, f'{resident["Name"]}.jpg') for index, resident in residents_df.iterrows()]
    })
    paths_df.to_csv('image_paths.csv', index=False)
    print("Image paths saved to image_paths.csv")


# Load residents from CSV and image URLs from JSON
residents_df = pd.read_csv('residents_moore.csv')
image_urls = pd.read_json('villager_image_urls.json', typ='series')

# Create the presentation
create_presentation(residents_df, image_urls)
