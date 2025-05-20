from PIL import Image

def resize_image(input_path, output_path, width, height):
    img = Image.open(input_path)
    img = img.resize((width, height))
    img.save(output_path)

def compress_image(input_path, output_path, quality=70):
    img = Image.open(input_path)
    img.save(output_path, optimize=True, quality=quality)
