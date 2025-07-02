from match_nfa import *
from count import *
from termcolor import colored, cprint
import time
#from count import *

w1 = "(a+aa+aaa)%"
regGrammar = lark.Lark.open("lang/regexp_test.lark", start="rege", parser="lalr")
tree = regGrammar.parse(w1)
reg = BuildRegexp(context={"sigma": None}).transform(tree)
reg.setSigma(reg.setOfSymbols())
x : matchNFA = reg.toNFA("nfaPosCount")
# x.display()

w2 = "aaaaaaaaa"
#x.table_matcher(w2)

before = time.time()
d = x.table_matcher(w2)
c1 = time.time()
f = x.enum_matches(d, w2)
c2 = time.time()

print("Expected matches:", len(w2)-4)
print("Number of matches:", sum([len(set(d[s])) for s in d]))

print("Time for table matcher:", c1-before)
# print("Time for enum matches:", c2-c1)

# print(d)