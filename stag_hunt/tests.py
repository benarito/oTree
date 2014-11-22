# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play(self):
        self.submit(views.Introduction)
        self.submit(views.Question1, {
            "training_question_1_my_payoff": random.randint(0, 100),
            "training_question_1_other_payoff": random.randint(0, 100),
        })
        self.submit(views.Feedback1)
        self.submit(
            views.Decide, {"decision": random.choice(['Stag', 'Hare'])}
        )
        self.submit(views.Results)

    def validate_play(self):
        pass
