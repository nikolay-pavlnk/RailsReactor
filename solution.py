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
	def __init__(self, path):
		self.path = path + '/'
		self.file_names = os.listdir(path) 
        
        
	def hash_image(self, image_path, size=(4,4)):
		"""
		input: image_path - string,
				size - tuple(int, int)

		output: hash - int
		"""
		
		image = Image.open(image_path).resize(size, Image.LANCZOS).convert(mode="L")
		mean = ImageStat.Stat(image).mean[0]
		return sum((1 if p > mean else 0) << i for i, p in enumerate(image.getdata()))
    
    
	def get_similar_images(self):
		similar_img = {}
		"""
		This method is based on assumption that pictures with the same hash are similar.

		output: similar_img - dictionary
		"""
	        
		for image in self.file_names:
			file_names_cutted = self.file_names.copy()
			file_names_cutted.remove(image)

			row = [self.hash_image(self.path + image_temp) for image_temp in file_names_cutted]

			suspected_hash = self.hash_image(self.path + image)

			if suspected_hash in row:
				if row.count(suspected_hash) > 1:

					for index in np.where(np.array(row) == suspected_hash)[0]:
						suspected_name = file_names_cutted[index]

						if image not in similar_img.values():

							if image in similar_img.keys():
								similar_img[similar_img[image]] = image

							similar_img[image] = suspected_name

				else:
					suspected_name = file_names_cutted[row.index(suspected_hash)]

					if image not in similar_img.values():
						similar_img[image] = suspected_name

		return similar_img


if __name__ == '__main__':
	handle_commands(sys.argv)