# AFBot
Ini adalah bot AFBostäder yang diprogram dengan Python untuk memudahkan penyaringan untuk menemukan akomodasi siswa yang sempurna untuk Anda!

Script ini dapat digunakan oleh pengguna yang tidak memiliki pengalaman dalam pemrograman sebelumnya. Silakan lihat bagian [Cara menjalankannya](#cara menjalankannya) untuk informasi lebih lanjut.


### How it works

Setelah skrip berjalan, data dari API AFBostäder diunduh berisi informasi dalam file JSON tentang sewa, area, lantai, dan lainnya.
Setiap objek JSON (akomodasi) berisi parameter untuk pemfilteran, ini dapat ditentukan sendiri sesuai dengan kebutuhan Anda. Parameter ini kemudian dikirim ke fungsi yang memeriksa apakah persyaratan Anda terpenuhi, jika fungsi tersebut akan menyetujui akomodasi ini dan memasukkannya ke dalam email.

Email ini menggunakan Protokol SMTP GMail dengan akun tempat sampah untuk mengirim email ke penerima. Setiap akomodasi yang disetujui akan dimasukkan dalam daftar dengan string yang berisi area, sewa, dan meter persegi dengan URL ke akomodasi. Ketika setiap akomodasi telah diperiksa di situs web, daftar akomodasi yang disetujui akan dikirim ke fungsi yang menyiapkan email. Di sini kami mengekspor akun gmail dengan kata sandi Aplikasi yang sesuai yang disimpan dalam file ```.env``` tempat juga alamat email penerima disimpan. Anda dapat mengirim ke beberapa alamat dengan fungsi ini. Ingatlah bahwa file ```.env``` harus dibuat agar berfungsi dan tidak mengekspos kredensial sensitif secara langsung dalam kode. Cara membuat file ```.env``` dijelaskan di ```.env```.

Objek Email dibuat berisi semua informasi yang dibutuhkan SMTP untuk mengirimkannya. Dalam kode berikut adalah bagaimana SMTP akan mengirim email dengan informasi yang diperoleh. SMTP diekspos di port 465 dan menggunakan fungsi login dengan kredensial akun dumpster yang diekspor dari file ```.env``` untuk login ke layanan GMail dan mengirim pesan. Kami kemudian keluar dari SMTP sehingga tidak terjadi hal yang tidak biasa.

```python
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.ehlo()
        smtp.login(sender_email_adress, sender_email_password)
        smtp.send_message(msg)
        smtp.quit()
```

Untuk melihat contoh jika objek JSON menyimpan parameter yang berbeda, silakan lihat [example.json](example.json).

Saat ini bot sedang mengirim email jika akomodasi telah ditambahkan yang belum pernah didengar oleh penerima. Dengan kata lain, Anda tidak boleh mendapatkan akomodasi yang sama dua kali melalui surat Anda.

### How to run it

Untuk dapat menjalankan skrip, Anda perlu menginstal Python dan dependensi lainnya.

#### Install software
##### Python
Jika Anda tidak yakin, buka baris perintah Anda (cari Terminal atau CMD) dan jalankan baris ini
```bash
python3 --version
```
Outputnya harus seperti ini
```bash
Python 3.10.6
```
Jika ini bukan masalahnya, cukup ikuti panduan di bawah ini untuk OS Anda masing-masing

[Linux](https://docs.python-guide.org/starting/install3/linux/)

[Windows](https://www.digitalocean.com/community/tutorials/install-python-windows-10    )

[MacOS](https://www.dataquest.io/blog/installing-python-on-mac/)


##### dotenv

Python-dotenv membaca pasangan nilai kunci dari file .env dan dapat mengaturnya sebagai variabel lingkungan. Ini membantu dalam pengembangan aplikasi dan juga menjaga beberapa nilai tetap aman jika Anda memilih untuk membagikan kode di suatu tempat karena Anda tidak membagikan file ```.env```.

Buka terminal Anda dan ketik berikut ini untuk menginstal dotenv
```bash
pip install python-dotenv
```
Jika ini tidak berhasil coba dengan
```bash
pip3 install python-dotenv
```


#### Persyaratan
Untuk dapat menjalankan skrip dengan benar, Anda perlu membuat file lingkungan dan menggunakan akun gmail.

##### .env
File ```.env``` berisi informasi tentang akun tempat sampah yang akan digunakan dan alamat email penerima. Buat file ```.env``` di folder yang sama dengan skrip dan masukkan yang berikut ini

```c#
EMAIL_ADDRESS=example@gmail.com
EMAIL_PASSWORD=apppasswordhere
RECEIVER_EMAIL_ADDRESS=example1@gmail.com
```
Karena skrip dapat menggunakan lebih dari satu alamat untuk dikirim, dimungkinkan untuk menambahkan lebih banyak jika Anda mau. Masukkan alamat email akun dumpster Anda dan kata sandi Aplikasi. Periksa bagian berikutnya untuk informasi lebih lanjut tentang ini. Jangan lupa untuk menambahkan alamat email Anda sendiri sebagai penerima

##### Akun tempat sampah
Saya sangat merekomendasikan untuk menggunakan akun tempat sampah untuk bot, untuk alasan keamanan. Untuk membuat akun tempat sampah cukup buka [Create account GMail](https://support.google.com/mail/answer/56256?hl=en). Untuk tidak mengekspos kata sandi Anda ke dalam ```.env```, Anda dapat menetapkan kata sandi Aplikasi ke akun Anda. Ikuti ini [App password](https://support.google.com/mail/answer/185833?hl=en-GB) atau (with pictures) [App password with pictures](https://devanswers.co/create-application-specific-password-gmail/) dan paste di ```ÈMAIL_PASSWORD```di file ```.env```. Seharusnya terlihat seperti sekumpulan huruf yang dicampur dalam blender seperti ini **vhgksciebfjvlsk**.

#### Running the script

Jika Anda telah menginstal Python dan semuanya sudah diatur, silakan buka direktori tempat Anda mengkloning/mengunduh program. Anda dapat melakukan ini di Terminal atau di pengelola file Anda.
Cukup klik dua kali skrip [af-bot.py](af-bot.py) atau run
```
python3 af-bot.py
```
Tidak ada output yang akan dicetak jika semuanya diatur dengan benar dan Anda harus memiliki email di alamat yang Anda ketikkan di file [.env](#.env). Jika terjadi kesalahan, silakan periksa bahwa setiap langkah di atas dilakukan dan diinstal.


#### Specify your needs to the script

Persyaratan saat ini yang dinyatakan dalam skrip adalah untuk kebutuhan saya sendiri. Jika Anda tidak menginginkan konfigurasi ini, saya telah menambahkan beberapa penjelasan di bagian atas [af-bot.py](af-bot.py) apa yang dilakukan parameter dan bagaimana tampilannya.

```python
# Persyaratan pengguna untuk akomodasi
disetujui_areas = ["Magasinet", "Studentlyckan", "Ulrikedal", "Vegalyckan"] # Area yang akan dipilih tercantum di sini https://www.afbostader.se/lediga-bostader/bostadsomraden/, ketikkan saja namanya dengan "" dan pisahkan setiap nama dengan ,
tertinggi_rent = 9000 # Nyatakan sewa tertinggi yang dapat Anda pikirkan, jika Anda tidak memiliki batas atas, ketikkan angka yang sangat tinggi
akomodasi_pilihan = "Lägenhet" # "Lägenhet" untuk apartemen atau "Korridorrum" untuk kamar koridor
minimum_sqrMtrs = 40,0 # Nyatakan meter persegi minimal akomodasi, jika ukuran bukan masalah, ketik saja angka yang sangat kecil
unknown_floor = 1 # Jika Anda memiliki lantai tertentu yang tidak ingin Anda tempati, ketik ini, hanya berfungsi untuk satu lantai
minimum_rooms = 2 # Sebutkan jumlah minimum kamar yang Anda inginkan di akomodasi, hanya berlaku untuk "Lägenhet"
```

Ini adalah parameter yang HARUS diisi agar bot dapat bekerja. Jika Anda tahu apa yang Anda lakukan maka Anda dapat menghapus atau bahkan menambahkan persyaratan di ***approved_accommodation_filter***. Jika Anda tidak tahu apa-apa tentang pengkodean, gunakan parameter di atas atau coba tiru apa yang saya lakukan di file python.

#### Eksekusi otomatis

Untuk membuat skrip menjadi otonom, seseorang dapat melakukannya dalam beberapa langkah. Anda dapat menggunakan misalnya Docker dan Cron-jobs.
Cara termudah dari keduanya adalah Cron-jobs. Silakan lihat panduan untuk OS Anda masing-masing untuk menerapkan skrip menggunakan Cron-jobs:

[Linux](https://www.freecodecamp.org/news/cron-jobs-in-linux/)

[Windows](https://active-directory-wp.com/docs/Usage/How_to_add_a_cron_job_on_Windows/index.html)

[MacOS](https://anvilproject.org/guides/content/creating-links)

Untuk informasi lebih lanjut tentang Cron-job, silakan lihat tautan berikut [Cron Job: A Comprehensive Guide for Beginners](https://www.hostinger.com/tutorials/cron-job)
