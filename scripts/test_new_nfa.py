from new_nfa import *
from count import *

regGrammar = lark.Lark.open("lang/regexp_test.lark", start="rege", parser="lalr")

r1 = "a(b+c)+cab"
r1 = "(ab)+(ba)"

tree = regGrammar.parse(r1)

reg = BuildRegexp(context={"sigma": None}).transform(tree)
reg.setSigma(reg.setOfSymbols())

x = reg.toNFA("nfaPosCount")

print(x.Sigma)

# w = "abaccabaaac"
# w = "aabaabbbabc"
# w = "ababbabaaa"
# ctr, post = cnt(x, w)

# for i in post:
# 	print("match", w[min(i):max(i)+1])

# print(ctr)
#print(x)