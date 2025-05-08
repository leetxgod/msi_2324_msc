from new_nfa import *

regGrammar = lark.Lark.open("lang/regexp_test.lark", start="rege", parser="lalr")

r1 = "a(b+c)+cab"
r1 = "a(b+c)+ac"

tree = regGrammar.parse(r1)

reg = BuildRegexp(context={"sigma": None}).transform(tree)
reg.setSigma(reg.setOfSymbols())

x = reg.toNFA("nfaCount")

w = "abaccabaaac"
w = "aaaccc"
ctr, post = cnt(x, w)

for i in post:
	print("match", w[min(i):max(i)+1])

print(ctr)
#print(x)