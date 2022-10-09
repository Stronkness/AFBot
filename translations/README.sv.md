# AFBot

Det här är en AFBostäder-bot programmerad i Python för enkel filtrering för att hitta det perfekta studentboendet för dig!

Detta skript kan användas av användare som inte har någon erfarenhet av programmering tidigare. Se avsnittet [Hur man kör skriptet](#hur-man-körskriptet) för mer information.


### Hur det fungerar

När skriptet körs laddas data från AFBostäders API ned innehållande information i en JSON-fil om hyra, område, våning med mera.
Varje JSON-objekt (boende) innehåller parametrar för filtrering, dessa kan bestämmas själv för att passa dina krav. Dessa parametrar skickas sedan till en funktion som kontrollerar om dina krav är uppfyllda, om de är så kommer funktionen att godkänna detta boende och inkludera det i ett e-postmeddelande.

Det här e-postmeddelandet använder Gmails SMTP-protokoll med ett dumpster-konto för att skicka e-postmeddelanden till mottagarna. Varje godkänt boende kommer att infogas i en lista med en sträng som innehåller område, hyra och kvadratmeter med URL till boendet. När varje boende har kontrollerats på hemsidan kommer listan över godkända boenden att skickas till en funktion som förbereder ett e-postmeddelande. Här exporterar vi ett gmail-konto med dess motsvarande App-lösenord som lagras i en ```.env```-fil där även mottagarnas e-postadresser finns lagrade i. Du kan skicka till flera adresser med denna funktion. Tänk på att filen ```.env``` måste skapas för att fungera och för att inte exponera känsliga referenser direkt i koden. Hur man skapar en ```.env```-fil förklaras i [.env](#.env).

Ett e-postobjekt skapas som innehåller all information som SMTP behöver för att skicka det. I följande kod är hur SMTP skickar ett e-postmeddelande med den information som erhållits. SMTP exponeras i port 465 och använder en inloggningsfunktion med dumpsterkontots referenser exporterade från filen ```.env``` för att logga in på Gmail-tjänsten och skicka meddelandet. Vi avslutar sedan SMTP så att inget ovanligt händer.

```python
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.ehlo()
        smtp.login(sender_email_adress, sender_email_password)
        smtp.send_message(msg)
        smtp.quit()
```

För att se ett exempel på hur JSON-objektet lagrar olika parametrar, se [example.json](example.json).

För närvarande skickar botten ett e-postmeddelande om ett boende har lagts till som mottagaren inte har hört talas om. Du ska med andra ord inte få samma boende två gånger med e-postmeddelandet.


### Hur man kör skriptet

För att kunna köra skriptet behöver du Python och andra dependencies installerade.

#### Installera mjukvara
##### Python
Om du är osäker om du har Python installerat öppna din kommandorad (sök efter Terminal eller CMD) och kör den här raden
``` bash
python3 --version
```
Utskriften bör vara något liknande detta
``` bash
Python 3.10.6
```
Om så inte är fallet, följ helt enkelt riktlinjerna nedan för ditt respektive operativsystem.

[Linux](https://docs.python-guide.org/starting/install3/linux/)

[Windows](https://www.digitalocean.com/community/tutorials/install-python-windows-10    )

[MacOS](https://www.dataquest.io/blog/installing-python-on-mac/)


##### dotenv

Python-dotenv läser nyckel-värdepar från en .env-fil och kan ställa in dem som miljövariabler. Det hjälper till vid utvecklingen av applikationer och håller även vissa värden säkra om du väljer att dela koden någonstans eftersom du inte delar filen ```.env```.

Öppna din terminal och skriv in följande för att installera dotenv
``` bash
pip installera python-dotenv
```
Om detta inte fungerar försök med
``` bash
pip3 installera python-dotenv
```


#### Krav
För att kunna köra skriptet korrekt behöver du skapa en miljöfil och använda ett gmail-konto.

##### .env
Filen ```.env``` innehåller information om dumpster-kontot som ska användas och mottagarens e-postadresser. Skapa en ```.env```-fil i samma mapp som skriptet och infoga följande

```c#
EMAIL_ADDRESS=example@gmail.com
EMAIL_PASSWORD=apppasswordhere
RECEIVER_EMAIL_ADDRESS=example1@gmail.com
```

Eftersom skriptet kan använda mer än en adress för att skicka till är det möjligt att lägga till fler om du vill. Ange e-postadressen för ditt dumpster-konto och applösenordet. Se nästa avsnitt för mer information om detta. Glöm inte att lägga till din egen e-postadress som mottagare.

##### Dumpster-konto
Jag rekommenderar starkt att du använder ett dumpster-konto för boten av säkerhetsskäl. För att skapa ett dumpster-konto går du bara till [Skapa konto GMail](https://support.google.com/mail/answer/56256?hl=sv). För att inte exponera ditt lösenord i ```.env``` filen kan du tilldela ett applösenord till ditt konto. Följ den här guiden för [Applösenord](https://support.google.com/mail/answer/185833?hl=sv-SE) eller den här (med bilder) [Applösenord med bilder](https://devanswers.co/create-application-specific-password-gmail/) och klistra in det i ```EMAIL_PASSWORD``` i filen ```.env```. Det ska se ut som ett gäng bokstäver som blandats i en mixer såsom denna **vhgksciebfjvlsk**.


#### Specifiera dina krav till skriptet

De nuvarande kraven som anges i skriptet är för mitt eget behov. Om du inte vill ha dessa konfigurationer så har jag lagt till en förklaring överst i [af-bot.py](af-bot.py) vad parametrarna gör och hur de kan se ut. 

```python
# Användarnas krav på boendet
approved_areas = ["Magasinet", "Studentlyckan", "Ulrikedal", "Vegalyckan"] # Områdena att välja mellan anges här https://www.afbostader.se/lediga-bostader/bostadsomraden/, skriv bara namnet med "" och separera varje namn med en ,
högsta_hyra = 9000 # Ange den högsta hyran du kan tänka dig, om du inte har någon övre gräns skriv in ett mycket högt tal
accommodation_choice = "Lägenhet" # "Lägenhet" för lägenheter eller "Korridorrum" för korridorrum
minimum_sqrMtrs = 40.0 # Ange de minsta kvadratmeterna för boendet, om storleken inte är ett problem skriv bara in ett mycket lågt tal
unwanted_floor = 1 # Om du har en viss våning du inte vill bo i skriv in den, fungerar bara för en våning
minimum_rooms = 2 # Ange det minsta antal rum som du vill ha i boendet, gäller endast "Lägenhet"
```

Detta är parametrarna som MÅSTE fyllas i för att boten ska fungera. Om du vet vad du gör kan du radera eller till och med lägga till krav i ***approved_accommodation_filter*** funktionen. Om du inte kan något om kodning använd då parametrarna ovan eller försök härma vad jag har gjort i pythonfilen.


#### Att köra skriptet

Om du har Python installerat och allt är konfigurerat, gå till katalogen där du klonade/laddade ner programmet till. Du kan göra detta i terminalen eller i din filhanterare.
Dubbelklicka bara på skriptet [af-bot.py](af-bot.py) eller kör följande i terminalen i den korrekta katalogen.
```
python3 af-bot.py
```
Ingen utdata kommer att skrivas ut om allt är korrekt inställt och du bör ha en ny e-post i din e-postadress som du skrev i filen [.env](.env). Om ett fel uppstår, kontrollera att varje steg ovan är gjort och installerat korrekt.



#### Automatiserad exekvering

För att göra skriptet autonomt kan man göra det i flera steg. Du kan använda till exempel Docker och Cron-jobs.
Det enklaste sättet av dessa två är Cron-jobs. Se guiden för ditt respektive operativsystem för att tillämpa skriptet med Cron-jobs:

[Linux](https://www.freecodecamp.org/news/cron-jobs-in-linux/)

[Windows](https://active-directory-wp.com/docs/Usage/How_to_add_a_cron_job_on_Windows/index.html)

[MacOS](https://anvilproject.org/guides/content/creating-links)

För mer information om Cron-jobs, se följande länk [Cron Job: A Comprehensive Guide for Beginners](https://www.hostinger.com/tutorials/cron-job)
