from django.db import models


# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=100, blank=False, null=True)
    thumbnail_image = models.ImageField(
        default="", blank=True, null=True, upload_to="course/")
    user = models.ForeignKey(
        "main.User", on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title


class CourseItem(models.Model):
    # place = models.ForeignKey(Place, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(
        Course, related_name="course", on_delete=models.CASCADE, blank=False, null=True)
    image = models.ImageField(blank=True, null=True, upload_to="courseitem/")
    comment = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.id
