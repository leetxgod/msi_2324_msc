import FAdo.reex
import FAdo.fa

from FAdo.fa import *
from FAdo.reex import *
from FAdo.fio import *
from FAdo.rndadfa import *


class cDFA(DFA):
	def __init__(self):
		DFA.__init__(self)
		self.markedTransitions = []
	
	def dup(self):
		"""Duplicate the basic structure into a new NFA. Basically a copy.deep.

		Returns:
			NFA: """
		new = cDFA()
		new.setSigma(self.Sigma)
		new.States = self.States[:]
		new.Initial = self.Initial
		new.Final = self.Final.copy()
		new.markedTransitions = self.markedTransitions.copy()
		for s in self.delta:
			new.delta[s] = {}
			for c in self.delta[s]:
				new.delta[s][c] = self.delta[s][c]
		return new
	
	def succintTransitions(self):
		""" Collects the transition information in a compact way suitable for graphical representation.

		Returns:
			list: list of tupples

		.. note:
			tupples in the list are stateout, label, statein

		.. versionadded:: 0.9.8"""
		foo = dict()
		for s in self.delta:
			for c in self.delta[s]:
				k = (s, self.delta[s][c])
				if k not in foo:
					foo[k] = []
				foo[k].append(c)
		lst = []
		for k in foo:
			cs = foo[k]
			s = "%s" % str(cs[0])
			for c in cs[1:]:
				s += ", %s" % str(c)
			lst.append((self.dotLabel(self.States[k[0]]), s, self.dotLabel(self.States[k[1]])))
		return lst

class cNFA(NFA):
	def __init__(self, markedTransitions=[]):
		NFA.__init__(self)
		self.markedTransitions = markedTransitions
	
	def dup(self):
		"""Duplicate the basic structure into a new NFA. Basically a copy.deep.

		Returns:
			NFA: """
		new = cNFA()
		new.setSigma(self.Sigma)
		new.States = self.States[:]
		new.Initial = self.Initial.copy()
		new.Final = self.Final.copy()
		new.markedTransitions = self.markedTransitions.copy()
		for s in self.delta:
			new.delta[s] = {}
			for c in self.delta[s]:
				new.delta[s][c] = self.delta[s][c].copy()
		return new
	
	def succintTransitions(self):
		""" Collects the transition information in a compact way suitable for graphical representation.
		Returns:
			list:

		.. note:
			tupples in the list are stateout, label, statein
		"""
		
		foo = dict()
		for s in self.delta:
			for c in self.delta[s]:
				for s1 in self.delta[s][c]:
					k = (s, s1)
					if k not in foo:
						foo[k] = []

					if (s,c,s1) in self.markedTransitions:
						foo[k].append("{}`".format(c))
					else:
						foo[k].append(c)
		l = []
		for k in foo:
			cs = foo[k]
			s = "%s" % graphvizTranslate(str(cs[0]))
			for c in cs[1:]:
				s += ", %s" % graphvizTranslate(str(c))
			l.append((self.dotLabel(self.States[k[0]]), s, self.dotLabel(self.States[k[1]])))
		return l
	
	def dotFormat(self, size="20,20", filename=None, direction="LR", strict=False, maxlblsz=6, sep="\n") -> str:
		""" A dot representation

		Args:
			direction (str): direction of drawing - "LR" or "RL"
			size (str): size of image
			filename (str): output file name
			sep (str): line separator
			maxlblsz (int): max size of labels before getting removed
			strict (bool): use limitations of label sizes
		Returns:
			str: the dot representation

		.. versionadded:: 0.9.6

		.. versionchanged:: 1.2.1"""
		if not strict and max([len(str(name)) for name in self.States]) > maxlblsz:
			o = self.dup()
			o.renameStates()
		else:
			o = self
		s = "digraph finite_state_machine {{{0:s}".format(sep)
		s += "rankdir={0:s};{1:s}".format(direction, sep)
		s += "size=\"{0:s}\";{1:s}".format(size, sep)
		for si in o.Initial:
			sn = o.dotLabel(o.States[si])
			s += "node [shape = point]; \"dummy{0:s}\"{1:s}".format(sn, sep)
			s += o.dotDrawState(si)
			s += "\"dummy{0:s}\" -> \"{1:s}\";{2:s}".format(sn, graphvizTranslate(sn), sep)
		ni_states = [i for i in range(len(o.States)) if i not in o.Initial]
		for sti in ni_states:
			s += o.dotDrawState(sti)
		for si in o.succintTransitions():
			s += o.dotDrawTransition(si[0], si[1], si[2])
		s += "}}{0:s}".format(sep)

		return s

	def addMarkedTransition(self, sti1, sym, sti2):
		self.markedTransitions.append((sti1, sym, sti2))
		self.addTransition(sti1, sym, sti2)

	def countMatches(self, word):
		""" Count the number of matches of a word in the NFA.

		Args:
			word (str): the word to be counted
		Returns:
			int: the number of matches
		"""

		temp_buffer = word
		last_states = set(self.Initial)
		match_count = 0

		while temp_buffer:
			psym = temp_buffer[0]

			for istate in self.delta:
				if istate in last_states:
					for isym in self.delta[istate]:
						if isym == psym:
							for fstate in self.delta[istate][isym]:
								last_states.add(fstate)
								if (istate,isym,fstate) in self.markedTransitions:
									print("found", istate, isym, fstate)
									match_count += 1

			temp_buffer = temp_buffer[1:]

		return match_count
	
	def newCountMatchesListed(self, word):
		before_symbol_states = list(self.Initial)
		rw=word
		c=0

		for i in word:
			if i not in self.Sigma:
				continue

			after_symbol_states = []
			
			for before_symbol_state in before_symbol_states:
				after_symbol_states.append(before_symbol_state)
				try:
					ls = list(self.delta[before_symbol_state][i])
				except KeyError or NameError:
					ls = []
				finally:
					for t in ls:
						print("\ttesting:", before_symbol_state, i, t)
						if (before_symbol_state, i, t) in self.markedTransitions:
							print("\t\tmatch found:", self.delta[before_symbol_state][i])
							after_symbol_states.remove(before_symbol_state)
							c+=1
						else:
							after_symbol_states.append(t)

			print("i:", i)
			print("rw:", rw)
			print("before", before_symbol_states)
			print("after", after_symbol_states)
			
			rw = rw[1:]
			before_symbol_states = after_symbol_states
		
		return c


	def newCountMatches(self, word):
		ilist = self.epsilonClosure(set(self.Initial))
		ctr = 0
		widx = 0
		lwidx = 0
		last_difference = set()

		remw = word

		for i in word:
			if i not in self.Sigma:
				continue

			print("w", remw)
			char=remw[0]
			print("c", char)
			remw=remw[1:]

			

			from_states = ilist # from states
			print("before", ilist)
			after_states = self.evalSymbol(ilist, i)
			ilist = after_states

			print("\tafter", ilist)

			if after_states-from_states == last_difference: # means there was a new state
				lwidx = widx

			last_difference = after_states-from_states

			for istate in from_states:
				for fstate in after_states:
					if (istate, i, fstate) in self.markedTransitions:
						ctr += 1
						# print("match", lwidx, widx, word[lwidx:widx+1])
						print("\t\tmatch! -> ", (istate, i, fstate))
						lwidx = widx+1
					# elif from_states==after_states:
					# 	ctr += 1
					# 	print("\t\tspecial match! -> ", from_states, after_states)

			widx += 1

		return ctr
	
	def toDFAc(self):
		if self.markedTransitions == []:
			return super().toDFA()

		aut = self.dup()

		# get unused symbol to identify marked transitions
		import string
		symbol_to_use = (set(string.ascii_lowercase) - set(aut.Sigma)).pop()
		# symbol_matches = {}

		for mtransition in aut.markedTransitions:
			from_state, symbol, to_state = mtransition
			del aut.delta[from_state][symbol]
			aut.addTransition(from_state, symbol_to_use, to_state)

		return aut.toDFA().toDFAc(set([symbol_to_use])) # type: ignore


def cnt(grp:FA, wrd):
	# ctr = 0 
	# positions = [] 
	# for i in range(len(wrd) - 1):
	# 	current_state = grp.epsilonClosure(set([0]))
	# 	two_chars = wrd[i:i+2]
	# 	match_positions = [i, i+1]

	# 	for char in two_chars:
	# 		current_state = grp.evalSymbol(current_state, char)

	# 	if any(s in current_state for s in grp.Final):
	# 		ctr += 1
	# 		positions.append(match_positions)

	# return ctr, positions

	ilist = grp.epsilonClosure(set([0]))
	ctr = 0
	pos = []
	nw = []
	idx=0
	for i in wrd:
		ilist = grp.evalSymbol(ilist, i)
		nw.append(idx)
		idx+=1

		print(i, idx-1, ilist)

		for s in grp.Final:
			if s in ilist:
				ctr+=1
				pos.append(nw)
				nw = nw[idx-1:]
				break

	return ctr, pos

# DEPRECATED
def gen_nfa(word):
	kp = word
	sigma = set(kp)
	sigma = sigma - set(["|", "*"])

	splt = kp.split("|")
	ng = cNFA()
	ng.setSigma(sigma)
	initial_state = ng.addState()
	final_state = ng.addState()
	ng.addInitial(initial_state)
	ng.addFinal(final_state)

	for s in splt:
		ck=0
		cur_init = ng.addState()
		ng.addTransitionStar(initial_state, cur_init)
		last_state = 0

		first_symbol_state = None

		letc = 0
		nas = sum([1 for i in s if i == "*"])

		for k in s:
			if k == "*":
				continue

			nl = None
			if letc+1 < len(s):
				nl = s[letc+1]

			if ck == 0:
				last_state = ng.addState()
				first_symbol_state = last_state
				ng.addTransition(initial_state, k, last_state)
			elif ck == len(s)-1-nas:
				ng.addTransition(last_state, k, final_state)
			else:
				old_state = last_state
				last_state = ng.addState()
				ng.addTransition(old_state, k, last_state)
				if nl == "*":
					ng.addTransition(last_state, k, last_state)
			ck+=1
			letc+=1

		for i in ng.States:
			if int(i) != 0:
				for z in sigma:
					if z != "|" and z!= "*":
						if z != s[0]:
							ng.addTransition(int(i), z, 0)
						else:
							ng.addTransition(int(i), s[0], first_symbol_state)
	return ng

def nfaCount(self: RegExp):
	aut = cNFA()
	added_states = {}

	if self.Sigma is not None:
		aut.setSigma(self.Sigma)

	i = aut.addState()
	aut.addInitial(i)
	added_states[self] = i

	aut.addTransitionStar(i,i)

	f = aut.addState()
	aut.addFinal(f)

	lf = self.linearForm()

	for head in lf:
		head_state = aut.addState()
		aut.addTransition(i, head, head_state)
		aut.addTransition(head_state, head, head_state)
		aut.addTransition(f, head, head_state)

		for tail in lf[head]:
			stack = [tail.linearForm()]

			last_state = head_state

			# here, head is the symbol from initial to the first wave state
			# tail represents the rest of the FA
			while stack:
				# compute rest of the FA after first wave
				# and save trail with lengths
				remainder_lf : dict = stack.pop()

				if len(remainder_lf) == 0:
					aut.addTransition(i, head, f)
					aut.deleteState(head_state)
					break
				else:
					for thead in remainder_lf:
						if thead in added_states:
							last_state = added_states[thead]
						else:
							outgoing = remainder_lf[thead].pop()
							if outgoing:
								olf = outgoing.linearForm()

								if olf == {}:
									aut.addTransition(last_state, thead, f)
								else:
									new_state = aut.addState()
									aut.addTransition(last_state, thead, new_state)
									last_state = new_state

									stack.append(olf)
	return aut

def nfaNewCount(self: RegExp):
	aut = cNFA()
	i = aut.addState(self)
	aut.addInitial(i)
	if self.Sigma is not None:
		aut.setSigma(self.Sigma)
	stack = [(self, i)]
	added_states = {self: i}

	#print(added_states)
	
	while stack:
		
		state, state_idx = stack.pop()
		# print("stack", state, state_idx)
		state_lf = state.linearForm()
		for head in state_lf:
			tails = state_lf[head]
			aut.addSigma(head)
			for pd in tails:
				if pd in added_states:
					pd_idx = added_states[pd]
				else:
					try:
						pd_idx = aut.addState(pd)
					except DuplicateName:
						pd_idx = aut.stateIndex(pd)
					added_states[pd] = pd_idx
					stack.append((pd, pd_idx))
				aut.addTransition(state_idx, head, pd_idx)
				# print("transition", state_idx, head, pd_idx)
		if state.ewp():
			aut.addFinal(state_idx)

	# if (aut.Final <= aut.Initial) is False:
	for i in aut.Initial:
		aut.addTransitionStar(i, i)
	
	# for i in aut.Final:
	# 	for z in aut.Initial:
	# 		aut.addTransitionStar(i, z)
	
	# for i in aut.Final:
	# 	aut.addTransitionStar(i, i)

	#for i in caut.delta:
	# if i in aut.Initial:
	# 	for z in aut.delta[i]:
	# 		for j in aut.delta[i][z]:
	# 			# i: from
	# 			# z: symbol
	# 			# j: to
	# 			aut.addTransition(j, z, j)

	for starter in aut.delta:
		for symbol in aut.delta[starter]:
			for ender in aut.delta[starter][symbol]:
				if ender in aut.Final:
					if ender != starter:
						aut.addMarkedTransition(starter, symbol, ender)
						print("added", starter, symbol, ender)

	return aut

def nfaPosCount(self: RegExp):
	aut = cNFA()
	i = aut.addState()
	aut.addInitial(i)
	
	if self.Sigma is not None:
		aut.setSigma(self.Sigma)

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
	for sym in freg.last():
		if sym in added_states:
			aut.addFinal(added_states[sym])

	return aut




def toDFAc(self: DFA, symbol_list: set) -> cDFA:
	caut = cDFA()
	caut.setSigma(self.Sigma)
	caut.States = self.States[:]
	caut.Initial = self.Initial # type: ignore
	caut.Final = self.Final.copy()
	for s in list(self.delta.keys()):
		caut.delta[s] = {}
		for c in list(self.delta[s].keys()):
			caut.delta[s][c] = self.delta[s][c]
			if c in symbol_list:
				caut.markedTransitions.append((s, c, self.delta[s][c]))

	return caut

setattr(RegExp, 'nfaCount', nfaCount)
setattr(RegExp, 'nfaNewCount', nfaNewCount)
setattr(RegExp, 'nfaPosCount', nfaPosCount)
setattr(DFA, 'toDFAc', toDFAc)