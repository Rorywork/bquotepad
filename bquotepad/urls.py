"""bquotepad URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url,include
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from quotepad.views import home, register, change_password, landing
from quotepad.forms import FormStepOne, FormStepTwo, FormStepThree, FormStepFour, FormStepFive, FormStepSix, FormStepSeven, FormStepEight, FormStepNine
from quotepad.views import FormWizardView, model_form_upload

from quotepad.views import edit_Profile_details, show_uploaded_files, quote_generated, test_quote_generated, quote_emailed, quote_not_possible, quotepad_template_help
from quotepad.views import ProductPriceList, ProductPriceCreate, ProductPriceUpdate, ProductPriceDelete
from quotepad.views import generate_quote_from_file, edit_quote_template, list_quote_archive, pdf_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('logout/', auth_views.LogoutView.as_view()),
    path('', landing, name='landing'),
    path('login/', auth_views.LoginView.as_view()),
    path('passwordreset/', auth_views.PasswordResetView.as_view()),
    path('register/', register),

    path('boilerinfo/', include('django.contrib.auth.urls')),

    path('productpricelist/', login_required(ProductPriceList.as_view()), name = 'productpricelist'),
    path('productpricecreate/', ProductPriceCreate, name = 'productpricecreate'),
	path('productpriceupdate/<int:product_id>/', ProductPriceUpdate, name = 'productpriceupdate'),
	path('productpricedelete/<int:pk>/', login_required(ProductPriceDelete.as_view()), name = 'productpricedelete'),

    path('quotegenerated/', quote_generated, name = 'quote_generated'),
	path('quoteemailed/', quote_emailed, name = 'quote_emailed'),
    path('quotenotpossible/', quote_not_possible, name = 'quote_not_possible'),
	path('quotepadtemplatehelp/', quotepad_template_help, name = 'quotepad_template_help'),
    path('testquotegenerated/', test_quote_generated, name = 'test_quote_generated'),

    path('loginredirect/', home, name = 'home'),
    path('changepassword/', change_password, name = 'change_password'),
    path('home/', home, name = 'home'),

    path('landing/', landing, name = 'landing'),
    path('boilerform/', login_required(FormWizardView.as_view([FormStepOne,FormStepTwo,FormStepThree, FormStepFour, FormStepFive, FormStepSix, FormStepSeven, FormStepEight, FormStepNine])), name = 'boilerform'),
    path('generatequotefromfile/<str:outputformat>/<str:quotesource>', generate_quote_from_file, name = 'generate_quote_from_file'),

    path('fileupload/', model_form_upload, name = 'file_upload'),
    path('showuploadedfiles/', show_uploaded_files, name = 'show_uploaded_files'),

    path('edit_Profile_details/', edit_Profile_details, name = 'edit_Profile_details'),
    path('editquotetemplate/', edit_quote_template, name = 'editquotetemplate'),
	path('listquotearchive/', list_quote_archive, name = 'listquotearchive'),
	path('pdfview/<str:pdf_file>', pdf_view, name = 'pdfview'),
	path('', include('payments.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
