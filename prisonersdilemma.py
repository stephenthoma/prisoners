class PrisonerBattle(object):
    def __init__(self):
        self.grid = [[(1, 1), (5, 0)], [(0, 5), (2, 2)]]
        self.score_one = 0
        self.score_two = 0

    def score(self, move_one, move_two):
        print move_one, move_two,
        score = self.grid[move_one][move_two]
        print score
        return score

    def do_battle(self, strat_one, strat_two, num_moves=4):
        for i in range(num_moves):
            move_one = strat_one.make_move_decision()
            move_two = strat_two.make_move_decision()

            score = self.score(move_one, move_two)
            self.score_one += score[0]
            self.score_two += score[1]

            strat_one.update_history(move_one, move_two)
            strat_two.update_history(move_two, move_one)

class CooperateMove(object):
    def __init__(self):
        self.value = 1

    def __str__(self):
        return 'Cooperate'

    def __index__(self):
        return self.value

class DefectMove(object):
    def __init__(self):
        self.value = 0

    def __str__(self):
        return 'Defect'

    def __index__(self):
        return self.value

class PrisonerMove(object):
    def __init__(self, move_one, move_two):
        self.move_one = move_one
        self.move_two = move_two

class PrisonerStrategy(object):
    def __init__(self):
        self.history = list()

    def update_history(self, self_move, other_move):
        move = PrisonerMove(self_move, other_move)
        self.history.append(move)

    def make_move_decision(self):
        return CooperateMove()

class TitTatStrategy(PrisonerStrategy):
    def make_move_decision(self):
        if len(self.history) > 0:
            move = self.history[-1].move_two
        else:
            move = CooperateMove()
        return move

class TitTwoStrategy(PrisonerStrategy):
    def make_move_decision(self):
        if len(self.history) > 1:
            if self.history[-1].move_two is DefectMove() and \
               self.history[-2].move_two is DefectMove():
                return DefectMove()
        return CooperateMove()

class TesterStrategy(PrisonerStrategy):
    def __init__(self):
        super(TesterStrategy, self).__init__()
        self.hist_defect = False

    def _check_history_for_defects(self):
        for move in self.history:
            if move.move_two is DefectMove():
                self.hist_defect = True
                return True
        return False

    def make_move_decision(self):
        if not self.hist_defect:
            self._check_history_for_defects()

        if len(self.history) == 0:
            return DefectMove()

        elif self.hist_defect:
            if self.history[-1].move_two is DefectMove():
                return DefectMove()
            else:
                return CooperateMove()

        elif len(self.history) <= 3:
            return CooperateMove()

        elif len(self.history) % 2 == 0:
            return DefectMove()

        else:
            return CooperateMove()

class RandomStrategy(PrisonerStrategy):
    def make_move_decision(self):
        from random import randint
        moves = [CooperateMove(), DefectMove()]
        return  moves[randint(0,1)]

if __name__ == "__main__":
    strat_one = TesterStrategy()
    strat_two = TitTatStrategy()

    battle = PrisonerBattle()
    battle.do_battle(strat_one, strat_two, num_moves=50)
    print 'Score one: {0}'.format(battle.score_one)
    print 'Score two: {0}'.format(battle.score_two)
