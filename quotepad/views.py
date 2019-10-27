from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, FileResponse, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, FormView

# Form wizard imports
from .forms import FormStepOne, FormStepTwo, FormStepThree, FormStepFour, FormStepFive, FormStepSix, FormStepSeven, FormStepEight, FormStepNine
from formtools.wizard.views import SessionWizardView

# imports associated with User Authentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django import forms
from .forms import UserRegistrationForm

# imports associated with change password
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


# import asscoated with file upload
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from quotepad.models import Document
from quotepad.forms import DocumentForm

# imports associated with xhtml2pdf
from django.http import HttpResponseRedirect, HttpResponse
from quotepad.utils import render_to_pdf, convertHtmlToPdf, convertHtmlToPdf2
import datetime
from pathlib import Path, PureWindowsPath
import os, os.path, errno

# imports associated with sending email
from django.core.mail import EmailMessage

from .models import Profile, ProductPrice
from .forms import ProfileForm, UserProfileForm, ProductPriceForm,EditQuoteTemplateForm

# import associated with signals (used for setting session variables)
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User, Group

# imports for managing .csv file upload
import csv, io
# for copying the template pdf file to the user folder
import shutil

@receiver(user_logged_in)
def sig_user_logged_in(sender, user, request, **kwargs):

	if Profile.objects.filter(user = request.user, first_name=''):
		request.session['Profile_updated'] = False
	else:
		request.session['Profile_updated'] = True

	if Document.objects.filter(user = request.user).count() > 0 :
		request.session['Image_loaded'] = True
	else:
		request.session['Image_loaded'] = False

	if ProductPrice.objects.filter(user = request.user).count() > 0 :
		request.session['ProductPrice_record'] = True
	else:
		request.session['ProductPrice_record'] = False

	if user.groups.filter(name = "Subscribed").exists():
		request.session['User_subscribed'] = True
	else:
		request.session['User_subscribed'] = False

	if user.groups.filter(name = "created_quote_template").exists():
		request.session['created_quote_template'] = True
	else:
		request.session['created_quote_template'] = False

	if user.groups.filter(name = "created_quote").exists():
		request.session['created_quote'] = True
	else:
		request.session['created_quote'] = False				

	return 

class FormWizardView(SessionWizardView):
	template_name = "boilerform.html"

	# Below method is to pass the logged in user to the
	# appropriate form to filter the drop down product listing
	def get_form_kwargs(self, step):
		if step == '8':
			seventh_step_data = self.storage.get_step_data('6')
			manuf = seventh_step_data.get('6-boiler_manufacturer','')
			print(manuf)
			return {'user': self.request.user, 'manufacturer': manuf}
		elif step == '6':
			return {'user': self.request.user}	
		else:
			return {}

	form_list = [FormStepOne, FormStepTwo, FormStepThree, FormStepFour, FormStepFive, FormStepSix, FormStepSeven, FormStepEight, FormStepNine]
	
	def done(self, form_list, **kwargs):
		# Initial check to see if user specific PDF template file exists
		# If it does then use that template, if not use the generic template
		usr_pdf_template_file = Path(settings.BASE_DIR + "/templates/pdf/user_{}/quote_for_pdf.html".format(self.request.user.username))

		if os.path.isfile(usr_pdf_template_file):
			sourceHtml = "pdf/user_{}/quote_for_pdf.html".format(self.request.user.username)      # Under templates folder
		else:

			sourceHtml = "pdf/quote_for_pdf.html"      # Under templates folder

		# Get the data for the Installer from Installer table to populate email(id) and pdf(idx)
		idx = Profile.objects.get(user = self.request.user)

		product_id = ([form.cleaned_data for form in form_list][8].get('product_choice').id)

		# Get the record of the product that was selected
		product_record = ProductPrice.objects.get(pk = product_id)

		# Get the record of the Product Image that was selected and handle exception
		# if no image exists.
		try:
			img_record = Document.objects.get(id = product_record.product_image.id)
		except Exception as e:
			img_record = None
			print(type(e)) 
			print("Error: No Image exists for the Product")

		# Calculate the daily_work_rate multiplied by the estimated_duration
		workload_cost = idx.daily_work_rate * int([form.cleaned_data for form in form_list][8].get('estimated_duration')[0])
		# Calculate the total quote price for the quote
		total_quote_price = workload_cost + product_record.price

		# Get the records of the images file for the current user
		frecords = Document.objects.filter(user=self.request.user.username).order_by('uploaded_at')

		# Get customer lastname
		customer_last_name = ([form.cleaned_data for form in form_list][0].get('customer_last_name'))

		# Assign file name to store generated PDF
		outputFilename = Path(settings.BASE_DIR + "/pdf_quote_archive/user_{}/Quote_{}_{}{}.pdf".format(self.request.user.username,idx.quote_prefix,customer_last_name.replace(" ","_"),f"{idx.current_quote_number:05}")) # pad with leading zeros (5 positions)

		# Write the form data input to a file in the folder pdf_quote_archive/user_xxxx/current_quote.txt
		current_quote_form_filename =  Path(settings.BASE_DIR + "/pdf_quote_archive/user_{}/current_quote.txt".format(self.request.user.username))
		file = open(current_quote_form_filename, 'w') #write to file
		for index, line in enumerate([form.cleaned_data for form in form_list]):
			if index == 8:
				# This code replaces the <object reference> in the form array[8] with the product_id
				string = str(line)
				firstDelPos=string.find("<") # get the position of <
				secondDelPos=string.find(">") # get the position of >
				stringAfterReplace = string.replace(string[firstDelPos:secondDelPos+1], "'" + str(product_id) + "'")
				file.write(str(stringAfterReplace) + "\n")
			else:	
				file.write(str(line) + "\n")
		file.close() #close file


		# Generate the PDF and write to disk
		convertHtmlToPdf2(sourceHtml, outputFilename, {
			'form_data': [form.cleaned_data for form in form_list],
			'idx':idx,
			'frecords': frecords,
			'product_record': product_record,
			'img_record': img_record,
			'workload_cost': workload_cost,
			'total_quote_price': total_quote_price})

		# Increment the Profile.current_quote_number by 1
		idx.current_quote_number = idx.current_quote_number + 1
		idx.save()
		return HttpResponseRedirect('/quotegenerated/')

@login_required
def quote_not_possible(request):
	return render(request,'quote_not_possible.html')

@login_required
def quote_generated(request):
	request.session['created_quote'] = True
	created_quote_group = Group.objects.get(name = 'created_quote')
	request.user.groups.add(created_quote_group)
	return render(request,'quote_generated.html')

@login_required
def test_quote_generated(request):
	return render(request,'test_quote_generated.html')

@login_required
def quote_emailed(request):
	return render(request,'quote_emailed.html')

def landing(request):
    return render(request, 'landing.html')    

@login_required
def quotepad_template_help(request):
	frecords = Document.objects.filter(user=request.user.username).order_by('-uploaded_at')
	return render(request,'quotepad_template_help.html', {'frecords': frecords, 'media_url':settings.MEDIA_URL})

# Functions associated with user authentication
@login_required
def home(request):
	usr_pdf_template_file = Path(settings.BASE_DIR + "/templates/pdf/{}/boilerform_pdf.html".format(request.user.username))
	print(usr_pdf_template_file)
	if os.path.isfile(usr_pdf_template_file):
		print("Using the user specific PDF template file - {}".format(usr_pdf_template_file))
	else:
		print("{} The user specific PDF template file does not exist".format(usr_pdf_template_file))
		print("Using the generic PDF template file.")
	return render(request, 'home.html')

def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		user_profile_form = UserProfileForm(request.POST)
		if form.is_valid() and user_profile_form.is_valid():

			userObj = form.cleaned_data
			username = userObj['username']
			email =  userObj['email']
			password =  userObj['password']
			if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
				User.objects.create_user(username, email, password)
				user = authenticate(username = username, password = password)
				login(request, user)
				profile = user_profile_form.save(commit=False)
				profile.user = user
				profile.email = email
				request.session['Profile_updated'] = False		# Set this to false initially following registration
				profile.save()

				# Create storage folders for the registered user 
				pdf_quote_archive_folder = os.path.join(settings.BASE_DIR, "pdf_quote_archive")
				TEMPLATE_DIRS = os.path.join(settings.BASE_DIR, 'templates')
				user_pdf_quote_archive_folder = os.path.join(pdf_quote_archive_folder,"user_{}".format(request.user.username))
				pdf_templates_folder = os.path.join(TEMPLATE_DIRS,"pdf")
				user_pdf_templates_folder = os.path.join(pdf_templates_folder,"user_{}".format(request.user.username))

				# Create the user specific folder for archiving quotes
				try:
					os.mkdir(user_pdf_quote_archive_folder)
				except OSError as e:
					if e.errno != errno.EEXIST:
						pass
					else:
						print(e)   
	
				# Create the user specific folder for storing the quote template
				try:
					os.mkdir(user_pdf_templates_folder)
				except OSError as e:
					if e.errno != errno.EEXIST:
						pass
					else:
						print(e)

				# Copy the template pdf-html file to the newly created user folder
				source = os.path.join(pdf_templates_folder, 'quote_for_pdf.html')
				print(source)
				target = user_pdf_templates_folder
				print(target)
				# exception handling
				try:
					shutil.copy(source, target)
				except IOError as e:
					print("Unable to copy file. %s" % e)
				
				messages.success(request, 'You are now registered on the site.')
				return HttpResponseRedirect('/loginredirect/')
			else:
				#raise forms.ValidationError('A profile with that username or email already exists.')
				messages.warning(request, 'A profile with that username or email already exists.')
	else:
		form = UserRegistrationForm()
		user_profile_form = UserProfileForm()
	return render(request, 'register.html', {'form' : form, 'user_profile_form': user_profile_form})

@login_required
def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Your password was successfully updated!')
			return render(request, 'change_password_success.html', {})
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'change_password.html', {'form': form})

@login_required
def model_form_upload(request):
	# Check to see the status of the number of images uploaded and assign an appropriate instruction
	if Document.objects.filter(user = request.user).count() == 0 :
		form_instructions = "Upload A Logo For Your Company"
	elif Document.objects.filter(user = request.user).count() == 1 :
		form_instructions = "Upload A Product Image To Be Used On Your Quotes"
	else:
		form_instructions = "Upload Images To Be Used On Your Quotes"

	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		print(request.user)
		if form.is_valid():
			document = form.save(commit=False)
			document.user = request.user
			document.save()
			request.session['Image_loaded'] = True
			messages.success(request, 'The image file was successfully added.')
			return redirect('/showuploadedfiles/')
	else:
		form = DocumentForm()
	return render(request, 'file_upload.html', {
		'form': form,
		'form_instructions': form_instructions
	})

@login_required
def show_uploaded_files(request):
	frecords = Document.objects.filter(user=request.user.username).order_by('-uploaded_at')
	return render(request, 'show_uploaded_files.html', {'frecords': frecords, 'media_url':settings.MEDIA_URL})
	
@login_required
def edit_Profile_details(request):
	print(request.user.username)
	profile = get_object_or_404(Profile, user = request.user )
	if request.method=="POST":
		form = ProfileForm(request.POST, instance=profile)
		if form.is_valid():
			alert = 1
			form.save()
			request.session['Profile_updated'] = True
			# messages.success(request, 'Your profile details have been updated.')
			# return redirect('/home/')
	else:
		alert = None
		form = ProfileForm(instance=profile)
		
	return render(request,"edit_Profile_details.html",{'form': form, 'alert': alert}) 

# Views to perform CRUD operations on the ProductPrice model

class ProductPriceList(ListView):
	context_object_name = 'products_by_user'

	def get_queryset(self):
		return ProductPrice.objects.filter(user=self.request.user).order_by('brand','model_name')

@login_required
def ProductPriceCreate(request):
	if request.method == "POST":
		form = ProductPriceForm(request.POST,  user = request.user)
		if form.is_valid():
			product = form.save(commit=False)
			product.user = request.user
			product.save()
			messages.success(request, 'The product details were successfully updated.')
			request.session['ProductPrice_record'] = True
			return redirect('/productpricelist/')
	else:
		form = ProductPriceForm(user = request.user)
	context = {
		'form': form,
		'form_instructions': 'Add New Product'
	}
	return render(request,'quotepad/productprice_form.html',context)

@login_required
def ProductPriceUpdate(request, product_id):
	product = ProductPrice.objects.get(pk = product_id)
	if request.method == "POST":
		form = ProductPriceForm(request.POST, instance=product, user = request.user)
		if form.is_valid():
			product = form.save()
			messages.success(request, 'The product details were successfully updated.')
			request.session['ProductPrice_record'] = True
			return redirect('/productpricelist/')
	else:
		form = ProductPriceForm(instance=product, user = request.user)
	context = {
		'form': form,
		'product': product,
		'form_instructions': 'Edit Product Details'
	}
	return render(request,'quotepad/productprice_form.html',context)

class ProductPriceDelete(DeleteView):
	model = ProductPrice
	success_url='/productpricelist/'

@login_required	  
def generate_quote_from_file(request, outputformat, quotesource):

	# Initial check to see if user specific PDF template file exists
	# If it does then use that template, if not then use the generic template
	usr_pdf_template_file = Path(settings.BASE_DIR + "/templates/pdf/user_{}/quote_for_pdf.html".format(request.user.username))
	print(usr_pdf_template_file)
	if os.path.isfile(usr_pdf_template_file):
		sourceHtml = "pdf/user_{}/quote_for_pdf.html".format(request.user.username)      # Under templates folder
	else:
		sourceHtml = "pdf/quote_for_pdf.html"      # Under templates folder

	# Determine where to source the quote data from - test_data.txt or the current quote for the user
	if quotesource == "testdata":
		quote_form_filename =  Path(settings.BASE_DIR + "/pdf_quote_archive/test_data.txt")
	else: # use the current quote data file	
		quote_form_filename =  Path(settings.BASE_DIR + "/pdf_quote_archive/user_{}/current_quote.txt".format(request.user.username))
		# if a current quote data file does not exist then revery back to using the test data file
		if not os.path.isfile(quote_form_filename):
			quote_form_filename =  Path(settings.BASE_DIR + "/pdf_quote_archive/test_data.txt")

	with open(quote_form_filename) as file:
		file_form_datax = []
		for line in file:
			file_form_datax.append(eval(line))
		
	file_form_data = file_form_datax
	product_id = file_form_data[8].get('product_choice')	

	idx = Profile.objects.get(user = request.user)

	# Get the ProductPrice record selection 
	if quotesource == "testdata":	# ProductPrice will come from the first user record or from the demo record	
		if ProductPrice.objects.filter(user = request.user).count() > 0 :	# Check if the user has created a product/price record
			product_record = ProductPrice.objects.filter(user = request.user).first()	# A product price record exists - use the first one
		else:	# Product Price record does not exist - select the Demo record
			product_record = ProductPrice.objects.first()			
	else:	# retrieve the user selected product record from the quote form
		product_record = ProductPrice.objects.get(pk = int(product_id))

	frecords = Document.objects.filter(user=request.user.username).order_by('uploaded_at')

	try:	# test to see if image is associated with product
		img_record = Document.objects.get(id = product_record.product_image.id )
	except: # if not then continue with empty object
		img_record = ""

	# Calculate the daily_work_rate multiplied by the estimated_duration
	workload_cost = idx.daily_work_rate * int(file_form_data[8].get('estimated_duration')[0])
	# Calculate the total quote price for the quote
	total_quote_price = workload_cost + product_record.price	

	# Determine whether to output to screen as PDF or HTML
	if outputformat == "PDFOutput":
		request.session['created_quote_template'] = True
		created_quote_template_group = Group.objects.get(name = 'created_quote_template')
		request.user.groups.add(created_quote_template_group)
		pdf = render_to_pdf(sourceHtml, {
			'form_data': file_form_data,
			'idx': idx,
			'frecords': frecords,
			'product_record': product_record,
			'img_record': img_record,
			'workload_cost': workload_cost,
			'total_quote_price': total_quote_price}) 
		return HttpResponse(pdf, content_type='application/pdf')

	elif outputformat == "EmailOutput":
		# Get customer lastname
		customer_last_name = (file_form_data[0].get('customer_last_name'))
		# Assign file name to store generated PDF
		outputFilename = Path(settings.BASE_DIR + "/pdf_quote_archive/user_{}/Quote_{}_{}{}.pdf".format(request.user.username,idx.quote_prefix,customer_last_name.replace(" ","_"),f"{idx.current_quote_number:05}")) # pad with leading zeros (5 positions)
		# Generate the PDF and write to disk
		convertHtmlToPdf2(sourceHtml, outputFilename, {
			'form_data': file_form_data,
			'idx':idx,
			'frecords': frecords,
			'product_record': product_record,
			'img_record': img_record,
			'workload_cost': workload_cost,
			'total_quote_price': total_quote_price})
		# Generate the email, attach the pdf and send out
		fd = file_form_data
		msg=""
		msg = msg + " Hi {}.\n Thank you for your enquiry to {}. The quote that you requested is on the attached PDF file.\n\n".format(fd[0]['customer_first_name'], idx.company_name)
		msg = msg + " Should you have any further questions please feel free to contact me on {}.\n\n".format(idx.telephone)
		msg = msg + " Kind regards,\n"
		msg = msg + " " + idx.first_name
		email = EmailMessage(
		'Your boiler installation quote from {}'.format(idx.company_name), msg, idx.email, [fd[0]['customer_email']])
		email.attach_file(outputFilename)
		email.send()
		return HttpResponseRedirect('/quoteemailed/')

	else:   # HTMLOutput
		return render(request, sourceHtml, {
			'form_data': file_form_data,
			'idx': idx,
			'frecords': frecords,
			'product_record': product_record,
			'img_record': img_record,
			'workload_cost': workload_cost,
			'total_quote_price': total_quote_price})

@login_required
def edit_quote_template(request):
	
	if request.method=="POST":
		form = EditQuoteTemplateForm(request.user)
		
		pdf_template_code = request.POST['pdf_template_code']
	
		usr_pdf_template_file = Path(settings.BASE_DIR + "/templates/pdf/user_{}/quote_for_pdf.html".format(request.user.username))	
		template_file = open(usr_pdf_template_file,'w', newline='')
		template_file.write(pdf_template_code)
		template_file.close()
		request.session['created_quote_template'] = True
		created_quote_template_group = Group.objects.get(name = 'created_quote_template')
		request.user.groups.add(created_quote_template_group)
		messages.success(request, 'Your quote template has been updated.')
	else:
		form = EditQuoteTemplateForm(request.user)
		return render(request,"edit_quote_template.html",{'form': form}) 

	return redirect('/home/')	

@login_required
def list_quote_archive(request):
	folder = Path(settings.BASE_DIR + "/pdf_quote_archive/user_{}/".format(request.user.username))
	#path="C:\\somedirectory"  # insert the path to your directory   
	pdf_files =os.listdir(folder)   
	return render(request, 'list_quote_archive.html', {'pdf_files': pdf_files})

@login_required
def pdf_view(request, pdf_file):
	file_to_render = Path(settings.BASE_DIR + "/pdf_quote_archive/user_{}/".format(request.user.username), pdf_file)
	try:
		return FileResponse(open(file_to_render, 'rb'), content_type='application/pdf')
	except FileNotFoundError:
		raise Http404()

