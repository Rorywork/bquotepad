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
from quotepad.views import home, register, change_password, dashboard
from quotepad.forms import FormStepOne, FormStepTwo, FormStepThree, FormStepFour, FormStepFive, FormStepSix, FormStepSeven, FormStepEight, FormStepNine
from quotepad.views import FormWizardView, model_form_upload

from quotepad.views import ProductPriceList, ProductPriceCreate, ProductPriceUpdate, ProductPriceDelete

from quotepad.views import edit_Profile_details, show_uploaded_files, quote_success, testpdflayout

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^boilerform/$', FormWizardView.as_view([FormStepOne,FormStepTwo])),
    #url(r'^$', home),
    #url(r'^register/', register),
    # url(r'^login/$', auth_views.login),
    #url(r'^logout/$', auth_views.LogoutView.as_view()),
    path('logout/', auth_views.LogoutView.as_view()),
    #url(r'^changepassword/$', change_password, name = 'change_password'),
    #path('', home_view, name='home'),
    path('', home, name='home'),
    path('login/', auth_views.LoginView.as_view()),
    path('passwordreset/', auth_views.PasswordResetView.as_view()),
    path('register/', register),

    #path('accounts/', include('accounts.urls')),
    path('boilerinfo/', include('django.contrib.auth.urls')),

    path('productpricelist/', ProductPriceList.as_view(), name = 'productpricelist'),
    path('productpricecreate/', ProductPriceCreate, name = 'productpricecreate'),
	path('productpriceupdate/<int:product_id>/', ProductPriceUpdate, name = 'productpriceupdate'),
	path('productpricedelete/<int:pk>/', ProductPriceDelete.as_view(), name = 'productpricedelete'),

    # Below loginredirect/ is in settings.py
    path('loginredirect/', home, name = 'home'),
    path('changepassword/', change_password, name = 'change_password'),
    path('home/', home, name = 'home'),
    path('dashboard/', dashboard, name = 'dashboard'),
    path('boilerform/', FormWizardView.as_view([FormStepOne,FormStepTwo,FormStepThree, FormStepFour, FormStepFive, FormStepSix, FormStepSeven, FormStepEight, FormStepNine]), name = 'boilerform'),
    path('testpdflayout/<str:testmode>', testpdflayout, name = 'test_pdf_layout'),
    #url(r'^', include('boilerform.urls'))
    path('fileupload/', model_form_upload, name = 'file_upload'),
    path('showuploadedfiles/', show_uploaded_files, name = 'show_uploaded_files'),
    path('quotesuccess/', quote_success, name = 'quote_success'),
    #url(r'^pdf/$', GeneratePDF.as_view()),
    # url(r'^pdf/$', GeneratePDF2, name = 'GenPDF'),
    path('edit_Profile_details/', edit_Profile_details, name = 'edit_Profile_details'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
