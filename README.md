# Quotepad

Quotepad is a full-stack web-based application that is designed to provide Software as a Service (Saas) initially focused on heating engineers carrying out surveys on user premises. The objective is to provide an easy to use tool for the engineer to build a quote based upon his findings during the survey. The user can upload their boiler image and branding, which can be added to the quote to provide a high level of customisation and then generate bespoke quotes for their customers, delivered as PDF's to the customer's email/ or printed. 

The site is designed to entice the user to subscribe to a monthly payment fee for the use of the service, however, some functionality is available for free.

[Check it out here!]([https://rorytesting.pythonanywhere.com/](https://rorytesting.pythonanywhere.com/))

## UX

The primary goal of Quotepad is to provide an application where heating engineers can generate bespoke quotations for there customers and then send these quotations via email, to generate more sales and improve business efficiency.

#### User Goals

-   Allow the user to register and upload their business information.
-   The user can create products that can be added as images to their bespoke quotations.
-   The user can create quotes for their customers.
-   The quotes can be printed or emailed as PDF files to their customers.
- Ensure the user can navigate the site easily and know what order to do things.

#### Business Goals

-   Decrease the time taken from the survey to quotation, therefore, improve the customer's experience and generating more sales for the heating engineers.
- Get engineers to sign up to a 15-pound monthly subscription service thereby making it a profitable piece of software with regular returns.

#### Ideal User

-   Heating engineers.
-   Computer savvy.
-   Can read English.
-   Wants to build bespoke quotations.

#### User Stories

-   As a user, I want to be able to log in and see my status.
-   As a user, I want to see what my quotes look like and edit them.
-   As a user, I want to be able to upload my branding.
-   As a user, I want to be able to create products that can be sold on the quotations.
-   As a user, I want to be able to navigate the site easily.
-   As a user, I want Quotepad to remember my previous quotes should they be needed.
-   As a user, I want to be able to reset my password should I forget it.
-   As a user, I want my customers to receive email quotations quickly.
-  As a user, I want the tool to help me generate more sales. 

#### Wireframes
[Landing Desktop](https://github.com/Rorywork/bquotepad/blob/master/wireframes/desktop-landing.PNG)
[Landing Tablet](https://github.com/Rorywork/bquotepad/blob/master/wireframes/tablet-landing.PNG)
[Landing Mobile](https://github.com/Rorywork/bquotepad/blob/master/wireframes/mobile-landing.PNG)
[Dashboard Desktop](https://github.com/Rorywork/bquotepad/blob/master/wireframes/desktop-dashboard.PNG)
[Dashboard Tablet](https://github.com/Rorywork/bquotepad/blob/master/wireframes/tablet-dashboard.PNG)
[Dashboard Mobile](https://github.com/Rorywork/bquotepad/blob/master/wireframes/mobile-dashboard.PNG)

#### Model Entity Relationship Diagram
[Click Here](https://github.com/Rorywork/bquotepad/blob/master/wireframes/Quotepad%20Entity%20Relationship%20Diagram.png)

## Features

#### Cross Application
Each page has a responsive navigation bar built using Bootstrap and incorporating the Boostrap Flatly theme. The navigation bar changes when the user is logged in and features the options glyph, this is a dropdown that allows users to navigate parts of the site. When logged out the navigation bar simple features a login button and a register button. 

Each page also has the footer which is the same colour as the navigation bar. It features the social links as well as a link to my Github so anyone interested in who built the application can find out more about my work. 

I used white text on a dark blue background to make it clear and easy to read with links highlighted in a light green colour. 

#### Landing
The landing page is used to entice the user to sign up for Quotepad. It contains two sign up buttons at the top and bottom so it is clear to the user where to go. I use the Bootstrap grid system to provide information about what Quotepad does and who the application is for. 

There is a 6 step process section which uses a list to explain to the user how to use the application and to guide users towards what to expect. Underneath this is a quote from a customer who has tried quotepad. Below this is the Trustpilot Logo used to build trust and assure the user this is a credible solution. 

#### Forms

The majority of the pages on the site utilise the same types of form to write information to the database and capture what is needed. I use the Django form tool regularly and they are then styled using Bootstrap classes so that they all look consistent. When you click on a form field the field will highlight in light blue and utilise a shadow effect. Buttons on forms either use the btn-primary or btn-secondary class to ensure consistent styling. 

The forms are set on a grey background which sites on the whitespace of the page to make them stand out yet remain a clean easily visible design. 

Upon completion of forms, a sweet alert utilising javascript pops up and informs the user the information has been captured before redirecting the user back to the dashboard. 

#### Edit Information

The edit information form specifically features a section called daily work rate. This information is captured and used later in quotation creation to tell the customer what part of the cost is for the engineer's time and what part of it is the cost of materials. This was added based on some user feedback I got from a heating engineer. 

#### Dashboard
The Dashboard page is the hub of Quotepad and shows the user what to do to use the tool. It uses six different cards that are numbered. These cards begin with red gradients that change to green once the instructions within the card are completed. This gives the site flow and makes it clear to the user what they need to do next to use the product effectively. 

The cards have borders and a box-shadow effect on hover which makes them stand out on the page and encourages the user to click on them. The text sits on a dark filter which makes it more readable. These are built using a transparent background colour class. 

The dashboard also uses Django to render the user's username next to the Hello text so the user can easily see that they are logged in. 

#### View Your Quote Layout
This section opens a test PDF using test data which the user can use to see what their quotations will look like. They can then go to the upload images and add product pages to make changes if necessary. 

This is useful as it lets the engineer see whether the quote is as they would like it before completing the longer surveys.

#### Subscribe
The subscribe page uses a Bootstrap jumbotron feature to entice the user to purchase Quotepad. Below this is are quotes from other users used to build trust. When you click to purchase, a Stripe checkout modal will appear which takes the user's email and payment details. Upon completion of this, the user will be able to access the quotepad step itself and start completing surveys. 

#### Complete a Quote
Once the user has completed the other steps they can now complete a quote. This is a large multi-page form which saves the information each stage so the user can navigate back and forth through the various questions. Many of the fields use the required attribute as these are needed to build the quotation. Some of them are optional. There are several pages of questions and at the end, the user can select which product (created earlier) they are quoting for. Alongside this, they can input into a description field and relevant further information. 

Upon completing the quote can be viewed as a PDF, printed or emailed to the email provided in the customer email field. Please note the service I am currently utilising to send the emails is free and can sometimes take a little bit of time to send out the email, It is proposed in the future I will purchase a more stable service should this become a real-life product. For not it is purely for my Code Institute submission.  

#### Previous Quotes
The previous quotes option on the navigation bar will only appear once the user has created a minimum of one quote. This page lists all the historical quotes should the engineer need to go back and find one. 

#### Features to be implemented in future

-   Privacy policy, as the website captures user data I will create a policy in the future.
-   GDPR cookie opt-in - this will be a pop up on the landing page and the register page so the user can decide what cookies they want.
-   In the future, it is planned users will be able to further edit the quotation using a built-in editor which will allow even more bespoke quotations.
- In the future, it is proposed we use a better service for delivery of the emails so that it is always instant and customers do not have to wait for their quotes. 
- 
## Technologies Used

-   HTML
-   CSS
-   Javascript
-   Python
-   Django
-   [Bootstrap](https://getbootstrap.com/)
-   [MySql]([https://www.mysql.com/](https://www.mysql.com/)) 

##### The following libraries were also used:
- Django-formtools
- Pillow
- Xhtml2pdf
- Stripe
- Mailgun

## Notes on the database
The initial local development has been done using the db.sqlite3 database however in deployment the MySQL environment will be used.

## Deployment to PythonAnywhere

The project was deployed to PythonAnywhere as opposed to Heroku for the primary reason that Heroku (free account) deletes uploaded image files periodically which makes it unsuitable for this project which relies heavily on uploaded images from users.
1. Go to [https://www.pythonanywhere.com/](https://www.pythonanywhere.com/)
2. Create an account and verify this account.
3. Click on the $ Bash button underneath New console, this will open as Bash terminal.
4.  `git clone https://github.com/Rorywork/bquotepad`
5.  `mkvirtualenv django2 --python=/usr/bin/python3.6`  
6. If in another session you need to reactivate the virtual environment then type: `workon django2`
7. You now need to install django type`pip install django`
8. Install all the Python/Django libraries that are required by my project (using pip install like above) see below:
* `pip install Django-formtools` Multi-page form management tool
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
14. Delete all the boilerplate code and add the code contained within this [file](https://github.com/Rorywork/bquotepad/blob/master/pythonanywhere_wsgi_file.py). Then click the green save button. 
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

Following these instructions will deploy Quotepad on PythonAnywhere.

## Testing

#### W3

I used automated testing with the W3 HTML checker. This displays any syntax errors within the HTML code. I used it on each page on the site to try and ensure there were no errors.

One of the challenges I encountered was that due to the use of Django, parts of the code which were not in HTML were picked up by the validator as errors when in fact they were necessary for the application to run.

I also ran the CSS code through the W3 validator to remove unnecessary bugs or errors.

#### Audits / Chrome Dev Tools

I used Chrome Dev Tools to run audits on the performance, accessibility and best practices on the website for both mobile and desktop layouts. I then took on board the feedback and made changes to my website where necessary to achieve higher scores.

#### Manual Testing

I have tested each page on the following browsers:

-   Google Chrome
-   Apple Safari
-   Microsoft Edge
-   Internet Explorer 
#### Devices Tested

-   iPhone X
-   iPhone 8
-   Microsoft Surface Book Pro
-   Samsung Tablet
-   Ultra Large Samsung Display
-   iPad Pro
-   iPad

#### Django Testing (Automated)

I used Django testing on Qutepad utilising the standard unittest library. This framework adds API methods and tools to help test web and Django specific behavior. The tests use 'assert' methods to test that expressions return in true or false values. Or that two values are equal.

Three aspects have been tested and broken into three separate files.

 test_models.py - used to validate the models used in the application. 
test_forms.py - used to validate the forms used in the application.
test_views.py - used to validate the views in the application.

It is proposed more testing is done should Quotepad be launched as a commercial product. A representative sample is included with this submission.

#### Debugging
During my user tests and having other users test the application, there were a lot of different examples where I had to debug, including:

- The navigation bar was initially displaying previous quotes as an option when no quotes had been uploaded. I used Django logic to fix this and ensure it only appeared when at least one quote existed. 

- Several bugs relating to the create a quote section without the user being subscribed became apparent upon user tests. To fix these several session variables have been used to capture the user state and progress to ensure a real quote could not be created without previous steps being complete.

- Problems with the layout of the PDF file not rendering the way it should require a significant degree of fine-tuning to get the layout correct. A known limitation is that if any of the free text fields are entered as a long string the layout can sometimes be adversely affected to a minor degree. It is proposed this layout is reviewed for future versions.

- A bug that was identified was that if two separate users uploaded a file with the same filename this would cause a problem. To remedy this separate individual folder are automatically created by the website to store images. 

- The requirement to use environment variables for the Django secret key and other secret keys proved to be challenging and took a degree of debugging and testing to resolve. This was highlighted to me by my tutor when he reviewed my code.

## Credits


## Code

-   [W3 Schools](https://www.w3schools.com/)  - a very useful site for finding out how to do specific fixes.
-   [Traversy](https://www.youtube.com/user/TechGuyWeb)  provided several tutorials I followed to help me with certain features in my application.
- [https://sweetalert2.github.io/](https://sweetalert2.github.io/) - Sweet Alert provided the pop-ups which happen when you input forms. 

#### Acknowledgements
-   My tutor Simen Daehlin provided useful links, tips, and advice on improving the website.
-   [Check out Simen's Github](https://github.com/Eventyret)

Disclaimer

The content of this website is currently for entertainment and educational purposes only, it does not currently have a commercial function. Users who upload images are responsible for the content of those images and ensuring they do not breach copyright laws.