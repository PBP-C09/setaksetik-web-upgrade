# SetakSetik
Sebuah aplikasi yang didekasikan untuk pecinta dan calon pecinta _steak_!

_Web upgraded version_ dari tugas mata kuliah PBP.

---

# Table of Contents
1. [Anggota Kelompok](#anggota-kelompok)
2. [Deskripsi Aplikasi](#deskripsi-aplikasi)
3. [Daftar Modul](#daftar-modul)
4. [Initial Dataset](#initial-dataset)
5. [Role atau Peran Pengguna](#role-atau-peran-pengguna)
6. [Tautan Deployment](#tautan-deployment)


# Anggota Kelompok
- 2306211401  |  Haliza Nafiah Syakira Arfa
- 2306244955  |  Muhammad Faizi Ismady Supardjo
- 2306165692  |  Nadira Aliya Nashwa
- 2306165963  |  Aimee Callista Ferlintera Prudence Ernanto
- 2306217304  |  Clara Aurelia Setiady


# Deskripsi Aplikasi
Untuk menjawab kebingungan pengguna dalam memilih menu _steak_ yang tepat, **SetakSetik** hadir sebagai solusi lengkap bagi para pecinta _steak_. Aplikasi ini dirancang dengan beragam fitur yang tidak hanya memudahkan pengguna dalam memilih menu, tetapi juga memberikan pengalaman bersantap yang lebih personal dan menyenangkan. 

**SetakSetik** dikembangkan dengan berbagai modul yang mendukung kemudahan dalam pemilihan menu serta kenyamanan pengguna. Fitur autentikasi memungkinkan pengguna untuk login dengan mudah. Pengguna dapat melakukan _explore_ dari banyaknya menu yang tersedia beserta filter, lalu selanjutnya melakukan _booking_ restoran dan memberikan _review_. Selain itu, terdapat juga fitur _spin the wheel_ yang merupakan elemen hiburan dalam menentukan pilihan menu, serta fitur _meat up_ untuk melihat pengguna lain dengan _public wishlist_ dan preferensi yang serupa.

Saat ini, aplikasi ini dirancang untuk pecinta _steak_ berbasis Jakarta. Dataset yang digunakan adalah menu dan _steakhouse_ yang tersebar di segala penjuru Jakarta. Jadi, jika menjejakkan kaki di Jakarta dan mendambakan _steak_, tak perlu bingung tak perlu ragu, **SetakSetik** akan membantu!


# Daftar Modul
1. **Autentikasi**
   - Pengguna register dan membuat akun (username, name, role, password and password confirmation)
   - Pengguna melakukan aktivitas login dan logout.

2. **Spin the Wheel - “Makan apa hari ini”** (Customer) : Haliza
   - Pengguna melakukan _spin wheel_ yang disesuaikan dengan preferensi pribadi terakhir.
   - Pilih jenis preferensi beef untuk add all, atau add manual makanan yang akan di-spin
   - Pengguna dapat menambah atau menghapus daftar menu yang dijadikan opsi pada _spin wheel_

3. **Explore Menu** (Customer, Admin) : Nadira
   - Pengguna dapat memfilter menu berdasarkan:
     - Jenis beef
     - Kota
     - Range rating
     - Search bar untuk nama menu

4. **Rating dan Review** (Customer, Admin) : Clara
   - Pengguna dapat memberikan _review_ dan _rating_ pada setiap menu yang telah dicoba.
   - Terdapat fitur _upvote_ dan _downvote_ untuk review pengguna lain.

5. **MeatUp - Teman Makan** (Customer) : Aimee
   - Pengguna dapat membuat "public wishlist" tentang menu yang berencana ingin dimakan.
   - Pengguna lain dengan wishlist serupa dapat saling terhubung sehingga mereka dapat berdiskusi tentang menu yang ingin dicoba.

6. **Booking Restoran** (Customer, Pemilik Restoran) : Faizi
   - Booking dilakukan berdasarkan restoran, nama pemesan, dan jumlah orang.
   - Pengguna memesan berdasarkan jumlah porsi.
   - Riwayat pemesanan yang sudah dilakukan.


# Initial Dataset

**Kategori:** Menu _steak_ dari berbagai _steakhouse_ di Jakarta.

- **Sumber:** [Kaggle](https://www.kaggle.com/datasets/miradelimanr/steakhouse-jakarta?resource=download).
- **Dataset Terproses:** [Google Sheets](https://docs.google.com/spreadsheets/d/1NDPuzQpybnalNUVGGFEaG_dutWjPqhmTbliIAJ24xuU/edit?usp=sharing).


# Role atau Peran Pengguna
1. **Pengguna Umum (Customer)**
   - Akses:
     - Mengakses seluruh konten publik seperti daftar menu, informasi restoran, harga, dan ulasan.
     - Membuat akun dan login/logout menggunakan akun yang sudah dibuat
   - Fitur:
     - **Explore**: Melihat daftar menu dan restoran yang tersedia dengan fitur filter serta search bar.
     - **Spin the Wheel**: Menggunakan fitur "spin the wheel" untuk memilih menu secara acak.
     - **MeatUp**: Menyimpan menu-menu favorit yang ingin dicoba di masa depan dan berinteraksi dengan pengguna lain.
     - **Review**: Memberi rating dan review pada menu yang sudah dicoba
     - **Booking**: Melakukan pemesanan tempat di restoran dan melihat riwayat booking.
       
2. **Admin**
   - Akses:
     - Mengelola konten yang ada pada website.
   - Fitur:
     - **Manage Menu**: Menambah, mengedit, atau menghapus informasi tentang menu.
     - **Manage Review**: Menghapus ulasan yang tidak sesuai.
     - **Manage Ownership**: Memastikan klaim kepemilikan sesuai.
       
3. **Pemilik Steakhouse**
   - Akses:
     - Mengatur menu serta booking pada _steakhouse_ yang telah diklaim.
   - Fitur:
     - **Claim**: Melakukan klaim kepemiikan terhadap _steakhouse_ yang dimiliki.
     - **Monitor Booking**: Memantau dan mengelola booking dari _steakhouse_ yang dimiliki.
     - **Monitor Review**: Memantau dan menjawab review dari _steakhouse_ yang dimiliki.


# Tautan Deployment
Tautan deployment aplikasi [**SetakSetik Upgrade**](https://haliza-nafiah-setaksetik.pbp.cs.ui.ac.id/).

