#DA RIVEDERE
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
        self.to_do_list.append(task)
        with open(self.file_name, "a") as f:
            f.write(task + "\n")

    def remove_task(self, task_index):
        if task_index < len(self.to_do_list):
            removed_task = self.to_do_list.pop(task_index)
            with open(self.file_name, "w") as f:
                f.writelines(self.to_do_list)
            return removed_task
        else:
            return None

    def get_task_list(self):
        return self.to_do_list
