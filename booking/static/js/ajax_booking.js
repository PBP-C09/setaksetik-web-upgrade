document.addEventListener("DOMContentLoaded", function () {
    const bookingForm = document.getElementById("bookingForm");

    // Menambahkan event listener untuk menangani submit form
    bookingForm.addEventListener("submit", function (event) {
        event.preventDefault(); 

        const formData = new FormData(bookingForm); 
        const url = bookingForm.getAttribute("action");

        // Mengirim data form menggunakan metode fetch dengan metode POST
        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",  // Checker bahwa ini request AJAX
            },
        })
        .then(response => response.json())  // Konversi respons menjadi JSON
        .then(data => {
            if (data.errors) {
                // Jika ada error pada data form
                console.log("Form errors: ", data.errors);
                alert("Booking gagal, silakan periksa input Anda."); 
            } else {
                // Jika berhasil, tangani data yang dikembalikan
                console.log("Success: ", data); 
                alert("Booking berhasil untuk " + data.menu_name + " di " + data.restaurant_name);
            }
        })
        .catch(error => {
            // Jika terjadi kesalahan selama proses pengiriman
            console.error("Error: ", error); 
            alert("Terjadi kesalahan saat memproses booking.");
        });
    });
});
