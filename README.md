# AFBot

This is a AFBostäder bot programmed in Python for easy filtering to find the perfect student accommodation for you!

This script can be used by users who have no experience in programming before. Please see the section [How to run it](#how-to-run-it) for further information.

For translations, please see the translations folder in this repository.

### How it works

Once the script runs, data from AFBostäder's API is downloaded containing information in a JSON file about rent, area, floor and more.
Every JSON object (accommodation) contains parameters for filtering, these can be decided yourself to suit your requirements. These parameters are then sent to a function which checks if your requirements are met, if they are the function will approve this accommodation and include it in an email.

This email is using GMail's SMTP Protocol with a dumpster account to send emails to the recipients. Every approved accommodation will be inserted in a list with a string containing the area, rent and square meters with the URL to the accommodation. When every accommodation have been checked on the website the list of approved accommodations will be sent to an function which prepares an email. Here we export an gmail account with its corresponing App password which is stored in a ```.env``` file where also the recipients email addresses are stored in. You can send to several addresses with this function. Keep in mind that the ```.env``` file must be created in order to function and to not expose sensitive credentials directly in the code. How to create a ```.env``` file is explained in ```.env```. 

An Email object is created containing all the information SMTP needs in order to send it. In the following code is how SMTP will send an email with the information acquired. SMTP is exposed in port 465 and uses a login function with the dumpster account's credentials exported from the ```.env``` file to login to the GMail service and sends the message. We then quit SMTP so that nothing unusal happens.

```python
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.ehlo()
        smtp.login(sender_email_adress, sender_email_password)
        smtp.send_message(msg)
        smtp.quit()
```

For viewing an example hos the JSON object is storing different parameters, please see [example.json](example.json).

Currently the bot is sending an email if an accommodation have been added which the receiever hav'nt heard about. In other words you should not get the same accommodation twice in your mail.


### How to run it

To be able to run the script you need Python and other dependencies installed.
If you get stuck or are very unsure what to do and need hints, check in the section [Still unsure how do preparations?](#still-unsure-how-do-preparations)

#### Install software
##### Python
If you are unsure, open your command line (search for Terminal or CMD) and run this line
```bash
python3 --version
```
The output should be something similar to this
```bash
Python 3.10.6
```
If this is not the case then simply follow the guideline below for your respective OS.

[Linux](https://docs.python-guide.org/starting/install3/linux/)

[Windows](https://www.digitalocean.com/community/tutorials/install-python-windows-10    )

[MacOS](https://www.dataquest.io/blog/installing-python-on-mac/)


##### dotenv

Python-dotenv reads key-value pairs from a .env file and can set them as environment variables. It helps in the development of applications and also keep some values secure if you choose to share the code somewhere as you don't share the ```.env``` file.

Open up your terminal and type in the following to install dotenv
```bash
pip install python-dotenv
```
If this doesn't work try with
```bash
pip3 install python-dotenv
```


#### Requirements
To be able to run the script correctly you need to create an environment file and use a gmail account.

##### .env
The ```.env``` file contains information about the dumpster account to be used and the receivers email addresses. Create a ```.env``` file in the same folder as the script and insert the following

```c#
EMAIL_ADDRESS=example@gmail.com
EMAIL_PASSWORD=apppasswordhere
RECEIVER_EMAIL_ADDRESS=example1@gmail.com
```

As the script can use more than one address to send to it is posibble to add more if you like to. Insert your dumpster accounts email address and the App password. Check the next section for more information about this. Don't forget to add your own email address as the receiver

##### Dumpster account
I highly recommend to use an dumpster account for the bot, for security reasons. To create a dumpster account simply go to [Create account GMail](https://support.google.com/mail/answer/56256?hl=en). To not expose your password to in the ```.env``` you can assign a App password to your account. Follow this [App password](https://support.google.com/mail/answer/185833?hl=en-GB) guide or this one (with pictures) [App password with pictures](https://devanswers.co/create-application-specific-password-gmail/) and paste it in the ```ÈMAIL_PASSWORD```in the ```.env```file.  It should look like a bunch of letters mixed in a blender like this **vhgksciebfjvlsk**. 

#### Running the script

If you have Python installed and everything setup please go the the directory where you cloned/downloaded the program to. You can do this in the Terminal or in your file manager.
Smply double-click the script [af-bot.py](af-bot.py) or run the following in the terminal
```
python3 af-bot.py
```
No output will be printed out if everything is correctly setup and you should have an email in your address you typed in the [.env](#.env) file. If an error occurs, please check that every step above is done and installed.


#### Specify your needs to the script

The current requirements stated in the script is for my own need. If you don't want these configurations then I have added some explanation at the top of the [af-bot.py](af-bot.py) what the parameters do and how they can look like. 

```python
# The users requirements for the accommodation
approved_areas = ["Magasinet", "Studentlyckan", "Ulrikedal", "Vegalyckan"] # The areas to choose from is stated here https://www.afbostader.se/lediga-bostader/bostadsomraden/, just type the name with "" and separate each name with a ,
highest_rent = 9000 # State the highest rent you can think of, if you have no upper limit then type in a very high number
accommodation_choice = "Lägenhet" # "Lägenhet" for apartments or "Korridorrum" for corridor rooms
minimum_sqrMtrs = 40.0 # State the minimal square meters of the accommodation, if size isn't a problm just type in a very low number
unwanted_floor = 1 # If you have a certain floor you don't want to live in type this in, only works for one floor
minimum_rooms = 2 # State the minimum amount of rooms that you want in the accommodation, only applicable for "Lägenhet"
```

This is the parameters that MUST be filled in order for the bot to work. If you know what you are doing then you can erase or even add requirements in the ***approved_accommodation_filter*** function. If you don't know anything about coding then use the parameters above or try to mimic what I've done in the python file.


#### Automated execution

To make the script autonomous one can do it in several steps. You can use for example Docker and Cron-jobs.
The easiest way of these two are Cron-jobs. Please see the guide for your respective OS to apply the script using Cron-jobs:

[Linux](https://www.freecodecamp.org/news/cron-jobs-in-linux/)

[Windows](https://active-directory-wp.com/docs/Usage/How_to_add_a_cron_job_on_Windows/index.html)

[MacOS](https://anvilproject.org/guides/content/creating-links)

For more information about Cron-jobs, please see the following link [Cron Job: A Comprehensive Guide for Beginners](https://www.hostinger.com/tutorials/cron-job)


### Still unsure how do preparations?

If you still feel clueless about how to prepare everything for the script then here are some hints that might help you.

- You don't actually have to look if Python is installed if you feel unsure about terminal use. You can just try to install it directly through the link (or follow the guide). If it is already installed it will tell you that or simply update the version to a newer one.
- For creating the ```.env``` file simply go the the catalog where you have this project and create a File without any type. This can be done in the terminal and in Notepad for Windows. Go into Notepad and add the parameters explained above in the [.env](#.env) section. Save the file and when naming the file typ in ".env" with the quotation marks, that will create a file with no extensions. For MacOS there should be a similar version to this like Notepad.
- If pip doesn't work try this guide [Geek-for-Geeks](https://www.geeksforgeeks.org/how-to-install-python-libraries-without-using-the-pip-command/) with the following [PyPI](https://pypi.org/project/python-dotenv/) link. Currently, it is difficult to install pip without terminal usage.
- For running the python script it is neccessary to do it in the terminal. Currently, it is quite difficult to make the script run when double-clicking the file as in the good old days. Remember that you can still apply [Cron-jobs](#automated-execution) to make it autonomous. But first make sure that the script works with your dumpster account and parameters.
