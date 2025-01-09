from FAdo.fa import *
from FAdo.reex import *
from FAdo.fio import *
from FAdo.rndadfa import *


class CCount(Power):
	def __init__(self, arg, n, sigma=None):
		self.arg = arg
		self.n = n
		self.sigma = sigma
		super().__init__(arg, n, sigma)

	def derivative(self, sigma):
		if self.n == 0:
			return CEmptySet()
		elif self.n == 1:
			return CEpsilon()
		else:
			d = self.arg.derivative(sigma)
			if d == CEpsilon():
				return CCount(self.arg, self.n-1, sigma)
			else:
				return CConcat(d, CCount(self.arg, self.n-1, sigma), sigma)

#r = CStar(CDisj(CCount(CAtom("a"),1), CConcat(CAtom("b"), CAtom("a"))))
a = CConcat(CCount(CAtom("a"), 2), CAtom("b"))
#a = CCount(CAtom("a"), 2)
#b = CConcat(CStar(CAtom("a")), CConcat(CAtom("b"), CAtom("a")))
#print(a)
#r = a.wordDerivative("a")
a.dfaBrzozowski().display()


# m3 = DFA()
# m3.setSigma(['0','1'])
# m3.addState('s1')
# m3.addState('s2')
# m3.addState('s3')
# m3.setInitial(0)
# m3.addFinal(0)
# m3.addTransition(0, '0', 0)
# m3.addTransition(0, '1', 1)
# m3.addTransition(1, '0', 2)
# m3.addTransition(1, '1', 0)
# m3.addTransition(2, '0', 1)
# m3.addTransition(2, '1', 2)
# m3.display()