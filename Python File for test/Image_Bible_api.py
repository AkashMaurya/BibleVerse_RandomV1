import requests
from decouple import config
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

def fetch_api_bible_verse():
    url = "https://bible-api.com/?random=verse"
    response = requests.get(url)
    data = response.json()

    if "verses" in data and isinstance(data["verses"], list):
        verse_data = data["verses"][0]
        book_name = verse_data["book_name"]
        chapter = verse_data["chapter"]
        verse = verse_data["verse"]
        text = verse_data["text"]

        return book_name, chapter, verse, text
    else:
        raise Exception("Failed to Fetch Data")

def fetch_random_nature_image():
    access_key = config("AccessKey_Pics")
    url = f"https://api.unsplash.com/photos/random?query=nature&client_id={access_key}"
    response = requests.get(url)
    data = response.json()

    if "urls" in data and "regular" in data["urls"]:
        image_url = data["urls"]["regular"]
        return image_url
    else:
        raise Exception("Failed to Fetch Image")

def download_image(url, save_path):
    img_data = requests.get(url).content
    with open(save_path, 'wb') as handler:
        handler.write(img_data)

def enhance_image(image):
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(0.6)  # Adjust brightness reduction (0.0 to 1.0)

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.3)  # Increase contrast

    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(1.2)  # Increase color

    return image

def wrap_text(text, font, max_width):
    lines = []
    words = text.split()
    while words:
        line = ''
        while words and font.getbbox(line + words[0])[2] <= max_width:
            line += (words.pop(0) + ' ')
        lines.append(line.strip())
    return lines

def add_text_to_image(image_path, text, output_path):
    image = Image.open(image_path)
    image = enhance_image(image)
    draw = ImageDraw.Draw(image)

    # Load a font (adjust path if needed)
    font_path = "arial.ttf"
    font_size = 50  # Adjust font size if necessary
    font = ImageFont.truetype(font_path, font_size)

    image_width, image_height = image.size
    max_width = image_width - 40  # Padding from the edges

    lines = wrap_text(text, font, max_width)

    # Calculate total text height
    total_text_height = sum([font.getbbox(line)[3] for line in lines])
    text_position = (20, (image_height - total_text_height) // 2)  # Centered vertically with padding

    # Add text with outline (optional)
    outline_color = "black"
    outline_range = 2  # Adjust outline thickness

    for line in lines:
        line_bbox = font.getbbox(line)
        line_width = line_bbox[2]
        line_height = line_bbox[3]
        x = (image_width - line_width) // 2  # Centered horizontally
        y = text_position[1]
        for xo in range(-outline_range, outline_range + 1):
            for yo in range(-outline_range, outline_range + 1):
                draw.text((x + xo, y + yo), line, font=font, fill=outline_color)
        draw.text((x, y), line, font=font, fill="white")
        text_position = (text_position[0], text_position[1] + line_height)

    # Save the result
    image.save(output_path)

def main():
    try:
        book_name, chapter, verse, text = fetch_api_bible_verse()
        verse_text = f"{text} \n\n {book_name} {chapter}:{verse}"
        
        image_url = fetch_random_nature_image()
        image_path = "random_nature_image.jpg"
        output_path = "output_image.jpg"
        
        download_image(image_url, image_path)
        add_text_to_image(image_path, verse_text, output_path)
        
        print(f"Bible verse added to image successfully. Saved as {output_path}")
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()
