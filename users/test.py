from users.models import Profile, Plan
from django.contrib.auth.models import User
from django.test import TestCase
from datetime import date

TEST_USER = {
    "username": "testuser1",
    "email": "testuser2@test1.com",
}

TEST_PROFILE = {
    "weight": 98,
    "height": 178,
    "birthday": "1974-04-11",
    "gender": "M",
}

TEST_USER_PLAN = {
    "activity_level": "SEDENTARY",
    "objetive": "FL",
    "intensity": "LOW",
}


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
        cls.user = User.objects.create(**TEST_USER)
        cls.profile = Profile.objects.create(user=cls.user, **TEST_PROFILE)
        cls.plan = Plan.objects.create(profile=cls.profile, **TEST_USER_PLAN)

    def test_get_rest_bmr(self):
        formula = (
            10 * self.profile.weight
            + 6.25 * self.profile.height
            - 5 * self.profile.get_age()
        )
        if self.profile.gender == "M":
            self.assertEqual(
                self.plan.get_rest_bmr(),
                formula + self.plan.MALE_CONST,
            )
        else:
            self.assertEqual(
                self.plan.get_rest_bmr(),
                formula + self.plan.FEMALE_CONST,
            )

    def test_get_maintain_bmr(self):
        self.assertEqual(
            self.plan.get_maintain_bmr(),
            self.plan.get_rest_bmr()
            * self.plan.activity_level,
        )

    def test_get_gain_bmr(self):
        maintain_bmr = self.plan.get_maintain_bmr()
        modified_bmr = (
            maintain_bmr * self.plan.INTENSITY_LEVEL_FACTOR[self.plan.intensity]
        )
        result = maintain_bmr + modified_bmr
        self.assertEqual(self.plan.get_gain_bmr(), result)

    def test_get_loss_bmr(self):
        maintain_bmr = self.plan.get_maintain_bmr()
        modified_bmr = (
            maintain_bmr * self.plan.intensity
        )
        result = maintain_bmr - modified_bmr
        self.assertEqual(self.plan.get_loss_bmr(), result)

    def test_get_proteins(self):
        
