import sys
import os
# Add project root to Python path
sys.path.insert(0,os.path.dirname(__file__))
from app import create_app
from services.auth_service import AuthService
from services.course_service import CourseService
from database.db import get_connection
def init_admin_user():
    """Create a default admin user"""
    conn=None
    try:
        conn=get_connection()
        row=conn.execute(
            "SELECT * FROM users WHERE username=?",
            ("Kamalesh Chandrasekaran",)
        ).fetchone()
        if row is None:
            success,message=AuthService.register_user(
                "Kamalesh Chandrasekaran",
                "kamalesh302003@gmail.com",
                "Kamalesh@2003"
            )

            if success:
                print("✓ Admin user created successfully")
                print("Username: Kamalesh Chandrasekaran")
                print("Password: Kamalesh@2003")
            else:
                print(f"✗ Failed to create admin user: {message}")
        else:
            print("✓ Admin user already exists")
    except Exception as e:
        print(f"✗ Error creating admin user:{e}")
    finally:
        if conn:
            conn.close()
def init_sample_courses():
    """Create sample courses"""
    sample_courses=[
        {
            "code":"MCS101",
            "title":"Advanced Python Programming",
            "description":"Master Python programming, OOP concepts, modules, and application development"
        },

        {
            "code":"MCS102",
            "title":"Data Structures and Algorithms",
            "description":"Learn advanced data structures and algorithm optimization techniques"
        },

        {
            "code":"MCS103",
            "title":"Database Management Systems",
            "description":"Study relational databases, SQL, normalization, and database design"
        },

        {
            "code":"MCS104",
            "title":"Web Application Development",
            "description":"Develop dynamic web applications using Flask, HTML, CSS, and JavaScript"
        },

        {
            "code":"MCS105",
            "title":"Software Engineering",
            "description":"Understand software development methodologies and project management"
        },

        {
            "code":"MCS106",
            "title":"Computer Networks",
            "description":"Learn network architecture, protocols, routing, and security concepts"
        },

        {
            "code":"MCS107",
            "title":"Operating Systems",
            "description":"Study process scheduling, memory management, and file systems"
        },

        {
            "code":"MCS108",
            "title":"Artificial Intelligence",
            "description":"Explore machine learning, intelligent systems, and AI applications"
        },

        {
            "code":"MCS109",
            "title":"Cyber Security",
            "description":"Learn information security, ethical hacking, and cyber defense techniques"
        },

        {
            "code":"MCS110",
            "title":"Cloud Computing",
            "description":"Understand cloud platforms, virtualization, and distributed computing"
        }
    ]
    conn=None

    try:
        conn=get_connection()
        cursor=conn.cursor()
        added_count=0
        for course in sample_courses:
            row=cursor.execute(
                "SELECT * FROM courses WHERE code=?",
                (course["code"],)
            ).fetchone()
            if row is None:
                success,message=CourseService.add_course(course)
                if success:
                    added_count+=1
        if added_count > 0:
            print(f"✓ Added {added_count} sample courses")
        else:
            print("✓ Sample courses already exist")
    except Exception as e:
        print(f"✗ Error adding sample courses:{e}")
    finally:
        if conn:
            conn.close()

if __name__=="__main__":

    print("=" * 60)
    print("      STUDENT MANAGEMENT SYSTEM INITIALIZATION")
    print("=" * 60)

    try:
        app=create_app()
        print("✓ Database initialized")
        init_admin_user()
        init_sample_courses()
        print("\n" + "=" * 60)
        print("✓ SYSTEM INITIALIZED SUCCESSFULLY")
        print("=" * 60)
        print("\nDefault Login Credentials")
        print("-" * 30)
        print("Username: Kamalesh Chandrasekaran")
        print("Password: Kamalesh@2003")
        print("\nRun the application:")
        print("python app.py")

    except Exception as e:
        print(f"\n✗ Initialization failed:{e}")