from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from .models import *

class ModelTests(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_userpage_creation(self):
        userpage = Userpage.objects.create(owner=self.user)
        self.assertEqual(self.user, userpage.owner)

    def test_achievement_creation(self):
        achievement = Achievement.objects.create(name="Speed Reader")
        achievement.earners.add(self.user)
        self.assertEqual(achievement.name, "Speed Reader")
        self.assertIn(self.user, achievement.earners.all())

    def test_book_creation(self):
        book = Book.objects.create(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            pages=180,
            ol_key="1234567"
        )
        book.wishlisted_by.add(self.user)
        self.assertEqual(book.title, "The Great Gatsby")
        self.assertIn(self.user, book.wishlisted_by.all())

    def test_progress_record_creation(self):
        book = Book.objects.create(title="Loreum Ipsum", author="Steve Jobs")
        progress = ProgressRecord.objects.create(
            owner=self.user,
            name="How to be Me",
            stage_final=180,
            stage_current=50,
            book=book
        )
        self.assertEqual(progress.name, "How to be Me")
        self.assertEqual(progress.book.title, "Loreum Ipsum")

    # 5. ReadRecord Tests
    def test_read_record_creation(self):
        date = datetime(2026, 9, 12, 21, 30)
        book = Book.objects.create(title="Harry Potter and the Great Pile of Ash", author="")
        read_record = ReadRecord.objects.create(
            user=self.user,
            book=book,
            rating=5,
            date_read=date
        )
        self.assertEqual(read_record.rating, 5)
        self.assertEqual(read_record.user.username, 'testuser')
        self.assertEqual(read_record.date_read, date)

    def test_review_creation(self):
        book = Book.objects.create(title="Cooking 301", author="Oranje Djuss")
        review = Review.objects.create(text="Burnt my house down.", book=book)
        self.assertEqual(str(review), f"Review of book {book.title}")
        self.assertEqual(book, review.book)

    def test_goal_creation(self):
        goal = Goal.objects.create(title_goal="4 in 10 Challenge", books=10)
        goal.current_goals.add(self.user)
        self.assertEqual(goal.title_goal, "4 in 10 Challenge")
        self.assertIn(self.user, goal.current_goals.all())
