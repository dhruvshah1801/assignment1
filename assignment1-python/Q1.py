def main():
    # Read n, k and m
    n, k, m = map(int, input().split())

    students = []
    semester_groups = {}
    subject_top = {}

    # Read student records
    for _ in range(n):
        data = input().split()

        enrollment = data[0]
        name = data[1]
        semester = int(data[2])
        cpi = float(data[3])
        marks = list(map(int, data[4:]))

        average = sum(marks) / m

        # Store record using tuple
        student = (enrollment, name, semester, cpi, marks, average)
        students.append(student)

        # Group students semester-wise
        if semester not in semester_groups:
            semester_groups[semester] = []

        semester_groups[semester].append(student)

        # Find subject-wise toppers
        for j in range(m):
            subject = j + 1
            mark = marks[j]

            if subject not in subject_top:
                subject_top[subject] = (mark, [enrollment])
            else:
                best_mark, enrollments = subject_top[subject]

                if mark > best_mark:
                    subject_top[subject] = (mark, [enrollment])

                elif mark == best_mark:
                    enrollments.append(enrollment)

    # Print semester-wise top K students
    for semester in sorted(semester_groups):
        group = semester_groups[semester]

        # Sort according to:
        # 1. Higher CPI
        # 2. Higher average marks
        # 3. Smaller enrollment number
        group.sort(
            key=lambda x: (-x[3], -x[5], x[0])
        )

        top_students = group[:k]

        print(
            f"Semester {semester}: "
            + " ".join(student[0] for student in top_students)
        )

    # Print subject-wise toppers
    for subject in range(1, m + 1):
        enrollments = sorted(subject_top[subject][1])

        print(
            f"S{subject}: "
            + " ".join(enrollments)
        )


if __name__ == "__main__":
    main()