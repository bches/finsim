class vote:
    def __init__(self, description=None):
        self._for = {}
        self._against = {}
        self.voters = {}
        self.quorum = 1
        self.description = description

    def __repr__(self):
        return '{:>{width}} : {}\n\
        {}\n{:{prec}}|{:{prec}}\n'.format('For',
                                          'Against', '-'*21,
                                          self.total_for(),
                                          self.total_against(),
                                          width=10, prec=10)

    def total_for(self):
        return sum([votes for voter, votes in self._for.items()])

    def total_against(self):
        return sum([votes for voter, votes in self._against.items()])

    def cast_vote(self, voter, in_favor, number_of_votes=1):
        assert voter in self.voters.keys(), '%s cannot not vote' % voter
        if in_favor:
            self._for[voter] = number_of_votes
        else:
            self._against[voter] = number_of_votes

    def add_voter(self, voter, number_of_votes=1):
        if voter in self.voters.keys():
            self.voters[voter] += number_of_votes
        else:
            self.voters[voter] = number_of_votes

    def majority(self):
        Y = self.total_for()
        N = self.total_against()
        assert Y + N >= self.quorum, 'Failed to reach a quorum'
        return ((float(Y) / (Y + N)) > 0.5)

    def two_thirds(self):
        Y = self.total_for()
        N = self.total_against()
        assert Y + N >= self.quorum, 'Failed to reach a quorum'
        return ((float(Y) / (Y + N)) >= (2.0/3))


if __name__ == '__main__':
    dut = vote('To do some stuff')

    dut.add_voter('me')
    dut.add_voter('you')

    dut.cast_vote(voter='me', in_favor=True)
    dut.cast_vote(voter='you', in_favor=False)

    print(dut)
    print('Majority:', dut.majority())
