from PIL import Image

def rgb_to_rgb565(red, green, blue):
    # Chuyển đổi giá trị màu từ 8-bit sang 5-bit (RGB565)
    red = (red >> 3) & 0x1F
    green = (green >> 2) & 0x3F
    blue = (blue >> 3) & 0x1F
    # Kết hợp các giá trị màu lại với nhau
    rgb565 = (red << 11) | (green << 5) | blue
    return rgb565

def rgb565_to_hex(rgb565):
    hex_string = format(rgb565, '04X')  # Sử dụng format để đảm bảo có đủ 4 chữ số hex
    return f"0x{hex_string}"

def convert_image_to_hex_array(image_path):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    hex_array = []

    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            rgb565 = rgb_to_rgb565(r, g, b)
            hex_value = rgb565_to_hex(rgb565)
            hex_array.append(hex_value)
    return hex_array, width, height

# image_path = "C:/Users/dangh/OneDrive/Hình ảnh/Untitled.bmp"
image_path = "C:/Users/dangh/OneDrive/Hình ảnh/frame_001_delay-0.08s.bmp"
hex_array, img_width, img_height = convert_image_to_hex_array(image_path)

# Inserting a new line after every 16 elements
hex_array_with_newlines = [f"{value}, " if (i + 1) % 16 != 0 else f"{value},\n" for i, value in enumerate(hex_array)]

# Combining the elements into a single string
output_string = ''.join(hex_array_with_newlines)

# Forming Arduino C code
arduino_c_code = f"const uint16_t PROGMEM img[] = {{{'\n' + output_string}}};"
img_size_code = f"const int imgWidth = {img_width};\n" + f"const int imgHeight = {img_height};\n"

# print(img_size_code)
print(arduino_c_code)
