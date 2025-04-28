# def linearForm(self): # https://www.dcc.fc.up.pt/~nam/resources/publica/51480046.pdf
	# 	arg_lf = self.arg.linearForm()
	# 	#print(arg_lf)
	# 	lf = dict()
	# 	for head in arg_lf:
	# 		lf[head] = set()
	# 		for tail in arg_lf[head]:
	# 			if tail.emptysetP():
	# 				lf[head].add(CEmptySet(self.Sigma))
	# 			elif tail.epsilonP():
	# 				if self.max == "inf" or self.max == None:
	# 					if self.min - 1 == 0: #[n,m[
	# 						lf[head].add(CStar(self.arg))
	# 					elif self.min - 1 == 1:
	# 						lf[head].add(self.arg)
	# 					else:
	# 						self.min -= 1
	# 						lf[head].add(self)
	# 				else:
	# 					mav = int(self.max)
	# 					if mav-1 == self.min:
	# 						lf[head].add(CEpsilon())
	# 					elif mav-1 == self.min+1:
	# 						lf[head].add(self.arg)
	# 					else:
	# 						self.max = mav - 1
	# 						lf[head].add(self)
	# 			else:
	# 				if self.max == "inf" or self.max == None:
	# 					if self.min - 1 == 0: #[n,m[
	# 						lf[head].add(CConcat(tail, CStar(self.arg), self.Sigma))
	# 					elif self.min - 1 == 1:
	# 						lf[head].add(CConcat(tail, self.arg, self.Sigma))
	# 					else:
	# 						self.min -= 1
	# 						lf[head].add(CConcat(tail, self, self.Sigma))
	# 				else:
	# 					mav = int(self.max)
	# 					if mav-1 == self.min:
	# 						lf[head].add(CConcat(tail, CEpsilon(), self.Sigma))
	# 					elif mav-1 == self.min+1:
	# 						lf[head].add(CConcat(tail, self.arg, self.Sigma))
	# 					else:
	# 						self.max = mav - 1
	# 						lf[head].add(CConcat(tail, self, self.Sigma))

	# 	#print(lf)
					
	# 	return lf

	# def partialDerivatives(self, sigma):
	# 	arg_pdset = self.arg.partialDerivatives(sigma)
	# 	pds = set()
	# 	for pd in arg_pdset:
	# 		if pd.emptysetP():
	# 			pds.add(CEmptySet(self.Sigma))
	# 		elif pd.epsilonP():
	# 			if self.max == "inf" or self.max == None:
	# 				if self.min - 1 == 0: #[n,m[
	# 					pds.add(CStar(self.arg))
	# 				elif self.min - 1 == 1:
	# 					pds.add(self.arg)
	# 				else:
	# 					self.min -= 1
	# 					pds.add(self)
	# 			else:
	# 				mav = int(self.max)
	# 				if mav-1 == self.min:
	# 					pds.add(CEpsilon())
	# 				elif mav-1 == self.min+1:
	# 					pds.add(self.arg)
	# 				else:
	# 					self.max = mav - 1
	# 					pds.add(self)
	# 		else:
	# 			if self.max == "inf" or self.max == None:
	# 				if self.min - 1 == 0: #[n,m[
	# 					pds.add(CConcat(pd, CStar(self.arg), self.Sigma))
	# 				elif self.min - 1 == 1:
	# 					pds.add(CConcat(pd, self.arg, self.Sigma))
	# 				else:
	# 					self.min -= 1
	# 					pds.add(CConcat(pd, self, self.Sigma))
	# 			else:
	# 				mav = int(self.max)
	# 				if mav-1 == self.min:
	# 					pds.add(CConcat(pd, CEpsilon(), self.Sigma))
	# 				elif mav-1 == self.min+1:
	# 					pds.add(CConcat(pd, self.arg, self.Sigma))
	# 				else:
	# 					self.max = mav - 1
	# 					pds.add(CConcat(pd, self, self.Sigma))
	# 		# else:
	# 		# 	pds.add(CConcat(pd, self, self.Sigma))
	# 	return pds
	
	# def derivative(self, sigma): # how ...?
		

	# def derivative(self, sigma): # how ...?
	# 	if self.max == "inf" or self.max == None:
	# 		if self.min-1 == 0:
	# 			return CStar(self.arg, self.Sigma)
	# 		elif self.min-1 == 1:
	# 			#print(self.min)
	# 			return CConcat(self.arg.derivative(sigma), CStar(self.arg, self.Sigma), self.Sigma)
	# 		else:
	# 			self.min -= 1
	# 			#print(self)
	# 			return CConcat(self.arg.derivative(sigma), self, self.Sigma)
	# 		# else:
	# 		# 	d = self.arg.derivative(sigma)
	# 		# 	if d == CEpsilon():
	# 		# 		return CCount(self.arg, self.min-1, self.__in(), self.Sigma)
	# 		# 	else:
	# 		# 		return CCount(self.arg, self.min-1, self.__in(), self.Sigma)
	# 	else:
	# 		m_v = int(self.max)
	# 		if self.min == m_v:
	# 			return CEpsilon()
	# 		elif self.min == m_v-1: # [1,2[
	# 			return self.arg
	# 		else:
	# 			self.max = m_v-1
	# 			return self