async function addToWishlist(itemName, description, isPublic) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;  // Ensure this token is fetched correctly

    const response = await fetch("{% url 'meatup:add_to_wishlist' %}", {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ item_name: itemName, description: description, is_public: isPublic }),
    });

    const data = await response.json();
    if (!response.ok) {
        console.error('Error adding to wishlist:', data.error);
        alert('Failed to save wishlist item: ' + data.error);
    } else {
        console.log('Wishlist item added:', data);
        alert('Wishlist item added successfully: ' + data.item_name);
    }
}