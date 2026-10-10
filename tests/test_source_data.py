"""Validate source CSV relationships without changing educational records."""

import csv
import unittest
from pathlib import Path


DATA = Path(__file__).resolve().parents[1] / "data"


def read_csv(name):
    with (DATA / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class SourceDataContracts(unittest.TestCase):
    def test_unique_primary_keys(self):
        for file_name, key in (
            ("students.csv", "student_id"),
            ("teachers.csv", "teacher_id"),
            ("courses.csv", "course_id"),
        ):
            with self.subTest(file=file_name):
                records = read_csv(file_name)
                ids = [record[key] for record in records]
                self.assertTrue(all(ids))
                self.assertEqual(len(ids), len(set(ids)))

    def test_courses_reference_known_students_and_teachers(self):
        students = {row["student_id"] for row in read_csv("students.csv")}
        teachers = {row["teacher_id"] for row in read_csv("teachers.csv")}
        for course in read_csv("courses.csv"):
            with self.subTest(course=course["course_id"]):
                self.assertIn(course["student_id"], students)
                self.assertIn(course["teacher_id"], teachers)

    def test_student_teacher_references(self):
        teachers = {row["teacher_id"] for row in read_csv("teachers.csv")}
        for student in read_csv("students.csv"):
            self.assertIn(student["teacher_id"], teachers)

    def test_course_hours_are_valid_when_recorded(self):
        for course in read_csv("courses.csv"):
            scheduled = float(course["scheduled_hours"])
            self.assertGreater(scheduled, 0, course["course_id"])
            completed_text = course["completed_hours"].strip()
            if completed_text:
                completed = float(completed_text)
                self.assertGreaterEqual(completed, 0, course["course_id"])
                self.assertLessEqual(completed, scheduled, course["course_id"])

    def test_missing_course_fields_are_explicit(self):
        missing_grades = 0
        missing_hours = 0
        for course in read_csv("courses.csv"):
            if not course["grade"].strip():
                missing_grades += 1
                self.assertFalse(course["pass_fail"].strip(), course["course_id"])
            if not course["completed_hours"].strip():
                missing_hours += 1
        self.assertEqual(missing_grades, 32)
        self.assertEqual(missing_hours, 22)

    def test_grade_result_consistency(self):
        incomplete = 0
        for course in read_csv("courses.csv"):
            grade, result = course["grade"].strip(), course["pass_fail"].strip()
            if not grade:
                incomplete += 1
                self.assertFalse(result, course["course_id"])
                continue
            value = float(grade)
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 20)
            self.assertEqual(result, "Réussi" if value >= 10 else "Échoué")
        self.assertGreater(incomplete, 0)


if __name__ == "__main__":
    unittest.main()
