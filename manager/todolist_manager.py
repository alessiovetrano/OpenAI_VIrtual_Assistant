from manager.tts_manager import speak


class ToDoListManager:
    def __init__(self):
        self.file_name = "to_do_list.txt"
        self.to_do_list = []
        try:
            with open(self.file_name, "r") as f:
                self.to_do_list = f.readlines()
        except FileNotFoundError:
            with open(self.file_name, "w"):
                pass

    def add_task(self, task):
        if task.startswith("aggiungi"):
            task = task.replace("aggiungi", "").replace("alla lista delle cose da fare", "").replace(
                "alla mia lista delle cose da fare", "").replace("alle cose da fare", "").strip()
        self.to_do_list.append(task)
        with open(self.file_name, "a") as f:
            f.write(task + "\n")

    def remove_task(self, task):
        print("Rimozione ...")
        if task.startswith("rimuovi") or task.startswith("elimina"):
            task = task.replace("elimina", "").replace("rimuovi", "").replace("dalla lista delle cose da fare",
                                                                              "").replace(
                "dalla mia lista delle cose da fare", "").strip() + "\n"
            print("task" + task)
            print(self.to_do_list)
        if task in self.to_do_list:
            self.to_do_list.remove(task)
            speak("Eliminato con successo")
            with open(self.file_name, "w") as f:
                f.writelines(self.to_do_list)
            return task
        return None

    def get_task_list(self):
        speak('\n'.join(self.to_do_list))