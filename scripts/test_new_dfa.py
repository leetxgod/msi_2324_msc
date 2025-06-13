from new_nfa import *
from count import *

regGrammar = lark.Lark.open("lang/regexp_test.lark", start="rege", parser="lalr")

r1 = "a(b+c)+cab"
r1 = "(ab)+(ba)"

tree = regGrammar.parse(r1)

reg = BuildRegexp(context={"sigma": None}).transform(tree)
reg.setSigma(reg.setOfSymbols())

x = reg.toNFA("nfaNewCount")
y = x.toDFA()

print(y)