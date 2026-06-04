from src.database.db import supabase
import bcrypt

def register_teacher(name, username, password):
    # check username already exists
    existing = supabase.table("teachers")\
        .select("*")\
        .eq("username", username)\
        .execute()

    if existing.data:
        return {"success": False, "message": "Username already taken"}

    # hash password
    hashed_password = bcrypt.hashpw(
        password.encode(), 
        bcrypt.gensalt()
    ).decode()

    res = supabase.table("teachers").insert(
        {
            "name": name,
            "username": username,
            "password": hashed_password
        }
    ).execute()

    return {"success": True, "data": res.data}



def login_teacher(username, password):
    result = supabase.table("teachers")\
        .select("*")\
        .eq("username", username)\
        .execute()

    if not result.data:
        return {"success": False, "message": "Username not found"}

    teacher = result.data[0]

    match = bcrypt.checkpw(
        password.encode(), 
        teacher["password"].encode()
    )

    if not match:
        return {"success": False, "message": "Wrong password"}

    return {"success": True, "data": teacher}



def create_subject(subject_code, name, section, teacher_id):
    data = {
        "subject_code": subject_code,
        "name": name, 
        "section": section, 
        "teacher_id": teacher_id
    }
    res = supabase.table("subjects").insert(data).execute()

    return res.data



def get_teacher_subjects(teacher_id):
    res = (
        supabase
        .table('subjects')
        .select("*, subject_students(count), attendance_logs(timestamp)")
        .eq("teacher_id", teacher_id)
        .execute()
    )
    subjects = res.data

    for sub in subjects:
        sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
        attendance = sub.get('attendance_logs', [])
        unique_sessions = len(set(log['timestamp'] for log in attendance))
        sub['total_classes'] = unique_sessions


        sub.pop('subject_student', None)
        sub.pop('attendance_logs', None)

    return subjects


def create_attendance(logs):
    response = supabase.table('attendance_logs').insert(logs).execute()
    return response.data

def get_attendance_for_teacher(teacher_id):
    res = (
        supabase
        .table('attendance_logs')
        .select("*, subjects!inner(*)")
        .eq('subjects.teacher_id', teacher_id)
        .execute()
    )
    return res.data