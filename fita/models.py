from django.db import models

# Restaurant model
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    rating = models.FloatField()
    city = models.CharField(max_length=100)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Optional: Model to store customer feedback (if you plan to save sentiment input)
class Feedback(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    review_text = models.TextField()
    sentiment = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.restaurant.name if self.restaurant else 'General'} - {self.sentiment}"
