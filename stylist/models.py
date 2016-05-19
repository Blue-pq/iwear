from __future__ import unicode_literals

from collections import defaultdict

from django.contrib.auth.models import AbstractUser
from django.db import models

from iwear import settings


class MyUser(AbstractUser):
    city = models.CharField(max_length=256)
    woeid = models.IntegerField()
    zip_code = models.IntegerField()


class Item(models.Model):
    PANTS = 0
    SKIRT = 1
    SHORTS = 2
    SHIRT = 3
    SWEATER = 4
    TEE = 5
    TYPE_CHOICES = (
        (PANTS, 'Pants'),
        (SHORTS, 'Shorts'),
        (SKIRT, 'Skirt'),
        (SHIRT, 'Shirt'),
        (SWEATER, 'Sweater'),
        (TEE, 'Tee'),
    )
    BLACK = 0
    WHITE = 1
    RED = 2
    PINK = 3
    COLOR_CHOICES = (
        (BLACK, 'Black'),
        (WHITE, 'White'),
        (RED, 'Red'),
        (PINK, 'Pink'),
    )
    WARM = 0
    MILD = 1
    COLD = 2
    DIURNAL_VARIATION = 18
    TEMPERATURE_CHOICES = (
        (WARM, 'Warm'),
        (MILD, 'Mild'),
        (COLD, 'Cold'),
    )
    TEMP_WARM_MIN = 68
    TEMP_COLD_MAX = 50

    BOTTOMS = [PANTS, SKIRT, SHORTS]
    TOPS = [SHIRT, TEE]
    OUTERS = [SWEATER]

    COLOR_SET_SCORES = defaultdict(int)
    COLOR_SET_SCORES.update({
            frozenset([BLACK]): 2,
            frozenset([BLACK, PINK]): 3,
            frozenset([BLACK, RED]): 4,
            frozenset([BLACK, WHITE]): 5,
            frozenset([WHITE]): 4,
            frozenset([WHITE, PINK]): 5,
            frozenset([WHITE, RED]): 3,
            frozenset([RED]): 1,
            frozenset([RED, PINK]): 0,
            frozenset([PINK]): 1,
            frozenset([BLACK, WHITE, RED]): 4,
            frozenset([BLACK, WHITE, PINK]): 5,
            frozenset([BLACK, RED, PINK]): 1,
            frozenset([WHITE, RED, PINK]): 0,
    })

    @classmethod
    def classify_temperature(cls, temp):
        """Map temperature to one of TEMPERATURE_CHOICES intervals."""
        if temp >= cls.TEMP_WARM_MIN:
            return cls.WARM
        elif temp <= cls.TEMP_COLD_MAX:
            return cls.COLD
        else:
            return cls.MILD

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    item_type = models.IntegerField(choices=TYPE_CHOICES)
    color = models.IntegerField(choices=COLOR_CHOICES)
    temperature = models.IntegerField(choices=TEMPERATURE_CHOICES,
                                      verbose_name='I wear it when it\'s')

    def __unicode__(self):
        return "%s %s for %s weather" % (self.get_color_display(),
                                         self.get_item_type_display(),
                                         self.get_temperature_display())
