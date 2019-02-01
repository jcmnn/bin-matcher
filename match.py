from enum import Enum
import struct

class PatternType(Enum):
	BYTES = 1
	ANY = 2


class PatternKey(Enum):
	SKIP_NEXT = 9000
	SKIP_MATCHES = 9001


class Pattern:
	def __init__(self, *args):
		self.patterns = []
		self.debug = False
		self.skip_matches = 0

		skip_next = False
		skip_matches_next = False

		for arg in args:
			if arg == PatternKey.SKIP_NEXT:
				skip_next = True
				continue
			if arg == PatternKey.SKIP_MATCHES:
				skip_matches_next = True
				continue
			elif arg == False:
				self.debug = True
			elif isinstance(arg, int):
				if skip_matches_next:
					self.skip_matches = arg
				else:
					self.patterns.append((PatternType.ANY, arg, not skip_next))
			elif isinstance(arg, bytes):
				self.patterns.append((PatternType.BYTES, arg, not skip_next))
			else:
				raise TypeError("Expected 'bytes' or 'int'")
			skip_next = False
			skip_matches_next = False


	def search(self, bin):
		data = bytearray()
		iter = enumerate(bin)
		matches_to_do = self.skip_matches
		for (offset, x) in iter:
			start_offset = offset
			data = bytearray()
			failed = False
			successes = 0
			for (ptype, arg, arg2) in self.patterns:
				if ptype == PatternType.BYTES:
					if arg != bin[offset:offset + len(arg)]:
						if successes >= 1 and self.debug:
							print(bin[offset:offset + len(arg)])
						failed = True
						break
					else:
						if self.debug:
							print(hex(offset))
						[next(iter) for x in range(len(arg) - 1)]
						
				elif ptype == PatternType.ANY:
					if (arg > len(bin) - offset):
						failed = True
						break
					if arg2:
						data.append(x)
					if self.debug:
						print(arg)
					for n in range(arg - 1):
						if arg2:
							data.append(next(iter)[1])
						else:
							next(iter)
				try:
					offset, x = next(iter)
				except StopIteration:
					pass
				successes = successes + 1

			if not failed:
				if matches_to_do == 0:
					return (start_offset, data)
				else:
					matches_to_do = matches_to_do - 1
		return None


