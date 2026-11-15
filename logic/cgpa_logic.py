
class CgpaManager:

    def __init__(self):
        self.subjects = []

    def add_subject(self, subject, credits, grade_point):

        subject_data = {
            "subject": subject,
            "credits": credits,
            "grade_point": grade_point
        }

        self.subjects.append(subject_data)

    def calculate_sgpa(self):

        total_credits = sum(
            item["credits"] for item in self.subjects
        )

        if total_credits == 0:
            return 0

        total_points = sum(
            item["credits"] * item["grade_point"]
            for item in self.subjects
        )

        return total_points / total_credits

    def update_subject(self, index, subject, credits, grade_point):

        if 0 <= index < len(self.subjects):

            self.subjects[index] = {
                "subject": subject,
                "credits": credits,
                "grade_point": grade_point
            }

    def delete_subject(self, index):

        if 0 <= index < len(self.subjects):
            self.subjects.pop(index)

    def get_subjects(self):
        return self.subjects

    def calculate_cgpa(self, semester_sgpas):

        total_credits = sum(
            credits for sgpa, credits in semester_sgpas
        )

        if total_credits == 0:
            return 0

        total_points = sum(
            sgpa * credits for sgpa, credits in semester_sgpas
        )

        return total_points / total_credits
