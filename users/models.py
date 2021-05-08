from django.db import models
from django.contrib.auth.models import User
from enum import Enum
from datetime import date
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    """# This class represents the Profile table

    ## Attributes
    user: `User model object`
        A valid User model instance
    weight: int
        User current weight represented in grams
    height: int
        User current height represented in centimeters
    birthday: str
        Represented in YYYY-MM-DD and its used to calculate dinamically their metrics
    """

    HEART_FEMALE_CONST = 224
    HEART_MALE_CONST = 220

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.FloatField(blank=False, null=False)
    height = models.IntegerField(blank=False, null=False)
    birthday = models.DateField(blank=False, null=False)
    gender = models.TextField()

    def get_max_hearth_rate(self):
        """Calculates de maximum hearth rate according to the old

        Return
        ---
        Maximum hearth_rate: int

        """
        age = self.get_age()
        return (
            self.HEART_MALE_CONST - age
            if self.gender == "M"
            else self.HEART_FEMALE_CONST - age
        )

    def get_age(self):
        """
        Calculates the user's age
        """
        today_year = date.today().year
        age = today_year - int(self.birthday.split("-")[0])
        return age


class Plan(models.Model):
    """#This class represents the user health plan
    ## Attributes
    activity_level: int
        Represents how often the user gets in phisicall tasks as walk, keep stand, excercise, etc.
        * 0 - Sedentary ... please continue

    """

    class PlanObjective(models.TextChoices):
        FAT_LOSS = "FL", _("fat loss")
        MAINTAIN_WEIGHT = "MW", _("maintain weight")
        MUSCLE_GAIN = "MG", _("muscle gain")

    class ActivityLevel(float, models.Choices):
        SEDENTARY = 1.2, _("Sedentary")
        LIGHT = 1.375, _("Lightly active")
        MODERATE = 1.55, _("Moderately active")
        HIGHT = 1.725, _("Very active")
        EXTREME = 1.9, _("Extra active")

    class Intensity(float, models.Choices):
        DEFAULT = 0.0, _("Maintain")
        LOW = 0.15, _("Low")
        MODERATE = 0.225, _("Moderate")
        HIGH = 0.3, _("High")

    MALE_CONST = 5
    FEMALE_CONST = -161
    # Cambiar los numeros por nombres descriptivos, no olvidar los test

    PROTEIN_FACTOR = {
        "sedentario": 0.1,
        "poca": 0.15,
        "moderada": 0.2,
        "alta": 0.25,
        "extrema": 0.3,
    }

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    activity_level = models.CharField(
        max_length=9,
        choices=ActivityLevel.names,
        default=ActivityLevel.SEDENTARY.name,
    )
    objetive = models.CharField(
        max_length=2,
        choices=PlanObjective.choices,
        default=PlanObjective.MAINTAIN_WEIGHT,
    )
    intensity = models.CharField(
        max_length=8,
        choices=Intensity.names,
        default=Intensity.DEFAULT.name,
    )

    def get_rest_bmr(self) -> int:
        """
        This method its based in the [Harris-Benedict BMR ecuation(1990)](https://en.wikipedia.org/wiki/Harris%E2%80%93Benedict_equation)
        this formula stimates the daily caloric consumption at rest in function of individual's weight, height and age.
        """
        formula = (
            10 * self.profile.weight
            + 6.25 * self.profile.height
            - 5 * self.profile.get_age()
        )
        return (
            formula + self.MALE_CONST
            if self.profile.gender == "M"
            else formula + self.FEMALE_CONST
        )

    def get_maintain_bmr(self):
        return self.get_rest_bmr() * getattr(self.ActivityLevel, self.activity_level).value

    def get_gain_bmr(self):
        maintain_bmr = self.get_maintain_bmr()
        modified_bmr = maintain_bmr * getattr(self.Intensity, self.intensity).value 
        return maintain_bmr + modified_bmr

    def get_loss_bmr(self):
        maintain_bmr = self.get_maintain_bmr()
        modified_bmr = maintain_bmr * getattr(self.Intensity, self.intensity).value
        return maintain_bmr - modified_bmr

    def get_proteins(self):
        pass

    def get_carbohydrates(self):
        pass

    def get_lipids(self):
        pass

    def get_stimated_weight_progress(self):
        pass
