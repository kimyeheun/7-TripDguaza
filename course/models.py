from django.db import models
from django.db.models import Sum

REVIEW_RATING_CHOICES = (
    (1, '1점'),
    (2, '2점'),
    (3, '3점'),
    (4, '4점'),
    (5, '5점'),
)


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

    @property
    def reviews_count(self):
        from .models import Review
        cnt = Review.objects.filter(course=self.id).count()
        return cnt

    @property
    def reviews_sum(self):
        from .models import Review
        sums = Review.objects.filter(course=self.id).aggregate(Sum('rating'))
        sum = sums.get('rating__sum')
        return sum

    @property
    def review_average(self):
        sum = self.reviews_sum
        cnt = self.reviews_count
        if cnt == 0:
            avg = 0
        else:
            avg = round(float(sum/cnt), 1)
        return avg


class CourseItem(models.Model):
    # place = models.ForeignKey(Place, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(
        Course, related_name="course", on_delete=models.CASCADE, blank=False, null=True)
    image = models.ImageField(blank=True, null=True, upload_to="courseitem/")
    comment = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.id


class Review(models.Model):
    user = models.ForeignKey("main.User", on_delete=models.CASCADE, blank=False)
    course = models.ForeignKey(Course, related_name="reviews", on_delete=models.CASCADE, blank=False, null=True)
    content = models.TextField(blank=False, max_length=1000)
    rating = models.FloatField(choices=REVIEW_RATING_CHOICES, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.id