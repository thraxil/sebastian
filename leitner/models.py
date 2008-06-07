from django.db import models
from sorl.thumbnail.fields import ImageWithThumbnailsField
from datetime import datetime, timedelta
from django.contrib.auth.models import User

class Face(models.Model):
    content = models.TextField(default="")
    image = ImageWithThumbnailsField(upload_to="faces",
                                     thumbnail = {
        'size' : (200,200)
        })
    tex = models.TextField(default="")

    class Admin: pass

class Card(models.Model):
    front = models.ForeignKey(Face,related_name="front")
    back  = models.ForeignKey(Face,related_name="back")
    added = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now=True)

    class Admin: pass    

class Deck(models.Model):
    name = models.CharField(max_length=256)

    class Admin: pass    

class DeckCard(models.Model):
    deck = models.ForeignKey(Deck)
    card = models.ForeignKey(Card)

    class Admin: pass    

class UserCard(models.Model):
    user = models.ForeignKey(User)
    card = models.ForeignKey(Card)
    priority = models.PositiveSmallIntegerField(default=1)
    due = models.DateTimeField(blank=True)
    rung = models.SmallIntegerField(default=-1)        # -1 means never presented to the user
    ease = models.PositiveSmallIntegerField(default=10) # number right out of the last 10 tests

    class Admin: pass    

    def update_due(self):
        """ figure out the next due date for this card based on rung, difficulty, and current
        datetime """

        # if rung == -1, the user has never been presented with this card, so we should never be here
        if self.rung == -1:
            return

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

    class Admin: pass    
        
