import os
import sys
from random import randint

from PIL import Image, ImageDraw, ImageFont

import app_exceptions.FileExceptions as file_excep
import app_exceptions.ImageExceptions as img_excep
import helper_func.helper as helper_


class MemeEngine:
    """This class has the following functionalities,
        # Load image
        # Resize
        # Add caption
        # Save modified image

    This class can only handle two file formats; '.jpg' and '.png'. It can be extended by modifying the 'self._extensions' variable.
    """

    def __init__(self, output_dir):
        self._output_dir = (
            output_dir  # Output directory path to save the captioned image
        )
        self._extensions = [".jpg", ".png"]  # List of valid image extension to support
        self._font_path = "./font/arialbd.ttf"  # Font object file

    @helper_.Helper.check_extension
    @helper_.Helper.check_path
    def _load_image(self, img_path):
        """Load image with the PIL library.
        This class has two decorators which first check that the path given exists, then makes sure
        the file extension is valid
        @param:
            img_path: str
                path to the image to open
        @return:
            image: object
                Object return from opening the file with PIL
        """
        try:
            image = Image.open(img_path)
            return image
        except IOError as er:
            print(er)

    def _text_wrap(self, text, font, max_width):
        """Wrap text base on specified width.
        This is to enable text of width more than the image width to be display
        nicely.

        @params:
            text: str
                text to wrap
            font: obj
                font of the text
            max_width: int
                width to split the text with
        @return
            lines: list[str]
                list of wrap strings
        """
        lines = []

        # If the text width is smaller than the image width, then no need to split
        # just add it to the line list and return
        # if font.getsize(text)[0] <= max_width:
        if font.getbbox(text)[2] <= max_width:
            lines.append(text)
        else:
            # split the line by spaces to get words
            words = text.split(" ")
            i = 0
            # append every word to a line while its width is shorter than the image width
            while i < len(words):
                line = ""
                while i < len(words) and font.getbbox(line + words[i])[2] <= max_width:
                    line = line + words[i] + " "
                    i += 1
                if not line:
                    line = words[i]
                    i += 1
                lines.append(line)
        return lines

    def _resize_image(self, loaded_img, width):
        """Resize image by the given width while maintaining aspect ratio
        @params:
            loaded_img : obj
                image object opened with PIL
            width: int
                width to resize the image with
        @return:
            resized_img: obj
                resized image
        """
        img_w = loaded_img.size[0]
        img_h = loaded_img.size[1]
        hsize = helper_.Helper.get_resizedHeight_from_width(width, img_w, img_h)
        resized_img = None

        if float(img_w) >= width and float(img_h) >= hsize:
            resized_img = loaded_img.resize((width, hsize), Image.Resampling.LANCZOS)
        return resized_img

    def _save_image(self, captioned_img, img_path):
        """Save image
        @params:
            captioned_img: obj
                Image that has been added a caption
            img_path: str
                path to save the image
        """
        if not os.path.exists(self._output_dir):
            raise file_excep.FilePathInvalid(self._output_dir)

        img_path = os.path.join(self._output_dir, os.path.basename(img_path))
        # We may check if this file exist already before saving it

        # Check for IOError if any during saving the image
        captioned_img.save(img_path, optimize=True)
        return img_path

    def _add_caption(self, resized_img, text, author):
        """Add caption to image
        We calcalute the x and y axis base on the shape of the image and the size of the text
        so that we don't overflow the text on the image

        @params:
            resized_img: obj
                image that has been resized to the required shape
            text: str
                text that represents the body of the quote
            author: str
                The author of the quote
        @return:
            resized_img: obj
                the captioned image
        """

        draw = ImageDraw.Draw(resized_img)

        # specified font style and size
        font_size = 20
        font = ImageFont.truetype(self._font_path, font_size)

        # Calculate x axis to display text
        x_min = (resized_img.size[0] * 8) // 100  # 8%
        x_max = (resized_img.size[0] * 50) // 100  # 50%
        range_x = randint(x_min, x_max)

        # Split text base on font and random position x
        lines = self._text_wrap(text, font, resized_img.size[0] - range_x)
        # line_height = font.getsize("hg")[1]  # Get line spacing
        line_height = font.getbbox("hg")[3]  # Get line spacing

        # Calculate y axis for text display
        y_min = (resized_img.size[1] * 4) // 100  # 4%
        y_max = (resized_img.size[1] * 90) // 100  # 90%
        y_max -= len(lines) * line_height  # adjust base on number of lines
        range_y = randint(y_min, y_max)

        # draw text
        for line in lines:
            draw.text((range_x, range_y), line, font=font, align="left")
            range_y += line_height

        # Calculate x and y axis to display author
        range_y += 5
        range_x += 20
        # draw author
        draw.text((range_x, range_y), "- " + author, font=font, align="left")

        return resized_img

    def make_meme(self, img_path: str, text: str, author: str, width=500) -> str:
        """Controls the process of loading image with PIL, resizing and captioning the image
        It makes use of methods defined above.

        @param:
            img_path: str
                path containing the image to load, resize and caption
            text: str
                text that represents the body of the quote
            author: str
                The author of the quote
            width: int
                width to resize the image with
        @return:
            captioned_path: str
                path to the captioned image
        """

        load_img = self._load_image(img_path)
        resized_img = self._resize_image(load_img, width)

        if not resized_img:
            img_w = load_img.size[0]
            img_h = load_img.size[1]
            error = "Error! Image size small: Image is {}x{}. Expected size should be above {}x{}".format(
                int(img_w),
                int(img_h),
                width,
                helper_.Helper.get_resizedHeight_from_width(
                    width, float(img_w), float(img_h)
                ),
            )

            raise img_excep.ImageSmall(img_path, error)

        captioned_img = self._add_caption(resized_img, text, author)
        captioned_path = self._save_image(captioned_img, img_path)
        return captioned_path
