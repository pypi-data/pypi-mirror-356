from fuzzywuzzy import fuzz

class profanityfilter:
	def __init__(self, profanities, threshold=70):
		self.profanities = profanities
		self.threshold = threshold
	def boolscan(self, query):
		for profanity in self.profanities:
			self.rating = fuzz.partial_ratio(query, profanity)
			if self.rating >= self.threshold:
				return True
		return False
	def percentscan(self, query):
		highrate = 0
		for profanity in self.profanities:
			if (rating := fuzz.partial_ratio(query, profanity)) > highrate:
				highrate = rating
	def fillerscan(self, query, filler):
		for word in range(len((splquer := query.split(' ')))):
			for profanity in self.profanities:
				rating = fuzz.ratio(splquer[word], profanity)
				if rating >= self.threshold:
					splquer[word] = filler
		return ' '.join(splquer)
