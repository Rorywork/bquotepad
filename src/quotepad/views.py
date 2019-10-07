from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
#from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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
from django.views.generic import View
from quotepad.utils import render_to_pdf, convertHtmlToPdf, convertHtmlToPdf2
import datetime
from pathlib import Path, PureWindowsPath
import os.path

# imports associated with sending email
from django.core.mail import send_mail
# or ( should not be both )
from django.core.mail import EmailMessage

from .models import Profile
from .forms import ProfileForm, UserProfileForm

class FormWizardView(SessionWizardView):
    template_name = "boilerform.html"
    form_list = [FormStepOne, FormStepTwo, FormStepThree, FormStepFour, FormStepFive, FormStepSix, FormStepSeven, FormStepEight, FormStepNine]
    
    # Below is code that outputs the forminfo to HTML
    # def done(self, form_list, **kwargs):    
    #     id = Installer.objects.get(company_name='Abode Boilers Ltd.')
    #     idx = Installer.objects.filter(company_name='Abode Boilers Ltd.')
    #     print(id.email)
    #     print(idx)
    #     print(id)
    #     return render(self.request, 'pdf/boilerform_pdf.html', {
    #         'form_data': [form.cleaned_data for form in form_list],
    #         'idx': idx},
    #     )

    # Below code renders the form output to a PDF format on screen
    # def done(self, form_list, **kwargs):
    #     pdf = render_to_pdf('pdf/boilerform_pdf.html', {'form_data': [form.cleaned_data for form in form_list]})
    #     return HttpResponse(pdf, content_type='application/pdf')

    # Below code renders the form output to a PDF format and downloads it (downloads folder)
    # def done(self, form_list, **kwargs):
    #     pdf = render_to_pdf('pdf/boilerform_pdf.html', {'form_data': [form.cleaned_data for form in form_list]})
    #     if pdf:
    #         response = HttpResponse(pdf, content_type='application/pdf')
    #         #dest_folder = "C:\Users\gordo\Dev\gordonenv\src\pdfs"
    #         filename = "Invoice_%s.pdf" %("123456")
    #         content = "inline; filename=%s" %(filename)
    #         #download = self.request.GET.get("download")
    #         #if download:
    #         content = "attachment; filename=%s" %(filename)
    #         response['Content-Disposition'] = content
    #         return response
    #     return HttpResponse("Not found")

    # Below code renders the form to an email  in plain text format- sends to Mailtrap.io
    # def done(self, form_list, **kwargs):
    #     fd = [form.cleaned_data for form in form_list]
    #     print(fd)
    #     msg = " Bill to : {} {} \n Home Phone: {} \n Status: {} \n\n Address: \n{}{}\n{}\n{}\n{}".format(fd[0]['customer_first_name'], fd[0]['customer_last_name'], fd[0]['customer_home_phone'], fd[0]['owner_or_tenant'], fd[1]['installation_address'], fd[1]['street_address'], fd[1]['city'], fd[1]['county'], fd[1]['postcode'])
    #     send_mail('Hello from QuotePad',
    #     msg,
    #     'gordon@quotepad.com',
    #     ['email2@example.com'],
    #     fail_silently=False)
    #     return render(self.request, 'home.html')

    # Below code renders the pdf file and sends it as an email
    # def done(self, form_list, **kwargs):
    #     fd = [form.cleaned_data for form in form_list]
    #     print(fd)
    #     msg = " Bill to : {} {} \n Home Phone: {} \n Status: {} \n\n Address: \n{}{}\n{}\n{}\n{}".format(fd[0]['customer_first_name'], fd[0]['customer_last_name'], fd[0]['customer_home_phone'], fd[0]['owner_or_tenant'], fd[1]['installation_address'], fd[1]['street_address'], fd[1]['city'], fd[1]['county'], fd[1]['postcode'])
    #     send_mail('Hello from QuotePad',
    #     msg,
    #     'gordon@quotepad.com',
    #     ['email2@example.com'],
    #     fail_silently=False)
    #     return render(self.request, 'home.html')

    # Below code sends an email with an attached pdf file
    # def done(self, form_list, **kwargs):
    #     fd = [form.cleaned_data for form in form_list]
    #     msg = " Bill to : {} {} \n Home Phone: {} \n Status: {} \n\n Address: \n{}{}\n{}\n{}\n{}".format(fd[0]['customer_first_name'], fd[0]['customer_last_name'], fd[0]['customer_home_phone'], fd[0]['owner_or_tenant'], fd[1]['installation_address'], fd[1]['street_address'], fd[1]['city'], fd[1]['county'], fd[1]['postcode'])
    #     email = EmailMessage(
    #     'Hello from Quotepad', msg, 'gordon@quotepad.com', ['email@to.com'])
    #     email.attach_file('pdfs/Invoice_123456.pdf')
    #     email.send()
    #     return render(self.request, 'home.html')

    # Below code does the whole damn thang!
    def done(self, form_list, **kwargs):
        # Initial check to see if user specific PDF template file exists
        # If it does then use that template, if not use the generic template
        usr_pdf_template_file = Path(settings.BASE_DIR + "/templates/pdf/user_{}/quote_for_pdf.html".format(self.request.user.username))
        print(usr_pdf_template_file)
        if os.path.isfile(usr_pdf_template_file):
            print("Using the user specific PDF template file - {}".format(usr_pdf_template_file))
            sourceHtml = "pdf/user_{}/quote_for_pdf.html".format(self.request.user.username)      # Under templates folder
        else:
            print("{} The user specific PDF template file does not exist".format(usr_pdf_template_file))
            print("Using the generic PDF template file.")
            sourceHtml = "pdf/quote_for_pdf.html"      # Under templates folder

        # Get the data for the Installer from Installer table to populate email(id) and pdf(idx)
        id = Profile.objects.get(user = self.request.user)
        idx = Profile.objects.filter(user = self.request.user)

        # Get the records of the images file for the current user
        frecords = Document.objects.filter(user=self.request.user.username).order_by('uploaded_at')
        outputFilename = "pdf_quote_archive/user_{}/Quote_{}{}.pdf".format(self.request.user.username,id.company_name.replace(" ","_"),f"{id.cur_quote_no:05}") # pad with leading zeros (5 positions)

        # Generate the PDF and write to disk
        convertHtmlToPdf2(sourceHtml, outputFilename, {
            'form_data': [form.cleaned_data for form in form_list],
            'idx':idx,
            'frecords': frecords})

        # Generate the email, attach the pdf and send out
        fd = [form.cleaned_data for form in form_list]
        msg = " Quote prepared for : {} {} \n Home Phone: {} \n Status: {} \n\n Address: \n {} {}\n {}\n {}\n {}\n\n".format(fd[0]['customer_first_name'], fd[0]['customer_last_name'], fd[0]['customer_home_phone'], fd[0]['owner_or_tenant'], fd[1]['installation_address'], fd[1]['street_address'], fd[1]['city'], fd[1]['county'], fd[1]['postcode'])
        msg = msg + " Hi {}. Thank you for your enquiry. The quote that you requested is on the attached PDF file.".format(fd[0]['customer_first_name'])
        email = EmailMessage(
        'Your boiler installation quote from {}'.format(id.company_name), msg, id.email, [fd[0]['customer_email']])
        email.attach_file(outputFilename)
        email.send()

        # Increment the Profile.cur_quote_no by 1
        id.cur_quote_no = id.cur_quote_no + 1
        id.save()
        return HttpResponseRedirect('/quotesuccess/')

def quote_success(request):
    return render(request,'quote_success.html')

# Views associated with user authentication
def home(request):
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
               profile.save()
               # currently redirection is to the quotepad form wizard but next version will require redirect to set up profile details
               return HttpResponseRedirect('/loginredirect/')
            else:
               raise forms.ValidationError('A profile with that username or email already exists.')
    else:
        form = UserRegistrationForm()
        user_profile_form = UserProfileForm()
    return render(request, 'register.html', {'form' : form, 'user_profile_form': user_profile_form})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            #return redirect('change_password') .. commented out by GL 14-07-19
            return render(request, 'change_password_success.html', {})
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        print(request.user)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            return redirect('/showuploadedfiles/')
    else:
        form = DocumentForm()
    return render(request, 'file_upload.html', {
        'form': form
    })

def show_uploaded_files(request):
    frecords = Document.objects.filter(user=request.user.username).order_by('-uploaded_at')
    return render(request, 'show_uploaded_files.html', {'frecords': frecords, 'media_url':settings.MEDIA_URL})
    

def edit_Profile_details(request):
    print(request.user.username)
    profile = get_object_or_404(Profile, user = request.user )
    if request.method=="POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('/home/')
    else:
        form = ProfileForm(instance=profile)
        
    return render(request,"edit_Profile_details.html",{'form': form})

def testpdflayout(request, testmode):

    # Initial check to see if user specific PDF template file exists
    # If it does then use that template, if not use the generic template
    usr_pdf_template_file = Path(settings.BASE_DIR + "/templates/pdf/user_{}/quote_for_pdf.html".format(request.user.username))
    print(usr_pdf_template_file)
    if os.path.isfile(usr_pdf_template_file):
        sourceHtml = "pdf/user_{}/quote_for_pdf.html".format(request.user.username)      # Under templates folder
    else:
        sourceHtml = "pdf/quote_for_pdf.html"      # Under templates folder

    test_form_data = [{'customer_first_name': 'Alan', 'customer_last_name': 'Green', 'customer_home_phone': '01202 123456', 'customer_mobile_phone': '07768 150701', 'customer_email': 'gordonlindsay@virginmedia.com', 'owner_or_tenant': 'Owner'},
    {'installation_address': '12', 'street_address': 'Stourvale Avenue', 'city': 'Bournemouth', 'county': 'Dorset', 'postcode': 'BH6 3PT', 'property_type': 'Detached'},
    {'current_fuel_type': 'Gas', 'current_boiler_type': 'Floor Standing - Conventional', 'current_boiler_location': 'Kitchen', 'current_flue_system': 'Vertical - Open Flue', 'current_flue_location': 'Ground Floor', 'current_controls': 'Wired - Programmer'},
    {'removals': ['Hot Water Cylinder', 'Feed and Expansion Tank']},
    {'new_fuel_type': 'Gas', 'new_boiler_type': 'Floor Standing - Conventional', 'new_boiler_location': 'Kitchen', 'new_flue_system': 'Vertical - Open Flue', 'new_flue_location': 'Ground Floor', 'new_flue_diameter': '100mm', 'plume_management_kit': 'Required', 'condensate_termination': 'Drain', 'new_controls': 'Wired - Programmer', 'cws_flow_rate': '4', 'new_flue_metres': '1'},
    {'system_treatment': 'Chemical Flush & Inhibitor', 'gas_supply': 'Use esxisting supply', 'gas_supply_length': '9-15m', 'asbestos_containing_materials_identified': 'No Asbestos Identified', 'electrical_work_required': 'Connect to existing wiring'},
    {'boiler_manufacturer': 'Worcester Bosch', 'boiler_model': '7733600074 Worcester Bosch Greenstar 12Ri', 'manufacturer_guarentee': '5 Years', 'flue_components': 'Horizontal Flue Kit', 'programmer_thermostat': 'Drayton Twin Channel Programmer', 'central_heating_system_filter': 'Worcester Bosch 22mm System Filter', 'scale_reducer': '15mm in line scale reducer'},
    {'radiator_requirements': 'Thermostatic Radiator Valves Only', 'thermostatic_radiator_valves_size': '22', 'thermostatic_radiator_valves_type': 'Stainless Steel', 'thermostatic_radiator_valves_quantity': '5'},
    {'estimated_duration': '1 Day', 'description_of_works': 'Full installation of new boiler and removal of existing one.'}]

    idx = Profile.objects.filter(user = request.user)

    frecords = Document.objects.filter(user=request.user.username).order_by('uploaded_at')

    # Determine whether to output to screen as PDF or HTML
    if testmode == "PDFOutput":
        pdf = render_to_pdf(sourceHtml, {
            'form_data': test_form_data,
            'idx': idx,
            'frecords': frecords})
        return HttpResponse(pdf, content_type='application/pdf')
    else:   # HTMLOutput
        return render(request, sourceHtml, {
            'form_data': test_form_data,
            'idx': idx,
            'frecords': frecords},
            )




