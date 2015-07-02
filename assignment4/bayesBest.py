# Name: Xiaolin Li
# Date: May 11, 2015
# Description: HW4 for EECS348
#
#

import math, os, pickle, re, random


class Bayes_Classifier:
	def __init__(self, cross=False):
		"""This method initializes and trains the Naive Bayes Sentiment Classifier.  If a
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text."""
		if cross == False:
			self.pos = {}
			self.neg = {}
			IFile = []
			for jObj in os.walk("./"):
				IFile = jObj[2]
				break
			# pickled file names:
			pos_file = "pickled_pos"
			neg_file = "pickled_neg"
			# check if there is existing pickled files
			if (pos_file in IFile) and (neg_file in IFile):
				self.pos = self.load(pos_file)
				self.neg = self.load(neg_file)
				print "data imported"
				self.chi2filt()
			else:
				self.train()
		else: # start 10-fold cross validation
			self.pos = {}
			self.neg = {}
			IFile = []
			for jObj in os.walk("./"):
				IFile = jObj[2]
				break
			#pickled file names for cross validation
			pos_file_cv = "pos_cv"
			neg_file_cv = "neg_cv"
			#check if there is existing pickled files for cross validation
			if (pos_file_cv in IFile) and (neg_file_cv in IFile):
				self.pos_cv = self.load(pos_file_cv)
				self.neg_cv = self.load(neg_file_cv)
			else:
				self.train_cv()





	def train_cv(self):
		"""Cross validation for the designed classifier"""
		IFileList = []
		for fFileObj in os.walk("reviews/"):
			IFileList = fFileObj[2]
			break
		New_filelist = []
		for Fname in IFileList:
			if Fname[0] == 'm':
				New_filelist.append(Fname)
		#so far, we have collect all the file names, the next step is to break them into 10 folds

		#divide the files into 10 folds:
		fold = [[]]
		for i in range(9):
			fold.append([])
		# initialize the empty fold
		count_fold = 0
		while len(New_filelist) != 0:
			rand_num = random.randint(0, len(New_filelist)-1)
			if count_fold == 9:
				count_fold = 0
			else:
				count_fold += 1
			fold[count_fold].append(New_filelist.pop(rand_num))
		# by this point, 10 folds have been generated.
		for ii in range(10):
			train_file = []
			test_file = []

			for jj in range(10):
				if ii != jj:
					for files in fold[jj]:
						train_file.append(files)
			for files in fold[ii]:
				test_file.append(files)
			print "Training fold #" + str(ii + 1)
			self.neg = {}
			self.pos = {}
			for Fname in train_file:
				if Fname[0] == "m":
					words = self.tokenize(self.loadFile("reviews/"+Fname))
					for ele in words:
						Rrate = Fname.split("-")[1]
						if Rrate == "1":
							if ele not in self.neg.keys():
								self.neg[ele] = 1
							else:
								self.neg[ele] += 1
						elif Rrate == "5": #positive review
							if ele not in self.pos.keys():
								self.pos[ele] = 1
							else:
								self.pos[ele] += 1
			labeled = []
			classified = []
			for Fname in test_file:
				if Fname[0] == "m":
					inputText = self.loadFile("reviews/"+Fname)
					prediction = self.classify(inputText)
					label = Fname.split("-")[1]
					if label == "1":
						labeled.append(-1)
					else:
						labeled.append(1)
					if prediction == "negative":
						classified.append(-1)
					elif prediction == "positive":
						classified.append(1)

			#evaluation starts
			true_pos = 0
			true_neg = 0
			false_pos = 0
			false_neg = 0
			pos_total = 0
			neg_total = 0
			for num in range(len(classified)):
				if classified[num] == 1:
					pos_total += 1
					if labeled[num] == 1:
						true_pos += 1
					elif labeled[num] == -1:
						false_pos += 1
				elif classified[num] == -1:
					neg_total += 1
					if labeled[num] == -1:
						true_neg += 1
					elif labeled[num] == 1:
						false_neg += 1
			print "Test #" + str(ii + 1) +":"
			Accuracy = (float(true_pos) + float(true_neg)) / (float(pos_total) + float(neg_total))
			print "Accuracy: " + str(Accuracy)
			Precision_pos = float(true_pos) / float(pos_total)
			Precision_neg = float(true_neg) / float(neg_total)
			print "Precision_pos: " + str(Precision_pos)
			print "Precision_neg: " + str(Precision_neg)
			Recall_pos = float(true_pos) / (float(false_neg) + float(true_pos))
			Recall_neg = float(true_neg) / (float(false_pos) + float(true_neg))
			print "Recall_pos: " + str(Recall_pos)
			print "Recall_neg: " + str(Recall_neg)
			F1_pos = 2 * float(Precision_pos) * float(Recall_pos) / (float(Precision_pos) + float(Recall_pos))
			F1_neg = 2 * float(Precision_neg) * float(Recall_neg) / (float(Precision_neg) + float(Recall_neg))
			print "F1_pos: " + str(F1_pos)
			print "F1_neg: " + str(F1_neg)



	def train(self):
		"""Trains the Naive Bayes Sentiment Classifier."""
		IFileList = []
		for fFileObj in os.walk("reviews/"):
			IFileList = fFileObj[2]
			break
		for Fname in IFileList:
			if Fname[0] == 'm':
				#print Fname
				words = []
				words = self.tokenize(self.loadFile("reviews/"+Fname))
				for ele in words:
					Rrate = Fname.split("-")[1]
					#print Rrate
					if Rrate == "1": #negative review
						if ele not in self.neg.keys():
							self.neg[ele] = 1
						else:
							self.neg[ele] += 1
					elif Rrate == "5": #positive review
						if ele not in self.pos.keys():
							self.pos[ele] = 1
						else:
							self.pos[ele] += 1
		self.chi2filt()
		self.save(self.pos, 'pickled_pos')
		self.save(self.neg, 'pickled_neg')

	def chi2filt(self):
		"""Using chi-square test to determine the informative features"""
		# insert the tags/features that only exists in neg_dict into the pos_dict
		for feature in self.neg.keys():
			if feature not in self.pos.keys():
				self.pos[feature] = 0
		# insert the tags/features that only exists in the pos_dict into the neg_dict
		for feature in self.pos.keys():
			if feature not in self.neg.keys():
				self.neg[feature] = 0
		total = sum(self.pos.values() + self.neg.values())
		self.chi2score_pos = {}
		self.chi2score_neg = {}
		self.chi2score_total = {}
		for feature in self.pos.keys():
			expected_pos = ((float(self.pos[feature]) + float(self.neg[feature])) / float(total)) \
											* float(sum(self.pos.values()))
			expected_neg = ((float(self.pos[feature]) + float(self.neg[feature])) / float(total)) \
											* float(sum(self.neg.values()))
			observed_pos = float(self.pos[feature])
			observed_neg = float(self.neg[feature])
			DOF = len(self.pos.keys()) - 1  # degree of freedom for chi-square test
			self.chi2score_pos[feature] = (float(expected_pos - observed_pos))**2 / expected_pos
			self.chi2score_neg[feature] = (float(expected_neg - observed_neg))**2 / expected_neg
			self.chi2score_total[feature] = abs(self.chi2score_pos[feature] - self.chi2score_neg[feature])
		# sort the feature based on the total chi2score
		feature_list = []
		significance_list = []
		for key, value in sorted(self.chi2score_total, key = lambda (k,v) : (v,k)):
			feature_list.append(key)
			significance_list.append(value)
		print feature_list





	def classify(self, sText):
		"""Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """
		self.sum_pos = sum(self.pos.values())
		self.sum_neg = sum(self.neg.values())
		words = self.tokenize(sText)
		logP_pos = 0
		logP_neg = 0
		for ele in words:
			if ele in self.pos.keys():
				logP_pos += math.log((self.pos[ele]+1)/float(self.sum_pos))
			else:
				logP_pos += math.log(1/float(self.sum_pos))

			if ele in self.neg.keys():
				logP_neg += math.log((self.neg[ele]+1)/float(self.sum_neg))
			else:
				logP_neg += math.log(1/float(self.sum_neg))
		if logP_pos > logP_neg:
			return "positive"
		else:
			return "negative"



	def loadFile(self, sFilename):
		"""Given a file name, return the contents of the file as a string."""
		f = open(sFilename, "r")
		sTxt = f.read()
		f.close()
		return sTxt

	def save(self, dObj, sFilename):
		"""Given an object and a file name, write the object to the file using pickle."""

		f = open(sFilename, "w")
		p = pickle.Pickler(f)
		p.dump(dObj)
		f.close()

	def load(self, sFilename):
		"""Given a file name, load and return the object stored in the file."""

		f = open(sFilename, "r")
		u = pickle.Unpickler(f)
		dObj = u.load()
		f.close()
		return dObj

	def tokenize(self, sText):
		"""Given a string of text sText, returns a list of the individual tokens that
      occur in that string (in order)."""

		lTokens = []
		sToken = ""
		for c in sText:
			if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
				sToken += c
			else:
				if sToken != "":
					lTokens.append(sToken)
					sToken = ""
				if c.strip() != "":
					lTokens.append(str(c.strip()))

		if sToken != "":
			lTokens.append(sToken)

		return lTokens
