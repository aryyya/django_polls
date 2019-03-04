import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        one_day_ago = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=one_day_ago)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_new_question(self):
        almost_one_day_ago = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        new_question = Question(pub_date=almost_one_day_ago)
        self.assertIs(new_question.was_published_recently(), True)

class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is shown.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['question_list'], [])
