from django import forms
# Added by GL 19/07/19 - File upload capability
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from boilerinfo.models import Document, Profile, ProductPrice

# For Editing the template
from django.conf import settings
from pathlib import Path

OWNER_OR_TENANT_DROPDOWN = (
	('Owner','Owner'),
	('Tenant','Tenant'),
)

PROPERTY_TYPE_DROPDOWN = (
	('Detached','Detached'),
	('Semi Detached','Semi Detached'),
	('Terraced','Terraced'),
	('Bungalow','Bungalow'),
	('Flat','Flat'),
)

CURRENT_FUEL_TYPE_DROPDOWN = (
	('Gas','Gas'),
	('LPG','LPG'),
	('Oil','Oil'),
	('Electric','Electric'),
	('None','None'),
)

CURRENT_BOILER_TYPE_DROPDOWN = (
	('Floor Standing - Conventional','Floor Standing - Conventional'),
	('Floor Standing - Combi','Floor Standing - Combi'),
	('Floor Standing - System','Floor Standing - System'),
	('Wall Hung - Conventional','Wall Hung - Conventional'),
	('Wall Hung - Combi','Wall Hung - Combi'),
	('Wall Hung - System','Wall Hung - System'),
)

CURRENT_BOILER_LOCATION_DROPDOWN = (
	('Kitchen','Kitchen'),
	('Bathroom','Bathroom'),
	('Bedroom','Bedroom'),
	('Utility','Utility'),
	('Airing Cupboard','Airing Cupboard'),
	('Lounge','Lounge'),
	('Loft','Loft'),
	('Garage','Garage'),
	('Other','Other'),
)

CURRENT_FLUE_SYSTEM_DROPDOWN = (
	('Vertical - Open Flue','Vertical - Open Flue'),
	('Vertical - Fan assisted','Vertical - Fan assisted'),
	('Horizontal','Balanced Flue'),
	('Horizontal','Fan Flue'),
)

CURRENT_FLUE_LOCATION_DROPDOWN = (
	('Ground Floor','Ground Floor'),
	('First Floor','First Floor'),
	('Second Floor','Second Floor'),
	('Third Floor','Third Floor'),
	('Fourth Floor','Fourth Floor'),
	('Fifth Floor','Fifth Floor'),
)

CURRENT_CONTROLS_DROPDOWN = (
	('Wired - Programmer','Wired - Programmer'),
	('Wired - Room Thermostat','Wired - Room Thermostat'),
	('Wired - Cylinder Thermostat','Wired - Cylinder Thermostat'),
	('Wireless-Room Thermostat','Wireless-Room Thermostat'),
	('Wireless-Programmable Thermostat','Wireless-Programmable Thermostat'),
	('Smart Thermostat','Smart Thermostat'),
	('None','None'),
)

REMOVALS_CHOICES = (
	('Boiler','Boiler'),
	('Hot Water Cylinder','Hot Water Cylinder'),
	('Cold Water Storage Tank','Cold Water Storage Tank'),
	('Feed and Expansion Tank','Feed and Expansion Tank'),
	('Rubbish','Rubbish'),
)

NEW_FUEL_TYPE_DROPDOWN = (
	('Gas','Gas'),
	('LPG','LPG'),
	('Oil','Oil'),
	('Electric','Electric'),
	('None','None'),
)

NEW_BOILER_TYPE_DROPDOWN = (
	('Floor Standing - Conventional','Floor Standing - Conventional'),
	('Floor Standing - Combi','Floor Standing - Combi'),
	('Floor Standing - System','Floor Standing - System'),
	('Wall Hung - Conventional','Wall Hung - Conventional'),
	('Wall Hung - Combi','Wall Hung - Combi'),
	('Wall Hung - System','Wall Hung - System'),
)

NEW_BOILER_LOCATION_DROPDOWN = (
	('Kitchen','Kitchen'),
	('Bathroom','Bathroom'),
	('Bedroom','Bedroom'),
	('Utility','Utility'),
	('Airing Cupboard','Airing Cupboard'),
	('Lounge','Lounge'),
	('Loft','Loft'),
	('Garage','Garage'),
	('Other','Other'),
)

NEW_FLUE_SYSTEM_DROPDOWN = (
	('Vertical - Open Flue','Vertical - Open Flue'),
	('Vertical - Fan assisted','Vertical - Fan assisted'),
	('Horizontal','Balanced Flue'),
	('Horizontal','Fan Flue'),
)

NEW_FLUE_LOCATION_DROPDOWN = (
	('Ground Floor','Ground Floor'),
	('First Floor','First Floor'),
	('Second Floor','Second Floor'),
	('Third Floor','Third Floor'),
	('Fourth Floor','Fourth Floor'),
	('Fifth Floor','Fifth Floor'),
)

NEW_FLUE_DIAMETER_DROPDOWN = (
	('100mm','100mm'),
	('125mm','125mm'),
	('150mm','150mm'),
)

PLUME_MANAGEMENT_KIT_DROPDOWN = (
	('Not Required','Not Required'),
	('Required','Required'),
)

CONDENSATE_TERMINATION_DROPDOWN = (
	('Drain','Drain'),
	('Soak Away','Soak Away'),
	('Pumped','Pumped'),
)
NEW_CONTROLS_DROPDOWN = (
	('Wired - Programmer','Wired - Programmer'),
	('Wired - Room Thermostat','Wired - Room Thermostat'),
	('Wired - Cylinder Thermostat','Wired - Cylinder Thermostat'),
	('Wireless - Room Thermostat','Wireless - Room Thermostat'),
	('Wireless-Programmable Thermostat','Wireless-Programmable Thermostat'),
	('Smart Controls-Nest','Smart Controls - Nest'),
	('Smart Controls-ESI','Smart Controls - ESI'),
	('Use Existing','Use Existing'),
)

CWS_FLOW_RATE_DROPDOWN = (
	('4','4'),
	('5','5'),
	('6','6'),
	('7','7'),
	('8','8'),
	('9','9'),
	('10','10'),
	('11','11'),
	('12','12'),
	('13','13'),
	('14','14'),
	('15','15'),
	('16','16'),
	('17','17'),
	('18+','18+'),
)

NEW_FLUE_METRES_DROPDOWN = (
	('1','1'),
	('2','2'),
	('3','3'),
	('4','4'),
	('5','5'),
	('6','6'),
	('7','7'),
	('8','8'),
	('9','9'),
	('10','10'),
	('11','11'),
	('12','12'),
)

SYSTEM_TREATMENT_DROPDOWN = (
	('Chemical Flush & Inhibitor','Chemical Flush & Inhibitor'),
	('Magna Pro Flush & Inhibitor','Magna Pro Flush & Inhibitor'),
	('Power Flush & Inhibitor','Power Flush & Inhibitor'),
)

GAS_SUPPLY_DROPDOWN = (
	('Use existing supply','Use existing supply'),
	('New internal supply required','New internal supply required'),
	('New external supply required','New external supply required'),
)

GAS_SUPPLY_LENGTH_DROPDOWN = (
	('N/A','N/A'),
	('3-9m','3-9m'),
	('9-15m','9-15m'),
	('15-21m','15-21m'),
	('21-27m','21-27m'),
	('27m+','27m+'),
)

ASBESTOS_CONTAINING_MATERIALS_IDENTIFIED_DROPDOWN = (
	('No Asbestos Identified','No Asbestos Identified'),
	('Boiler','Boiler'),
	('Flue','Flue'),
	('CWS Tank','CWS Tank'),
	('Other ACM Identifed','Other ACM Identifed'),
)

ELECTRICAL_WORK_REQUIRED_DROPDOWN = (
	('Connect to existing wiring','Connect to existing wiring'),
	('New wiring to fuse spur','New wiring to fuse spur'),
	('New wiring S plan','New wiring S plan'),
	('New wiring Y plan','New wiring Y plan'),
	('New boiler on plug','New boiler on plug'),
)

BOILER_MANUFACTURER_DROPDOWN = (
	('Worcester Bosch','Worcester Bosch'),
	('Viessmann','Viessmann'),
	('Vaillant','Vaillant'),
	('Glowworm','Glowworm'),
	('Ideal','Ideal'),
	('Baxi','Baxi'),
	('Potterton','Potterton'),
)

MANUFACTURER_GUARANTEE_DROPDOWN = (
	('5 Years','5 Years'),
	('6 Years','6 Years'),
	('7 Years','7 Years'),
	('8 Years','8 Years'),
	('9 Years','9 Years'),
	('10 Years','10 Years'),
)

FLUE_COMPONENTS_DROPDOWN = (
	('Horizontal Flue Kit','Horizontal Flue Kit'),
	('Vertical Flue Kit','Vertical Flue Kit'),
	('Flue Extension','Flue Extension'),
	('Pair 45 Degree Bends','Pair 45 Degree Bends'),
	('Single 90 Degree Bend','Single 90 Degree Bend'),
	('Roof Flashing','Roof Flashing'),
)

PROGRAMMER_THERMOSTAT_DROPDOWN = (
	('Drayton Twin Channel Programmer','Drayton Twin Channel Programmer'),
	('Drayton Single Channel Programmer','Drayton Single Channel Programmer'),
	('Drayton RTS1 Room Thermostat','Drayton RTS1 Room Thermostat'),
	('Siemens Wireless Thermostat','Siemens Wireless Thermostat'),
	('Nest Smart Thermostat','Nest Smart Thermostat'),
	('ESI Smart Thermostat','ESI Smart Thermostat'),
	('Drayton Y Plan Pack','Drayton Y Plan Pack'),
	('Drayton S Plan Pack','Drayton S Plan Pack'),
	('None Required','None Required'),
)

CENTRAL_HEATING_SYSTEM_FILTER_DROPDOWN = (
	('Worcester Bosch 22mm System Filter','Worcester Bosch 22mm System Filter'),
	('Worcester Bosch 28mm System Filter','Worcester Bosch 28mm System Filter'),
	('MagnaClean 22mm System Filter','MagnaClean 22mm System Filter'),
	('MagnaClean 28mm System Filter','MagnaClean 28mm System Filter'),
	('SpiroVent 22mm System Filter','SpiroVent 22mm System Filter'),
	('SpiroVent 28mm System Filter','SpiroVent 28mm System Filter'),
	('Valiant (Boiler Protection Pack)','Valiant (Boiler Protection Pack)'),
	('None Required','None Required'),
)

SCALE_REDUCER_DROPDOWN = (
	('15mm in line scale reducer','15mm in line scale reducer'),
	('22mm in line scale reducer','22mm in line scale reducer'),
	('28mm in line scale reducer','28mm in line scale reducer'),
	('22mm water softener','22mm water softener'),
	('None Required','None Required'),
)

RADIATOR_REQUIREMENTS_DROPDOWN = (
	('N/A','N/A'),
	('Thermostatic Radiator Valves Only','Thermostatic Radiator Valves Only'),
	('Thermostatic Radiator Valves and Lock Shield','Thermostatic Radiator Valves and Lock Shield'),
	('New Panel Radiators and Valves','New Panel Radiators and Valves'),
)

ESTIMATED_DURATION_DROPDOWN = (
	('1 Day','1 Day'),
	('2 Days','2 Days'),
	('3 Days','3 Days'),
	('4 Days','4 Days'),
	('5 Days','5 Days'),
)


class FormStepOne(forms.Form):
	# Fields in this class are rendered in the quote_for_pdf.html file with the following notation
	# within double curly braces...
	# form_data.0.field_name e.g. form_data.0.customer_first_name
	customer_first_name = forms.CharField(max_length=100)
	customer_last_name = forms.CharField(max_length=100)
	customer_home_phone = forms.CharField(max_length=100)
	customer_mobile_phone = forms.CharField(max_length=100)
	customer_email = forms.EmailField()
	owner_or_tenant = forms.ChoiceField(choices=OWNER_OR_TENANT_DROPDOWN)
	#choice = forms.ModelChoiceField(queryset=ProductPrice.objects.filter(user = self.user, brand = 'Worcester Bosch'), empty_label = 'Select Product for quote')
	

class FormStepTwo(forms.Form):
	# Fields in this class are rendered in the quote_for_pdf.html file with the following notation
	# within double curly braces...
	# form_data.1.field_name e.g. form_data.1.installation_address
	installation_address = forms.CharField(max_length=100)
	street_address = forms.CharField(max_length=100)
	city = forms.CharField(max_length=100)
	county = forms.CharField(max_length=100)
	postcode = forms.CharField(max_length=100)
	property_type = forms.ChoiceField(choices=PROPERTY_TYPE_DROPDOWN)

class FormStepThree(forms.Form):
	# Fields in this class are rendered in the quote_for_pdf.html file with the following notation
	# within double curly braces...
	# form_data.2.field_name e.g. form_data.2.current_fuel_type
	current_fuel_type = forms.ChoiceField(choices=CURRENT_FUEL_TYPE_DROPDOWN)
	current_boiler_type = forms.ChoiceField(choices=CURRENT_BOILER_TYPE_DROPDOWN)
	current_boiler_location = forms.ChoiceField(choices=CURRENT_BOILER_LOCATION_DROPDOWN)
	current_flue_system = forms.ChoiceField(choices=CURRENT_FLUE_SYSTEM_DROPDOWN)
	current_flue_location = forms.ChoiceField(choices=CURRENT_FLUE_LOCATION_DROPDOWN)
	current_controls = forms.ChoiceField(choices=CURRENT_CONTROLS_DROPDOWN)
	
class FormStepFour(forms.Form):
	# Fields in this class are rendered in the quote_for_pdf.html file with the following notation
	# within double curly braces...
	# form_data.3.field_name e.g. form_data.3.removals
	removals = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
											 choices=REMOVALS_CHOICES)

class FormStepFive(forms.Form):
	# Fields in this class are rendered in the quote_for_pdf.html file with the following notation
	# within double curly braces...
	# form_data.4.field_name e.g. form_data.4.new_fuel_type
	new_fuel_type = forms.ChoiceField(choices=NEW_FUEL_TYPE_DROPDOWN)
	new_boiler_type = forms.ChoiceField(choices=NEW_BOILER_TYPE_DROPDOWN)
	new_boiler_location = forms.ChoiceField(choices=NEW_BOILER_LOCATION_DROPDOWN)
	new_flue_system = forms.ChoiceField(choices=NEW_FLUE_SYSTEM_DROPDOWN)
	new_flue_location = forms.ChoiceField(choices=NEW_FLUE_LOCATION_DROPDOWN)
	new_flue_diameter = forms.ChoiceField(choices=NEW_FLUE_DIAMETER_DROPDOWN)
	plume_management_kit = forms.ChoiceField(choices=PLUME_MANAGEMENT_KIT_DROPDOWN)
	condensate_termination = forms.ChoiceField(choices=CONDENSATE_TERMINATION_DROPDOWN)
	new_controls = forms.ChoiceField(choices=NEW_CONTROLS_DROPDOWN)
	cws_flow_rate = forms.ChoiceField(choices=CWS_FLOW_RATE_DROPDOWN)
	new_flue_metres = forms.ChoiceField(choices=NEW_FLUE_METRES_DROPDOWN)
	
class FormStepSix(forms.Form):
	# Fields in this class are rendered in the quote_for_pdf.html file with the following notation
	# within double curly braces...
	# form_data.5.field_name e.g. form_data.5.new_fuel_type
	system_treatment = forms.ChoiceField(choices=SYSTEM_TREATMENT_DROPDOWN)
	gas_supply = forms.ChoiceField(choices=GAS_SUPPLY_DROPDOWN)
	gas_supply_length = forms.ChoiceField(choices=GAS_SUPPLY_LENGTH_DROPDOWN)
	asbestos_containing_materials_identified = forms.ChoiceField(choices=ASBESTOS_CONTAINING_MATERIALS_IDENTIFIED_DROPDOWN)
	electrical_work_required = forms.ChoiceField(choices=ELECTRICAL_WORK_REQUIRED_DROPDOWN)

class FormStepSeven(forms.Form):
	# Fields in this class are rendered in the quote_for_pdf.html file with the following notation
	# within double curly braces...
	# form_data.6.field_name e.g. form_data.6.boiler_manufactureruel_type

	#boiler_manufacturer = forms.ChoiceField(choices=BOILER_MANUFACTURER_DROPDOWN)
	def __init__(self, *args, **kwargs):
		# Get the user to seed the filter on the boiler_manufacturer drop down.
		self.user = kwargs.pop('user')
		super(FormStepSeven, self).__init__(*args, **kwargs)
		self.fields['boiler_manufacturer'] = forms.ModelChoiceField(queryset=ProductPrice.objects.filter(user = self.user).order_by('brand').values_list('brand', flat=True).distinct(), to_field_name='brand',empty_label = 'Select Boiler Brand for quote')
	manufacturer_guarantee = forms.ChoiceField(choices=MANUFACTURER_GUARANTEE_DROPDOWN)
	flue_components = forms.ChoiceField(choices=FLUE_COMPONENTS_DROPDOWN)
	programmer_thermostat = forms.ChoiceField(choices=PROGRAMMER_THERMOSTAT_DROPDOWN)
	central_heating_system_filter = forms.ChoiceField(choices=CENTRAL_HEATING_SYSTEM_FILTER_DROPDOWN)
	scale_reducer = forms.ChoiceField(choices=SCALE_REDUCER_DROPDOWN)

	#field_order = ['boiler_manufacturer','flue_components','programmer_thermostat','central_heating_system_filter','scale_reducer', 'manufacturer_guarantee']
	
class FormStepEight(forms.Form):
	# Fields in this class are rendered in the quote_for_pdf.html file with the following notation
	# within double curly braces...
	# form_data.7.field_name e.g. form_data.7.radiator_requirements
	radiator_requirements = forms.ChoiceField(choices=RADIATOR_REQUIREMENTS_DROPDOWN)
	thermostatic_radiator_valves_size = forms.CharField(max_length=100)
	thermostatic_radiator_valves_type = forms.CharField(max_length=100)
	thermostatic_radiator_valves_quantity = forms.CharField(max_length=100)
	
class FormStepNine(forms.Form):
	# Fields in this class are rendered in the quote_for_pdf.html file with the following notation
	# within double curly braces...
	# form_data.8.field_name e.g. form_data.8.estimated_duration
	def __init__(self, *args, **kwargs):
		# Get the user to seed the filter on the drop down.
		self.user = kwargs.pop('user')
		self.manuf = kwargs.pop('manufacturer')
		super(FormStepNine, self).__init__(*args, **kwargs)
		self.fields['product_choice'] = forms.ModelChoiceField(queryset=ProductPrice.objects.filter(user = self.user, brand = self.manuf), empty_label = 'Select Product for quote')
	estimated_duration = forms.ChoiceField(choices=ESTIMATED_DURATION_DROPDOWN)
	description_of_works = forms.CharField(max_length=2000, widget=forms.Textarea(attrs={'rows':3, 'cols':20}))
	
	
class UserRegistrationForm(forms.Form):
	username = forms.CharField(
			required = True,
			label = 'Username',
			max_length = 32
		)
	email = forms.EmailField(
			required = True,
			label = 'Email',
			max_length = 64,
		)
	password = forms.CharField(
			required = True,
			label = 'Password',
			max_length = 32,
			widget = forms.PasswordInput()
		)


# File upload capability
class DocumentForm(forms.ModelForm):
	class Meta:
		model = Document
		fields = ('document', 'description')

# Pricing File Form
#class PricingFileForm(forms.ModelForm):
#	class Meta:
#		model = PricingFile
#		fields = ('document', 'description')		
		
# Installer details
class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('first_name','last_name','email','company_name','telephone', 'daily_work_rate', 'quote_prefix', 'cur_quote_no')
		
class UserProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('company_name',)

class ProductPriceForm(forms.ModelForm):
	
	class Meta:
		model = ProductPrice
		fields = ['brand', 'model_name', 'product_code','price','product_image']


	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		super(ProductPriceForm, self).__init__(*args, **kwargs)
		self.fields['product_image'].queryset=Document.objects.filter(user = self.user)


class EditQuoteTemplateForm(forms.Form):

	pdf_template_code = forms.CharField(widget=forms.Textarea(attrs={'rows':24, 'cols':60}))

	def __init__(self, user, *args, **kwargs):
		#self.user = kwargs.pop('user')
		self.user = user
		super(EditQuoteTemplateForm, self).__init__(*args, **kwargs)
		usr_pdf_template_file = Path(settings.BASE_DIR + "/templates/pdf/user_{}/quote_for_pdf.html".format(self.user.username))
		#usr_pdf_template_file = Path(settings.BASE_DIR + "/templates/pdf/user_test/quote_for_pdf.html")
		#print(usr_pdf_template_file)
		template_file = open(usr_pdf_template_file,'r')
		self.fields['pdf_template_code'].initial = template_file.read
		alert = None





