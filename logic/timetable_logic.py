
class TimetableManager:
    def __init__(self):
        self.classes = []

    def add_class(self, day, subject, start_time, end_time, room):
        new_class = {
            "day": day,
            "subject": subject,
            "start_time": start_time,
            "end_time": end_time,
            "room": room
        }

        self.classes.append(new_class)

    def get_classes(self, day=None):
        if day:
            return [
                cls for cls in self.classes
                if cls["day"] == day
            ]

        return self.classes

    def update_class(self, index, day, subject, start_time, end_time, room):
        if 0 <= index < len(self.classes):
            self.classes[index] = {
                "day": day,
                "subject": subject,
                "start_time": start_time,
                "end_time": end_time,
                "room": room
            }

    def delete_class(self, index):
        if 0 <= index < len(self.classes):
            self.classes.pop(index)
