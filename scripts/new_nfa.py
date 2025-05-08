import FAdo.reex

from FAdo.fa import *
from FAdo.reex import *
from FAdo.fio import *
from FAdo.rndadfa import *

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

		print(i, idx-1)

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
	ng = NFA()
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
	aut = NFA()
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
	aut = NFA()
	caut : NFA = self.toNFA("nfaPDNaive")

	for i in caut.Initial:
		caut.addTransitionStar(i, i)

	for i in caut.delta:
		if i in aut.Initial:
			for z in caut.delta[i]:
				for j in caut.delta[i][z]:
					# i: from
					# z: symbol
					# j: to

					caut.addTransition(j, z, j)

	for i in caut.Final:
		for z in caut.Initial:
			caut.addTransitionStar(i, z)

	return caut

setattr(RegExp, 'nfaCount', nfaCount)
setattr(RegExp, 'nfaNewCount', nfaNewCount)