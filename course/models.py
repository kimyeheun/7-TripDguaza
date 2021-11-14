from django.db import models

# Create your models here.
class Course(models.Model):
    image = models.ImageField(blank=True, null=True, upload_to="blog/%Y/%m/%d")
    title = models.CharField(max_length=100, blank=True, null=True)
    comment = models.TextField(max_length=1000, blank=True, null=True)
    # place = models.ForeignKey(Place, on_delete=models.CASCADE, blank=True, null=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title