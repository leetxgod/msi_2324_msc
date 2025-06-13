# add gen words (concat them) and test the cFA (with overlapping)

from new_nfa import *
from count import *

class RandomwordGenerator:
	def __init__(self, re, langpath):
		regGrammar = lark.Lark.open(langpath, start="rege", parser="lalr")
		tree = regGrammar.parse(re)
		self.reg = BuildRegexp(context={"sigma": None}).transform(tree)
		self.reg.setSigma(self.reg.setOfSymbols())

		self.nfa : cNFA = self.reg.toNFA("nfaNewCount")

		self.enum : EnumNFA = EnumNFA(self.nfa)
		self.enum.initStack()
	
	def get_fa_obj(self):
		return self.nfa

	def count_matches(self, word):
		return self.nfa.newCountMatches(word)

	def gen(self, wordCount):
		self.enum.enum(wordCount)
		return self.enum.Words
	
	def gen_test(self, rmin:int, rmax:int, wordCount:int, overlap:bool = False):
		# Generate 'wordCount' words of length between 'rmin' and 'rmax'
		import random
		import time
		random.seed(time.time())
		word = ""
		for _ in range(wordCount):
			rw = self.gen(random.randint(rmin, rmax))
			if overlap:
				up = random.random() > 0.5
				rw = rw[0:len(rw)//2] if not up else rw[len(rw)//2:]
			word += "".join(rw)
		return word


r1 = "(a+((ba)*))c"
r1 = "(ba)*c"
r1 = "(bab)aa"
test = RandomwordGenerator(r1, "lang/regexp_test.lark")

# 10 words of length between 1 and 3
w = test.gen_test(1, 5, 10, True)
print("Generated word: ", w)
print(test.count_matches(w))

# Write p