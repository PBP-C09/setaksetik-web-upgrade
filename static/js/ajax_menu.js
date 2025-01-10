async function showAddMenuModal() {
    document.querySelector("#modal").classList.remove("hidden");
    
    document.getElementById('price').addEventListener('input', function() {
        const value = this.value;
        if (value < 1000 || value > 1800000) {
            showError(this, 'Price must be between Rp 1,000 and Rp 1,800,000');
        } else {
            clearError(this);
        }
    });

    document.getElementById('rating').addEventListener('input', function() {
        const value = this.value;
        if (value < 0 || value > 5) {
            showError(this, 'Rating must be between 0 and 5');
        } else {
            clearError(this);
        }
    });
}
  
function closeModal() {
    const form = document.querySelector("#form");
    form.reset();
    document.querySelector("#modal").classList.add("hidden");
    clearErrorMessages();
}

  function validateForm() {
    let isValid = true;
    clearErrorMessages();

    const fields = [
        { id: 'menu_name', label: 'Menu Name' },
        { id: 'restaurant_name', label: 'Restaurant Name' },
        { id: 'price', label: 'Price', min: 1000, max: 1800000 },
        { id: 'rating', label: 'Rating', min: 0, max: 5 },
        { id: 'image_url', label: 'Image URL' },
        { id: 'city', label: 'City' },
        { id: 'category', label: 'Category' },
        { id: 'specialized', label: 'Specialized' }
    ];

    fields.forEach(field => {
        const element = document.getElementById(field.id);
        let value = "";
        try {
            value = element.value.trim();
        } catch (error) {
            value = "";
        }

        if (!value) {
            showError(element, `${field.label} is required`);
            isValid = false;
        } else if (field.id === 'price') {
            const numValue = Number(value);
            if (numValue < field.min || numValue > field.max) {
                showError(element, `Price must be between Rp ${field.min} and Rp ${field.max}`);
                isValid = false;
            }
        } else if (field.id === 'rating') {
            const numValue = Number(value);
            if (numValue < field.min || numValue > field.max) {
                showError(element, `Rating must be between ${field.min} and ${field.max}`);
                isValid = false;
            }
        }
    });

    return isValid;
}

function showError(element, message) {
    const errorDiv = element.parentElement.querySelector('.error-message');
    if (errorDiv) {
        errorDiv.textContent = message;
    } else {
        const newErrorDiv = document.createElement('div');
        newErrorDiv.className = 'error-message text-red-500 text-sm mt-1';
        newErrorDiv.textContent = message;
        element.parentElement.appendChild(newErrorDiv);
    }
    element.classList.add('border-red-500');
}

function clearError(element) {
    const errorDiv = element.parentElement.querySelector('.error-message');
    if (errorDiv) {
        errorDiv.remove();
    }
    element.classList.remove('border-red-500');
}

function clearErrorMessages() {
    document.querySelectorAll('.error-message').forEach(error => error.remove());
    document.querySelectorAll('.border-red-500').forEach(element => {
        element.classList.remove('border-red-500');
    });
}
  
async function addMenu() {
    const form = document.querySelector("#form");
    const submitBtn = document.getElementById("confirm-modal");
    
    try {
        submitBtn.disabled = true; 
        
        if (!validateForm()) {
            submitBtn.disabled = false;
            return false;
        }

        const formData = new FormData(form);
        const response = await fetch("/explore/add_menu/", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Failed to add menu");
        }

        closeModal();
        
        await refreshMenuList();
        
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to add menu. Please try again.');
    } finally {
        submitBtn.disabled = false;
    }
}

async function refreshMenuList() {
    try {
        const response = await fetch('/explore/get_menu/');
        const menus = await response.json();
        
        const menuContainer = document.querySelector('.grid.grid-cols-2.md\\:grid-cols-3');
        if (!menuContainer) return;

        menuContainer.innerHTML = menus.map(menu => `
            <div class="max-w-md rounded-lg overflow-hidden shadow-lg bg-[#F5F5DC] relative border flex flex-col">
                <div class="absolute top-4 left-4 flex space-x-2 z-10">
                    <a href="/explore/edit-menu/${menu.pk}" class="bg-yellow-300 hover:bg-yellow-500 text-white rounded-full p-2 transition duration-300 shadow-lg">
                        <!-- Edit icon -->
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" viewBox="0 0 20 20" fill="currentColor">
                            <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                        </svg>
                    </a>
                    <a href="/explore/delete/${menu.pk}" class="bg-rose-400 hover:bg-rose-600 text-white rounded-full p-2 transition duration-300 shadow-lg">
                        <!-- Delete icon -->
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                        </svg>
                    </a>
                </div>
                <div class="relative">
                    <img class="w-full h-64 object-cover" src="${menu.fields.image}" alt="${menu.fields.menu}">
                </div>
                <div class="px-4 py-4 flex-grow">
                    <div class="text-xl text-[#3E2723] font-bold mb-4" style="font-family: 'Playfair Display', serif;">
                        ${menu.fields.menu}
                    </div>
                    <div class="flex items-center text-sm text-[#3E2723] mb-2">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 mr-3">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" />
                        </svg>
                        ${menu.fields.restaurant_name}, ${menu.fields.city}
                    </div>
                    <div class="flex items-center text-sm text-[#3E2723] mb-2">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 mr-3">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0L6.982 20.54a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z" />
                        </svg>
                        ${menu.fields.rating} / 5
                    </div>
                    <div class="flex items-center text-sm text-[#3E2723] mb-2">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 mr-3">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18.75a60.07 60.07 0 0 1 15.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 0 1 3 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 0 0-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 0 1-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 0 0 3 15h-.75M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm3 0h.008v.008H18V10.5Zm-12 0h.008v.008H6V10.5Z" />
                        </svg>
                        Rp ${menu.fields.price}
                    </div>
                    <div class="flex flex-wrap gap-2 mb-2 mt-4">
                        <span class="bg-[#F7B32B] text-white text-sm font-medium py-1 px-3 rounded-full">
                            ${menu.fields.category}
                        </span>
                        <span class="bg-[#F7B32B] text-white text-sm font-medium py-1 px-3 rounded-full">
                            ${menu.fields.specialized}
                        </span>
                    </div>
                </div>
                <div class="flex justify-center mt-auto p-4">
                    <a href="/explore/admin_detail/${menu.pk}" class="bg-[#6D4C41] hover:bg-[#B71C1C] text-white font-medium py-2 px-6 w-full text-center rounded focus:outline-none focus:shadow-outline transition duration-300 ease-in-out">
                        See Details
                    </a>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error refreshing menu list:', error);
    }
}

// Event Listeners
document.getElementById("confirm-modal").addEventListener("click", async function(e) {
    e.preventDefault();
    await addMenu();
});


  function submitFilterForm() {
    var form = document.getElementById('filterForm');
    form.reset();
    form.submit();
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