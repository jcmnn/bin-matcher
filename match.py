

class Matcher:
	def __init__(self, bin):
		self.bin = bin
		pass

	def match(self, patterns):
		if len(patterns) == 0:
			return

		def search_next(pattern, bin):
			if len(pattern) == 0:
				return
			pattern_idx = 0
			pattern_char = pattern[0]
			for offset, c in enumerate(bin):
				if pattern_char == c:
					pattern_idx += 1
					if pattern_idx == len(pattern):
						return offset + 1
					pattern_char = pattern[pattern_idx]
				else:
					pattern_idx = 0

		curr_bin = self.bin

		for pattern in patterns:
			offset = search_next(pattern, curr_bin)
			if offset == None:
				print("Failed to find pattern")
				return