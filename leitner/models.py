from django.db import models
from sorl.thumbnail.fields import ImageWithThumbnailsField
from datetime import datetime, timedelta

class Face(models.Model):
    content = models.TextField(default="")
    image = ImageWithThumbnailsField(upload_to="faces")
    tex = models.TextField(default="")

class Card(models.Model):
    front = models.ForeignKey(Face)
    back  = models.ForeignKey(Face)
    added = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now=True)

class Deck(models.Model):
    name = models.CharField(max_length=256)

class DeckCard(models.Model):
    deck = models.ForeignKey(Deck)
    card = models.ForeignKey(Card)

class UserCard(models.Model):
    user = models.ForeignKey(User)
    card = models.ForeignKey(Card)
    priority = models.PositiveSmallIntegerField(default=1)
    due = models.DateTimeField()
    rung = models.PositiveSmallIntegerField(default=0)        
    ease = models.PositiveSmallIntegerField(default=10) # number right out of the last 10 tests

    def update_due(self):
        """ figure out the next due date for this card based on rung, difficulty, and current
        datetime """

        # Leitner's intervals
        intervals = [
            (5,"seconds"), (25,"seconds"), (2 * 60 ,"seconds"), (10 * 60 , "seconds"),
            (1, "hours"), (5, "hours"), (1, "days"), (5, "days"), (25, "days"),
            (4 * 4, "weeks"), (2 * 52, "weeks")]

        (n,u) = intervals[self.rung]

        # extend interval based on ease. Ie, if they've gotten it right
        # 10 times out of 10, the interval gets doubled. 0 out of the last 10,
        # we stick with leitner's interval. Anything in between is proportional
        
        n *= (1.0 + (self.ease / 10.0))
        d = timedelta(**{u:n})
        now = datetime.now()
        self.due = now + d
        self.save()

    def test_correct(self):
        """ user got it right, so we update accordingly """
        self.rung += 1
        self.rung = self.rung % 10

        self.ease += 1
        self.ease = self.ease % 10

        self.update_due()

    def test_wrong(self):
        self.rung = 0
        self.ease -= 1
        if self.ease < 0: self.ease = 0
        self.update_due()

class UserCardTest(models.Model):
    """ represents an instance of a user being tested on a given card.
    basically here for logging/statistics/history purposes. might be possible
    to remove """
    usercard = models.ForeignKey(UserCard)
    timestamp = models.DateTimeField(auto_now=True)
    correct = models.BooleanField(default=True)
        
