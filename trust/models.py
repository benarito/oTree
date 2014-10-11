# -*- coding: utf-8 -*-
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets


doc = """
This is a standard 2-player trust game where the amount sent by player 1 gets tripled. 
The trust game was first proposed by <a href="http://econweb.ucsd.edu/~jandreon/Econ264/papers/Berg%20et%20al%20GEB%201995.pdf" targe="_blank">Berg, Dickhaut, and McCabe (1995)</a>.
<br />
Source code <a href="https://github.com/oTree-org/oTree/tree/master/trust"
target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'trust'

    amount_allocated = models.PositiveIntegerField(
        default=100,
        doc="""Initial amount allocated to each player"""
    )


class Group(otree.models.BaseGroup):
    BONUS = 10

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 2

    sent_amount = models.PositiveIntegerField(
        doc="""Amount sent by P1""",
    )

    sent_back_amount = models.PositiveIntegerField(
        doc="""Amount sent back by P2""",
    )

    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.payoff = p2.payoff = 0
        p1.points = self.BONUS + self.subsession.amount_allocated\
            - self.sent_amount + self.sent_back_amount
        p2.points = self.BONUS + self.subsession.amount_allocated\
            + self.sent_amount * 3 - self.sent_back_amount

    def sent_amount_error_message(self, value):
        if not 0 <= value <= self.subsession.amount_allocated:
            return 'Your entry is invalid.'

    def sent_back_amount_error_message(self, value):
        if not 0 <= value <= self.subsession.amount_allocated\
                + self.sent_amount * 3:
            return 'Your entry is invalid.'


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>
    training_answer_x = models.PositiveIntegerField(
        null=True, verbose_name='X would be:')
    training_answer_y = models.PositiveIntegerField(
        null=True, verbose_name='Y would be:')
    points = models.PositiveIntegerField()
    feedback = models.PositiveIntegerField(
        choices=(
            (5, 'Very well'),
            (4, 'Well'),
            (3, 'OK'),
            (2, 'Badly'),
            (1, 'Very badly')), widget=widgets.RadioSelectHorizontal(),
        verbose_name='')

    def role(self):
        return {1: 'A', 2: 'B'}[self.id_in_group]
