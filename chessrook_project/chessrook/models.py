from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class ChessGames(models.Model):
    game_name = models.CharField(max_length=50) 
    # name of game
    game_play_monitor_instance = models.BinaryField() 
    # the game play state
    date_started = models.DateTimeField(default=timezone.now) 
    # the date when the game was created
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    # notes about the game
    game_notes = models.CharField(max_length=5000, default="none_notes")

    def __str__(self):
        return self.game_name