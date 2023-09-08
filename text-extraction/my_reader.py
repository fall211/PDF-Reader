import PyPDF2
import my_openai

class MyReader():
    def __init__(self):
        self.reader = None
        self.file_path = None

    def set_file_path(self, file_path):
        self.file_path = file_path
        self.reader = PyPDF2.PdfReader(file_path)

    def get_file_path(self):
        return self.file_path

    def get_page_count(self):
        return len(self.reader.pages)

    def get_text_from_page(self, page_number):
        text = self.reader.pages[page_number].extract_text()
        if text == "":
            return ""
        return my_openai.clean_text(text)