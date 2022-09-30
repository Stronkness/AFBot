from re import S
import requests
import json
import smtplib
import os
from bs4 import BeautifulSoup
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# The users requirements for the accommodation
approved_areas = ["Magasinet", "Studentlyckan", "Ulrikedal", "Vegalyckan"] # The areas to choose from is stated here https://www.afbostader.se/lediga-bostader/bostadsomraden/, just type the name with "" and separate each name with a ,
highest_rent = 9000 # State the highest rent you can think of, if you have no upper limit then type in a very high number
accommodation_choice = "Lägenhet" # "Lägenhet" for apartments or "Korridorrum" for corridor rooms
minimum_sqrMtrs = 40.0 # State the minimal square meters of the accommodation, if size isn't a problm just type in a very low number
unwanted_floor = 1 # If you have a certain floor you don't want to live in type this in, only works for one floor
minimum_rooms = 2 # State the minimum amount of rooms that you want in the accommodation, only applciable for "Lägenhet"

already_sent_accommodations = []
newly_approved = []

def logger(sending):
    """
    Creates a logger file which will be used for logging events based on the output of sending the mail.
    If logger file is created already then no new file wil be created.
    Is stored in the repository directory.
    Is created as a .txt file for easier user-experience on Windows and MacOS. Doesn't matter for Linus.
    """
    file = open("logger.txt", "a")

    if sending:
        logger_info = ""
        for accommodation in newly_approved:
            logger_info += accommodation + "\n"
    else:
        logger_info = f"No new accommodations. E-mail not sent"

    now = datetime.now()
    current_time_day = now.strftime("%Y-%m-%d %H:%M:%S")

    flavor_text_start = f"[LOG EVENT] {current_time_day}"
    in_between = "\n{ \n"
    flavor_text_end = "\n} \n\n"
    new_log = flavor_text_start + in_between + logger_info + flavor_text_end

    file.write(new_log)
    file.close()


def write_accommodations_to_file():
    """
    Writes every approved accommodation to the file for future checks
    """
    file = open("sent_accommodations.txt", "w+")
    for element in newly_approved:
        file.write(element + "\n")
    file.close()


def prepare_already_sent():
    """
    Reads a text file to prepare the accommodations which have been sent already.
    Creates a new text file if it does not exist
    """
    file = open("sent_accommodations.txt", "w+")
    sent_accomodations = file.readlines()
    for element in sent_accomodations:
        already_sent_accommodations.append(element[:len(element)-1])
    file.close()


def check_post_expiration_date():
    """
    Filters out the accommodations which is not on the website anymore
    """
    for element in already_sent_accommodations:
        expire_date = datetime.strptime(element.split()[1], "%Y-%m-%d")
        present_time = datetime.now()
        if present_time.date() > expire_date.date():
            already_sent_accommodations.remove(element)


def download_af():
    """
    Data scraped AFBostäders API for vacant accommodations

    @return the data of the accommodations
    """
    page_data = requests.get("https://api.afbostader.se:442/redimo/rest/vacantproducts")
    page_data = page_data.text
    return page_data


def approved_accommodation_filter(accommodation_type, rent, sqr_meters, floor, area, rooms):
    """
    Filters out the apartments which suits the requirements

    @param accomodation_type: String, tells if the accommodation is an Lägenhet or Korridorrum
    @param rent: String, states the rent of the accommodation
    @param sqr_meters: String, states the size in square meters of the accommodation
    @param floor: String, states the floor the accommodation is located in
    @param area: String, states the area the accommodation is located in
    @param rooms: String, states the amount of rooms the accommodation have

    @return the condition if the accommodation is approved or not
    """
    if accommodation_choice == "Korridorrum":
        if (
            accommodation_type == accommodation_choice and 
            int(rent) <= highest_rent and 
            float(sqr_meters) >= minimum_sqrMtrs and 
            int(floor) != unwanted_floor and
            area in approved_areas
        ): 
            return True
        else: 
            return False

    else:
        if (
            accommodation_type == accommodation_choice and 
            int(rent) <= highest_rent and 
            float(sqr_meters) >= minimum_sqrMtrs and 
            int(floor) != unwanted_floor and
            int(rooms) >= minimum_rooms and 
            area in approved_areas
        ): 
            return True
        else: 
            return False


def send_email(approved):
    """
    Sends an email if the requirements for an apartment is met.
    Provides with several apartments in the same email if it occurs more than once.

    @param approved: List, contains all approved accommodations to be sent
    """
    sender_email_adress = os.environ.get("EMAIL_ADDRESS")
    sender_email_password = os.environ.get("EMAIL_PASSWORD")

    receiver_email_adress = os.environ.get("RECEIVER_EMAIL_ADDRESS")

    msg = EmailMessage()
    msg["Subject"] = "New AFBostäder accommodations found!"
    msg["From"] = sender_email_adress
    msg["To"] = receiver_email_adress
    content = ""
    for accommodation in approved:
        content += accommodation + "\n"
    msg.set_content(content)
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.ehlo()
        smtp.login(sender_email_adress, sender_email_password)
        smtp.send_message(msg)
        smtp.quit()


def main():
    data = download_af()
    soup = BeautifulSoup(data, "html.parser")
    json_site = json.loads(soup.text)
    products = json_site["product"]
    accommodations = [x for x in products]
    approved = []
    for accommodation in accommodations:
        accommodation_type = accommodation["type"]
        rent = accommodation["rent"]
        sqr_meters = accommodation["sqrMtrs"]
        floor = accommodation["floor"]
        area = accommodation["area"]
        rooms = accommodation["shortDescription"][0]
        if approved_accommodation_filter(accommodation_type, rent, sqr_meters, floor, area, rooms):
            object_id = accommodation["productId"]
            check = accommodation["reserveUntilDate"]
            check = f"{object_id} {check}"
            if check not in already_sent_accommodations:
                URL = f"https://www.afbostader.se/lediga-bostader/bostadsdetalj/?obj={object_id}&area={area}&mode=0"
                message = f"{area} {rent}:- {sqr_meters}m^2 \n{URL}\n"
                approved.append(message)
                newly_approved.append(check)
    if approved:
        write_accommodations_to_file()
        send_email(approved)
    logger(True) if newly_approved else logger(False)

if __name__ == "__main__":
    prepare_already_sent()
    check_post_expiration_date()
    main()
