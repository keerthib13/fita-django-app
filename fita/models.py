from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    rating = models.FloatField()
    city = models.CharField(max_length=100)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-rating']
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'


class Feedback(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='feedbacks'
    )
    review_text = models.TextField()
    sentiment = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.restaurant.name if self.restaurant else 'General'} - {self.sentiment}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'

