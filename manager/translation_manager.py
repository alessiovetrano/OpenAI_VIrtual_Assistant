from googletrans import Translator


class TranslationManager:
    def __init__(self):
        self.translator = Translator()

    def translate(self, text):
        return self.translator.translate(text, dest='it').text
