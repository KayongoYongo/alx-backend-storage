#!/usr/bin/env python3
"""Find the average score"""


def top_students(mongo_collection):
    """Returns the average of the sorted out list"""
    students = mongo_collection.find({}, {"topics": 1})
    students_list = []

    for student in students:
        topics = student["topics"]
        total_score = sum(topic["score"] for topic in topics)
        average_score = total_score / len(topics)
        student["averageScore"] = average_score
        students_list.append(student)

    sorted_students = sorted(students_list, key=lambda s: s["averageScore"], reverse=True)
    return sorted_students
