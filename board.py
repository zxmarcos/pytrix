# ================================================================================
# TETRIS CLONE
# Marcos Medeiros
# ================================================================================
from pieces import *

# ================================================================================
# Nosso 'tabuleiro'
# ================================================================================
class Board(object):
	def __init__(self, row=4, columns=4):
		self.rows = row
		self.columns = columns
		self.matrix = [[0 for i in range(columns)] for x in range(row)]

	def check(self, piece, at):
		# verfica se realmente é uma peça
		if not isinstance(piece, Piece):
			return False
		(y, x) = at
		for i, j in piece.points:
			# só verificamos a checagem se está dentro dos limites do tabuleiro
			if y + i < self.rows and x + j < self.columns:
				if self.matrix[y +  i][x + j] > 0:
					return False
			else:
				return False
		return True

	def clear(self):
		for y in range(self.rows):
			for x in range(self.columns):
				self.matrix[y][x] = 0

	# Insere o bloco no tabuleiro
	def insert(self, piece, at):
		# verfica se realmente é uma peça
		if not isinstance(piece, Piece):
			return False
		if 1:#self.check(piece, at):
			(y, x) = at
			for i, j in piece.points:
				self.matrix[y +  i][x + j] = piece.color
			return True
		else:
			return False

	def linesToDrop(self, piece, at):
		y, x = at
		while not self.collide(piece, (y, x)):
			y += 1
		return y

	def clearLine(self, line):
		for y in range(line, 1, -1):
			if y > 0:
				self.matrix[y] = self.matrix[y - 1]
		self.matrix[0] = [0 for i in range(self.columns)]


	def getCompleteLines(self):
		complete = []
		for y, line in enumerate(self.matrix):
			line_clear = True	
			for x in line:
				if not x:
					line_clear = False
					break
			if line_clear:
				complete.append(y)
		return complete

	def collide(self, piece, at):
		(y, x) = at
		for py, px in piece.points:
			y2 = y + py + 1
			# se chegamos a linha máxima, então encaixamos
			if (x + px) > self.columns:
				return True
			if y2 >= self.rows:
				return True
			if self.matrix[y2][x + px]:
				return True
		return False

	def up_collide(self, piece, at):
		(y, x) = at
		for py, px in piece.points:
			y2 = y + py - 1
			if y2 < 0:
				return True
			# se chegamos a linha máxima, então encaixamos
			if y2 >= self.rows:
				return True
			if self.matrix[y2][x + px]:
				return True
		return False

	# 1 - colisão na esquerda, 2 na direita
	def hcollide(self, piece, at):
		(y, x) = at
		for py, px in piece.points:
			if (x + px) == 0:
				return 1
			if (x + px + 1) >= self.columns:
				return 2
			if self.matrix[y + py][x + px - 1]:
				return 1
			if self.matrix[y + py][x + px + 1]:
				return 2
		return False

	def anycollide(self, piece, at):
		if self.hcollide(piece, at) or self.up_collide(piece, at):
			return True
		return False

	def show(self):
		'''Mostra a situacao atual do tabuleiro'''
		for i in range(self.rows):
			for j in range(self.columns):
				print(self.matrix[i][j], end=' ')
			print(end='\n')