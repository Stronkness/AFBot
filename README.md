# AFBot

This is a AFBostäder bot programmed in Python for easy filtering to find the perfect student accommodation for you!

This script can be used by users who have no experience in programming before. Please see the section [How to run it](#how-to-run-it) for further information.


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


### How to run it

To be able to run the script you need Python and other dependencies installed.

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
If this is not the case then simply follow the guideline below for your respective OS

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

##### Dumpster account

#### Running the script

If you have Python installed and everything setup please go the the directory where you cloned/downloaded the program to. You can do this in the Terminal or in your file manager.
Smply double-click the script [af-bot.py](af-bot.py) or run the following in the terminal
```
python3 af-bot.py
```
No output will be printed out if everything is correctly setup and you should have an email in your address you typed in the [.env](#.env) file. If an error occurs, please check that every step above is done and installed.


#### Automated execution

To make the script autonomous one can do it in several steps. You can use for example Docker and Cron-jobs.
The easiest way of these two are Cron-jobs. Please see the guide for your respective OS to apply the script using Cron-jobs:

[Linux](https://www.freecodecamp.org/news/cron-jobs-in-linux/)

[Windows](https://active-directory-wp.com/docs/Usage/How_to_add_a_cron_job_on_Windows/index.html)

[MacOS](https://anvilproject.org/guides/content/creating-links)

For more information about Cron-jobs, please see the following link [Cron Job: A Comprehensive Guide for Beginners](https://www.hostinger.com/tutorials/cron-job)
