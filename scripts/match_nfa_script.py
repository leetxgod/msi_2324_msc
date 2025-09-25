from match_nfa import *
from count import *
from termcolor import colored, cprint
import time
#from count import *

w1 = "(aa+aaa)(aaa+aa)"
regGrammar = lark.Lark.open("lang/regexp_test.lark", start="rege", parser="lalr")
tree = regGrammar.parse(w1)
reg = BuildRegexp(context={"sigma": None}).transform(tree)
reg.setSigma(reg.setOfSymbols())
x : matchNFA = reg.toNFA("nfaPosCount")
# x.display()

def enum_matches(self, pos_tab: dict, string: str):
	match_count = 0
	for entry in pos_tab:
		print(f"State {entry} matches ({len(set(pos_tab[entry]))}):")
		match_set = set(pos_tab[entry])
		match_count += len(match_set)
		for match in sorted(match_set):
			first_index = string[0:match[0]]
			second_index = string[match[1]:]
			print("Match:", colored(first_index, 'red') + colored(string[match[0]:match[1]], 'green') + colored(second_index, 'red'), "=>", match)
	print("Total matches:", match_count)

w2 = "aaaaabaaaaa"
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