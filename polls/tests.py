import datetime
import json
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

def create_question(question_text, days):
    return Question.objects.create(question_text=question_text, pub_date=timezone.now() + datetime.timedelta(days=days))

class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is shown.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are shown on the index page.
        """
        create_question('Past question?', -2)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['question_list'],
            ['<Question: Past question?>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future are not shown on the index page.
        """
        create_question('Future question?', +2)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['question_list'], [])

    def test_future_and_past_questions(self):
        """
        Only past questions are shown on the index page.
        """
        create_question(question_text='Past question', days=-5)
        create_question(question_text='Future question', days=+5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['question_list'], ['<Question: Past question>'])

    def test_multiple_past_questions(self):
        """
        Multiple past questions are shown on the index page.
        """
        create_question(question_text='Past question 1', days=-1)
        create_question(question_text='Past question 2', days=-2)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['question_list'],
            ['<Question: Past question 1>', '<Question: Past question 2>']
        )


