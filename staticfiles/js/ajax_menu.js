async function showAddMenuModal() {
    document.querySelector("#modal").classList.remove("hidden");
    document.getElementById("confirm-modal").onclick = async function () { 
      await addMenu(); 
      closeModal();
    };
  }
  
  function closeModal() {
    document.querySelector("#form").reset();
    document.querySelector("#modal").classList.add("hidden");
  }
  
  async function addMenu() {
    const form = new FormData(document.querySelector("#form"));
    const response = await fetch("/explore/add_menu/", {
      method: "POST",
      body: form,
    });
  
    if (!response.ok) {
      throw new Error("Failed to add menu");
    }
    document.querySelector("#form").reset();
  }

  function submitFilterForm(event) {
    event.preventDefault(); // Mencegah form dari submit default

    const form = document.getElementById('filterForm');
    const formData = new FormData(form);

    // Mengirim data form menggunakan Fetch API
    fetch(form.action, {
        method: 'GET',
        body: formData
    })
    then(response => {
      if (response.ok) {
          return response.text(); 
      }
      throw new Error('Network response was not ok.');
    })
    .then(data => {
        form.reset();
    })
    .catch(error => {
        console.error('Error:', error);
    });
  }
  
  function returnToList(){
    window.location.href="/explore";
  }

  function toggleFilter() {
    const filterOptions = document.getElementById("filter-options");
    if (filterOptions.classList.contains("hidden")) {
        filterOptions.classList.remove("hidden");
    } else {
        filterOptions.classList.add("hidden");
    }
}

function showEditMenuModal(menuId) {
  $.ajax({
      url: `/get-menu/${menuId}/`,
      method: 'GET',
      success: function(data) {
          document.getElementById('menu_name').value = data.menu_name; 
          document.getElementById('restaurant_name').value = data.restaurant_name; 
          document.getElementById('menu_id').value = data.id; 
          $('#editMenuModal').modal('show'); 
      },
      error: function(xhr, status, error) {
          console.error('Error fetching menu data:', error);
          alert('Failed to fetch menu data.');
      }
  });
}

function deleteMenu(menuId) {
  if (confirm("Are you sure you want to delete this menu?")) {
      $.ajax({
          url: `/delete-menu/${menuId}/`, 
          method: 'DELETE',
          success: function(response) {
              alert('Menu deleted successfully!');
              location.reload(); 
          },
          error: function(xhr, status, error) {
              console.error('Error deleting menu:', error);
              alert('Failed to delete menu.');
          }
      });
  }
}

// Fungsi untuk mengupdate menu
function updateMenu() {
  const menuId = document.getElementById('menu_id').value; // Ambil ID menu
  const menuName = document.getElementById('menu_name').value; // Ambil nama menu
  const restaurantName = document.getElementById('restaurant_name').value; // Ambil nama restoran

  // Kirim data ke server untuk diupdate
  $.ajax({
      url: `edit-menu/<int:menu_id>/`, // Sesuaikan dengan endpoint untuk mengupdate menu
      method: 'POST', // Atau POST sesuai dengan implementasi backend
      data: {
          menu_name: menuName,
          restaurant_name: restaurantName
      },
      success: function(response) {
          alert('Menu updated successfully!');
          // Refresh atau perbarui tampilan setelah pengupdatean
          location.reload(); // Menggunakan reload untuk memperbarui tampilan
      },
      error: function(xhr, status, error) {
          console.error('Error updating menu:', error);
          alert('Failed to update menu.');
      }
  });
}
  
document.getElementById("cancel-modal").addEventListener("click", closeModal);