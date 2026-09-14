from flask import Flask, render_template, request, redirect, url_for, session, flash
from database.connection import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = "skilltrack_secret_key_2026"



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/features")
def features():
    return render_template("features.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT *
            FROM users
            WHERE email = %s
        """

        cursor.execute(query, (email,))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user and (
            check_password_hash(user["password"], password)
            if user["password"].startswith(("scrypt:", "pbkdf2:"))
            else user["password"] == password
        ):

            session["user_id"] = user["user_id"]
            session["user_name"] = user["name"]
            session["user_role"] = user["role"]

            # Role ke according dashboard open hoga
            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("dashboard"))

        else:
            return "Invalid email or password!"

    return render_template("login.html")
@app.route("/profile", methods=["GET", "POST"])
def profile():
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        college = request.form["college"]
        course = request.form["course"]
        semester = request.form["semester"]
        target_role = request.form["target_role"]
        career_objective = request.form["career_objective"]
        phone = request.form["phone"]

        # Check if profile already exists
        cursor.execute("""
            SELECT profile_id
            FROM student_profiles
            WHERE user_id = %s
        """, (user_id,))

        existing_profile = cursor.fetchone()

        if existing_profile:

            # Update existing profile
            query = """
                UPDATE student_profiles
                SET college = %s,
                    course = %s,
                    semester = %s,
                    target_role = %s,
                    career_objective = %s,
                    phone = %s
                WHERE user_id = %s
            """

            cursor.execute(
                query,
                (college, course, semester, target_role,
                 career_objective, phone, user_id)
            )

            message = "Profile Updated Successfully!"

        else:

            # Create new profile
            query = """
                INSERT INTO student_profiles
                (user_id, college, course, semester, target_role,
                 career_objective, phone)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (user_id, college, course, semester, target_role,
                 career_objective, phone)
            )

            message = "Profile Saved Successfully!"

        connection.commit()

        cursor.close()
        connection.close()

        flash(message, "success")

        return redirect(url_for("profile"))

    # Get existing profile data
    cursor.execute("""
        SELECT *
        FROM student_profiles
        WHERE user_id = %s
    """, (user_id,))

    profile_data = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "profile.html",
        profile_data=profile_data
    )

@app.route("/skills", methods=["GET", "POST"])
def skills():
    user_id = session.get("user_id")

    if not user_id:
      return redirect(url_for("login"))
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        skill_id = request.form["skill_id"]
        skill_level = request.form["skill_level"]

        query = """
            INSERT INTO student_skills
            (user_id, skill_id, skill_level)
            VALUES (%s, %s, %s)
        """

        cursor.execute(
            query,
            (user_id, skill_id, skill_level)
        )

        connection.commit()
        flash("Skill Added Successfully!", "success")
        return redirect(url_for("skills"))

    query = """
        SELECT skills.skill_name,
               skills.category,
               student_skills.skill_level
        FROM student_skills
        JOIN skills
        ON student_skills.skill_id = skills.skill_id
        WHERE student_skills.user_id = %s
    """

    cursor.execute(query, (user_id,))
    student_skills = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "skills.html",
        student_skills=student_skills
    )
    
@app.route("/courses", methods=["GET", "POST"])
def courses():
    user_id = session.get("user_id")

    if not user_id:
      return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        course_name = request.form["course_name"]
        platform = request.form["platform"]
        start_date = request.form["start_date"] or None
        completion_date = request.form["completion_date"] or None
        status = request.form["status"]

        query = """
            INSERT INTO courses
            (user_id, course_name, platform, start_date,
             completion_date, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (user_id, course_name, platform, start_date,
             completion_date, status)
        )

        connection.commit()
        flash("Course Added Successfully!", "success")
        cursor.close()
        connection.close()
        return redirect(url_for("courses"))

    query = """
        SELECT course_name,
               platform,
               start_date,
               completion_date,
               status
        FROM courses
        WHERE user_id = %s
        ORDER BY course_id DESC
    """

    cursor.execute(query, (user_id,))
    student_courses = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "courses.html",
        student_courses=student_courses
    )
@app.route("/certifications", methods=["GET", "POST"])
def certifications():
    user_id = session.get("user_id")

    if not user_id:
      return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        certificate_name = request.form["certificate_name"]
        organization = request.form["organization"]
        issue_date = request.form["issue_date"] or None
        credential_id = request.form["credential_id"]
        certificate_link = request.form["certificate_link"]

        query = """
            INSERT INTO certifications
            (user_id, certificate_name, organization, issue_date,
             credential_id, certificate_link)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (user_id, certificate_name, organization, issue_date,
             credential_id, certificate_link)
        )

        connection.commit()

        cursor.close()
        connection.close()

        flash("Certification added successfully!", "success")

        return redirect(url_for("certifications"))

    query = """
        SELECT certification_id,
               certificate_name,
               organization,
               issue_date,
               credential_id,
               certificate_link
        FROM certifications
        WHERE user_id = %s
        ORDER BY certification_id DESC
    """

    cursor.execute(query, (user_id,))
    student_certifications = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "certifications.html",
        student_certifications=student_certifications
    )
@app.route("/projects", methods=["GET", "POST"])
def projects():
    user_id = session.get("user_id")

    if not user_id:
      return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        project_name = request.form["project_name"]
        description = request.form["description"]
        technologies = request.form["technologies"]
        completion_date = request.form["completion_date"] or None
        github_link = request.form["github_link"]

        query = """
            INSERT INTO projects
            (user_id, project_name, description, technologies,
             completion_date, github_link)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (user_id, project_name, description, technologies,
             completion_date, github_link)
        )

        connection.commit()

        flash("Project Added Successfully!", "success")

        cursor.close()
        connection.close()

        return redirect(url_for("projects"))

    query = """
        SELECT project_name,
               description,
               technologies,
               completion_date,
               github_link
        FROM projects
        WHERE user_id = %s
        ORDER BY project_id DESC
    """

    cursor.execute(query, (user_id,))
    student_projects = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "projects.html",
        student_projects=student_projects
    )
@app.route("/tests", methods=["GET", "POST"])
def tests():
    user_id = session.get("user_id")

    if not user_id:
      return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        test_name = request.form["test_name"]
        category = request.form["category"]
        score = request.form["score"]
        test_date = request.form["test_date"] or None

        query = """
            INSERT INTO aptitude_tests
            (user_id, test_name, category, score, test_date)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (user_id, test_name, category, score, test_date)
        )

        connection.commit()

        flash("Test Result Added Successfully!", "success")

        cursor.close()
        connection.close()

        return redirect(url_for("tests"))

    query = """
        SELECT test_name,
               category,
               score,
               test_date
        FROM aptitude_tests
        WHERE user_id = %s
        ORDER BY test_id DESC
    """

    cursor.execute(query, (user_id,))
    student_tests = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "tests.html",
        student_tests=student_tests
    )
@app.route("/interview", methods=["GET", "POST"])
def interview():
    user_id = session.get("user_id")

    if not user_id:
      return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        communication = request.form["communication"]
        technical = request.form["technical"]
        confidence = request.form["confidence"]
        problem_solving = request.form["problem_solving"]
        interview_date = request.form["interview_date"] or None

        query = """
            INSERT INTO interview_scores
            (user_id, communication, technical, confidence,
             problem_solving, interview_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (user_id, communication, technical, confidence,
             problem_solving, interview_date)
        )

        connection.commit()

        flash("Interview Score Added Successfully!", "success")

        cursor.close()
        connection.close()

        return redirect(url_for("interview"))

    query = """
        SELECT communication,
               technical,
               confidence,
               problem_solving,
               interview_date
        FROM interview_scores
        WHERE user_id = %s
        ORDER BY interview_id DESC
    """

    cursor.execute(query, (user_id,))
    interview_scores = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "interview.html",
        interview_scores=interview_scores
    )
@app.route("/dashboard")
def dashboard():
    user_id = session.get("user_id")
    if not user_id:
      return redirect(url_for("login"))
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Skills Score
    cursor.execute("""
        SELECT AVG(skill_level) AS skill_score
        FROM student_skills
        WHERE user_id = %s
    """, (user_id,))

    skill_result = cursor.fetchone()
    skill_score = skill_result["skill_score"] or 0


    # Projects Score
    cursor.execute("""
        SELECT COUNT(*) AS project_count
        FROM projects
        WHERE user_id = %s
    """, (user_id,))

    project_result = cursor.fetchone()
    project_count = project_result["project_count"]

    project_score = min(project_count * 25, 100)


    # Certifications Score
    cursor.execute("""
        SELECT COUNT(*) AS certification_count
        FROM certifications
        WHERE user_id = %s
    """, (user_id,))

    certification_result = cursor.fetchone()
    certification_count = certification_result["certification_count"]

    certification_score = min(certification_count * 25, 100)


    # Aptitude Score
    cursor.execute("""
        SELECT AVG(score) AS aptitude_score
        FROM aptitude_tests
        WHERE user_id = %s
    """, (user_id,))

    aptitude_result = cursor.fetchone()
    aptitude_score = aptitude_result["aptitude_score"] or 0


    # Interview Score
    cursor.execute("""
        SELECT AVG(
            (communication +
             technical +
             confidence +
             problem_solving) / 4
        ) AS interview_score
        FROM interview_scores
        WHERE user_id = %s
    """, (user_id,))

    interview_result = cursor.fetchone()
    interview_score = interview_result["interview_score"] or 0


    # Overall Readiness Score
    readiness_score = (
        (float(skill_score) * 0.35) +
        (float(project_score) * 0.20) +
        (float(certification_score) * 0.10) +
        (float(aptitude_score) * 0.20) +
        (float(interview_score) * 0.15)
    )

    readiness_score = round(readiness_score, 2)

    # Skills Count
    cursor.execute("""
        SELECT COUNT(*) AS skill_count
        FROM student_skills
        WHERE user_id = %s
    """, (user_id,))

    skill_count = cursor.fetchone()["skill_count"]


    # Projects Count
    cursor.execute("""
        SELECT COUNT(*) AS project_count
        FROM projects
        WHERE user_id = %s
    """, (user_id,))

    project_count = cursor.fetchone()["project_count"]


    # Certifications Count
    cursor.execute("""
        SELECT COUNT(*) AS certification_count
        FROM certifications
        WHERE user_id = %s
    """, (user_id,))

    certification_count = cursor.fetchone()["certification_count"]
    
    # Aptitude Average Score
    cursor.execute("""
    SELECT AVG(score) AS aptitude_score
    FROM aptitude_tests
    WHERE user_id = %s
    """, (user_id,))

    aptitude_result = cursor.fetchone()
    aptitude_score = aptitude_result["aptitude_score"] or 0


    # Interview Average Score
    cursor.execute("""
    SELECT AVG(
        (communication +
         technical +
         confidence +
         problem_solving) / 4
    ) AS interview_score
    FROM interview_scores
    WHERE user_id = %s
    """, (user_id,))

    interview_result = cursor.fetchone()
    interview_score = interview_result["interview_score"] or 0
    
    # Skill Chart Data
    cursor.execute("""
    SELECT
        skills.skill_name,
        student_skills.skill_level
    FROM student_skills
    JOIN skills
        ON student_skills.skill_id = skills.skill_id
    WHERE student_skills.user_id = %s
    ORDER BY student_skills.skill_level DESC
    """, (user_id,))

    skill_results = cursor.fetchall()

    skill_names = []
    skill_levels = []

    for skill in skill_results:
     skill_names.append(skill["skill_name"])
     skill_levels.append(skill["skill_level"])
    cursor.close()
    connection.close()

    return render_template(
    "dashboard.html",
    readiness_score=readiness_score,
    skill_count=skill_count,
    project_count=project_count,
    certification_count=certification_count,
    aptitude_score=round(float(aptitude_score), 2),
    interview_score=round(float(interview_score), 2),
    skill_names=skill_names,
    skill_levels=skill_levels
    )
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        
        password = generate_password_hash(password)
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO users (name, email, password)
            VALUES (%s, %s, %s)
        """

        cursor.execute(query, (name, email, password))
        connection.commit()

        cursor.close()
        connection.close()

        return "Registration Successful!"

    return render_template("register.html")

@app.route("/admin-dashboard")
def admin_dashboard():

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("admin_login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Verify that logged-in user is actually an admin
    cursor.execute("""
        SELECT user_id, name, email, role
        FROM users
        WHERE user_id = %s
    """, (user_id,))

    admin = cursor.fetchone()

    if not admin or admin["role"] != "admin":
        cursor.close()
        connection.close()
        session.clear()
        return redirect(url_for("admin_login"))

    # Total Students
    cursor.execute("""
        SELECT COUNT(*) AS total_students
        FROM users
        WHERE role = 'student'
    """)
    total_students = cursor.fetchone()["total_students"]

    # Total Skill Records
    cursor.execute("""
        SELECT COUNT(*) AS total_skills
        FROM student_skills
    """)
    total_skills = cursor.fetchone()["total_skills"]

    # Total Projects
    cursor.execute("""
        SELECT COUNT(*) AS total_projects
        FROM projects
    """)
    total_projects = cursor.fetchone()["total_projects"]

    # Total Certifications
    cursor.execute("""
        SELECT COUNT(*) AS total_certifications
        FROM certifications
    """)
    total_certifications = cursor.fetchone()["total_certifications"]
    # Placement Readiness Overview

    readiness = {
        "excellent": 0,
        "good": 0,
        "needs_improvement": 0,
        "beginner": 0
    }

    cursor.execute("""
        SELECT user_id
        FROM users
        WHERE role = 'student'
    """)

    student_users = cursor.fetchall()

    for student in student_users:

        student_id = student["user_id"]

        # Average Skill Score
        cursor.execute("""
            SELECT AVG(skill_level) AS avg_skill
            FROM student_skills
            WHERE user_id = %s
        """, (student_id,))

        skill_result = cursor.fetchone()
        skill_score = float(skill_result["avg_skill"] or 0)

        # Project Score
        cursor.execute("""
            SELECT COUNT(*) AS project_count
            FROM projects
            WHERE user_id = %s
        """, (student_id,))

        project_count = cursor.fetchone()["project_count"]
        project_score = min(project_count * 25, 100)

        # Certification Score
        cursor.execute("""
            SELECT COUNT(*) AS certification_count
            FROM certifications
            WHERE user_id = %s
        """, (student_id,))

        certification_count = cursor.fetchone()["certification_count"]
        certification_score = min(certification_count * 25, 100)

        # Aptitude Score
        cursor.execute("""
            SELECT AVG(score) AS avg_aptitude
            FROM aptitude_tests
            WHERE user_id = %s
        """, (student_id,))

        aptitude_result = cursor.fetchone()
        aptitude_score = float(aptitude_result["avg_aptitude"] or 0)

        # Interview Score
        cursor.execute("""
            SELECT AVG(
                (communication + technical + confidence + problem_solving) / 4
            ) AS avg_interview
            FROM interview_scores
            WHERE user_id = %s
        """, (student_id,))

        interview_result = cursor.fetchone()
        interview_score = float(interview_result["avg_interview"] or 0)

        # Final Placement Readiness
        final_score = (
            (skill_score * 0.35) +
            (project_score * 0.20) +
            (certification_score * 0.10) +
            (aptitude_score * 0.20) +
            (interview_score * 0.15)
        )

        if final_score >= 80:
            readiness["excellent"] += 1

        elif final_score >= 70:
            readiness["good"] += 1

        elif final_score >= 50:
            readiness["needs_improvement"] += 1

        else:
            readiness["beginner"] += 1
    # Student List
    cursor.execute("""
    SELECT
        u.user_id,
        u.name,
        u.email,
        sp.course,
        sp.semester,
        sp.target_role
    FROM users u
    LEFT JOIN student_profiles sp
        ON u.user_id = sp.user_id
    WHERE u.role = 'student'
    ORDER BY u.user_id DESC
""")

    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "admin_dashboard.html",
        admin=admin,
        total_students=total_students,
        total_skills=total_skills,
        total_projects=total_projects,
        total_certifications=total_certifications,
        students=students,
        readiness=readiness
    )
@app.route("/admin/student/<int:student_id>")
def admin_student_details(student_id):

    # Check login
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("admin_login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Verify logged-in user is admin
    cursor.execute("""
        SELECT user_id, name, email, role
        FROM users
        WHERE user_id = %s
    """, (user_id,))

    admin = cursor.fetchone()

    if not admin or admin["role"] != "admin":
        cursor.close()
        connection.close()
        session.clear()
        return redirect(url_for("admin_login"))

    # Get selected student
    cursor.execute("""
        SELECT
            u.user_id,
            u.name,
            u.email,
            sp.college,
            sp.course,
            sp.semester,
            sp.target_role,
            sp.career_objective,
            sp.phone
        FROM users u
        LEFT JOIN student_profiles sp
            ON u.user_id = sp.user_id
        WHERE u.user_id = %s
        AND u.role = 'student'
    """, (student_id,))

    student = cursor.fetchone()

    # Get student skills
    cursor.execute("""
        SELECT
            s.skill_name,
            s.category,
            ss.skill_level
        FROM student_skills ss
        JOIN skills s
            ON ss.skill_id = s.skill_id
        WHERE ss.user_id = %s
        ORDER BY s.category, s.skill_name
    """, (student_id,))

    skills = cursor.fetchall()
        # Get student projects
    cursor.execute("""
        SELECT
            project_name,
            description,
            technologies,
            completion_date,
            github_link
        FROM projects
        WHERE user_id = %s
        ORDER BY completion_date DESC
    """, (student_id,))

    projects = cursor.fetchall()
        # Get student certifications
    cursor.execute("""
        SELECT
            certificate_name,
            organization,
            issue_date,
            credential_id,
            certificate_link
        FROM certifications
        WHERE user_id = %s
        ORDER BY issue_date DESC
    """, (student_id,))

    certifications = cursor.fetchall()
        # Get student aptitude tests
    cursor.execute("""
        SELECT
            test_name,
            category,
            score,
            test_date
        FROM aptitude_tests
        WHERE user_id = %s
        ORDER BY test_date DESC
    """, (student_id,))

    aptitude_tests = cursor.fetchall()
        # Get student interview scores
    cursor.execute("""
        SELECT
            communication,
            technical,
            confidence,
            problem_solving,
            interview_date
        FROM interview_scores
        WHERE user_id = %s
        ORDER BY interview_date DESC
    """, (student_id,))

    interview_scores = cursor.fetchall()
        # Calculate student placement readiness

    # Average Skill Score
    cursor.execute("""
        SELECT AVG(skill_level) AS avg_skill
        FROM student_skills
        WHERE user_id = %s
    """, (student_id,))

    skill_result = cursor.fetchone()
    skill_score = float(skill_result["avg_skill"] or 0)

    # Project Score
    cursor.execute("""
        SELECT COUNT(*) AS project_count
        FROM projects
        WHERE user_id = %s
    """, (student_id,))

    project_count = cursor.fetchone()["project_count"]
    project_score = min(project_count * 25, 100)

    # Certification Score
    cursor.execute("""
        SELECT COUNT(*) AS certification_count
        FROM certifications
        WHERE user_id = %s
    """, (student_id,))

    certification_count = cursor.fetchone()["certification_count"]
    certification_score = min(certification_count * 25, 100)

    # Aptitude Score
    cursor.execute("""
        SELECT AVG(score) AS avg_aptitude
        FROM aptitude_tests
        WHERE user_id = %s
    """, (student_id,))

    aptitude_result = cursor.fetchone()
    aptitude_score = float(aptitude_result["avg_aptitude"] or 0)

    # Interview Score
    cursor.execute("""
        SELECT AVG(
            (communication + technical + confidence + problem_solving) / 4
        ) AS avg_interview
        FROM interview_scores
        WHERE user_id = %s
    """, (student_id,))

    interview_result = cursor.fetchone()
    interview_score = float(interview_result["avg_interview"] or 0)

    # Final Readiness Score
    readiness_score = (
        (skill_score * 0.35) +
        (project_score * 0.20) +
        (certification_score * 0.10) +
        (aptitude_score * 0.20) +
        (interview_score * 0.15)
    )

    # Readiness Status
    if readiness_score >= 80:
        readiness_status = "Excellent - Placement Ready"
    elif readiness_score >= 70:
        readiness_status = "Good - Almost Placement Ready"
    elif readiness_score >= 50:
        readiness_status = "Needs Improvement"
    else:
        readiness_status = "Beginner - Keep Improving"
    cursor.close()
    connection.close()

    # If ID is not a student
    if not student:
        return "Student not found!", 404

    return render_template(
        "admin_student_details.html",
        admin=admin,
        student=student,
        skills=skills,
        projects=projects,
        certifications=certifications,
        aptitude_tests=aptitude_tests,
        interview_scores=interview_scores,
        readiness_score=readiness_score,
        readiness_status=readiness_status
    )
@app.route("/readiness")
def readiness():
    user_id = session.get("user_id")

    if not user_id:
      return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # 1. Skills Score
    cursor.execute("""
        SELECT AVG(skill_level) AS skill_score
        FROM student_skills
        WHERE user_id = %s
    """, (user_id,))

    skill_result = cursor.fetchone()

    skill_score = skill_result["skill_score"] or 0


    # 2. Projects Score
    cursor.execute("""
        SELECT COUNT(*) AS project_count
        FROM projects
        WHERE user_id = %s
    """, (user_id,))

    project_result = cursor.fetchone()

    project_count = project_result["project_count"]

    project_score = min(project_count * 25, 100)


    # 3. Certifications Score
    cursor.execute("""
        SELECT COUNT(*) AS certification_count
        FROM certifications
        WHERE user_id = %s
    """, (user_id,))

    certification_result = cursor.fetchone()

    certification_count = certification_result["certification_count"]

    certification_score = min(certification_count * 25, 100)


    # 4. Aptitude Score
    cursor.execute("""
        SELECT AVG(score) AS aptitude_score
        FROM aptitude_tests
        WHERE user_id = %s
    """, (user_id,))

    aptitude_result = cursor.fetchone()

    aptitude_score = aptitude_result["aptitude_score"] or 0


    # 5. Interview Score
    cursor.execute("""
        SELECT AVG(
            (communication +
             technical +
             confidence +
             problem_solving) / 4
        ) AS interview_score
        FROM interview_scores
        WHERE user_id = %s
    """, (user_id,))

    interview_result = cursor.fetchone()

    interview_score = interview_result["interview_score"] or 0


    # Overall Placement Readiness
    readiness_score = (
        (float(skill_score) * 0.35) +
        (float(project_score) * 0.20) +
        (float(certification_score) * 0.10) +
        (float(aptitude_score) * 0.20) +
        (float(interview_score) * 0.15)
    )

    readiness_score = round(readiness_score, 2)


    # Readiness Status
    if readiness_score >= 80:
        readiness_status = "Excellent - Placement Ready"

    elif readiness_score >= 70:
        readiness_status = "Good - Almost Placement Ready"

    elif readiness_score >= 50:
        readiness_status = "Needs Improvement"

    else:
        readiness_status = "Beginner - Keep Improving"


    cursor.close()
    connection.close()


    return render_template(
        "readiness.html",
        readiness_score=readiness_score,
        readiness_status=readiness_status,
        skill_score=round(float(skill_score), 2),
        project_score=round(float(project_score), 2),
        certification_score=round(float(certification_score), 2),
        aptitude_score=round(float(aptitude_score), 2),
        interview_score=round(float(interview_score), 2)
    )
@app.route("/skill-gap")
def skill_gap():
    user_id = session.get("user_id")

    if not user_id:
      return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Target role - currently Data Analyst
    target_role = "Data Analyst"


    # Get role ID
    cursor.execute("""
        SELECT role_id
        FROM target_roles
        WHERE role_name = %s
    """, (target_role,))

    role_result = cursor.fetchone()

    skill_gaps = []


    if role_result:

        role_id = role_result["role_id"]

        # Get required skills and student's current skill levels
        cursor.execute("""
            SELECT
                skills.skill_name,
                role_skills.required_level,
                COALESCE(student_skills.skill_level, 0) AS current_level
            FROM role_skills

            JOIN skills
                ON role_skills.skill_id = skills.skill_id

            LEFT JOIN student_skills
                ON role_skills.skill_id = student_skills.skill_id
                AND student_skills.user_id = %s

            WHERE role_skills.role_id = %s

            ORDER BY skills.skill_name
        """, (user_id, role_id))

        results = cursor.fetchall()


        # Calculate skill gaps
        for skill in results:

            required_level = skill["required_level"]
            current_level = skill["current_level"]

            gap = max(required_level - current_level, 0)

            skill_gaps.append({
                "skill_name": skill["skill_name"],
                "required_level": required_level,
                "current_level": current_level,
                "gap": gap
            })


    # Summary calculations

    total_skills = len(skill_gaps)

    skills_to_improve = sum(
        1 for skill in skill_gaps
        if skill["gap"] > 0
    )

    skills_ready = sum(
        1 for skill in skill_gaps
        if skill["gap"] == 0
    )


    cursor.close()
    connection.close()


    return render_template(
        "skill_gap.html",
        target_role=target_role,
        skill_gaps=skill_gaps,
        total_skills=total_skills,
        skills_to_improve=skills_to_improve,
        skills_ready=skills_ready
    )
@app.route("/recommendations")
def recommendations():
    user_id = session.get("user_id")

    if not user_id:
      return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    target_role = "Data Analyst"

    recommendations_list = []


    # Get Target Role ID
    cursor.execute("""
        SELECT role_id
        FROM target_roles
        WHERE role_name = %s
    """, (target_role,))

    role_result = cursor.fetchone()


    if role_result:

        role_id = role_result["role_id"]


        # Get Required Skills and Current Skills
        cursor.execute("""
            SELECT
                skills.skill_name,
                role_skills.required_level,
                COALESCE(student_skills.skill_level, 0) AS current_level

            FROM role_skills

            JOIN skills
                ON role_skills.skill_id = skills.skill_id

            LEFT JOIN student_skills
                ON role_skills.skill_id = student_skills.skill_id
                AND student_skills.user_id = %s

            WHERE role_skills.role_id = %s

            ORDER BY skills.skill_name
        """, (user_id, role_id))


        skill_results = cursor.fetchall()


        # Generate Recommendations
        for skill in skill_results:

            required_level = skill["required_level"]
            current_level = skill["current_level"]

            gap = max(required_level - current_level, 0)


            if gap > 0:

                skill_name = skill["skill_name"]


                if skill_name == "Python":

                    message = (
                        "Practice Python programming, "
                        "Pandas and data analysis projects."
                    )

                elif skill_name == "SQL":

                    message = (
                        "Practice SQL queries, joins, "
                        "subqueries and data analysis."
                    )

                elif skill_name == "Microsoft Excel":

                    message = (
                        "Improve Excel skills such as "
                        "XLOOKUP, Pivot Tables and advanced formulas."
                    )

                elif skill_name == "Power BI":

                    message = (
                        "Create Power BI dashboards and practice "
                        "data modelling and DAX."
                    )

                else:

                    message = (
                        "Practice this skill regularly and "
                        "work on practical projects."
                    )


                recommendations_list.append({
                    "skill_name": skill_name,
                    "gap": gap,
                    "message": message
                })


    cursor.close()
    connection.close()


    return render_template(
        "recommendations.html",
        recommendations=recommendations_list
    )
@app.route("/progress")
def progress():
    user_id = session.get("user_id")

    if not user_id:
      return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # 1. Skills Score
    cursor.execute("""
        SELECT AVG(skill_level) AS skill_score
        FROM student_skills
        WHERE user_id = %s
    """, (user_id,))

    skill_result = cursor.fetchone()
    skill_score = skill_result["skill_score"] or 0
    # Skills Count
    cursor.execute("""
    SELECT COUNT(*) AS skill_count
    FROM student_skills
    WHERE user_id = %s
""", (user_id,))

    skill_count = cursor.fetchone()["skill_count"]

    # 2. Projects Score
    cursor.execute("""
        SELECT COUNT(*) AS project_count
        FROM projects
        WHERE user_id = %s
    """, (user_id,))

    project_result = cursor.fetchone()
    project_count = project_result["project_count"]

    project_score = min(project_count * 25, 100)


    # 3. Certifications Score
    cursor.execute("""
        SELECT COUNT(*) AS certification_count
        FROM certifications
        WHERE user_id = %s
    """, (user_id,))

    certification_result = cursor.fetchone()
    certification_count = certification_result["certification_count"]

    certification_score = min(certification_count * 25, 100)


    # 4. Aptitude Score
    cursor.execute("""
        SELECT AVG(score) AS aptitude_score
        FROM aptitude_tests
        WHERE user_id = %s
    """, (user_id,))

    aptitude_result = cursor.fetchone()
    aptitude_score = aptitude_result["aptitude_score"] or 0


    # 5. Interview Score
    cursor.execute("""
        SELECT AVG(
            (communication +
             technical +
             confidence +
             problem_solving) / 4
        ) AS interview_score
        FROM interview_scores
        WHERE user_id = %s
    """, (user_id,))

    interview_result = cursor.fetchone()
    interview_score = interview_result["interview_score"] or 0


    # 6. Overall Placement Readiness
    readiness_score = (
        (float(skill_score) * 0.35) +
        (float(project_score) * 0.20) +
        (float(certification_score) * 0.10) +
        (float(aptitude_score) * 0.20) +
        (float(interview_score) * 0.15)
    )

    readiness_score = round(readiness_score, 2)


    # Close database
    cursor.close()
    connection.close()


    return render_template(
        "progress.html",
        readiness_score=readiness_score,
        skill_score=round(float(skill_score), 2),
        project_score=round(float(project_score), 2),
        certification_score=round(float(certification_score), 2),
        aptitude_score=round(float(aptitude_score), 2),
        interview_score=round(float(interview_score), 2),
        skill_count=skill_count,
        project_count=project_count,
        certification_count=certification_count
    )
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))
if __name__ == "__main__":
    app.run(debug=True)