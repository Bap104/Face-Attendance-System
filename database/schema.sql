"""
Students
--------
student_id TEXT PRIMARY KEY
name TEXT NOT NULL
face_embedding BLOB   -- vector numpy đã serialize (giai đoạn 9)
created_at TEXT

Attendance
----------
id INTEGER PRIMARY KEY AUTOINCREMENT
student_id TEXT NOT NULL
date TEXT NOT NULL
time TEXT NOT NULL
status TEXT NOT NULL
UNIQUE(student_id, date)  -- chống điểm danh trùng trong ngày
"""
