# SWD_BACKEND_TEST-Nuttapat_Chakpech
---
## ข้อ 2
  - ### 2.1 ให้ทำ todo list โดยใช้ django framework มีใช้หน้า server side หรือapi ก็ได้
    
    **App Location** -> todoapp
    
**Future**

    - Add Task

    POST http://{ip}:{port}/todo/api/task

      Herder

            {"Content-Type" : "application/json"}

      Body

            {
              "title": "Task a",
              "description":"Do task a", // option
              "status" : false, // option
              "due_datetime": "2023-02-13" // option
            }

  ---
            
      - Edit Task

              PUT http://{ip}:{port}/todo/api/task

              Herder

                    {"Content-Type" : "application/json"}

              Body

                    {
                      "title": "Task a",
                      "description":"Do task a", // option
                      "status" : false, // option
                      "due_datetime": "2023-02-13" // option
                    }
      
