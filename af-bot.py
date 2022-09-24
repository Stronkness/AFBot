import requests
import json
import smtplib
import os
from bs4 import BeautifulSoup
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()

def downloadAF():
    """
    Data scraped AFBostäders API for vacant accommodations

    @return the data of the accommodations
    """
    page_data = requests.get("https://api.afbostader.se:442/redimo/rest/vacantproducts")
    page_data = page_data.text
    return page_data

def approvedAccommodationFilter(accommodation_type, rent, sqr_meters, floor, area, rooms):
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
    approved_areas = ["Magasinet", "Marathon", "Studentlyckan", "Ulrikedal", "Vegalyckan"]
    if (
        accommodation_type == "Lägenhet" and int(rent) <= 9000 and 
        float(sqr_meters) >= 40.0 and int(floor) != 1 and
        int(rooms) >= 2 and area in approved_areas
       ): 
         return True
    else: 
         return False

def sendEmail(approved):
    """
    Sends an email if the requirements for an apartment is met.
    Provides with several apartments in the same email if it occurs more than once.

    @param approved: List, contains all approved accommodations to be sent
    """
    sender_email_adress = os.environ.get("EMAIL_ADDRESS")
    sender_email_password = os.environ.get("EMAIL_PASSWORD")

    receiver_email_adress = os.environ.get("RECEIVER_EMAIL_ADDRESS")
    receiver_email_adress_2 = os.environ.get("RECEIVER_EMAIL_ADDRESS_2")

    msg = EmailMessage()
    msg["Subject"] = "New AFBostäder accommodations found!"
    msg["From"] = sender_email_adress
    msg["To"] = receiver_email_adress + "," + receiver_email_adress_2
    content = ""
    for accommodation in approved:
        content += accommodation + "\n"
    msg.set_content(content)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp: #port 465? 587?
        smtp.ehlo()
        smtp.login(sender_email_adress, sender_email_password)
        smtp.send_message(msg)
        smtp.quit()

def main():
    data = downloadAF()
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
        if approvedAccommodationFilter(accommodation_type, rent, sqr_meters, floor, area, rooms):
            object_id = accommodation["productId"]
            URL = "https://www.afbostader.se/lediga-bostader/bostadsdetalj/?obj=" + object_id
            message = f"{area} {rent}:- {sqr_meters}m^2 \n{URL}\n"
            approved.append(message)
    if approved:
        sendEmail(approved)

if __name__ == "__main__":
    main()