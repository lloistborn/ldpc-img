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
	result 		= "seems you are not enter any images"

	if request.method == 'POST':
		uploaded_filename = handle_upload_file(request.FILES['img'])

		lsb = LSB() # buat objek dari kelas LSB

		result = lsb.extract_msg(uploaded_filename) 

		if not result:
			result = "tipe gambar tidak sesuai, gagal mengekstrak pesan"
		
		return render(request, 'app/result.html', {
			'title_page' 	: title_page,
			'result'		: result,
			})	

	return render(request, 'app/result.html', {
		'title_page' 	: title_page,
		'result'		: result,
		})

def handle_upload_file(file):
	# create the folder if it doesn't exist.
	try:
		os.mkdir(os.path.join(settings.MEDIA_ROOT))
	except:
		pass

	# save the uploaded file inside that folder.
	full_filename = os.path.join(settings.MEDIA_ROOT, file.name)
	fout = open(full_filename, 'wb+')
	
	# Iterate through the chunks.
	for chunk in file.chunks():
		fout.write(chunk)
	fout.close()

	return full_filename