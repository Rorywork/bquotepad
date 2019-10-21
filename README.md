# Quotepad

Quotepad is an full-stack web based application which is designed to provide Software as a Service (Saas) initially focused on heating engineers carrying out surveys in user premises. The objective is ton provide an easy to use tool for the engineer to build a quote based upon his findings during the survey. The user can upload their boiler image and branding, which can be added to the quote to provide a high level of customisation and then generate bespoke quotes for thir customers, delivered as PDF's to the customer's email/ or printed. 

The site is designed to entice the user to subscribe to a monthly payment fee for the use of the service, however some functionality is available for free.

## Notes on the database
The intial local development has been done using the db.sqlite3 database however in deployment the MySQL environment will be used.

## Deployment to PythonAnywhere

The project was deployed to PythonAnywhere as opposed to Heroku for the primary reason that Heroku (free account) deletes uploaded image files periodically which makes it unsuitable for this project which relies heavily on uploaded images from users.
1. Go to [https://www.pythonanywhere.com/](https://www.pythonanywhere.com/)
2. Create a an account and verify this account.
3. Click on the $ Bash button underneath New console, this will open as Bash terminal.
4.  `git clone https://github.com/Rorywork/bquotepad`
5.  `mkvirtualenv django2 --python=/usr/bin/python3.6`  
6. If in another session you need to reactivate the virtual environment then type: `workon django2`
7. You now need to install django type`pip install django`
8. Install all the Python/Django libraries that are required by my project (using pip install like above) see below:
* `pip install Django-formtools` Multi page form management tool
* `pip install Pillow` Managing image uploads
* `pip install Xhtml2pdf` HTML to PDF rendering library
* `pip install stripe` Payment processing library
* `pip install mysqlclient` Python library for MySQL database
* `pip install django-mailgun` Email service library

9. Open another window (keep the bash terminal open) - go to the web tab and click on  Add a new web app button, then click next.
10. Select Manual Configuration, then select Python 3.6, then click next.
11. You will now be in the configuration screen, go to the virtualenv: section and click on *Enter path to a virtualenv, if desired*
12. Type `django2` and click the tick button.
13. In the Code section click on the link for the WSGI configuration file.
14. Delete all the boilerplating code and add the code contained within this [file](https://github.com/Rorywork/bquotepad/blob/master/pythonanywhere_wsgi_file.py). Then click the green save button. 
15. Click the burger button in top right, then click on *files*.
16. Navigate to the `settings.py` and click on it. Update the below lines:
* `ALLOWED_HOSTS = ['bquotepad.pythonanywhere.com']`
*  `STATIC_ROOT = '/home/bquotepad/static'`
17. Click the green save button.
18. Go to the web tab (inside the burger button) and find the *Static files:* section.
* Click *Enter URL*  and type `/static/`, then click the blue tick.
* Click *Enter Path* and type `[/home/Rorywork/bquotepad/static]`, then click the blue tick.

### Initialising MySQL

1. Click the *Databases* tab from the main page on PythonAnywhere.
2. Enter a suitable password and click *Initialize MySQL*.
3. Enter a name for the database within the *Create a database* section and click *Create*.
4. Open the `settings.py` file from earlier and add the following code to the *DATABASES* section [database_entry_for_settings.txt](https://github.com/Rorywork/bquotepad/blob/master/database_entry_for_settings.txt) then click Save.
5. Go back to the bash terminal.
6. Navigate to the location of `manage.py` and enter the following commands to create the models for the project:
* `python manage.py makemigrations`
* `python manage.py migrate`
* `python manage.py createsuperuser` then enter your credentials for the admin tool within Django.

### Create Admin Groups

1. Go to the Django admin console, sign in as the superuser created earlier and create the following groups.
* Subscribed
* created_quote
* created_quote_template 

2. These groups are used to keep track of user functionality within the modules of the site. I.e a user placed in the *Subscribed* group has paid a subscription and has full access to Quotepad.
 
### Mailgun 
1. Register an account on [https://www.mailgun.com/](https://www.mailgun.com/)  
2. You will need a credit card or debit card to register however you can select the *Concept Plan* which will allow you to send 10,000 emails free of charge. This will be suitable for non-production use. Click on Go to Dashboard.
3. In `settings.py` replace the email settings with the following:
* `EMAIL_BACKEND = 'django_mailgun.MailgunBackend'`
* `MAILGUN_ACCESS_KEY = 'your access key'`
* `MAILGUN_SERVER_NAME ='your server name'`

Following these instrcutions will deploy Quotepad on PythonAnywhere.


Author credit for the icons

        <div>Icons made by <a href="https://www.flaticon.com/authors/smashicons" title="Smashicons">Smashicons</a> from <a href="https://www.flaticon.com/"     title="Flaticon">www.flaticon.com</a></div><div>Icons made by <a href="https://www.flaticon.com/authors/good-ware" title="Good Ware">Good Ware</a> from <a href="https://www.flaticon.com/"     title="Flaticon">www.flaticon.com</a></div><div>Icons made by <a href="https://www.flaticon.com/authors/monkik" title="monkik">monkik</a> from <a href="https://www.flaticon.com/"     title="Flaticon">www.flaticon.com</a></div><div>Icons made by <a href="https://www.flaticon.com/authors/icongeek26" title="Icongeek26">Icongeek26</a> from <a href="https://www.flaticon.com/"     title="Flaticon">www.flaticon.com</a></div><div>Icons made by <a href="https://www.flaticon.com/authors/pixelmeetup" title="Pixelmeetup">Pixelmeetup</a> from <a href="https://www.flaticon.com/"     title="Flaticon">www.flaticon.com</a></div><div>Icons made by <a href="https://www.flaticon.com/authors/smalllikeart" title="smalllikeart">smalllikeart</a> from <a href="https://www.flaticon.com/"     title="Flaticon">www.flaticon.com</a></div>