import FAdo.reex

from FAdo.fa import *
from FAdo.reex import *
from FAdo.fio import *
from FAdo.rndadfa import *

def cnt(grp, wrd):
	ilist = grp.epsilonClosure(set([0]))
	ctr = 0
	for i in wrd:
		ilist = grp.evalSymbol(ilist, i)
		for s in grp.Final:
			if s in ilist:
				ctr+=1
				break

	return ctr

def gen_nfa(word):
	kp = word
	sigma = set(kp)

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
					if z != s[0]:
						ng.addTransition(int(i), z, 0)
					else:
						ng.addTransition(int(i), s[0], first_symbol_state)
	return ng

def nfaCount(self: RegExp):
	aut = NFA()
	if self.Sigma is not None:
		aut.setSigma(self.Sigma)

	i = aut.addState(CEpsilon())
	aut.addInitial(i)

	f = aut.addState()
	aut.addFinal(f)

	lf = self.linearForm()
	stck = []
	for head in lf:
		stck.append((head, lf[head].pop(), None))

	passn = 0

	while stck:
		head, tail, initial = stck.pop()
		new_state = aut.addState()
		
		if isinstance(tail, CStar):
			print("found star instance tail")
			return None
		
		if isinstance(head, CStar):
			print("found star instance head")
			return None

		nlf = tail.linearForm()

		if len(nlf):
			for nhead in nlf:
				stck.append((nhead, nlf[nhead].pop(), new_state))
		else:
			aut.addTransition(initial, head, f)
			aut.deleteState(new_state)
		if initial is not None:
			aut.addTransition(initial, head, new_state)
		else:
			aut.addTransition(i, head, new_state)
	

	# handle initial transitions

	
	# while stck:
	# 	head, tail, wave, last_state = stck.pop()
		
	# 	if isinstance(tail, set):
	# 		tail = tail.pop()
		
	# 	# based on initial transitions..
	# 	if wave==0:
	# 		new_state = aut.addState()
	# 		aut.addTransition(i, head, new_state)
	# 	else:
	# 		new_state = aut.addState()
	# 		aut.addTransition(last_state, head, new_state)

	# 	tail_lf = tail.linearForm()

	# 	# print(tail_lf)

	# 	for t_head in tail_lf:
	# 		stck.append((t_head, tail_lf[t_head], wave+1, new_state))

		# print("head: ", head)
		# print("tail: ", tail)
		# print("wave: ", wave)
		# print("last_state: ", last_state)


	# print(stck)
	#print(self)
	# print(aut)

	return aut

setattr(RegExp, 'nfaCount', nfaCount)