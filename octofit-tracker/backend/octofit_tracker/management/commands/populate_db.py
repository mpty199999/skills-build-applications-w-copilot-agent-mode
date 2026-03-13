from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models

from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create unique index on email for users
        db.users.create_index([('email', 1)], unique=True)

        # Sample users
        users = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': 'Marvel'},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team': 'Marvel'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': 'DC'},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': 'DC'},
        ]
        db.users.insert_many(users)

        # Sample teams
        teams = [
            {'name': 'Marvel', 'members': ['ironman@marvel.com', 'cap@marvel.com']},
            {'name': 'DC', 'members': ['wonderwoman@dc.com', 'batman@dc.com']},
        ]
        db.teams.insert_many(teams)

        # Sample activities
        activities = [
            {'user_email': 'ironman@marvel.com', 'activity': 'Running', 'duration': 30},
            {'user_email': 'cap@marvel.com', 'activity': 'Cycling', 'duration': 45},
            {'user_email': 'wonderwoman@dc.com', 'activity': 'Swimming', 'duration': 60},
            {'user_email': 'batman@dc.com', 'activity': 'Jumping', 'duration': 20},
        ]
        db.activities.insert_many(activities)

        # Sample leaderboard
        leaderboard = [
            {'team': 'Marvel', 'points': 75},
            {'team': 'DC', 'points': 80},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Sample workouts
        workouts = [
            {'user_email': 'ironman@marvel.com', 'workout': 'Pushups', 'reps': 50},
            {'user_email': 'cap@marvel.com', 'workout': 'Situps', 'reps': 40},
            {'user_email': 'wonderwoman@dc.com', 'workout': 'Squats', 'reps': 60},
            {'user_email': 'batman@dc.com', 'workout': 'Pullups', 'reps': 30},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
