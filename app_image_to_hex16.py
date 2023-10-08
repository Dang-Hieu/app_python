from tkinter import Tk, Button, Label, filedialog, Text, Entry, END, messagebox
from PIL import Image
import os
import pyperclip

class ImageToHexConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to Hex Converter")

        self.label_file = Label(root, text="Chọn một tệp hình ảnh:")
        self.label_file.pack(pady=10)

        self.button_file = Button(root, text="Chọn tệp", command=self.choose_file)
        self.button_file.pack(pady=10)

        self.label_array_name = Label(root, text="Đặt tên cho mảng:")
        self.label_array_name.pack(pady=10)

        self.entry_array_name = Entry(root)
        self.entry_array_name.pack(pady=10)

        self.convert_button = Button(root, text="Chuyển đổi", command=self.convert_image)
        self.convert_button.pack(pady=10)

        self.code_text = Text(root, height=25, width=150)
        self.code_text.pack(pady=10)

        self.copy_button = Button(root, text="Copy Code", command=self.copy_code)
        self.copy_button.pack(pady=10)

    def choose_file(self):
        file_path = filedialog.askopenfilename(title="Chọn một tệp hình ảnh", filetypes=[("Image files", "*.png;*.jpg;*.bmp")])
        self.file_path = file_path

    def convert_image(self):
        if hasattr(self, 'file_path'):
            img_width, img_height = self.get_image_size(self.file_path)

            # 2D array to store the converted image
            hex_array, _, _ = self.convert_image_to_hex_array(self.file_path)

            # Get the array name from the Entry widget or use default name "img"
            array_name = self.entry_array_name.get()
            if not array_name:
                array_name = "img"

            # Displaying the array in the Text widget
            self.display_array(hex_array, img_width, img_height, array_name)

    def display_array(self, hex_array, img_width, img_height, array_name):
        self.code_text.delete(1.0, END)

        # Forming Arduino C code with the specified array name
        hex_array_with_newlines = [f"{value}, " if (i + 1) % img_width != 0 else f"{value},\n" for i, value in enumerate(hex_array)]
        output_string = ''.join(hex_array_with_newlines)

        arduino_c_code = f"const int imgWidth = {img_width};\n" + f"const int imgHeight = {img_height};\n"
        arduino_c_code += f"const uint16_t PROGMEM {array_name}[] = {{{'\n' + output_string}}};"

        self.code_text.insert(END, arduino_c_code)

    def copy_code(self):
        code_to_copy = self.code_text.get(1.0, END)
        if code_to_copy.strip():  # Check if there is code to copy
            # Ask for confirmation before copying
            response = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn sao chép mã này?")
            if response:
                pyperclip.copy(code_to_copy)
                print("Code copied to clipboard!")
            else:
                print("Sao chép mã đã hủy.")

    def convert_image_to_hex_array(self, image_path):
        img = Image.open(image_path).convert("RGB")
        width, height = img.size
        hex_array = []

        for y in range(height):
            for x in range(width):
                r, g, b = img.getpixel((x, y))
                rgb565 = self.rgb_to_rgb565(r, g, b)
                hex_value = self.rgb565_to_hex(rgb565)
                hex_array.append(hex_value)
        return hex_array, width, height

    def rgb_to_rgb565(self, red, green, blue):
        red = (red >> 3) & 0x1F
        green = (green >> 2) & 0x3F
        blue = (blue >> 3) & 0x1F
        rgb565 = (red << 11) | (green << 5) | blue
        return rgb565

    def rgb565_to_hex(self, rgb565):
        hex_string = format(rgb565, '04X')
        return f"0x{hex_string}"

    def get_image_size(self, image_path):
        img = Image.open(image_path).convert("RGB")
        return img.size

if __name__ == "__main__":
    root = Tk()
    app = ImageToHexConverter(root)
    root.mainloop()
