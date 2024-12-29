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
		print("N:{} -> {} -> {}".format(self.n, self.arg, self.arg.derivative(sigma)))
		return CCount(self.arg.derivative(sigma), self.n-1)

#r = CStar(CDisj(CCount(CAtom("a"),1), CConcat(CAtom("b"), CAtom("a"))))
a = CCount(CAtom("aaa"), 3)
print(a)
r = a.evalWordP("aaa")
print(r)


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