from users.models import Profile, Plan
from django.contrib.auth.models import User
from django.test import TestCase
from datetime import date

TEST_USER = {
    "username": "testuser1",
    "email": "testuser2@test1.com",
}

TEST_PROFILE = {
    "weight": 98.0,
    "height": 178,
    "birthday": "1974-04-11",
    "gender": "M",
}

TEST_USER_PLAN = {
    "activity_level": "SEDENTARY",
    "objective": "FAT_LOSS",
    "intensity": "LOW",
}

# The important thing of testing its, if its necesary repeat the code the times
# that be necesary because the any test shall to depends on other test pass
# Thas why its necesary to define all the formulas as setup if its necesary to
# get the expected result even if in the main function be processed in other way


class TestProfileModel(TestCase):
    """
    Probe User model and his methods
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(**TEST_USER)
        cls.profile = Profile.objects.create(user=cls.user, **TEST_PROFILE)

    def test_get_hearth_rate(self):
        AGE = date.today().year - int(self.profile.birthday.split("-")[0])
        if self.profile.gender == "M":
            self.assertEqual(
                self.profile.get_max_hearth_rate(),
                self.profile.HEART_MALE_CONST - AGE,
            )
        else:
            self.assertEqual(
                self.profile.get_max_hearth_rate(),
                self.profile.HEART_FEMALE_CONST - AGE,
            )

    def test_get_age(self):
        self.assertEqual(
            self.profile.get_age(),
            date.today().year - int(self.profile.birthday.split("-")[0]),
        )


class TestPlanModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Objects
        # Its necesary to create 2 objects of every class because we need probe Male users
        # and Female users to probe the code efectivity, and check whats fixtures do
        cls.user = User.objects.create(**TEST_USER)
        cls.profile = Profile.objects.create(user=cls.user, **TEST_PROFILE)

        # This var its temporal since I code the PlanSerilializer that format the request from
        # the front end because this var is stored as float type, but for human legibility
        # in the json request comes as String like LOW, MODERATE, etc.
        _activity_level = getattr(Plan.ActivityLevel, TEST_USER_PLAN["activity_level"])
        _intensity = getattr(Plan.Intensity, TEST_USER_PLAN["intensity"])
        _objective = getattr(Plan.Objective, TEST_USER_PLAN["objective"])
        cls.plan = Plan.objects.create(
            profile=cls.profile,
            activity_level=_activity_level,
            objective=_objective,
            intensity=_intensity,
        )

        # Const
        cls.AGE = date.today().year - int(cls.profile.birthday.split("-")[0])
        cls.GENDER_CONST = (
            cls.plan.MALE_CONST if cls.profile.gender == "M" else cls.plan.FEMALE_CONST
        )
        cls.REST_BMR = 10 * cls.profile.weight + 6.25 * cls.profile.height - 5 * cls.AGE + cls.GENDER_CONST
        cls.MAINTENANCE_BMR = cls.REST_BMR * cls.plan.activity_level
        cls.GAP_BMR = cls.MAINTENANCE_BMR * cls.plan.intensity
        cls.DIET_BMR = cls.MAINTENANCE_BMR + (
            cls.GAP_BMR if cls.plan.objective == "MG" else -cls.GAP_BMR
        )
        cls.PROTEIN_CONST = getattr(
            Plan.ProteinFactor, TEST_USER_PLAN["activity_level"]
        ).value
        cls.RECOMENDED_LIPIDS_PERCENTAGE = 0.3

    def test_get_rest_bmr(self):
        self.assertEqual(
            self.plan.get_rest_bmr(),
            self.REST_BMR,
        )

    def test_get_maintain_bmr(self):
        self.assertEqual(
            self.plan.get_maintain_bmr(),
            self.MAINTENANCE_BMR,
        )

    def test_get_gap_bmr(self):
        self.assertEqual(self.plan.get_gap_bmr(), self.GAP_BMR)

    def test_get_diet_bmr(self):
        self.assertEqual(self.plan.get_diet_bmr(), self.DIET_BMR)

    def test_get_proteins(self):
        proteins = self.DIET_BMR * self.PROTEIN_CONST / 4
        self.assertEqual(self.plan.get_proteins(), proteins)

    def test_get_lipids(self):
        lipids_calories = self.DIET_BMR * self.RECOMENDED_LIPIDS_PERCENTAGE / 9
        self.assertEqual(self.plan.get_lipids(), lipids_calories)
