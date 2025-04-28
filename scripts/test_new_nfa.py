from new_nfa import *

regGrammar = lark.Lark.open("lang/regexp_test.lark", start="rege", parser="lalr")
tree = regGrammar.parse("aab")

reg = BuildRegexp(context={"sigma": None}).transform(tree)
reg.setSigma(reg.setOfSymbols())
#print("RegExp: ", reg)
reg.toNFA("nfaCount")