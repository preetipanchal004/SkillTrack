# SkillTrack – Student Skill Development & Placement Analytics Website

## 📌 Project Overview

SkillTrack is a web-based Student Skill Development and Placement Analytics system developed to help students track their skills, courses, certifications, projects, aptitude performance, interview performance, and overall placement readiness.

The system provides personalized skill gap analysis, recommendations, progress tracking, and placement readiness analytics. An admin dashboard is also provided for monitoring student performance.

## 🎯 Objectives

- To provide a centralized platform for student skill development.
- To track technical and soft skills.
- To manage courses, certifications, and projects.
- To monitor aptitude and interview performance.
- To calculate overall placement readiness.
- To identify skill gaps according to target job roles.
- To provide personalized recommendations.
- To provide basic analytics for the placement/admin team.

## ✨ Key Features

### Student Features

- Student Registration and Login
- Student Profile Management
- Skill Tracking
- Course Tracking
- Certification Management
- Project Portfolio Management
- Aptitude Test Performance
- Interview Performance Tracking
- Placement Readiness Score
- Skill Gap Analysis
- Personalized Recommendations
- Progress Analytics

### Admin Features

- Secure Admin Login
- Admin Dashboard
- Student Performance Overview
- Student Details
- Placement Readiness Monitoring
- Skills, Projects, Certifications and Performance Data Viewing

## 📊 Placement Readiness

SkillTrack calculates placement readiness using multiple performance factors:

- Skills – 35%
- Projects – 20%
- Certifications – 10%
- Aptitude – 20%
- Interview – 15%

The system categorizes students into different readiness levels such as:

- Excellent – Placement Ready
- Good – Almost Placement Ready
- Needs Improvement
- Beginner – Keep Improving

## 🛠️ Technologies Used

### Frontend
- HTML
- CSS
- JavaScript
- Chart.js

### Backend
- Python
- Flask

### Database
- MySQL

### Tools
- Visual Studio Code
- MySQL Workbench
- Git
- GitHub
- Microsoft Edge

## 🗄️ Database

The project uses MySQL database named:

`skilltrack_db`

The database contains tables for:

- Users
- Student Profiles
- Skills
- Student Skills
- Courses
- Certifications
- Projects
- Aptitude Tests
- Interview Scores
- Target Roles
- Role Skills

## 📁 Project Structure

```text
SkillTrack/
│
├── app.py
│
├── database/
│   └── connection.py
│
├── templates/
│   ├── index.html
│   ├── about.html
│   ├── features.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── skills.html
│   ├── courses.html
│   ├── certifications.html
│   ├── projects.html
│   ├── tests.html
│   ├── interview.html
│   ├── readiness.html
│   ├── skill_gap.html
│   ├── recommendations.html
│   ├── progress.html
│   ├── admin_dashboard.html
│   └── admin_student_details.html
│
├── static/
│   └── css/
│       └── style.css
│
└── README.md
