from django.db import models
class TodoList(models.Model):
    user_id             = models.
    task_title          = models.CharField(max_length=256)
    task_status         = models.BooleanField(default=False)
    task_description    = models.CharField(max_length=256)
    #task_time           = models.DateTimeField(auto_now_add=True,editable=False)

    def __str__(self):
        return self.task_description