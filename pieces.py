# ================================================================================
# TETRIS CLONE
# Marcos Medeiros
# ================================================================================
from random import randrange

# ================================================================================
# Nosso classe que representa uma peça
# ================================================================================
class Piece(object):
	def __init__(self):
		self.pos = 0
		self.points = []
		self.color = 0

	def rotate_left(self):
		if not self.pos:
			self.pos = 3
		else:
			self.pos = self.pos - 1
		self.points = self.forms[self.pos]

	def rotate_right(self):
		if self.pos < 3:
			self.pos = self.pos + 1
		else:
			self.pos = 0
		self.points = self.forms[self.pos]

# ================================================================================
# Bloco em forma de L
# ================================================================================
class Piece_L(Piece):
	def __init__(self):
		self.pos = 0
		self.color = 0
		self.forms = [[(0,0), (1,0), (1,1), (1,2)],
					  [(0,1), (0,2), (1,1), (2,1)],
					  [(2,2), (1,0), (1,1), (1,2)],
					  [(0,1), (2,0), (1,1), (2,1)]]
		self.points = self.forms[self.pos]

# ================================================================================
# Bloco em forma de L invertido
# ================================================================================
class Piece_InvL(Piece):
	def __init__(self):
		self.pos = 0
		self.color = 0
		self.forms = [[(0,2), (1,0), (1,1), (1,2)],
					  [(0,0), (2,1), (1,0), (2,0)],
					  [(0,0), (0,1), (0,2), (1,0)],
					  [(0,1), (1,1), (2,1), (0,0)]]
		self.points = self.forms[self.pos]

# ================================================================================
# Bloco em forma de quadrado
# ================================================================================
class Piece_Square(Piece):
	def __init__(self):
		self.color = 0
		self.pos = 0
		self.forms = [[(0,0), (0,1), (1,0), (1,1)],
					  [(0,0), (0,1), (1,0), (1,1)],
					  [(0,0), (0,1), (1,0), (1,1)],
					  [(0,0), (0,1), (1,0), (1,1)]]
		self.points = self.forms[self.pos]

# ================================================================================
# Bloco em forma de linha
# ================================================================================
class Piece_Line(Piece):
	def __init__(self):
		self.color = 0
		self.pos = 0
		self.forms = [[(0,0), (0,1), (0,2), (0,3)],
					  [(0,0), (1,0), (2,0), (3,0)],
					  [(0,0), (0,1), (0,2), (0,3)],
					  [(0,0), (1,0), (2,0), (3,0)]]
		self.points = self.forms[self.pos]

# ================================================================================
# Bloco em forma de S
# ================================================================================
class Piece_S(Piece):
	def __init__(self):
		self.color = 0
		self.pos = 0
		self.forms = [[(1,0), (1,1), (0,1), (0,2)],
					  [(0,0), (1,0), (1,1), (2,1)],
					  [(1,0), (1,1), (0,1), (0,2)],
					  [(0,0), (1,0), (1,1), (2,1)]]
		self.points = self.forms[self.pos]

# ================================================================================
# Bloco em forma de S invertido
# ================================================================================
class Piece_InvS(Piece):
	def __init__(self):
		self.color = 0
		self.pos = 0
		self.forms = [[(0,0), (0,1), (1,1), (1,2)],
					  [(0,1), (1,1), (1,0), (2,0)],
					  [(0,0), (0,1), (1,1), (1,2)],
					  [(0,1), (1,1), (1,0), (2,0)]]
		self.points = self.forms[self.pos]

# ================================================================================
# Bloco em forma de T
# ================================================================================
class Piece_T(Piece):
	def __init__(self):
		self.color = 0
		self.pos = 0
		self.forms = [[(1,0), (1,1), (1,2), (0,1)],
					  [(0,0), (1,0), (2,0), (1,1)],
					  [(0,0), (0,1), (0,2), (1,1)],
					  [(1,0), (0,1), (1,1), (2,1)]]
		self.points = self.forms[self.pos]
