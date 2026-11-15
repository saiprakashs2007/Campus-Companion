
class AttendanceManager:

    def __init__(self):
        self.subjects = []

    def add_subject(self, subject, total_classes, attended_classes):

        subject_data = {
            "subject": subject,
            "total_classes": total_classes,
            "attended_classes": attended_classes
        }

        self.subjects.append(subject_data)

    def get_attendance_percentage(self, subject):

        for item in self.subjects:

            if item["subject"] == subject:

                total = item["total_classes"]
                attended = item["attended_classes"]

                if total == 0:
                    return 0

                return (attended / total) * 100

        return 0

    def get_classes_needed(self, subject, target=75):

        for item in self.subjects:

            if item["subject"] == subject:

                total = item["total_classes"]
                attended = item["attended_classes"]

                if total == 0:
                    return 0

                percentage = (attended / total) * 100

                if percentage >= target:
                    return 0

                needed = 0

                while ((attended + needed) / (total + needed)) * 100 < target:
                    needed += 1

                return needed

        return 0

    def update_attendance(self, subject, total_classes, attended_classes):

        for item in self.subjects:

            if item["subject"] == subject:

                item["total_classes"] = total_classes
                item["attended_classes"] = attended_classes

                return True

        return False

    def delete_subject(self, subject):

        for item in self.subjects:

            if item["subject"] == subject:

                self.subjects.remove(item)
                return True

        return False

    def get_all_subjects(self):
        return self.subjects
