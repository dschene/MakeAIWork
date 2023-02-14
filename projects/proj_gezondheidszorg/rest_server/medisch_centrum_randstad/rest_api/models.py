from django.db import models

class Netlify(models.Model):
    genetic = models.IntegerField(null=True)
    length = models.IntegerField(null=True)
    mass = models.IntegerField(null=True)
    exercise = models.IntegerField(null=True)
    smoking = models.IntegerField(null=True)
    alcohol = models.IntegerField(null=True)
    sugar = models.IntegerField(null=True)
    lifespan = models.IntegerField(null=True)

    def __str__(self):
        return f"""{self.genetic} {self.length} 
            {self.mass} {self.exercise} {self.smoking} 
            {self.alcohol} {self.sugar} {self.lifespan}"""