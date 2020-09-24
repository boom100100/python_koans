#!/usr/bin/env python
# -*- coding: utf-8 -*-

# EXTRA CREDIT:
#
# Create a program that will play the Greed Game.
# Rules for the game are in GREED_RULES.TXT.
#
# You already have a DiceSet class and score function you can use.
# Write a player class and a Game class to complete the project.  This
# is a free form assignment, so approach it however you desire.

from runner.koan import *

class AboutExtraCredit(Koan):
    class Game:
        from .about_dice_project import DiceSet
        class Player:
            def __init__(self, name):
                self._name = name
                self._points = 0

        def __init__(self, n_players):
            self._diceSet = self.DiceSet();
            self._players = []
            for n in range(n_players):
                # self.__setattr__('_player' + str(n), self.Player())
                self._players.append(self.Player('player' + str(n)))

        def __setattr__(self, attr_name, value):
            object.__setattr__(self, attr_name, value)

        import functools
        def highest_score(self, players):
            return self.functools.reduce(lambda a,b : a._points if a._points > b._points else b._points, players)

        def play(self):
            final_round = False

            while final_round == False:
                for p in self._players:
                    if p._points >= 3000:
                        final_round = True
                self.round()

            return self.calculate_winner()

        def calculate_winner(self):
            winner = ''
            highest_score = self.highest_score(self._players)
            for p in self._players:
                if p._points == highest_score:
                    if winner == '':
                        winner += p._name
                    else:
                        winner += ', ' + p._name
            announcement = winner + ' won!'
            print(announcement)
            return announcement

        from . import about_scoring_project#, one_five_processor
        def round(self):
            for p in self._players:
                n_dice = 5
                prev_points = -1
                accum_points = 0
                can_add_to_total = False
                cont = True

                while prev_points != 0 and cont == True:
                    values = self._diceSet.roll(n_dice)
                    prev_points = self.about_scoring_project.score(values)
                    n_dice = self.find_num_dice(values)
                    accum_points += prev_points

                    if prev_points == 0:
                        accum_points = 0
                        cont = False
                    print('Current player: ' + p._name)
                    print('Round total: ' + str(accum_points))
                    print()
                    if accum_points >= 300:
                        can_add_to_total = True
                        cont = self.choose_cont(p, n_dice)

                p._points += accum_points
                print('Score:')
                for p in self._players:
                    print(p._name + ': ' + str(p._points) + ' points')
                print()

        def find_num_dice(self, values):
            target = 0
            nonscoring = 0

            d = {k: values.count(k) for k in values}
            for k, v in d.items():
                if k != 1 and k != 5 and v <= 2:
                    nonscoring += v

            target = (5 if nonscoring == 0 else nonscoring)
            return target

        def choose_cont(self, player, n_dice):
            choice = ''
            while choice != 'Y' and choice != 'N':
                print(player._name + ', you must make a choice. \nYou have ' + str(n_dice) + ''' dice.
Your game total is ''' + str(player._points) + '.')
                choice = input('Continue? Enter Y or N.\n')
                print()
                choice = choice.upper()
            return True if choice == 'Y' else False

    # Write tests here. If you need extra test classes add them to the
    # test suite in runner/path_to_enlightenment.py
    def test_01_can_create_game(self):
        game = self.Game(2)
        self.assertTrue("DiceSet", game._diceSet.__name__)

    def test_02_can_find_num_dice(self):
        game = self.Game(2)
        n = game.find_num_dice([2])
        self.assertEqual(n, 1)

        n = game.find_num_dice([2,2])
        self.assertEqual(n, 2)

        n = game.find_num_dice([2,2,3])
        self.assertEqual(n, 3)

        n = game.find_num_dice([2,2,3,3,4])
        self.assertEqual(n, 5)

        n = game.find_num_dice([1,2])
        self.assertEqual(n, 1)

        n = game.find_num_dice([5,2,2])
        self.assertEqual(n, 2)

        n = game.find_num_dice([1,1,1])
        self.assertEqual(n, 5)

        n = game.find_num_dice([1])
        self.assertEqual(n, 5)

        n = game.find_num_dice([5,5])
        self.assertEqual(n, 5)

        n = game.find_num_dice([2,2,2])
        self.assertEqual(n, 5)

    def test_04_can_choose_continue(self):
        game = self.Game(2)
        val = game.choose_cont(game._players[0], 5)
        self.assertEqual(val, True)

    def test_05_can_deny_continue(self):
        game = self.Game(2)
        val = game.choose_cont(game._players[0], 5)
        self.assertEqual(val, False)

    def test_06_can_calculate_highest_score(self):
        game = self.Game(2)
        players = game._players

        players[0]._points = 3000
        players[1]._points = 3001
        self.assertEqual(3001, game.highest_score(players))

        players[0]._points = 3002
        players[1]._points = 3001
        self.assertEqual(3002, game.highest_score(players))

        players[0]._points = 3003
        players[1]._points = 3003
        self.assertEqual(3003, game.highest_score(players))

    def test_07_can_calculate_correct_winner(self):
        game = self.Game(2)
        players = game._players

        players[0]._points = 3000
        players[1]._points = 3001
        self.assertRegex(game.calculate_winner(), 'player1')
        self.assertNotRegex(game.calculate_winner(), 'player0')

        players[0]._points = 3002
        players[1]._points = 3001
        self.assertRegex(game.calculate_winner(), 'player0')
        self.assertNotRegex(game.calculate_winner(), 'player1')


        players[0]._points = 3003
        players[1]._points = 3003
        self.assertRegex(game.calculate_winner(), 'player1')
        self.assertRegex(game.calculate_winner(), 'player0')

    def test_08_can_play(self):
        game = self.Game(2)
        game.play()
        self.assertRegex(game.calculate_winner(), 'player')
