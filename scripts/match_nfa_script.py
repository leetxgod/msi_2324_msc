from match_nfa import *
from termcolor import colored, cprint
#from count import *

w1 = "(ab+ab)%"
regGrammar = lark.Lark.open("lang/regexp_test.lark", start="rege", parser="lalr")
tree = regGrammar.parse(w1)
reg = BuildRegexp(context={"sigma": None}).transform(tree)
reg.setSigma(reg.setOfSymbols())
x : matchNFA = reg.toNFA("nfaPosCount")
# x.display()

w2 = "aaababa"
#x.table_matcher(w2)
d = x.table_matcher(w2)
f = x.enum_matches(d, w2)

print("Expected matches:", len(w2)-4)
print("Number of matches:", sum([len(set(d[s])) for s in d]))

# print(d)