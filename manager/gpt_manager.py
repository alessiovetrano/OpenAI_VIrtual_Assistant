import openai

from tts_manager import speak

openai.api_key = "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"


class GptManager:
    def __init__(self):
        self.model_engine = "text-davinci-003"
        self.temperature = 0.5
        self.old_prompts = []

    def ask(self, value):
        # Aggiunge la richiesta alla conversazione
        self.old_prompts.append(value)
        text = ""
        for prompt in self.old_prompts:
            text += prompt + "\n"

        response = openai.Completion.create(
            engine=self.model_engine,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=self.temperature,
            prompt=text
        )
        respText = response["choices"][0]["text"].strip()
        # Aggiunge la risposta alla conversazione
        self.old_prompts.append(respText)
        # Elimina i primi output per evitare di riempire la memoria
        if len(self.old_prompts) >= 1000:
            self.old_prompts.pop(0)
        print("Risposta: " + respText)
        speak(respText)
