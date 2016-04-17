from django.shortcuts import render
from django.conf import settings
import os

from .lsb import LSB

# Create your views here.
def index(request):
	title_page = 'Home'

	return render(request, 'app/index.html', {
		'title_page' :	title_page,
		})

def encode(request):
	title_page 	= "result"
	result 		= "seems you are not enter any images and text"

	if request.method == 'POST':
		msg = request.POST['pesan']

		uploaded_filename = handle_upload_file(request.FILES['img'])

		lsb = LSB() # buat objek dari kelas LSB

		if lsb.embed_msg(uploaded_filename, msg): # masukan pesan ke dalam gambar
			result = "berhasil"
		else:
			result = "gagal memasukkan pesan, tipe gambar tidak sesuai"

		return render(request, 'app/result.html', {
			'title_page' 	: title_page,
			'result'		: result,
			})	

	return render(request, 'app/result.html', {
		'title_page' 	: title_page,
		'result'		: result,
		})

def decode(request):
	title_page 	= "result"
	result 		= "seems you are not entering any images"
	val_psnr	= 0

	if request.method == 'POST':
		uploaded_filename = request.FILES['img']

		lsb = LSB() # buat objek dari kelas LSB

		result = lsb.extract_msg(uploaded_filename)
		# print(result)

		if not result:
			result = "tipe gambar tidak sesuai, gagal mengekstrak pesan"
		else:
			stego_img		= os.path.join(settings.MEDIA_ROOT, uploaded_filename.name)
			temp 			= uploaded_filename.name.split('.')
			original_img 	= temp[0][:-4]+"."+temp[1]
			original_img	= os.path.join(settings.MEDIA_ROOT, original_img)

			val_psnr = lsb.count_psnr(original_img, stego_img) # hitung nilai psnr
		
		return render(request, 'app/result.html', {
			'title_page' 	: title_page,
			'result'		: result,
			'psnr'			: val_psnr,
			})	

	return render(request, 'app/result.html', {
		'title_page' 	: title_page,
		'result'		: result,
		'psnr'			: val_psnr,
		})

def handle_upload_file(file):
	# create the folder if it doesn't exist.
	try:
		os.mkdir(os.path.join(settings.MEDIA_ROOT))
	except:
		pass

	# save original file
	original_img = os.path.join(settings.MEDIA_ROOT, file.name) # save the uploaded file inside that folder.
	fout = open(original_img, 'wb+')
	
	# Iterate through the chunks.
	for chunk in file.chunks():
		fout.write(chunk)
	fout.close()

	# ---------------------------------------------------------

	# save stego images
	temp = file.name.split('.')
	
	full_filename = os.path.join(settings.MEDIA_ROOT, temp[0]+"_out."+temp[1]) # save the uploaded file inside that folder.
	fout = open(full_filename, 'wb+')
	
	# Iterate through the chunks.
	for chunk in file.chunks():
		fout.write(chunk)
	fout.close()

	return full_filename