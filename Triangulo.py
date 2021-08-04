import pygame, sys, math
import pygame.freetype
from pygame.locals import *

#------------ Setup --------------#
pygame.init()
pygame.display.set_caption("Triangulos")
screen = pygame.display.set_mode((800,800),0,32)
font = pygame.freetype.SysFont("Arial",30)
#---------------------------------#

#------------ Classes ------------#
class Triangle():
	def __init__(self,p1,p2,p3):
		self.p1 = {"pos":pygame.Rect(p1[0],p1[1],15,15),"color":(255,255,255)}
		self.p2 = {"pos":pygame.Rect(p2[0],p2[1],15,15),"color":(255,255,255)}
		self.p3 = {"pos":pygame.Rect(p3[0],p3[1],15,15),"color":(255,255,255)}
		self.biz = [self.p2['pos'][0]+514,self.p2['pos'][1]-500]
		self.points = [self.p1,self.p2,self.p3]

	def draw(self,screen):
		pygame.draw.line(screen, (255,255,255), self.p1['pos'].center,self.p2['pos'].center,2)
		pygame.draw.line(screen, (255,255,255), self.p2['pos'].center,self.p3['pos'].center,2)
		pygame.draw.line(screen, (255,255,255), self.p3['pos'].center,self.p1['pos'].center,2)
		pygame.draw.ellipse(screen,(self.p1['color']), self.p1['pos'])
		pygame.draw.ellipse(screen,(self.p2['color']), self.p2['pos'])
		pygame.draw.ellipse(screen,(self.p3['color']), self.p3['pos'])

	def update(self, x, y, point):
		if point == self.p2:
			self.p1['pos'].x += x - self.p2['pos'].x
			self.p1['pos'].y += y - self.p2['pos'].y
			self.p3['pos'].x += x - self.p2['pos'].x
			self.p3['pos'].y += y - self.p2['pos'].y
			self.p2['pos'].x += x - self.p2['pos'].x
			self.p2['pos'].y += y - self.p2['pos'].y
			self.p2['color'] = (0,0,255)
		elif point == self.p1:
			self.p1['pos'].y = y
			self.p1['color'] = (0,0,255)
		else:
			self.p3['pos'].x = x
			self.p3['color'] = (0,0,255)

	def getP(self,p):
		return self.points[p-1]['pos'].center
#---------------------------------#

triangle = Triangle([70,70],[70,720],[720,720])
clicking = False
drawing = False
drawStartPos = []
drawEndPos = []
point = None

while True:
	mx, my = pygame.mouse.get_pos()

	if pygame.mouse.get_pressed(num_buttons=3)[2]:
		drawEndPos = [mx,my]

	for p in triangle.points:
		p['color'] = (255,255,255)
	if clicking:
		triangle.update(mx,my, point)

	triangle.draw(screen)

	if drawing:
		pygame.draw.line(screen,(255,0,0), drawStartPos, drawEndPos)
		font.render_to(screen,(drawEndPos[0]+20,drawEndPos[1]),"{:.2f}cm".format(medida),(255,255,255))

	co = abs((triangle.getP(2)[1]-triangle.getP(1)[1])/44.6735395189)
	ca = abs((triangle.getP(3)[0]-triangle.getP(2)[0])/44.6735395189)
	hypot = math.sqrt((co**2)+(ca**2))
	m = (co**2)/hypot
	n = (ca**2)/hypot
	h = math.sqrt(m*n)
	try:
		medida = math.sqrt(((drawEndPos[0]-drawStartPos[0])/44.6735395189)**2+((drawEndPos[1]-drawStartPos[1])/44.6735395189)**2)
	except:
		medida = 0

	co_txt = "cateto oposto: {:.2f} cm".format(co)
	ca_txt = "cateto adjacente: {:.2f} cm".format(ca)
	hypot_txt = "hipotenusa: {:.2f} cm".format(hypot)
	m_txt = "m: {:.2f} cm".format(m)
	n_txt = "n: {:.2f} cm".format(n)
	h_txt = "h: {:.2f} cm".format(h)

	font.render_to(screen,(500,20),ca_txt,(255,255,255))
	font.render_to(screen,(500,70),co_txt,(255,255,255))
	font.render_to(screen,(500,120),hypot_txt,(255,255,255))
	font.render_to(screen,(500,170),m_txt,(255,255,255))
	font.render_to(screen,(500,220),n_txt,(255,255,255))
	font.render_to(screen,(500,270),h_txt,(255,255,255))


	for e in pygame.event.get():
		if e.type == QUIT:
			pygame.quit()
			sys.exit()
		if e.type == MOUSEBUTTONDOWN:
			for p in triangle.points:
				if e.button == 1 and p['pos'].collidepoint(mx,my):
					clicking = True
					point = p
			if e.button == 3:
				drawing = True
				drawStartPos = [mx,my]
			if e.button == 2:
				drawing = False
		if e.type == MOUSEBUTTONUP:
			if e.button == 1:
				clicking = False
				point = None
	pygame.display.update()
	screen.fill((0,0,0))
