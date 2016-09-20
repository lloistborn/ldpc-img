from django.shortcuts import render
from django.conf import settings
import os

from .lsb import LSB
from .nlsb import NLSB
from .ipsnr import IPSNR

# Create your views here.
def index(request):
	title_page = 'Home'

	return render(request, 'app/index.html', {
		'title_page' :	title_page,
		})

def encode(request):
	title_page 	= "result"
	result 		= "seems you are not enter any images and text"
	data 		= False

	if request.method == 'POST':
		msg = request.POST['pesan']

		# encode menggunakan metode LSB
		if 'encodelsb' in request.POST:
			uploaded_filename = handle_upload_file(request.FILES['img'], 'imgforlsb')
			
			lsb = LSB() # buat objek dari kelas LSB

			data = lsb.embed_msg(uploaded_filename, msg)
			if data: # masukan pesan ke dalam gambar
				result = "berhasil"
			else:
				result = "gagal memasukkan pesan, tipe gambar tidak sesuai"
		# encode menggunakan metode Improved LSB
		elif 'encodenlsb' in request.POST:
			uploaded_filename = handle_upload_file(request.FILES['img'], 'imgfornlsb')

			nlsb = NLSB() # buat objek dari kelas NLSB

			data = nlsb.embed_msg(uploaded_filename, msg)
			if data: # masukan pesan ke dalam gambar
				result = "berhasil"
			else:
				result = "gagal memasukkan pesan, tipe gambar tidak sesuai"

		return render(request, 'app/index.html', {
			'title_page' 	: title_page,
			'result'		: result,
			'data'			: data
			})	

	return render(request, 'app/index.html', {
		'title_page' 	: title_page,
		'result'		: result,
		'data'			: data
		})

def decode(request):
	title_page 	= "result"
	result 		= "seems you are not entering any images"
	val_psnr	= 0
	folderimg	= ''

	if request.method == 'POST':
		uploaded_filename = request.FILES['img']

		temp = uploaded_filename.name.split('.')
		if(temp[-3:] != "out"):
			return render(request, 'app/index.html', {
				'title_page' 	: title_page,
				'result'		: "image does not contains any messages",
				'psnr'			: val_psnr,
				'method'		: ""
				})		

		if 'decodelsb' in request.POST:
			method = 'Improve LSB'
			folderimg = 'imgforlsb'
			lsb = LSB() # buat objek dari kelas LSB

			result = lsb.extract_msg(uploaded_filename)

		elif 'decodenlsb' in request.POST:
			method = 'Old LSB'
			folderimg = 'imgfornlsb'
			nlsb = NLSB() # buat objek dari kelas LSB

			result = nlsb.extract_msg(uploaded_filename)

		if not result:
			result = "tipe gambar tidak sesuai, gagal mengekstrak pesan"
		else:
			stego_img		= os.path.join(settings.MEDIA_ROOT, folderimg, uploaded_filename.name)
			temp 			= uploaded_filename.name.split('.')
			original_img 	= temp[0][:-4]+"."+temp[1]
			original_img	= os.path.join(settings.MEDIA_ROOT, folderimg, original_img)

			psnr = IPSNR()
			val_psnr = psnr.count_psnr(original_img, stego_img) # hitung nilai psnr

		return render(request, 'app/index.html', {
			'title_page' 	: title_page,
			'result'		: result,
			'psnr'			: val_psnr,
			'method'		: method,
			})	

	return render(request, 'app/index.html', {
		'title_page' 	: title_page,
		'result'		: result,
		'psnr'			: val_psnr,
		})

def handle_upload_file(file, tofolder):
	# create the folder if it doesn't exist.
	try:
		os.mkdir(os.path.join(settings.MEDIA_ROOT, tofolder))
	except:
		pass

	# save original file
	original_img = os.path.join(settings.MEDIA_ROOT, tofolder, file.name) # save the uploaded file inside that folder.
	fout = open(original_img, 'wb+')
	
	# Iterate through the chunks.
	for chunk in file.chunks():
		fout.write(chunk)
	fout.close()

	# save stego images
	temp = file.name.split('.')
	
	full_filename = os.path.join(settings.MEDIA_ROOT, tofolder, temp[0]+"_out."+temp[1]) # save the uploaded file inside that folder.
	fout = open(full_filename, 'wb+')
	
	# Iterate through the chunks.
	for chunk in file.chunks():
		fout.write(chunk)
	fout.close()

	return full_filename