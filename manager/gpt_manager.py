from openai import OpenAI


client = OpenAI(api_key="YOUR-KEY")

class GptManager:
    def __init__(self):
        self.model_engine = "gpt-3.5-turbo"
        self.temperature = 0.5
        self.old_prompts = []

    def ask(self, value):
        # Aggiunge la richiesta alla conversazione
        self.old_prompts.append(value)
        text = ""
        for prompt in self.old_prompts:
            text += prompt + "\n"

        response = client.completions.create(
            model=self.model_engine,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=self.temperature,
            prompt=text
        )
        respText = response.choices[0].text.strip()
        print(respText)
        # Aggiunge la risposta alla conversazione
        self.old_prompts.append(respText)
        # Elimina i primi output per evitare di riempire la memoria
        if len(self.old_prompts) >= 1000:
            self.old_prompts.pop(0)
        return respText

    def clear_history(self, num=0):
        if num == 0:
            self.old_prompts.clear()
        else:
            for i in range(num):
                self.old_prompts.pop()
