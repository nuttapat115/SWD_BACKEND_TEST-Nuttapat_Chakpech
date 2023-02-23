from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from todoapp.models import  Task
from todoapp.serializers import TaskSerializer
from datetime import datetime


class CreateTaskAPIView(APIView):

    @staticmethod
    def post(request, *args, **kwargs):

        task_name = request.data.get("title", None)
        task_des = request.data.get("description", "")
        task_status = request.data.get("status", True)
        task_due = request.data.get("due_datetime")

        print(task_name, task_des, task_status, task_due)

        if task_name == None or task_name == "":
            payload = { 
                "status" : 400,
                "massage" : "Bad Request: Invalid request payload",
                "detial" : "The request payload must include 'task_name'"
            }
            return Response(payload,status=status.HTTP_400_BAD_REQUEST)
        date_time_obj = None
        if task_due:
            try:
                date_time_obj = datetime.strptime(task_due,'%Y-%m-%d')
            except:
                payload = { 
                    "status" : 400,
                    "massage" : "Bad Request: Invalid request payload",
                    "detial" : "The request payload 'due_datetime' must be format '%Y-%m-%d'"
                }
                return Response(payload,status=status.HTTP_400_BAD_REQUEST)

        if isinstance(task_status, bool):
            pass
        else:
            payload = { 
                "status" : 400,
                "massage" : "Bad Request: Invalid request payload",
                "detial" : "The request payload 'status' must be boolean"
            }
            return Response(payload,status=status.HTTP_400_BAD_REQUEST)

        Task.objects.create(task_title = task_name,task_description=task_des,
                            tast_status=task_status, due_date=task_due)
        payload = {
                "status": 201,
                "massage" : "Create success",
                "data" : {"task_name":task_name, "task_des": task_des, 
                          "task_status": task_status, "task_due":date_time_obj}
                }
        return Response(payload,status=status.HTTP_201_CREATED)
    
class TaskAPIView(APIView):
    @staticmethod
    def put(request, *args, **kwargs):
        taskId = kwargs.get("id", None)
        task_name = request.data.get("title", None)
        task_des = request.data.get("description", None)
        task_status = request.data.get("status", None)
        task_due = request.data.get("due_datetime")

        print(task_name, task_des, task_status, task_due)


        task_checkObj = Task.objects.filter(id=taskId)

        if len(task_checkObj) == 0:
            payload = { 
                "status" : 400,
                "massage" : "Bad Request: Invalid request payload",
                "detial" : "Task not found",
            }
            return Response(payload,status=status.HTTP_400_BAD_REQUEST)

        if task_name :
            task_checkObj.update(task_title = task_name)
        if task_des != None:
            task_checkObj.update(task_description = task_des)
        if task_status != None:
            if isinstance(task_status, bool):
                pass
            else:
                payload = { 
                    "status" : 400,
                    "massage" : "Bad Request: Invalid request payload",
                    "detial" : "The request payload 'status' must be boolean"
                }
                return Response(payload,status=status.HTTP_400_BAD_REQUEST)
            task_checkObj.update(tast_status = task_status)

        if task_due:
            try:
                date_time_obj = datetime.strptime(task_due, '%Y-%m-%d')
            except:
                payload = { 
                    "status" : 400,
                    "massage" : "Bad Request: Invalid request payload",
                    "detial" : "The request payload 'due_datetime' must be format '%Y-%m-%d'"
                }
                return Response(payload,status=status.HTTP_400_BAD_REQUEST)
            task_checkObj.update(due_date = date_time_obj)
        
        payload = {
                "status": 200,
                "massage" : "Update success",
                }
        return Response(payload,status=status.HTTP_200_OK)
    
    @staticmethod
    def get(request, *args, **kwargs):
        taskId = kwargs.get("id", None)
        task_checkObj = Task.objects.filter(id=taskId)

        if len(task_checkObj) == 0:
            payload = { 
                "status" : 400,
                "massage" : "Bad Request: Invalid request payload",
                "detial" : "Task not found",
            }
            return Response(payload,status=status.HTTP_400_BAD_REQUEST)
        task_checkObj = Task.objects.filter(id=taskId)
        serializer = TaskSerializer(task_checkObj, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

