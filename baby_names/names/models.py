from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class BabyName(models.Model):
    name = models.CharField(max_length=125)
    BOY = 'boy'
    GIRL = 'girl'
    sexs = [
        (BOY,'Boy'),
        (GIRL,'Girl')
    ]
    sex = models.CharField(
        max_length=4,
        choices=sexs,
        default=BOY,
    )
    def __str__(self):
        return '{} ({})'.format(self.name, self.sex)

class Reaction(models.Model):
    reaction = models.CharField(max_length=124)
    def __str__(self):
        return self.reaction

class UserNameReaction(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    name = models.ForeignKey(
        BabyName,
        on_delete=models.CASCADE,
        related_name='baby_name_reaction'
        )
    reaction = models.ForeignKey(Reaction,on_delete=models.CASCADE)

    def __str__(self):
        return '{} reacted to {} with {}'.format(
            self.user,
            self.name.name,
            self.reaction.reaction
        )