// Fungsi untuk update input price
function updateInput(inputId, value) {
    const minSlider = document.getElementById('min_price');
    const maxSlider = document.getElementById('max_price');
    
    if (inputId === 'min_price') {
        if (parseInt(value) > parseInt(maxSlider.value) - 1000) {
            value = parseInt(maxSlider.value) - 1000; // Mengatur batas minimum
        }
        document.getElementById(`${inputId}_input`).value = value;
        minSlider.value = value;
    } else if (inputId === 'max_price') {
        if (parseInt(value) < parseInt(minSlider.value) + 1000) {
            value = parseInt(minSlider.value) + 1000; // Mengatur batas minimum
        }
        document.getElementById(`${inputId}_input`).value = value;
        maxSlider.value = value;
    }
    
    updateSliderBackgroundPrice();
  }
  
  // Fungsi untuk update slider price
  function updateSlider(sliderId, value) {
    const minSlider = document.getElementById('min_price');
    const maxSlider = document.getElementById('max_price');
  
    if (sliderId === 'min_price') {
        if (parseInt(value) > parseInt(maxSlider.value) - 1000) {
            value = parseInt(maxSlider.value) - 1000; // Mengatur batas minimum
        }
        minSlider.value = value;
        document.getElementById('min_price_input').value = value;
    } else if (sliderId === 'max_price') {
        if (parseInt(value) < parseInt(minSlider.value) + 1000) {
            value = parseInt(minSlider.value) + 1000; // Mengatur batas minimum
        }
        maxSlider.value = value;
        document.getElementById('max_price_input').value = value;
    }
  
    updateSliderBackgroundPrice();
  }
  
  // Fungsi untuk background price slider
  function updateSliderBackgroundPrice() {
    const minSlider = document.getElementById('min_price');
    const maxSlider = document.getElementById('max_price');
    
    const minValue = parseInt(minSlider.value);
    const maxValue = parseInt(maxSlider.value);
    
    const minPercent = ((minValue - 1000) / (1800000 - 1000)) * 100;
    const maxPercent = ((maxValue - 1000) / (1800000 - 1000)) * 100;
    
    const track = document.querySelector('.price-slider-track');
    track.style.background = `linear-gradient(to right, #ddd ${minPercent}%, #502911 ${minPercent}%, #502911 ${maxPercent}%, #ddd ${maxPercent}%)`;
}
  
  // Fungsi untuk update input rating
  function updateInputRating(inputId, value) {
    const minSlider = document.getElementById('min_rating');
    const maxSlider = document.getElementById('max_rating');
    
    if (inputId === 'min_rating') {
        if (parseFloat(value) > parseFloat(maxSlider.value) - 0.1) {
            value = parseFloat(maxSlider.value) - 0.1; // Mengatur batas minimum
        }
        document.getElementById(`${inputId}_input`).value = value;
        minSlider.value = value;
    } else if (inputId === 'max_rating') {
        if (parseFloat(value) < parseFloat(minSlider.value) + 0.1) {
            value = parseFloat(minSlider.value) + 0.1; // Mengatur batas minimum
        }
        document.getElementById(`${inputId}_input`).value = value;
        maxSlider.value = value;
    }
    
    updateSliderBackgroundRate();
  }
  
  // Fungsi untuk update slider rating
  function updateSliderRating(sliderId, value) {
    const minSlider = document.getElementById('min_rating');
    const maxSlider = document.getElementById('max_rating');
  
    if (sliderId === 'min_rating') {
        if (parseFloat(value) > parseFloat(maxSlider.value) - 0.1) {
            value = parseFloat(maxSlider.value) - 0.1; // Mengatur batas minimum
        }
        minSlider.value = value;
        document.getElementById('min_rating_input').value = value;
    } else if (sliderId === 'max_rating') {
        if (parseFloat(value) < parseFloat(minSlider.value) + 0.1) {
            value = parseFloat(minSlider.value) + 0.1; // Mengatur batas minimum
        }
        maxSlider.value = value;
        document.getElementById('max_rating_input').value = value;
    }
  
    updateSliderBackgroundRate();
  }
  
  // Fungsi untuk background rating slider
  function updateSliderBackgroundRate() {
    const minSlider = document.getElementById('min_rating');
    const maxSlider = document.getElementById('max_rating');
    
    const minValue = parseFloat(minSlider.value);
    const maxValue = parseFloat(maxSlider.value);
    
    const minPercent = (minValue / 5) * 100;
    const maxPercent = (maxValue / 5) * 100;
    
    const track = document.querySelector('.rating-slider-track');
    track.style.background = `linear-gradient(to right, #ddd ${minPercent}%, #502911 ${minPercent}%, #502911 ${maxPercent}%, #ddd ${maxPercent}%)`;
}
  
  // Inisialisasi background slider saat halaman dimuat
  document.addEventListener("DOMContentLoaded", function() {
    updateSliderBackgroundPrice();
    updateSliderBackgroundRate();
  });
  