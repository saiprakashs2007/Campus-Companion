
class TaskManager:

    def __init__(self):
        self.tasks = []

    def add_task(self, title, subject, deadline, priority):
        task = {
            "title": title,
            "subject": subject,
            "deadline": deadline,
            "priority": priority,
            "completed": False
        }

        self.tasks.append(task)

    def get_tasks(self, status=None):
        if status == "Pending":
            return [task for task in self.tasks if not task["completed"]]

        elif status == "Completed":
            return [task for task in self.tasks if task["completed"]]

        return self.tasks

    def complete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["completed"] = True

    def update_task(self, index, title, subject, deadline, priority):
        if 0 <= index < len(self.tasks):
            self.tasks[index].update({
                "title": title,
                "subject": subject,
                "deadline": deadline,
                "priority": priority
            })

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
