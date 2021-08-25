import pygame, random, pygame.gfxdraw, cv2, time
import numpy as np
from PIL import Image
from shapely.geometry import Polygon
from shapely.ops import cascaded_union
import geopandas as gpd


class Shape(object):
	def __init__(self, contour):
		self.contour = contour # [[x1, y1], ..., [xn, yn]]
		self.x, self.y = self.find_centroid()
		self.color = pygame.Color(0,0,0)
		self.alpha = 100
		self.hue = 360*random.random()
		self.color.hsla = (self.hue, 70, 70, self.alpha)
	def find_centroid(self):
		''' 
		find the centroid (center of mass) of contour, source https://www.pyimagesearch.com/2016/02/01/opencv-center-of-contour/
		'''
		M = cv2.moments(np.array(self.contour)[:, None, :])
		cX = int(M['m10'] / M['m00'])
		cY = int(M['m01'] / M['m00'])
		return cX, cY
	def moveto(self, newx, newy):
		''' 
		translate every point on contour and reset its centroid
		'''
		newcontour =  [(x - self.x + newx, y - self.y + newy) for x, y in self.contour]
		self.contour = newcontour
		self.x, self.y = newx, newy
		return self
	def enlarge(self, scale=1.0):
		cnt = np.array(self.contour)[:, None, :]
		cnt_norm = cnt - [self.x, self.y]
		cnt_scaled = (cnt_norm * scale + [self.x, self.y]).astype(np.int32)
		self.contour = cnt_scaled[:, 0, :].tolist()
		return self
	def rotate(self, angle):
		''' rotate every point on contour clockwise wrt centroid, radians angle '''
		self.contour = [self.rotate_helper(self.x, self.y, x, y, angle) for x,y in self.contour]
		return self
	def rotate_helper(self, originx, originy, x, y, angle):
		rotatedx = originx + np.cos(angle) * (x - originx) - np.sin(angle) * (y - originy)
		rotatedy = originy + np.sin(angle) * (x - originx) + np.cos(angle) * (y - originy)
		return int(rotatedx), int(rotatedy)
	def draw(self, canvas):
		''' render the shape on a pygame display (canvas) using contour '''
		pygame.gfxdraw.filled_polygon(canvas, self.contour, self.color)



def main(original_shape, added_area, change=True, video_name='test'):

	SCREEN_WIDTH = 1200
	SCREEN_HEIGHT = 500
	CURTAIN_WIDTH = 300
	CURTAIN_HEIGHT = 510
	ONEWAY_PADDING = 130 # change moving direction when distance to screen edge is this length
	FPS = 60
	OBJECT_SPEED = 2.8
	CURTAIN_SPEED = 2.8
	MAX_T = 40000000000 # max video duration
	CURTAIN_DOWN_T = 1000000000 # curtain start to move
	PYGAME_T = 16666667 # duration of each cycle update

	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # returns a Surface (rectangle)
	clock=pygame.time.Clock()

	# initialize object after change
	changed_contour = np.dstack(gpd.GeoSeries(cascaded_union([Polygon(original_shape.contour), Polygon(added_area.contour)]))[0].boundary.coords.xy).squeeze().astype(dtype=np.int32).tolist()
	print('changed contour', changed_contour)
	changed_shape = Shape(changed_contour)
	changed_shape.color, changed_shape.color.hsla = original_shape.color, original_shape.color.hsla
	x_correction, y_correction = changed_shape.x - original_shape.x, changed_shape.y - original_shape.y 
	original_shape.moveto(ONEWAY_PADDING, SCREEN_HEIGHT/2) # place original shape at initial position

	# initialize curtain
	curtain = pygame.Surface((CURTAIN_WIDTH, CURTAIN_HEIGHT)) # size
	curtain.fill((68, 68, 68)) # fill in gray
	rect = curtain.get_rect() # make the surface a rectangle
	curtain_center = ((SCREEN_WIDTH - curtain.get_width())/2, -300) # (xmiddle, ytop)


	# prepare running loop variables
	running = True
	initial_t = time.time_ns()
	current_t = initial_t
	video_content = []
	do_change = True
	cur_shape = original_shape
	last_change_t = None
	
	# run until time out
	while current_t - initial_t <= MAX_T: 

		for event in pygame.event.get(): # quit if user clicked the quit window button
			if event.type == pygame.QUIT:
				running = False
		
		# add frame to output list
		pixel = pygame.image.tostring(screen, "RGB")
		video_content.append(pixel)

		# screen background, white 255x3, black 0x3
		screen.fill((255,255,255))

		if (CURTAIN_DOWN_T <= current_t  - initial_t) and (curtain_center[1] < (SCREEN_HEIGHT - CURTAIN_HEIGHT)/2): # curtain start to move
			curtain_center = (curtain_center[0], curtain_center[1] + CURTAIN_SPEED)

		if cur_shape.x < ONEWAY_PADDING or cur_shape.x > SCREEN_WIDTH - ONEWAY_PADDING: # turn around moving direction
			OBJECT_SPEED = -1 * OBJECT_SPEED

		if (change) and (SCREEN_WIDTH/2 <= cur_shape.x < SCREEN_WIDTH/2 + abs(OBJECT_SPEED)) and (last_change_t==None or current_t-last_change_t>=20*PYGAME_T): # change shape
			if do_change: # time to use changed shape
				changed_shape.moveto(original_shape.x + x_correction, original_shape.y + y_correction)
				cur_shape = changed_shape
				do_change = False
			else: # time to use original shape
				cur_shape = original_shape
				do_change = True
			last_change_t = current_t

		if curtain_center[1] >= (SCREEN_HEIGHT - CURTAIN_HEIGHT)/2: # shape start moving after curtain down
			cur_shape.moveto(cur_shape.x + OBJECT_SPEED, cur_shape.y) # move in x direction

		
		# render and update cycle
		cur_shape.draw(screen)
		screen.blit(curtain, curtain_center)
		pygame.display.update()
		current_t += PYGAME_T 


	# write to video
	codec = fourcc = cv2.VideoWriter_fourcc(*'H264')
	out = cv2.VideoWriter(video_name+'.mp4', codec, FPS, (SCREEN_WIDTH, SCREEN_HEIGHT))
	video_content.pop(0)
	for i in video_content:
		image = Image.frombytes("RGB",(SCREEN_WIDTH, SCREEN_HEIGHT), i, "raw")
		frame = np.array(image)
		temp = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
		out.write(temp)


	# Done! Time to quit.
	pygame.quit()
	out.release()







if __name__ == '__main__':

	# A ------------------------------------------
	# original_shape = Shape([[527, 367], [651, 249], [691, 159], [483, 157], [617, 219], [545, 287]]) # A original
	# added_area = Shape([[617, 219], [545, 287], [587, 205]]) # A concave small
	# added_area = Shape([[617, 219], [570, 263], [570, 197]]) # A concave large
	# added_area = Shape([[617, 219], [545, 287], [587, 205]]).rotate(0.8).moveto(610, 150) # A convex small
	# added_area = Shape([[617, 219], [570, 263], [570, 197]]).rotate(0.75).moveto(663, 143) # A convex large
	

	# B ------------------------------------------
	# original_shape = Shape([[551, 300], [605, 288], [657, 174], [519, 50], [493, 150], [531, 136], [609, 194], [563, 264]]) # B original
	# added_area = Shape([[531, 136], [609, 194], [593, 217]]) # B concave small
	# added_area = Shape([[554, 153], [609, 194], [579, 240]]) # B concave large
	# added_area = Shape([[531, 136], [609, 194], [593, 217]]).rotate(-0.19).moveto(615, 125) # B convex small
	# added_area = Shape([[554, 153], [609, 194], [579, 240]]).rotate(-0.55).moveto(635, 137) # B convex large


	# C ------------------------------------------
	original_shape = Shape([[684, 333], [626, 155], [500, 157], [604, 195], [590, 231], [570, 261], [594, 317], [634, 339]]) # C original
	added_area = Shape([[556, 177], [604, 195], [584, 250]]) # C concave large
	added_area = Shape([[556, 177], [604, 195], [584, 250]]).rotate(2.8).moveto(594, 137) # C convex large



	# run
	main(original_shape, added_area, change=False, video_name='C_nochange_4')