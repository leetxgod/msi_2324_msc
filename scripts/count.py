import FAdo.reex

from FAdo.fa import *
from FAdo.reex import *
from FAdo.fio import *
from FAdo.rndadfa import *

import lark
from match_nfa import CPlus

class CPower(Unary):
    def __init__(self, arg, n, sigma=None):
        self.arg = arg
        self.n = n
        self.Sigma = sigma
        self._ewp = False if self.n > 0 else True
        #super(CPower, self).__init__(arg, n)
    
    def __str__(self):
        """String representation of the regular expression."""
        return '{}^{}'.format(self.arg, self.n)
    
    def __repr__(self):
        """String representation of the regular expression."""
        return '{}^{}'.format(self.arg, self.n)
    
    def _strP(self):
        """String representation of the regular expression."""
        return '{}^{}'.format(self.arg, self.n)
    
    def ewp(self):
        return self.n==0

    def linearForm(self):
        arg_lf = self.arg.linearForm()
        #print(arg_lf)
        lf = dict()
        for head in arg_lf:
            lf[head] = set()
            for tail in arg_lf[head]:
                # if tail.emptysetP():
                # 	lf[head].add(CEmptySet(self.Sigma))
                # else:
                if self.n == 0:
                    lf[head].add(CEmptySet(self.Sigma))
                elif self.n == 1:
                    lf[head].add(CEpsilon(self.Sigma))
                else:
                    lf[head].add(CPower(self.arg, self.n-1, self.Sigma))

        return lf

    def partialDerivatives(self, sigma):
        return self.arg.partialDerivatives(sigma)

    def derivative(self, sigma):
        if str(sigma) in str(self.arg):
            if self.n == 0:
                return CEmptySet(sigma)
            elif self.n == 1:
                return self.arg.derivative(sigma)
            else:
                return CConcat(self.arg.derivative(sigma), CPower(self.arg, self.n-1, self.Sigma))
        else:
            return CEmptySet(sigma)
    
    def first(self, parent_first=None):
        return self.arg.first(parent_first)
    
    def last(self, parent_first=None):
        return self.arg.last(parent_first)
    
    # def followLists(self, lists=None):
    #     for i in range(self.n):
    #         lists = self.arg.followLists(lists)

    #     for symbol in self.arg.last():
    #         for i in range(self.n-1):
    #             if symbol not in lists:
    #                 lists[symbol] = self.arg.first()
    #             else:
    #                 lists[symbol] += self.arg.first()
    #     return lists
    
    def followListsStar(self, lists=None):
        return self.arg.followListsStar(lists)

    def followListsD(self, lists=None):
        # print("self", self)

        for i in range(self.n):
            lists = self.arg.followLists(lists)

        for symbol in self.arg.last():
            # print(self.arg, self.arg.first(), self.arg.last())
            for i in range(self.n-1):
                if symbol not in lists:
                    lists[symbol] = self.arg.first()
                else:
                    lists[symbol] += self.arg.first()
        return lists

    def unmarked(self):
            return CPower(self.arg.unmarked(), self.n, self.Sigma)

    def _marked(self, pos):
        def nested(values):
            if not values:
                return None
            elif len(values) == 1:
                return values[0]
            else:
                return CConcat(values[0], nested(values[1:]))
        
        lst = [self.arg for _ in range(self.n)]
        (r1, pos1) = nested(lst)._marked(pos)

        return r1, pos1
        
setattr(FAdo.reex, 'CPower', CPower)

class CCount(Unary):
    def __init__(self, arg, min, max = None, sigma = None):
        self.arg = arg
        self.min = int(min)
        self.max = "inf" if max == -1 or max == "inf" else int(max)-1
        self.Sigma = sigma

        if self.min==0:
            self._ewp = True
    
    def __str__(self):
        """String representation of the regular expression."""
        return 'CCount({},[{}[)'.format(self.arg, self.min if self.max=="inf" else '{},{}'.format(self.min, self.max+1))
    
    def _strP(self):
        """String representation of the regular expression."""
        return 'CCount({},[{}[)'.format(self.arg, self.min if self.max=="inf" else '{},{}'.format(self.min, self.max+1))

    def __repr__(self):
        """Representation of the regular expression's syntactical tree."""
        return 'CCount({},[{}[)'.format(self.arg, self.min if self.max=="inf" else '{},{}'.format(self.min, self.max+1))

    def epsilonP(self):
        if self.max == "inf" or self.max == None:
            return self.min == 0
        else:
            m_v = int(self.max)
            return self.min == 0 and m_v == 0
        
    def ewp(self):
        return self.min==0
    
    def _ewp(self):
        return self.ewp()

    def derivative(self, sigma):
        if str(sigma) in str(self.arg) and str(sigma) != "":
            if self.max == "inf" or self.max == None:
                if self.min == 0: # means it was 1 -> [1, ...] -> argder.CStar
                    return CConcat(self.arg.derivative(sigma), CStar(self.arg, self.Sigma))
                else:
                    return CConcat(self.arg.derivative(sigma), CCount(self.arg, self.min-1, self.max, sigma), self.Sigma)
            else:
                if self.min == 0:
                    return CConcat(self.arg.derivative(sigma), CCount(self.arg, self.min, int(self.max), self.Sigma))
                else:
                    return CConcat(self.arg.derivative(sigma), CCount(self.arg, self.min-1, int(self.max), self.Sigma))
                    
        else:
            return CEmptySet(sigma)

    def partialDerivatives(self, sigma):
        arg_pdset = self.arg.partialDerivatives(sigma)
        pds = set()
        for pd in arg_pdset:
            if pd.emptysetP():
                pds.add(CEmptySet(self.Sigma))
            elif pd.epsilonP():
                pds.add(self)
            else:
                pds.add(CConcat(pd, self, self.Sigma))
        return pds

    def linearForm(self): # https://www.dcc.fc.up.pt/~nam/resources/publica/51480046.pdf
        def nested(values):
            if not values:
                return None
            elif len(values) == 1:
                return values[0]
            else:
                return CDisj(values[0], nested(values[1:]))

        arg_lf = self.arg.linearForm()
        lf = dict()
        for head in arg_lf:
            lf[head] = set()
            for tail in arg_lf[head]:
                if tail.emptysetP():
                    lf[head].add(CEmptySet(self.Sigma))
                elif tail.epsilonP():
                    if self.max == "inf" or self.max == None:
                        if self.min - 1 == 0:
                            lf[head].add(CStar(self.arg, self.Sigma))
                        else:
                            lf[head].add(CConcat(CPower(self.arg, self.min-1, self.Sigma), CStar(self.arg, self.Sigma), self.Sigma))
                    else:
                        mav = int(self.max)
                        lst = []
                        for i in range(self.min-1, mav):
                            if i > 0:
                                lst.append(CPower(self.arg, i, self.Sigma))
                            else:
                                lst.append(CEpsilon(self.Sigma))

                        lf[head].add(nested(lst))
                else:
                    if self.max == "inf" or self.max == None:
                        if self.min - 1 == 0:
                            lf[head].add(CConcat(tail, CStar(self.arg, self.Sigma)))
                        else:
                            lf[head].add(CConcat(tail, CConcat(CPower(self.arg, self.min-1, self.Sigma), CStar(self.arg, self.Sigma), self.Sigma)))
                    else:
                        mav = int(self.max)
                        lst = []
                        for i in range(self.min, mav):
                            lst.append(CPower(self.arg, i, self.Sigma))

                        lf[head].add(CConcat(tail, nested(lst), self.Sigma))

        return lf

    def followListsD(self, lists=None):
        # print("self", self)

        for i in range(self.n):
            lists = self.arg.followLists(lists)

        for symbol in self.arg.last():
            for i in range(self.max - self.min):
                if symbol not in lists:
                    lists[symbol] = self.arg.first()
                else:
                    lists[symbol] += self.arg.first()
        return lists

    def unmarked(self):
        return CCount(self.arg.unmarked(), self.min, self.max, self.Sigma)

    def _marked(self, pos):
        def nested(values):
            if not values:
                return None
            elif len(values) == 1:
                return values[0]
            else:
                return CDisj(values[0], nested(values[1:]))
        
        # print(self.arg, self.min, self.max, self.Sigma)

        lst = [CPower(self.arg, i, self.Sigma) for i in range(self.min, self.max+1)]
        (r1, pos1) = nested(lst)._marked(pos)

        return r1, pos1
    
setattr(FAdo.reex, 'CCount', CCount)

def pow_min(self, s, inf=False):
    (arg, n_r) = s
    n = int(n_r.children[0].value)
    if inf:
        if n == 0:
            r = CStar(arg, sigma=self.sigma)
        elif n == 1:
            r = CPlus(arg, sigma=self.sigma)
        else:
            r = CCount(arg, n, -1, sigma=self.sigma)
    else:
        r = CPower(arg, n, sigma=self.sigma)

    # r._ewp = False

    return r

def pow_minmax(self, s):
    (arg, n_mi, n_ma) = s
    n_min = n_mi.children[0].value
    n_max = n_ma.children[0].value

    r = CCount(arg, n_min, n_max, sigma=self.sigma)

    if n_max != "inf":
        if n_max == n_min:
            r = CAtom(arg, self.sigma)

    # r._ewp = False
    return r

def pow_inf(self, s):
    return self.pow_min(s, True)

setattr(BuildRegexp, 'pow_inf', pow_inf)
setattr(BuildRegexp, 'pow_min', pow_min)
setattr(BuildRegexp, 'pow_minmax', pow_minmax)