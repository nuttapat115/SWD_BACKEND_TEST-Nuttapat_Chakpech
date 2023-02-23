
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apis.models import SchoolStructure, Schools, Classes, Personnel, Subjects, StudentSubjectsScore

def grade_cal(score):
        if score >= 80:
            return "A", 4
        elif score >= 75:
            return "B+", 3.5
        elif score >= 70:
            return "B", 3
        elif score >= 65:
            return "C+", 2.5
        elif score >= 60:
            return "C", 2
        elif score >= 55:
            return "D+", 1.5
        elif score >= 50:
            return "D", 1
        else:
            return "F", 0

def gpa_cal(grade_set):
        point = 0
        tatal_credit = 0 
        for grade in grade_set:
            point += grade["value"]*grade["credits"]
            tatal_credit += grade["credits"]
        gpa = point/tatal_credit
        return f"{gpa:.2f}"
        # pass
        
class StudentSubjectsScoreAPIView(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        """
        [Backend API and Data Validations Skill Test]

        description: create API Endpoint for insert score data of each student by following rules.

        rules:      - ✅ Score must be number, equal or greater than 0 and equal or less than 100.
                    - ✅ Credit must be integer, greater than 0 and equal or less than 3.
                    - ✅ Payload data must be contained `first_name`, `last_name`, `subject_title` and `score`.
                        -✅ `first_name` in payload must be string (if not return bad request status).
                        - ✅`last_name` in payload must be string (if not return bad request status).
                        - ✅`subject_title` in payload must be string (if not return bad request status).
                        - ✅`score` in payload must be number (if not return bad request status).

                    -✅ Student's score of each subject must be unique (it's mean 1 student only have 1 row of score
                            of each subject).
                    - ✅ If student's score of each subject already existed, It will update new score
                            (Don't created it).
                    - ✅ If Update, Credit must not be changed.
                    -✅ If Data Payload not complete return clearly message with bad request status.
                    -✅ If Subject's Name or Student's Name not found in Database return clearly message with bad request status.
                    -✅ If Success return student's details, subject's title, credit and score context with created status.

        remark:     - `score` is subject's score of each student.
                    - `credit` is subject's credit.
                    - student's first name, lastname and subject's title can find in DATABASE (you can create more
                            for test add new score).

        """

        subjects_context = [{"id": 1, "title": "Math"}, {"id": 2, "title": "Physics"}, {"id": 3, "title": "Chemistry"},
                            {"id": 4, "title": "Algorithm"}, {"id": 5, "title": "Coding"}]

        credits_context = [{"id": 6, "credit": 1, "subject_id_list_that_using_this_credit": [3]},
                           {"id": 7, "credit": 2, "subject_id_list_that_using_this_credit": [2, 4]},
                           {"id": 9, "credit": 3, "subject_id_list_that_using_this_credit": [1, 5]}]

        credits_mapping = [{"subject_id": 1, "credit_id": 9}, {"subject_id": 2, "credit_id": 7},
                           {"subject_id": 3, "credit_id": 6}, {"subject_id": 4, "credit_id": 7},
                           {"subject_id": 5, "credit_id": 9}]

        student_first_name = request.data.get("first_name", None)
        student_last_name = request.data.get("last_name", None)
        subjects_title = request.data.get("subject_title", None)
        scoreInput = request.data.get("score", None)


        
        # The above code is checking if the student_first_name, student_last_name, subjects_title,
        # score are empty or not.
        if(student_first_name == None or student_last_name == None or subjects_title == None or scoreInput  == None
           or student_first_name == "" or student_last_name == "" or subjects_title == ""):
            payload = { 
                "status" : 400,
                "massage" : "Bad Request: Invalid request payload",
                "detial" : "The request payload must include 'first_name', 'last_name', 'subject_title' and 'score'.",
                "data" : {"first_name": student_first_name, "last_name": student_last_name, "subjects_title": subjects_title, "score": scoreInput},
            }
            return Response(payload,status=status.HTTP_400_BAD_REQUEST)
        
        
        # The above code is checking if the variables are strings.
        if isinstance(student_first_name, str) and isinstance(student_last_name, str) and isinstance(subjects_title, str):
            pass
        else:
            payload = { 
                "status" : 400,
                "massage" : "Bad Request: Invalid request payload",
                "detial" : "The request payload 'first_name', 'last_name', 'subject_title' must be string",
                "data" : {"first_name": student_first_name, "last_name": student_last_name, "subjects_title": subjects_title},
            }
            return Response(payload,status=status.HTTP_400_BAD_REQUEST)
        
        
        try:
            scoreInput = float(scoreInput)
            if scoreInput < 0 or scoreInput > 100:
                payload = { 
                "status" : 400,
                "massage" : "Bad Request: Invalid request payload",
                "detial" : "The request payload 'score' must be equal or greater than 0 and equal or less than 100",
                "data" : {"score":scoreInput},
                }
                return Response(payload,status=status.HTTP_400_BAD_REQUEST)
        except:
            payload = { 
                "status" : 400,
                "massage" : "Bad Request: Invalid request payload",
                "detial" : "The request payload 'score' must be number.",
                "data" : {"score":scoreInput},
            }
            return Response(payload,status=status.HTTP_400_BAD_REQUEST)


        students_check = Personnel.objects.filter(first_name = student_first_name,last_name=student_last_name,personnel_type = 1) | Personnel.objects.filter(first_name = student_first_name,last_name=student_last_name,personnel_type = 2)
        if len(students_check) == 0 :
            payload = { 
                "status" : 400,
                "massage" : "Bad Request: Invalid request payload",
                "detial" : "Student's name not found in Database.",
                "data" : {"first_name": student_first_name, "last_name": student_last_name},
            }
            return Response(payload,status=status.HTTP_400_BAD_REQUEST)
        for student in students_check:
            studentId = student.id
            studentObj = student
        

        subjects_check = Subjects.objects.filter(title=subjects_title)
        if len(subjects_check) == 0 :
            payload = { 
                "status" : 400,
                "massage" : "Bad Request: Invalid request payload",
                "detial" : "Subjects not found in Database.",
                "data" : {"subjects_title": subjects_title}
            }
            return Response(payload,status=status.HTTP_400_BAD_REQUEST)
        

        for subjects in subjects_check:
            subjectObj = subjects
            subjectId = subjects.id
            creditId = next(item["credit_id"] for item in credits_mapping if item["subject_id"] == subjectId)
            creditValue = next(item["credit"] for item in credits_context if item["id"] == creditId)

        check_score = StudentSubjectsScore.objects.filter(student = studentId, subjects = subjectId)
        if len(check_score) > 0:
            #  Update case
            check_score.update(score = scoreInput)
            payload = {
                "status": 200,
                "massage" : "Update success",
                "data" : {"first_name":student_first_name, "last_name": student_last_name, 
                          "subjects_title": subjects_title, "credit":creditValue, "score": scoreInput}
            }
            return Response(payload,status=status.HTTP_200_OK)

        if len(check_score) == 0:
            #  Create case
            insert_score = StudentSubjectsScore.objects.create(student = studentObj, subjects = subjectObj, credit = creditValue, score = scoreInput)
            payload = {
                "status": 201,
                "massage" : "Create success",
                "data" : {"first_name":student_first_name, "last_name": student_last_name, 
                          "subjects_title": subjects_title, "credit":creditValue, "score": scoreInput}
            }
            return Response(payload,status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentSubjectsScoreDetailsAPIView(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        # return {"payload": "Test"}
        """
        [Backend API and Data Calculation Skill Test]

        description: get student details, subject's details, subject's credit, their score of each subject,
                    their grade of each subject and their grade point average by student's ID.

        pattern:     Data pattern in 'context_data' variable below.

        remark:     - `grade` will be A  if 80 <= score <= 100
                                      B+ if 75 <= score < 80
                                      B  if 70 <= score < 75
                                      C+ if 65 <= score < 70
                                      C  if 60 <= score < 65
                                      D+ if 55 <= score < 60
                                      D  if 50 <= score < 55
                                      F  if score < 50

        """

        student_id = kwargs.get("id", None)
        student_find = Personnel.objects.filter(id = student_id,personnel_type=1) | Personnel.objects.filter(id = student_id,personnel_type=2)
        if len(student_find) == 0:
            payload = {
                "status" : 400,
                "massage" : "id not found or Personnel is 'class_teacher'"
            }
            return Response(payload,status=status.HTTP_400_BAD_REQUEST)
        for student in student_find:
            studentObf = student
            student_name = student.first_name+" "+student.last_name
            classObj = student.school_class
            schoolID = Classes.objects.get(id = classObj.id).school.id
            schoolName = Schools.objects.get(id = schoolID).title

        avgGrade = 0
        socres = StudentSubjectsScore.objects.filter(student = studentObf)
        subject_detail=[]
        grade_set = []
        if len(socres) > 0:
            for score in socres:
                grade, value = grade_cal(score.score)
                subjectTitle = Subjects.objects.get(id=score.subjects.id).title
                creditsValue = score.credit
                subject_detail.append({
                        "subject": subjectTitle,
                        "credits": creditsValue,
                        "score": score.score,
                        "grade": grade,
                        })
                grade_set.append({"credits": creditsValue, "value":value})
            avgGrade = gpa_cal(grade_set)
        else:
            pass

        context_data = {
            "student":
                {
                    "id": student_id,
                    "full_name": student_name,
                    "school": schoolName
                },

            "subject_detail": subject_detail,

            "grade_point_average": avgGrade,
        }

        return Response(context_data, status=status.HTTP_200_OK)

class PersonnelDetailsAPIView(APIView):

    def get(self, request, *args, **kwargs):
        """
        [Basic Skill and Observational Skill Test]

        description: get personnel details by school's name.

        data pattern:  {order}. school: {school's title}, role: {personnel type in string}, class: {class's order}, name: {first name} {last name}.

        result pattern : in `data_pattern` variable below.

        example:    1. school: Rose Garden School, role: Head of the room, class: 1, name: Reed Richards.
                    2. school: Rose Garden School, role: Student, class: 1, name: Blackagar Boltagon.

        rules:      - Personnel's name and School's title must be capitalize.
                    - Personnel's details order must be ordered by their role, their class order and their name.

        """

        data_pattern = [
            "1. school: Dorm Palace School, role: Teacher, class: 1,name: Mark Harmon",
            "2. school: Dorm Palace School, role: Teacher, class: 2,name: Jared Sanchez",
            "3. school: Dorm Palace School, role: Teacher, class: 3,name: Cheyenne Woodard",
            "4. school: Dorm Palace School, role: Teacher, class: 4,name: Roger Carter",
            "5. school: Dorm Palace School, role: Teacher, class: 5,name: Cynthia Mclaughlin",
            "6. school: Dorm Palace School, role: Head of the room, class: 1,name: Margaret Graves",
            "7. school: Dorm Palace School, role: Head of the room, class: 2,name: Darren Wyatt",
            "8. school: Dorm Palace School, role: Head of the room, class: 3,name: Carla Elliott",
            "9. school: Dorm Palace School, role: Head of the room, class: 4,name: Brittany Mullins",
            "10. school: Dorm Palace School, role: Head of the room, class: 5,name: Nathan Solis",
            "11. school: Dorm Palace School, role: Student, class: 1,name: Aaron Marquez",
            "12. school: Dorm Palace School, role: Student, class: 1,name: Benjamin Collins",
            "13. school: Dorm Palace School, role: Student, class: 1,name: Carolyn Reynolds",
            "14. school: Dorm Palace School, role: Student, class: 1,name: Christopher Austin",
            "15. school: Dorm Palace School, role: Student, class: 1,name: Deborah Mcdonald",
            "16. school: Dorm Palace School, role: Student, class: 1,name: Jessica Burgess",
            "17. school: Dorm Palace School, role: Student, class: 1,name: Jonathan Oneill",
            "18. school: Dorm Palace School, role: Student, class: 1,name: Katrina Davis",
            "19. school: Dorm Palace School, role: Student, class: 1,name: Kristen Robinson",
            "20. school: Dorm Palace School, role: Student, class: 1,name: Lindsay Haas",
            "21. school: Dorm Palace School, role: Student, class: 2,name: Abigail Beck",
            "22. school: Dorm Palace School, role: Student, class: 2,name: Andrew Williams",
            "23. school: Dorm Palace School, role: Student, class: 2,name: Ashley Berg",
            "24. school: Dorm Palace School, role: Student, class: 2,name: Elizabeth Anderson",
            "25. school: Dorm Palace School, role: Student, class: 2,name: Frank Mccormick",
            "26. school: Dorm Palace School, role: Student, class: 2,name: Jason Leon",
            "27. school: Dorm Palace School, role: Student, class: 2,name: Jessica Fowler",
            "28. school: Dorm Palace School, role: Student, class: 2,name: John Smith",
            "29. school: Dorm Palace School, role: Student, class: 2,name: Nicholas Smith",
            "30. school: Dorm Palace School, role: Student, class: 2,name: Scott Mckee",
            "31. school: Dorm Palace School, role: Student, class: 3,name: Abigail Smith",
            "32. school: Dorm Palace School, role: Student, class: 3,name: Cassandra Martinez",
            "33. school: Dorm Palace School, role: Student, class: 3,name: Elizabeth Anderson",
            "34. school: Dorm Palace School, role: Student, class: 3,name: John Scott",
            "35. school: Dorm Palace School, role: Student, class: 3,name: Kathryn Williams",
            "36. school: Dorm Palace School, role: Student, class: 3,name: Mary Miller",
            "37. school: Dorm Palace School, role: Student, class: 3,name: Ronald Mccullough",
            "38. school: Dorm Palace School, role: Student, class: 3,name: Sandra Davidson",
            "39. school: Dorm Palace School, role: Student, class: 3,name: Scott Martin",
            "40. school: Dorm Palace School, role: Student, class: 3,name: Victoria Jacobs",
            "41. school: Dorm Palace School, role: Student, class: 4,name: Carol Williams",
            "42. school: Dorm Palace School, role: Student, class: 4,name: Cassandra Huff",
            "43. school: Dorm Palace School, role: Student, class: 4,name: Deborah Harrison",
            "44. school: Dorm Palace School, role: Student, class: 4,name: Denise Young",
            "45. school: Dorm Palace School, role: Student, class: 4,name: Jennifer Pace",
            "46. school: Dorm Palace School, role: Student, class: 4,name: Joe Andrews",
            "47. school: Dorm Palace School, role: Student, class: 4,name: Michael Kelly",
            "48. school: Dorm Palace School, role: Student, class: 4,name: Monica Padilla",
            "49. school: Dorm Palace School, role: Student, class: 4,name: Tiffany Roman",
            "50. school: Dorm Palace School, role: Student, class: 4,name: Wendy Maxwell",
            "51. school: Dorm Palace School, role: Student, class: 5,name: Adam Smith",
            "52. school: Dorm Palace School, role: Student, class: 5,name: Angela Christian",
            "53. school: Dorm Palace School, role: Student, class: 5,name: Cody Edwards",
            "54. school: Dorm Palace School, role: Student, class: 5,name: Jacob Palmer",
            "55. school: Dorm Palace School, role: Student, class: 5,name: James Gonzalez",
            "56. school: Dorm Palace School, role: Student, class: 5,name: Justin Kaufman",
            "57. school: Dorm Palace School, role: Student, class: 5,name: Katrina Reid",
            "58. school: Dorm Palace School, role: Student, class: 5,name: Melissa Butler",
            "59. school: Dorm Palace School, role: Student, class: 5,name: Pamela Sutton",
            "60. school: Dorm Palace School, role: Student, class: 5,name: Sarah Murphy"
        ]
        rols = [0,1,2]
        rolsText = {0:"Teacher",1:"Head of the room",2:"Student"}
        school_title = kwargs.get("school_title", None)
        your_result = []
        try:
            schoolId = Schools.objects.get(title = school_title).id
        except:
            your_result = {
                "status" : 400,
                "massage" : "school not found in database"
            }
            return Response(your_result, status=status.HTTP_400_BAD_REQUEST)
        try:
            class_odersObj = Classes.objects.filter(school_id = schoolId)
        except:
            return Response(your_result, status=status.HTTP_200_OK)
        
        cont = 0
        for rol in rols:
            for classs in class_odersObj:
                dataset = Personnel.objects.filter(personnel_type=rol,school_class = classs)
                for data in dataset:
                    cont+=1
                    your_result.append(f'{cont}. school: {school_title}, role: {rolsText[rol]}, class: {classs.class_order}, name: {data.first_name+" "+data.last_name}')
        return Response(your_result, status=status.HTTP_200_OK)
        

class SchoolHierarchyAPIView(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        """
        [Logical Test]

        description: get personnel list in hierarchy order by school's title, class and personnel's name.

        pattern: in `data_pattern` variable below.

        """
        your_result = []
        rols = [0,1,2]
        allSchools = Schools.objects.all()
        for school in allSchools:
            schooldata = {}
            school_title = school.title
            schoolId = school.id
            schooldata.update({"school":school_title})
            class_odersObj = Classes.objects.filter(school_id = schoolId)
            for classs in class_odersObj:
                students = []
                className = f"class {classs.class_order}"
                for role in rols:                        
                    if role == 0:
                        personObj = Personnel.objects.get(personnel_type=role,school_class = classs)
                        personrFirstName = personObj.first_name
                        personLasttName = personObj.last_name
                        teacher = "Teacher: "+personrFirstName + ' ' + personLasttName
                    if role == 1:
                        personObj = Personnel.objects.get(personnel_type=role,school_class = classs)
                        personrFirstName = personObj.first_name
                        personLasttName = personObj.last_name
                        headRoom = {"Head of the room": personrFirstName + ' ' + personLasttName}
                        students.append(headRoom)
                    if role == 2:
                        personObj = Personnel.objects.filter(personnel_type=role,school_class = classs)
                        for preson in personObj:
                            studentsText = {"Student": preson.first_name + ' ' + preson.last_name}
                            students.append(studentsText)
                schooldata.update({className:{teacher:students}})
            your_result.append(schooldata)
                
        data_pattern = [
            {
                "school": "Dorm Palace School",
                "class 1": {
                    "Teacher: Mark Harmon": [
                        {
                            "Head of the room": "Margaret Graves"
                        },
                        {
                            "Student": "Aaron Marquez"
                        },
                        {
                            "Student": "Benjamin Collins"
                        },
                        {
                            "Student": "Carolyn Reynolds"
                        },
                        {
                            "Student": "Christopher Austin"
                        },
                        {
                            "Student": "Deborah Mcdonald"
                        },
                        {
                            "Student": "Jessica Burgess"
                        },
                        {
                            "Student": "Jonathan Oneill"
                        },
                        {
                            "Student": "Katrina Davis"
                        },
                        {
                            "Student": "Kristen Robinson"
                        },
                        {
                            "Student": "Lindsay Haas"
                        }
                    ]
                },
                "class 2": {
                    "Teacher: Jared Sanchez": [
                        {
                            "Head of the room": "Darren Wyatt"
                        },
                        {
                            "Student": "Abigail Beck"
                        },
                        {
                            "Student": "Andrew Williams"
                        },
                        {
                            "Student": "Ashley Berg"
                        },
                        {
                            "Student": "Elizabeth Anderson"
                        },
                        {
                            "Student": "Frank Mccormick"
                        },
                        {
                            "Student": "Jason Leon"
                        },
                        {
                            "Student": "Jessica Fowler"
                        },
                        {
                            "Student": "John Smith"
                        },
                        {
                            "Student": "Nicholas Smith"
                        },
                        {
                            "Student": "Scott Mckee"
                        }
                    ]
                },
                "class 3": {
                    "Teacher: Cheyenne Woodard": [
                        {
                            "Head of the room": "Carla Elliott"
                        },
                        {
                            "Student": "Abigail Smith"
                        },
                        {
                            "Student": "Cassandra Martinez"
                        },
                        {
                            "Student": "Elizabeth Anderson"
                        },
                        {
                            "Student": "John Scott"
                        },
                        {
                            "Student": "Kathryn Williams"
                        },
                        {
                            "Student": "Mary Miller"
                        },
                        {
                            "Student": "Ronald Mccullough"
                        },
                        {
                            "Student": "Sandra Davidson"
                        },
                        {
                            "Student": "Scott Martin"
                        },
                        {
                            "Student": "Victoria Jacobs"
                        }
                    ]
                },
                "class 4": {
                    "Teacher: Roger Carter": [
                        {
                            "Head of the room": "Brittany Mullins"
                        },
                        {
                            "Student": "Carol Williams"
                        },
                        {
                            "Student": "Cassandra Huff"
                        },
                        {
                            "Student": "Deborah Harrison"
                        },
                        {
                            "Student": "Denise Young"
                        },
                        {
                            "Student": "Jennifer Pace"
                        },
                        {
                            "Student": "Joe Andrews"
                        },
                        {
                            "Student": "Michael Kelly"
                        },
                        {
                            "Student": "Monica Padilla"
                        },
                        {
                            "Student": "Tiffany Roman"
                        },
                        {
                            "Student": "Wendy Maxwell"
                        }
                    ]
                },
                "class 5": {
                    "Teacher: Cynthia Mclaughlin": [
                        {
                            "Head of the room": "Nathan Solis"
                        },
                        {
                            "Student": "Adam Smith"
                        },
                        {
                            "Student": "Angela Christian"
                        },
                        {
                            "Student": "Cody Edwards"
                        },
                        {
                            "Student": "Jacob Palmer"
                        },
                        {
                            "Student": "James Gonzalez"
                        },
                        {
                            "Student": "Justin Kaufman"
                        },
                        {
                            "Student": "Katrina Reid"
                        },
                        {
                            "Student": "Melissa Butler"
                        },
                        {
                            "Student": "Pamela Sutton"
                        },
                        {
                            "Student": "Sarah Murphy"
                        }
                    ]
                }
            },
            {
                "school": "Prepare Udom School",
                "class 1": {
                    "Teacher: Joshua Frazier": [
                        {
                            "Head of the room": "Tina Phillips"
                        },
                        {
                            "Student": "Amanda Howell"
                        },
                        {
                            "Student": "Colin George"
                        },
                        {
                            "Student": "Donald Stephens"
                        },
                        {
                            "Student": "Jennifer Lewis"
                        },
                        {
                            "Student": "Jorge Bowman"
                        },
                        {
                            "Student": "Kevin Hooper"
                        },
                        {
                            "Student": "Kimberly Lewis"
                        },
                        {
                            "Student": "Mary Sims"
                        },
                        {
                            "Student": "Ronald Tucker"
                        },
                        {
                            "Student": "Victoria Velez"
                        }
                    ]
                },
                "class 2": {
                    "Teacher: Zachary Anderson": [
                        {
                            "Head of the room": "Joseph Zimmerman"
                        },
                        {
                            "Student": "Alicia Serrano"
                        },
                        {
                            "Student": "Andrew West"
                        },
                        {
                            "Student": "Anthony Hartman"
                        },
                        {
                            "Student": "Dominic Frey"
                        },
                        {
                            "Student": "Gina Fernandez"
                        },
                        {
                            "Student": "Jennifer Riley"
                        },
                        {
                            "Student": "John Joseph"
                        },
                        {
                            "Student": "Katherine Cantu"
                        },
                        {
                            "Student": "Keith Watts"
                        },
                        {
                            "Student": "Phillip Skinner"
                        }
                    ]
                },
                "class 3": {
                    "Teacher: Steven Hunt": [
                        {
                            "Head of the room": "Antonio Hodges"
                        },
                        {
                            "Student": "Brian Lewis"
                        },
                        {
                            "Student": "Christina Wiggins"
                        },
                        {
                            "Student": "Christine Parker"
                        },
                        {
                            "Student": "Hannah Wilson"
                        },
                        {
                            "Student": "Jasmin Odom"
                        },
                        {
                            "Student": "Jeffery Graves"
                        },
                        {
                            "Student": "Mark Roberts"
                        },
                        {
                            "Student": "Paige Pearson"
                        },
                        {
                            "Student": "Philip Fowler"
                        },
                        {
                            "Student": "Steven Riggs"
                        }
                    ]
                },
                "class 4": {
                    "Teacher: Rachael Davenport": [
                        {
                            "Head of the room": "John Cunningham"
                        },
                        {
                            "Student": "Aaron Olson"
                        },
                        {
                            "Student": "Amanda Cuevas"
                        },
                        {
                            "Student": "Gary Smith"
                        },
                        {
                            "Student": "James Blair"
                        },
                        {
                            "Student": "Juan Boone"
                        },
                        {
                            "Student": "Julie Bowman"
                        },
                        {
                            "Student": "Melissa Williams"
                        },
                        {
                            "Student": "Phillip Bright"
                        },
                        {
                            "Student": "Sonia Gregory"
                        },
                        {
                            "Student": "William Martin"
                        }
                    ]
                },
                "class 5": {
                    "Teacher: Amber Clark": [
                        {
                            "Head of the room": "Mary Mason"
                        },
                        {
                            "Student": "Allen Norton"
                        },
                        {
                            "Student": "Eric English"
                        },
                        {
                            "Student": "Jesse Johnson"
                        },
                        {
                            "Student": "Kevin Martinez"
                        },
                        {
                            "Student": "Mark Hughes"
                        },
                        {
                            "Student": "Robert Sutton"
                        },
                        {
                            "Student": "Sherri Patrick"
                        },
                        {
                            "Student": "Steven Brown"
                        },
                        {
                            "Student": "Valerie Mcdaniel"
                        },
                        {
                            "Student": "William Roman"
                        }
                    ]
                }
            },
            {
                "school": "Rose Garden School",
                "class 1": {
                    "Teacher: Danny Clements": [
                        {
                            "Head of the room": "Troy Rodriguez"
                        },
                        {
                            "Student": "Annette Ware"
                        },
                        {
                            "Student": "Daniel Collins"
                        },
                        {
                            "Student": "Jacqueline Russell"
                        },
                        {
                            "Student": "Justin Kennedy"
                        },
                        {
                            "Student": "Lance Martinez"
                        },
                        {
                            "Student": "Maria Bennett"
                        },
                        {
                            "Student": "Mary Crawford"
                        },
                        {
                            "Student": "Rodney White"
                        },
                        {
                            "Student": "Timothy Kline"
                        },
                        {
                            "Student": "Tracey Nichols"
                        }
                    ]
                },
                "class 2": {
                    "Teacher: Ray Khan": [
                        {
                            "Head of the room": "Stephen Johnson"
                        },
                        {
                            "Student": "Ashley Jones"
                        },
                        {
                            "Student": "Breanna Baker"
                        },
                        {
                            "Student": "Brian Gardner"
                        },
                        {
                            "Student": "Elizabeth Shaw"
                        },
                        {
                            "Student": "Jason Walker"
                        },
                        {
                            "Student": "Katherine Campbell"
                        },
                        {
                            "Student": "Larry Tate"
                        },
                        {
                            "Student": "Lawrence Marshall"
                        },
                        {
                            "Student": "Malik Dean"
                        },
                        {
                            "Student": "Taylor Mckee"
                        }
                    ]
                },
                "class 3": {
                    "Teacher: Jennifer Diaz": [
                        {
                            "Head of the room": "Vicki Wallace"
                        },
                        {
                            "Student": "Brenda Montgomery"
                        },
                        {
                            "Student": "Daniel Wilson"
                        },
                        {
                            "Student": "David Dixon"
                        },
                        {
                            "Student": "John Robinson"
                        },
                        {
                            "Student": "Kimberly Smith"
                        },
                        {
                            "Student": "Michael Miller"
                        },
                        {
                            "Student": "Miranda Trujillo"
                        },
                        {
                            "Student": "Sara Bruce"
                        },
                        {
                            "Student": "Scott Williams"
                        },
                        {
                            "Student": "Taylor Levy"
                        }
                    ]
                },
                "class 4": {
                    "Teacher: Kendra Pierce": [
                        {
                            "Head of the room": "Christopher Stone"
                        },
                        {
                            "Student": "Brenda Tanner"
                        },
                        {
                            "Student": "Christopher Garcia"
                        },
                        {
                            "Student": "Curtis Flynn"
                        },
                        {
                            "Student": "Jason Horton"
                        },
                        {
                            "Student": "Julie Mullins"
                        },
                        {
                            "Student": "Kathleen Mckenzie"
                        },
                        {
                            "Student": "Larry Briggs"
                        },
                        {
                            "Student": "Michael Moyer"
                        },
                        {
                            "Student": "Tammy Smith"
                        },
                        {
                            "Student": "Thomas Martinez"
                        }
                    ]
                },
                "class 5": {
                    "Teacher: Elizabeth Hebert": [
                        {
                            "Head of the room": "Caitlin Lee"
                        },
                        {
                            "Student": "Alexander James"
                        },
                        {
                            "Student": "Amanda Weber"
                        },
                        {
                            "Student": "Christopher Clark"
                        },
                        {
                            "Student": "Devin Morgan"
                        },
                        {
                            "Student": "Gary Clark"
                        },
                        {
                            "Student": "Jenna Sanchez"
                        },
                        {
                            "Student": "Jeremy Meyers"
                        },
                        {
                            "Student": "John Dunn"
                        },
                        {
                            "Student": "Loretta Thomas"
                        },
                        {
                            "Student": "Matthew Vaughan"
                        }
                    ]
                }
            }
        ]

       
            

        return Response(your_result, status=status.HTTP_200_OK)



def make_struc(items, parent_id=0):
    data = []
    for item in items:
        if item["parent_id"] == parent_id:
            subtree = make_struc(items, item["id"])
            if subtree:
                # node["sub"] = subtree
                data.append({"title": item["title"], "sub": subtree})
            else:
                data.append({"title": item["title"]})
    return data

class SchoolStructureAPIView(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        """
        [Logical Test]

        description: get School's structure list in hierarchy.

        pattern: in `data_pattern` variable below.

        """

        data_pattern = [
            {
                "title": "มัธยมต้น",
                "sub": [
                    {
                        "title": "ม.1",
                        "sub": [
                            {
                                "title": "ห้อง 1/1"
                            },
                            {
                                "title": "ห้อง 1/2"
                            },
                            {
                                "title": "ห้อง 1/3"
                            },
                            {
                                "title": "ห้อง 1/4"
                            },
                            {
                                "title": "ห้อง 1/5"
                            },
                            {
                                "title": "ห้อง 1/6"
                            },
                            {
                                "title": "ห้อง 1/7"
                            }
                        ]
                    },
                    {
                        "title": "ม.2",
                        "sub": [
                            {
                                "title": "ห้อง 2/1"
                            },
                            {
                                "title": "ห้อง 2/2"
                            },
                            {
                                "title": "ห้อง 2/3"
                            },
                            {
                                "title": "ห้อง 2/4"
                            },
                            {
                                "title": "ห้อง 2/5"
                            },
                            {
                                "title": "ห้อง 2/6"
                            },
                            {
                                "title": "ห้อง 2/7"
                            }
                        ]
                    },
                    {
                        "title": "ม.3",
                        "sub": [
                            {
                                "title": "ห้อง 3/1"
                            },
                            {
                                "title": "ห้อง 3/2"
                            },
                            {
                                "title": "ห้อง 3/3"
                            },
                            {
                                "title": "ห้อง 3/4"
                            },
                            {
                                "title": "ห้อง 3/5"
                            },
                            {
                                "title": "ห้อง 3/6"
                            },
                            {
                                "title": "ห้อง 3/7"
                            }
                        ]
                    }
                ]
            },
            {
                "title": "มัธยมปลาย",
                "sub": [
                    {
                        "title": "ม.4",
                        "sub": [
                            {
                                "title": "ห้อง 4/1"
                            },
                            {
                                "title": "ห้อง 4/2"
                            },
                            {
                                "title": "ห้อง 4/3"
                            },
                            {
                                "title": "ห้อง 4/4"
                            },
                            {
                                "title": "ห้อง 4/5"
                            },
                            {
                                "title": "ห้อง 4/6"
                            },
                            {
                                "title": "ห้อง 4/7"
                            }
                        ]
                    },
                    {
                        "title": "ม.5",
                        "sub": [
                            {
                                "title": "ห้อง 5/1"
                            },
                            {
                                "title": "ห้อง 5/2"
                            },
                            {
                                "title": "ห้อง 5/3"
                            },
                            {
                                "title": "ห้อง 5/4"
                            },
                            {
                                "title": "ห้อง 5/5"
                            },
                            {
                                "title": "ห้อง 5/6"
                            },
                            {
                                "title": "ห้อง 5/7"
                            }
                        ]
                    },
                    {
                        "title": "ม.6",
                        "sub": [
                            {
                                "title": "ห้อง 6/1"
                            },
                            {
                                "title": "ห้อง 6/2"
                            },
                            {
                                "title": "ห้อง 6/3"
                            },
                            {
                                "title": "ห้อง 6/4"
                            },
                            {
                                "title": "ห้อง 6/5"
                            },
                            {
                                "title": "ห้อง 6/6"
                            },
                            {
                                "title": "ห้อง 6/7"
                            }
                        ]
                    }
                ]
            }
        ]
        your_result = []
        structureAllObj = SchoolStructure.objects.all()
        structureList = []
        for structure in structureAllObj:
            if structure.parent_id == None:
                parent_id = 0
            else:
                parent_id = structure.parent_id
            structureList.append({"id":structure.id, "title":structure.title, "parent_id":parent_id})
        your_result = make_struc(structureList)
        
        return Response(your_result, status=status.HTTP_200_OK)
