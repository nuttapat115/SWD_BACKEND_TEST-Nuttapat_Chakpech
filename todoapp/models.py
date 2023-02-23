from django.db import models

class Task(models.Model):
    task_title = models.CharField(max_length=255, null=False, blank=False)
    task_description = models.TextField(max_length=255, null=False, blank=True)
    tast_status = models.BooleanField(null=False, blank=False, default=True)
    due_date = models.DateField(null=True, blank=True)

# class Tag(models.Model):
#     tag_name = models.CharField(max_length=255, null=False, blank=False)
#     def __str__(self):
#         return self.tag_name

# class StepOfTask(models.Model):
#     task_own = models.ForeignKey(Task, on_delete=models.CASCADE, null=False, blank=False)
#     step_text = models.TextField(max_length=255, null=False, blank=False)
#     state_step = models.BooleanField(null=False, blank=False, default=True)

# class TaskTagGruop(models.Model):
#     task = models.ForeignKey(Task, on_delete=models.CASCADE, null=False, blank=False)
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=False, blank=False)