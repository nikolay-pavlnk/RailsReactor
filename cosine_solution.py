from PIL import Image, ImageStat 
import numpy as np
import os
import sys


def handle_commands(commands):
	"""
	The function handle user's commands.

	input: commands - list. The list contains commands which user typed in console.
	"""

	usage = 'usage: {0} [-h] --path PATH'
	error = '\n{0}: error: the following arguments are required: --path'

	try:
		if len(commands) == 2:
			if commands[1] in ['--help', '-h']:
				print(usage.format(commands[0]))
		
		elif len(commands) == 3:
			if commands[1] == '--path':
				obj = BaseModel(commands[2])
				similar_pic = obj.get_similar_images()
		
				for key in similar_pic:
					print(key, similar_pic[key])
		else:
			print(usage.format(commands[0]) + error.format(commands[0]))
	except FileNotFoundError:
		print('There are no such folder name')


class BaseModel:
	def __init__(self, path, threshold=0.98):
		self.threshold = 0.98
		self.path = path + '/'
		self.file_names = os.listdir(path) 
        
        
	def get_vectorized_image(self, image_path, size=(4,4)):
		"""
		input: image_path - string,
				size - tuple(int, int)

		output: np.array - [int..int]
		"""
		
		image = Image.open(image_path).resize(size, Image.LANCZOS).convert(mode="L")
		mean = ImageStat.Stat(image).mean[0]
		img = np.array(image.getdata())
		    
		indexes_bigger = np.where(mean >= img)[0]
		indexes_less = np.where(mean < img)[0]
	    
		img[indexes_bigger] = 1
		img[indexes_less] = 0
	    
		return img
    
	def cosine_distance(self, X, Y):
		return np.dot(X, Y) / np.linalg.norm(X) / np.linalg.norm(Y)
    
	def get_similar_images(self):
		similar_img = {}
		"""
		This method is based on cosine similarity. The pictures which have high value of cosine similarity
		are similar.

		output: similar_img - dictionary
		"""
	    
		for image in self.file_names:
			file_names_cutted = self.file_names.copy()
			file_names_cutted.remove(image)

			row = [self.cosine_distance(self.get_vectorized_image(self.path + image), 
	                                 self.get_vectorized_image(self.path + image_temp))
	                                 for image_temp in file_names_cutted]
			max_value = np.max(row)
	        
			if max_value > self.threshold:
	            
				if row.count(max_value) > 1:
	                
					for index in np.where(row == max_value)[0]:
						if image not in similar_img.values():

							if image in similar_img.keys():
								similar_img[similar_img[image]] = image

						similar_img[image] = file_names_cutted[index]
	                    
				if image not in similar_img.values():
					similar_img[image] = file_names_cutted[np.argmax(row)] 
	                
		return similar_img


if __name__ == '__main__':
	handle_commands(sys.argv)