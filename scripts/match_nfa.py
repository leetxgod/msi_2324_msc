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

    def reduced(self, has_epsilon=False):
        rarg = self.arg._reducedS(False)
        if rarg.emptysetP():
            return CEmptySet(self.Sigma)
        if rarg.epsilonP():
            return CEpsilon(self.Sigma)
        if self.arg is rarg:
            return self
        reduced = CPlus(rarg, self.Sigma)
        return reduced

    # noinspection PyUnusedLocal
    def _reducedS(self, has_epsilon=False):
        return self.arg._reducedS(False)

    def derivative(self, sigma):
        d = self.arg.derivative(sigma)
        return CConcat(d, CStar(self.arg, self.Sigma), self.Sigma)

    def partialDerivatives(self, sigma):
        arg_pdset = self.arg.partialDerivatives(sigma)
        pds = set()
        star_arg = CStar(self.arg, self.Sigma)
        for pd in arg_pdset:
            if pd.emptysetP():
                pds.add(CEmptySet(self.Sigma))
            elif pd.epsilonP():
                pds.add(star_arg)
            else:
                pds.add(CConcat(pd, star_arg, self.Sigma))
        return pds

    def linearForm(self):
        arg_lf = self.arg.linearForm()
        lf = dict()
        star_arg = CStar(self.arg, self.Sigma)
        for head in arg_lf:
            lf[head] = set()
            for tail in arg_lf[head]:
                if tail.emptysetP():
                    lf[head].add(CEmptySet(self.Sigma))
                elif tail.epsilonP():
                    lf[head].add(star_arg)
                else:
                    lf[head].add(CConcat(tail, star_arg, self.Sigma))
        return lf

    def support(self, side=True):
        return self._odot(self.arg.support(side), side)

    def supportlast(self, side=True):
        return self._odot(self.arg.supportlast(side), side)

    def _memoLF(self):
        if hasattr(self, "_lf"):
            return
        self.arg._memoLF()
        self._lf = dict()
        star_arg = CStar(self.arg, self.Sigma)
        for head in self.arg._lf:
            pd_set = set()
            self._lf[head] = pd_set
            for tail in self.arg._lf[head]:
                if tail.emptysetP():
                    pd_set.add(CEmptySet(self.Sigma))
                elif tail.epsilonP():
                    pd_set.add(star_arg)
                else:
                    pd_set.add(CConcat(tail, star_arg, self.Sigma))

    def ewp(self):
        if hasattr(self, "_ewp"):
            self._ewp = self.arg.ewp()
        return self.arg.ewp()

    def tailForm(self):
        arg_tf = self.arg.tailForm()
        tf = dict()
        star_arg = CStar(self.arg, self.Sigma)
        for tail in arg_tf:
            tf[tail] = set()
            for head in arg_tf[tail]:
                if head.emptysetP():
                    tf[tail].add((CEmptySet(self.Sigma), CEmptySet(self.Sigma)))
                elif head.epsilonP():
                    tf[tail].add(star_arg)
                else:
                    new = _ifconcat(star_arg, head, both=True, sigma=self.Sigma)
                    tf[tail].add(new)
        return tf

    def snf(self, _hollowdot=False):
        if _hollowdot:
            return self.arg.snf(False)
        return CPlus(self.arg.snf(False), self.Sigma)

    def nfaThompson(self):
        sun = self.arg.nfaThompson()
        star_nfa = CStar(self.arg, self.Sigma).nfaThompson()
        au = sun.dup()
        star_au = star_nfa.dup()
        r_final = list(au.Final)
        star_initial = list(star_au.Initial)[0]
        state_map = {}
        for state in star_au.States:
            if state == star_initial:
                for f_state in r_final:
                    state_map[state] = f_state
            else:
                new_state = au.addState()
                state_map[state] = new_state
        for state in star_au.delta:
            for symbol in star_au.delta[state]:
                for target in star_au.delta[state][symbol]:
                    if state == star_initial:
                        for f_state in r_final:
                            au.addTransition(f_state, symbol, state_map[target])
                    else:
                        au.addTransition(state_map[state], symbol, state_map[target])
        new_finals = []
        for f_state in star_au.Final:
            if f_state == star_initial:
                new_finals.extend(r_final)
            else:
                new_finals.append(state_map[f_state])
        
        au.setFinal(new_finals)
        return au

    def _nfaGlushkovStep(self, aut, initial, final):
        previous_trans = dict()
        for i_state in initial:
            if i_state in aut.delta:
                previous_trans[i_state] = aut.delta[i_state]
                del aut.delta[i_state]
        
        new_initial, arg_final = self.arg._nfaGlushkovStep(aut, initial, final)
        for i_state in initial:
            if i_state in aut.delta:
                for symbol in aut.delta[i_state]:
                    for target in aut.delta[i_state][symbol]:
                        for f_state in arg_final:
                            aut.addTransition(f_state, symbol, target)
        for i_state in previous_trans:
            for sym in previous_trans[i_state]:
                for target in previous_trans[i_state][sym]:
                    aut.addTransition(i_state, sym, target)
        
        return new_initial, arg_final

    def _nfaFollowEpsilonStep(self, conditions):
        aut, initial, final = conditions
        arg_state = aut.addState()
        self.arg._nfaFollowEpsilonStep((aut, arg_state, arg_state))
        aut.addTransition(initial, Epsilon, arg_state)
        aut.addTransition(arg_state, Epsilon, final)
        tomerge = aut.epsilonPaths(arg_state, arg_state)
        aut.mergeStatesSet(tomerge)
    
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
							
				last_row = new_row

				# print(new_row)

			# print(sym, lr)
			symbol_counter+=1

		return (final_positions_table)

	def enum_matches(self, pos_tab: dict, string: str):
		for entry in pos_tab:
			print(f"State {entry} matches:")
			match_set = set(pos_tab[entry])
			for match in match_set:
				first_index = string[0:match[0]]
				second_index = string[match[1]:]
				print("Match:", colored(first_index, 'red') + colored(string[match[0]:match[1]], 'green') + colored(second_index, 'red'), "=>", match)
                    
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