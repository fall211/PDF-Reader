import pytesseract
from pdf2image import convert_from_path
import my_openai

class PDF2Text():
    def __init__(self):
        self.file_path = None
        self.images = None

    def set_file_path(self, file_path):
        self.file_path = file_path
        self.images = convert_from_path(self.file_path)

    def get_file_path(self):
        return self.file_path

    def get_page_count(self):
        return len(self.images)

    def get_text_from_page(self, page_number):
        text = pytesseract.image_to_string(self.images[page_number])
        if text == "":
            return ""
        return my_openai.clean_text(text)