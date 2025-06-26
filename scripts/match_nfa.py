from new_nfa import *
from termcolor import colored, cprint

class CPlus(Unary):
    def __str__(self):
        return "%s+" % self.arg._strP()

    _strP = __str__

    def _final(self):
        """ Nipkow auxiliary function final

        :rtype: bool"""
        return self.arg._final()

    def _follow(self, flag):
        """ Nipkow follow function

        :type flag: bool
        :rtype: CPlus"""
        return CPlus(self.arg._follow(self.arg._final() or flag), self.Sigma)

    def _read(self, val):
        """ Nipkow auxiliary function final

        :param val: symbol
        :returns: the p_regexp with all but val marks removed
        :rtype: CPlus """
        return CPlus(self.arg._read(val), self.Sigma)

    def rpn(self):
        return "+%s" % self.arg.rpn()

    def measure(self, from_parent=None):
        if not from_parent:
            from_parent = 9 * [0]
        measure = self.arg.measure(from_parent)
        measure[1] += 1
        measure[3] += 1
        measure[6] += 1
        return measure

    def epsilonLength(self):
        return self.arg.epsilonLength()

    def starHeight(self):
        return self.arg.starHeight()

    def first_l(self):
        """ First sets for locations"""
        if not hasattr(self, "_firstL"):
            self._firstL = self.arg.first_l().copy()
        return self._firstL

    def last_l(self):
        """ Last sets for locations"""
        if not hasattr(self, "_lastL"):
            self._lastL = self.arg.last_l().copy()
        return self._lastL

    def follow_l(self):
        """ Follow sets for locations"""
        if not hasattr(self, "_followL"):
            fol = self.arg.follow_l()
            for s in self.arg.last_l():
                fol[s] = fol.get(s, set()).union(self.arg.first_l())
            self._followL = fol
        return self._followL

    def first(self, parent_first=None):
        return self.arg.first(parent_first)

    def last(self, parent_first=None):
        return self.arg.last(parent_first)

    def followLists(self, lists=None):
        lists = self.arg.followLists(lists)
        for symbol in self.arg.last():
            if symbol not in lists:
                lists[symbol] = self.arg.first()
            else:
                lists[symbol] += self.arg.first()
        return lists

    def followListsD(self, lists=None):
        return self.arg.followListsStar(lists)

    def followListsStar(self, lists=None):
        return self.arg.followListsStar(lists)

    def unmarked(self):
        return CPlus(self.arg.unmarked())

    def _marked(self, pos):
        (r1, pos1) = self.arg._marked(pos)
        return CPlus(r1), pos1
    
def plus(self, s):
    r = CPlus(s[0], self.sigma)
    r._ewp = False
    return r

BuildRegexp.plus = plus

class matchNFA(NFA):
    def __init__(self):
        NFA.__init__(self)
    
    def table_matcher(self, string: str):
        print(self.Sigma)

        nw : list = [CEpsilon()]
        for c in string:
            nw.append(c)

        last_row = {}
        symbol_counter = 0
        final_positions_table = {}

        # ROW -> {state_id_1: [(s1,e1)], state_id_2: [(s1,e1), (s2,e2)]} .. 

        for sym in nw:
            if sym == CEpsilon():
                for initial_state in self.Initial:
                    # last_row[s] = (0,0)
                    last_row[initial_state] = [(0,0)]
            else:
                new_row = {}
                if sym in self.Sigma:
                    for last_row_start_state in last_row:
                        if last_row_start_state in self.delta:
                            if sym in self.delta[last_row_start_state]:
                                saved_positions = last_row[last_row_start_state] # [(s1,e1), (s2,e2)]

                                for pos_tuple in saved_positions:
                                    for last_row_end_state in self.delta[last_row_start_state][sym]:
                                        if last_row_end_state in self.Initial and last_row_end_state == last_row_start_state:
                                            new_row[last_row_end_state] = [(symbol_counter, symbol_counter)]
                                        else:
                                            if last_row_end_state not in new_row:
                                                new_row[last_row_end_state] = []
                                            
                                            new_row[last_row_end_state].append((pos_tuple[0], symbol_counter))

                                            if last_row_end_state in self.Final:
                                                if last_row_end_state in final_positions_table:
                                                    final_positions_table[last_row_end_state].append(new_row[last_row_end_state][-1])
                                                else:
                                                    final_positions_table[last_row_end_state] = [new_row[last_row_end_state][-1]]
                else:
                    for initial_state in self.Initial:
                        # last_row[s] = (0,0)
                        new_row[initial_state] = [(symbol_counter,symbol_counter)]
                
                for s in new_row:
                    print("State", s)
                    #for posset in new_row[s]:
                        #print("\t", posset)
                    print("\t", new_row[s])
#                print(new_row)
                print("----------------------")
                last_row = new_row

                # print(new_row)

            # print(sym, lr)
            symbol_counter+=1

        return (final_positions_table)


    def enum_matches(self, pos_tab: dict, string: str):
        match_count = 0
        for entry in pos_tab:
            print(f"State {entry} matches ({len(set(pos_tab[entry]))}):")
            match_set = set(pos_tab[entry])
            match_count += len(match_set)
            for match in sorted(match_set):
                first_index = string[0:match[0]]
                second_index = string[match[1]:]
                print("Match:", colored(first_index, 'red') + colored(string[match[0]:match[1]], 'green') + colored(second_index, 'red'), "=>", match)
        print("Total matches:", match_count)
                    
def nfaPosCount(self: RegExp):
    aut = matchNFA()
    i = aut.addState()
    aut.addInitial(i)
    
    if self.Sigma is not None:
        aut.setSigma(self.Sigma)

    aut.addTransitionStar(i, i)

    freg = self.marked()
    stack = []
    added_states = dict()
    
    for sym in freg.first():
        try:
            state_idx = aut.addState(str(sym))
        except DuplicateName:
            state_idx = aut.stateIndex(str(sym))
        added_states[sym] = state_idx
        stack.append((sym, state_idx))
        aut.addTransition(i, sym.symbol(), state_idx)
    
    follow_sets = freg.followListsD()

    while stack:
        state, state_idx = stack.pop()
        for sym in follow_sets[state]:
            if sym in added_states:
                next_state_idx = added_states[sym]
            else:
                next_state_idx = aut.addState(str(sym))
                added_states[sym] = next_state_idx
                stack.append((sym, next_state_idx))
            aut.addTransition(state_idx, sym.symbol(), next_state_idx)
    
    escape_state = aut.addState()
    aut.addTransitionStar(escape_state, escape_state)

    for sym in freg.last():
        if sym in added_states:
            aut.addFinal(added_states[sym])
            aut.addTransitionStar(added_states[sym], escape_state)

    return aut

setattr(RegExp, "nfaPosCount", nfaPosCount)