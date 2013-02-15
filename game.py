# ================================================================================
# PYTRIS
# Marcos Medeiros
# ================================================================================
import os
import sys
import pygame
from pieces import *
from random import randrange, seed
from board import *

class Game(object):
	def __init__(self, w=300, h=400):
		pygame.init()
		seed(None)

		self.ticks_factor = 10
		self.ticks = 0
		self.block_size = 20

		# cria o quadro
		self.board = Board(h // self.block_size, w // self.block_size)
		self.size = (400, h)
		# cria nossa janela
		self.screen = pygame.display.set_mode(self.size)
		self.board_surface = pygame.Surface((w, h))
		self.next_surface = pygame.Surface((self.block_size * 4, self.block_size * 3))
		self.hold_surface = pygame.Surface((self.block_size * 4, self.block_size * 3))


		self.bg_color = (0, 0, 0)
		self.fg_color = (255, 255, 255)
		self.shadow_color = (0, 100, 255)
		self.grid_color = (10, 30, 10)
		self.serial_color = 1

		self.hold_left = False
		self.hold_right = False
		self.hold_down = False
		self.hold_up = False
		self.do_harddrop = False

		self.font = pygame.font.SysFont('Comic Sans MS', 22)
		self.next_ren = self.font.render('Próxima', 1, self.fg_color)
		self.screen.blit(self.next_ren, (5,5))
		self.hold_ren = self.font.render('Reserva', 1, self.fg_color)
		self.screen.blit(self.hold_ren, (5,100))

		# cores dos blocos
		self.colors = [(0,0,0),
					   (255, 0, 0), (0, 255, 0), (0, 0, 255),
					   (255, 255, 0), (0, 255, 255), (255, 0, 255)]

		# cores dos blocos
		self.shad_factor = 0.4
		self.shad_colors = [(r * self.shad_factor, g * self.shad_factor, b * self.shad_factor) for (r,g,b) in self.colors]
		self.ishad_factor = 0.6
		self.ishad_colors = [(r * self.ishad_factor, g * self.ishad_factor, b * self.ishad_factor) for (r,g,b) in self.colors]

		self.current = self.getRandomPiece()
		self.next = self.getRandomPiece()
		self.hold = None
		self.pos = self.initPos()
		self.holded = False
		self.harddrop = False

	def initPos(self):
		return [0, self.board.columns // 2]

	def spawnPiece(self):
		self.current = self.next
		self.pos = self.initPos()
		self.next = self.getRandomPiece()
		self.holded = False

	def hardDrop(self):
		y = self.board.linesToDrop(self.current, self.pos)
		self.pos[0] = y
		self.harddrop = True


	def handleEvents(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(1)
			elif event.type == pygame.KEYDOWN:
				if event.key ==  pygame.K_RIGHT:
					self.hold_right = True
				elif event.key == pygame.K_LEFT:
					self.hold_left = True
				elif event.key == pygame.K_DOWN:
					self.hold_down = True
				elif event.key == pygame.K_UP:
					self.hold_up = True
				elif event.key == pygame.K_z:
					self.rotateLeft()
				elif event.key == pygame.K_x:
					self.rotateRight()
				elif event.key == pygame.K_c:
					self.holdPiece()
				elif event.key == pygame.K_SPACE:
					self.hardDrop()

				elif event.key == pygame.K_ESCAPE:
					sys.exit(1)
			elif event.type == pygame.KEYUP:
				if event.key ==  pygame.K_RIGHT:
					self.hold_right = False
				elif event.key == pygame.K_LEFT:
					self.hold_left = False
				elif event.key == pygame.K_DOWN:
					self.hold_down = False
				elif event.key == pygame.K_UP:
					self.hold_up = False

	def holdPiece(self):
		if self.holded:
			return False
		if self.hold:
			self.current.pos = 0
			self.hold, self.current = self.current, self.hold
			self.pos = self.initPos()
		else:
			self.hold = self.current
			self.spawnPiece()
		self.holded = True
		return True

	def run(self):
		while True:
			self.handleEvents()
			if self.hold_left:
				self.moveLeft()
			if self.hold_right:
				self.moveRight()
			if self.hold_down:
				self.moveDown()
			if self.hold_up:
				self.moveUp()

			if self.harddrop:
				self.board.insert(self.current, self.pos)
				self.spawnPiece()
				self.harddrop = False
			else:
				self.ticks += 1
				if self.ticks >= self.ticks_factor:
					if self.board.collide(self.current, self.pos):
						self.board.insert(self.current, self.pos)
						self.spawnPiece()
					self.moveDown()
					self.ticks = 0
				
			self.drawGame()
			if self.isGameOver():
				self.board.clear()
			l = self.board.getCompleteLines()
			for i in l:
				self.board.clearLine(i)

			pygame.display.flip()
			pygame.time.wait(50)

	def moveRight(self):
		if not self.current:
			return False
		if self.board.hcollide(self.current, self.pos) != 2:
			self.pos[1] += 1

	def moveLeft(self):
		if not self.current:
			return False
		if self.board.hcollide(self.current, self.pos) != 1:
			self.pos[1] -= 1

	def moveDown(self):
		if not self.current:
			return False
		if not self.board.collide(self.current, self.pos):
			self.pos[0] += 1

	def moveUp(self):
		if not self.current:
			return False
		if not self.board.up_collide(self.current, self.pos):
			self.pos[0] -= 1

	def rotateLeft(self):
		self.current.rotate_left()
		if self.board.anycollide(self.current, self.pos):
			self.current.rotate_right()

	def rotateRight(self):
		self.current.rotate_right()
		if self.board.anycollide(self.current, self.pos):
			self.current.rotate_left()

	# recebe uma peça aleatória
	# O aleatório aqui não é dos melhores
	def getRandomPiece(self):
		piece = randrange(0, 7919) % 29 % 7

		if not piece:
			piece = Piece_Square()
		elif piece == 1:
			piece = Piece_L()
		elif piece == 2:
			piece = Piece_S()
		elif piece == 3:
			piece = Piece_T()
		elif piece == 4:
			piece = Piece_Line()
		elif piece == 5:
			piece = Piece_InvL()
		elif piece == 6:
			piece = Piece_InvS()
		if self.serial_color >= len(self.colors):
			self.serial_color = 1
		piece.color = self.serial_color
		self.serial_color += 1
		return piece

	# Verfica se o jogo acabou
	def isGameOver(self):
		for x in range(self.board.columns):
			if self.board.matrix[0][x]:
				return True
		return False

	def drawGrid(self, surface=None):
		if not surface:
			surface = self.screen
		for x in range(0, self.size[0], self.block_size):
			pygame.draw.line(surface, self.grid_color, (x, 0), (x, self.size[1]))
		for y in range(0, self.size[1], self.block_size):
			pygame.draw.line(surface, self.grid_color, (0, y), (self.size[0], y))

	def drawPiece(self, surface=None, piece=None, at=None):
		if not at:
			at = self.pos
		if not surface:
			surface = self.screen
		if not piece:
			piece = self.current

		for y, x in piece.points:
			outrect = pygame.Rect((x + at[1]) * self.block_size, (y + at[0]) * self.block_size,
				self.block_size, self.block_size)
			innerrect = pygame.Rect((x + at[1]) * self.block_size + 1,
						(y + at[0]) * self.block_size + 1,
						self.block_size - 1,
						self.block_size - 1)
			rect = pygame.Rect((x + at[1]) * self.block_size + 2,
						(y + at[0]) * self.block_size + 2,
						self.block_size - 2,
						self.block_size - 2)
			pygame.draw.rect(surface, self.colors[piece.color], rect)
			pygame.draw.rect(surface, self.shad_colors[piece.color], outrect, 1)
			pygame.draw.rect(surface, self.ishad_colors[piece.color], innerrect, 1)

	def drawShadow(self, surface=None):
		if not surface:
			surface = self.screen
		y2 = self.board.linesToDrop(self.current, self.pos)

		py, px = y2, self.pos[1]
		for y, x in self.current.points:
			outrect = pygame.Rect((x + px) * self.block_size, (y + py) * self.block_size,
				self.block_size, self.block_size)
			pygame.draw.rect(surface, self.shadow_color, outrect, 1)

	def drawBoard(self, surface=None):
		if not surface:
			surface = self.screen
		for i in range(self.board.rows):
			for j in range(self.board.columns):
				if self.board.matrix[i][j]:
					k = self.board.matrix[i][j]
					innerrect = pygame.Rect(j * self.block_size + 1,
						i * self.block_size + 1,
						self.block_size - 1,
						self.block_size - 1)
					outrect = pygame.Rect(j * self.block_size, i * self.block_size, self.block_size, self.block_size)
					rect = pygame.Rect(j * self.block_size + 2,
						i * self.block_size + 2,
						self.block_size - 2,
						self.block_size - 2)

					pygame.draw.rect(surface, self.colors[k], rect)
					pygame.draw.rect(surface, self.ishad_colors[k], innerrect, 1)
					pygame.draw.rect(surface, self.shad_colors[k], outrect, 1)

	# desenha o jogo
	def drawGame(self):
		self.board_surface.fill(self.bg_color)
		self.drawGrid(self.board_surface)
		self.drawBoard(self.board_surface)
		self.drawPiece(self.board_surface)
		self.drawShadow(self.board_surface)
		self.next_surface.fill(self.bg_color)
		self.drawPiece(self.next_surface, self.next, (0,0))
		self.hold_surface.fill(self.bg_color)
		if self.hold:
			self.drawPiece(self.hold_surface, self.hold, (0,0))
		self.screen.blit(self.next_surface, (10,40))
		self.screen.blit(self.hold_surface, (10,140))
		self.screen.blit(self.board_surface, (100,0))

def main():
	game = Game()
	game.run()

if __name__ == '__main__':
	main()
