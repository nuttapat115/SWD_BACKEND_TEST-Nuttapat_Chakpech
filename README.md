# SWD_BACKEND_TEST-Nuttapat_Chakpech
---
## ข้อ 2
  - ### 2.1 ให้ทำ todo list โดยใช้ django framework มีใช้หน้า server side หรือapi ก็ได้
    
    **App Location** -> todoapp
    
    
**Future**

    - สามารถเพิ่ม task ได้
    - สามารถแก้ไข task ได้
    - สามารลบ task ได้
    - สามารเรียกดู task ได้
    - มี Response หากเกิด error และสำเร็จ

  Herder

    {"Content-Type" : "application/json"}
  
  ---
    # Add Task

    POST http://{ip}:{port}/todo/api/task

      Body

            {
              "title": "Task a",
              "description":"Do task a", // option
              "status" : false, // option
              "due_datetime": "2023-02-13" // option
            }


  ---
            
     # Edit Task

      PUT http://{ip}:{port}/todo/api/task/{task_id:int}

      Body

            {
              "title": "Task a", // option
              "description":"Do task a", // option
              "status" : false, // option
              "due_datetime": "2023-02-13" // option
            }
            
  ---
            
     # Delet Task

      DELET http://{ip}:{port}/todo/api/task/{task_id:int}

  ---
            
     # Get Task

      GET http://{ip}:{port}/todo/api/task/{task_id:int}
      
  ---
 
   - ### 2.2 สร้างระบบช่วยส่งอีเมลล์ตอบกลับ ด้วยDjango framework  มีใช้หน้า server side หรือ api ก็ได้โดยในการส่งให้ระบุอีเมลล์ผู้รับ ชื่อ เนื้อความ
  **App Location** -> emaildender
      
**Future**
    - สามารถส่ง email ระบุ email, subject, body
    - มี Response หากเกิด error และสำเร็จ

  Herder

    {"Content-Type" : "application/json"}
  
  ---
    # Send mail

    POST http://{ip}:{port}/emailsender/

      Body

            {
                "send_to": "receiver@mail.com",
                "subject": "Email Subject",
                "body": "Email body"
            }


  ---
  
   - ### 2.3 เขียนโปรแกรมหา index ของตัวเลขที่มีค่ามากที่สุดใน Array ด้วยภาษาpython 
  **App Location** -> Ex2/2.3 indexofmost.py
  
  ```python
  def index_of_most(arr):
    # เช่น [1,2,1,3,5,6,4] ลำดับที่มีค่ามากที่สุด คือ index = 5 
    # กำหนดค่าเริ่มต้น
    max_temp = arr[0]
    index_of_max = 0
    index_now = 0
    for i in arr:
        # ถ้า i มากกว่า max ปัจจุบัน
        if i > max_temp:
            # เปลี่ยน max
            max_temp = i
            # update index
            index_of_max = index_now
        index_now += 1
    
    return index_of_max
  ```
  
