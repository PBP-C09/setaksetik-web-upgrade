# setaksetik
Sebuah aplikasi yang didekasikan untuk pecinta dan calon pecinta steak!

---

# Table of Contents
1. [Anggota Kelompok](#anggota-kelompok)
2. [Deskripsi Aplikasi](#deskripsi-aplikasi)
3. [Daftar Modul](#daftar-modul)
4. [Sumber Initial Dataset](#sumber-initial-dataset)
5. [Role atau Peran Pengguna](#role-atau-peran-pengguna)
6. [Tautan Deployment](#tautan-deployment)


# Anggota Kelompok
- 2306211401  |  Haliza Nafiah Syakira Arfa
- 2306244955  |  Muhammad Faizi Ismady Supardjo
- 2306165692  |  Nadira Aliya Nashwa
- 2306165963  |  Aimee Callista Ferlintera Prudence Ernanto
- 2306217304  |  Clara Aurelia Setiady


# Deskripsi Aplikasi
Untuk menjawab kebingungan pengguna dalam memilih menu steak yang tepat, **SetakSetik** hadir sebagai solusi lengkap bagi para pecinta steak. Aplikasi ini dirancang dengan beragam fitur yang tidak hanya memudahkan pengguna dalam memilih menu, tetapi juga memberikan pengalaman bersantap yang lebih personal dan menyenangkan. 

**setaksetik** dikembangkan dengan berbagai modul yang mendukung kemudahan dalam pemilihan menu serta kenyamanan pengguna. Fitur autentikasi memungkinkan pengguna untuk registrasi serta login dengan mudah. Pengguna juga dapat mengakses riwayat pesanan, menyimpan _wishlist_ menu yang ingin dicoba, dan melacak program reward berdasarkan pesanan dan _review_. Selain itu, fitur "Spin the Wheel" menambahkan elemen hiburan dalam menentukan pilihan menu, sementara _filter_ menu yang komprehensif membantu pengguna menyesuaikan pencarian berdasarkan rasa, metode masak, harga, dan kriteria lainnya.

Saat ini, aplikasi ini dirancang untuk pecinta steak berbasis Jakarta. Dataset yang digunakan adalah menu dan _steakhouse_ yang tersebar di segala penjuru Jakarta. Jadi, jika menjejakkan kaki di Jakarta dan mendambakan steak, tak perlu bingung tak perlu ragu, **SetakSetik** akan membantu!


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


# Sumber Initial Dataset
Kategori utama produk berupa menu _steak_ unggulan dari berbagai _steakhouse_ di Jakarta.

Berikut sumber initial [dataset](https://www.kaggle.com/datasets/miradelimanr/steakhouse-jakarta?resource=download) kami.


# Role atau Peran Pengguna
1. **Pengguna Umum (Customer)**
   - Akses:
     - Mengakses seluruh konten publik seperti daftar menu, informasi restoran, harga, dan ulasan.
     - Membuat akun dan login/logout menggunakan akun yang sudah dibuat
     - **Spin the Wheel**: Menggunakan fitur "spin the wheel" untuk memilih menu secara acak.
     - **MeatUp**: Menyimpan menu-menu favorit yang ingin dicoba di masa depan dan berinteraksi dengan pengguna lain.
     - **Rating dan Review**: Memberi rating dan review pada menu yang sudah dicoba, serta mengunggah foto makanan.
     - **Booking Restoran**: Melakukan pemesanan tempat di restoran dan melihat riwayat booking.
       
2. **Admin**
   - Akses:
     - Mengelola konten website.
   - Fitur:
     - **Pengelolaan Menu & Restoran**: Menambah, mengedit, atau menghapus informasi tentang menu.
     - **Manajemen Ulasan**: Mengedit atau menghapus ulasan yang tidak sesuai.
     - **Manajemen Pengguna**: Mengelola akun pengguna..
       
3. **Pemilik Steakhouse**
   - Akses:
     - Mengelola proses booking restoran yang dimiliki.
   - Fitur:
     - **Manajemen Booking**: Memantau dan mengelola booking dari seluruh _steakhouse_.


# Tautan Deployment
Tautan deployment aplikasi [**SetakSetik Upgrade**](https://haliza-nafiah-setaksetik.pbp.cs.ui.ac.id/).

