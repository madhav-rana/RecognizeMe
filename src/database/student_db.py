from src.database.db import supabase


def get_all_students():

    # result = supabase.table("students").select("*").execute()

    # or 

    # result = supabase.table("students")\
    #     .select("*")\
    #     .execute()
    
    # or 

    res = (
        supabase
        .table("students")
        .select("*")
        .execute()
    )

    print(res)
    return res.data




def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {
        'name': new_name,
        'face_embedding':face_embedding,
        "voice_embedding": voice_embedding
    }
    result = (
        supabase
        .table('students')
        .insert(data)
        .execute()
    )
    print(result)
    return result.data



def  enroll_student_to_subject(student_id, subject_id):
    data = {
        "student_id": student_id,
        "subject_id": subject_id
    }
    res= (
        supabase
        .table('subject_students')
        .insert(data)
        .execute()
    )

    return res.data




def get_student_subjects(student_id):
    res = (
        supabase
        .table('subject_students')
        .select('*, subjects(*)')
        .eq('student_id', student_id)
        .execute()
    )
    return res.data




def get_student_attendance(student_id):
    res = (
        supabase
        .table('attendance_logs')
        .select('*, subjects(*)')
        .eq('student_id', student_id)
        .execute()
    )
    return res.data




def  unenroll_student_to_subject(student_id, subject_id):
    res= (
        supabase
        .table('subject_students')
        .delete()
        .eq('student_id', student_id)
        .eq('subject_id', subject_id)
        .execute()
    )
    return res.data



