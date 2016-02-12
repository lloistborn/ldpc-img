from django.shortcuts import render
from PIL import Image, ImageOps, ImageFilter
from django.conf import settings
import os

# Create your views here.
def index(request):
	title_page = 'Home'

	return render(request, 'app/index.html', {
		'title_page' :	title_page,
		})

def encode(request):
	title_page = 'encoded'

	if request.method == 'POST':
		msg = request.POST['pesan']

		uploaded_filename = handle_upload_file(request.FILES['img'])
		# output_filename = applyfilter(uploaded_filename)



		# print(uploaded_filename)
		# print(msg)
		# print(output_filename)

		return render(request, 'app/index.html', {
			'title_page' :	title_page,
			})	

	return render(request, 'app/index.html', {
		'title_page' :	title_page,
		})

# embedding process
def embedd_msg(filename, msg):
	inputfile = os.path.join(settings.MEDIA_ROOT, filename)
	f = filename.split('.')
	outputfilename = f[0] + '-out.jpg'

	outputfile = os.path.join(settings.MEDIA_ROOT, outputfilename)

	im = Image.open(inputfile)

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

	return file.name

# sepia
def applyfilter(filename):
	inputfile = os.path.join(settings.MEDIA_ROOT, filename)

	f = filename.split('.')
	outputfilename = f[0] + '-out.jpg'

	outputfile = os.path.join(settings.MEDIA_ROOT, outputfilename)

	im = Image.open(inputfile)
	
	sepia = []
	r, g, b = (239, 224, 185)
	for i in range(255):
		sepia.extend((r*i//255, g*i//255, b*i//255))

	im = im.convert('L')
	im.putpalette(sepia)
	im = im.convert('RGB')

	im.save(outputfile)
	return outputfilename