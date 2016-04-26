from PIL import Image
import binascii
from .ipsnr import IPSNR
import math

class NLSB(IPSNR):
	def rgb2hex(self, r, g, b):
		return '#{:02x}{:02x}{:02x}'.format(r, g, b)

	def hex2rgb(self, hexcode):
		# return tuple(map(ord, hexcode[1:].decode('hex')))
		return (int(hexcode[1:3], 16), int(hexcode[3:5], 16), int(hexcode[5:7], 16))

	def str2bin(self, message):
		binary = bin(int(binascii.hexlify(bytes(message, 'UTF-8')), 16))
		return binary[2:]

	def bin2str(self, binary):
		message = binascii.unhexlify('%x' % (int('0b'+binary, 2)))
		return message

	def encode(self, hexcode, digit):
		if hexcode[-1] in ('0', '1', '2', '3', '4', '5'):
			hexcode = hexcode[:-1] + digit
			return hexcode
		else:
			return None

	def decode(self, hexcode):
		if hexcode[-1] in ('0', '1'):
			return hexcode[-1]
		else:
			return None

	def embed_msg(self, filename, message):
		img = Image.open(filename)

		binary = self.str2bin(message) + '1111111111111110'

		if img.mode in ('RGBA'):
			img = img.convert('RGBA')
			datas = img.getdata()

			newData = []
			digit = 0

			for item in datas:
				if digit < len(binary):
					newpix = self.encode(self.rgb2hex(item[0], item[1], item[2]), binary[digit])
					# print(newpix)
					if newpix == None:
						newData.append(item)
					else:
						r, g, b = self.hex2rgb(newpix)
						newData.append((r, g, b, 255))
						digit += 1
				else:
					newData.append(item) 

			img.putdata(newData)
			img.save(filename, "PNG")

			return True # completed
		return False # incorrect image mode, couldn't hide

	def extract_msg(self, filename):
		img = Image.open(filename)
		binary = ""

		if img.mode in ('RGBA'):
			img = img.convert('RGBA')
			datas = img.getdata()

			for item in datas:
				digit = self.decode(self.rgb2hex(item[0], item[1], item[2]))

				if digit == None:
					pass
				else:
					binary += digit
					if binary[-16:] == '1111111111111110':
						return self.bin2str(binary[:-16]) # success

			return self.bin2str(binary)

		return False # incorrect image mode, couldn't retrieve

	def count_MSE(self, original_img, stego_img):
		img 	= Image.open(original_img)
		stega	= Image.open(stego_img)

		img 	= img.getdata()
		stega	= stega.getdata()

		MSE 	= 0

		width, height = img.size

		len_img = len(img)
		for i in range(len_img):
			img_pix		= (img[i][0] + img[i][1] + img[i][2]) / 3
			stega_pix	= (stega[i][0] + stega[i][1] + stega[i][2]) / 3

			MSE 		+= ((stega_pix - img_pix) * (stega_pix - img_pix)) # get MSE


		MSE /= (width*height)

		return MSE

	def count_psnr(self, original_img, stego_img):
		PSNR = 0
		MSE, CMax = self.count_MSE(original_img, stego_img)

		temp = (255*255) / MSE

		PSNR = 10 * math.log(10) * temp  

		return PSNR