let itemIndex = 1;


function addRow() {
    const table = document.getElementById('itemsTable').getElementsByTagName('tbody')[0];
    const newRow = table.insertRow();
    newRow.innerHTML = `
        <td><input type="text" class="form-control" name="items[${itemIndex}][name]" required></td>
        <td><input type="text" class="form-control" name="items[${itemIndex}][description]"></td>
        <td><input type="number" step="0.01" class="form-control" name="items[${itemIndex}][price]" required></td>
        <td>
            <select class="form-control" name="items[${itemIndex}][currency]" required>
                <option disabled selected value=null>Select</option>
                <option value="UGX">UGX</option>
                <option value="USD">USD</option>
            </select>
        </td>
        <td><input type="text" class="form-control" name="items[${itemIndex}][availability]"></td>
        <td><input type="text" class="form-control" name="items[${itemIndex}][image_path]"></td>
        <td><button type="button" class="btn btn-danger delete-row" onclick="removeRow(this)">Remove</button></td>
    `;
    itemIndex++;
}

function addNewItem() {
    const itemsContainer = document.getElementById('items-container');
    const newIndex = itemsContainer.children.length;
    const newItem = document.createElement('div');
    newItem.className = 'item-entry';
    newItem.innerHTML = `
        <div class="form-group">
            <label for="item_name_${newIndex}">Item Name:</label>
            <input type="text" class="form-control" id="item_name_${newIndex}" name="items[${newIndex}][name]" required>
        </div>
        <div class="form-group">
            <label for="description_${newIndex}">Description:</label>
            <textarea class="form-control" id="description_${newIndex}" name="items[${newIndex}][description]" required></textarea>
        </div>
        <div class="form-group">
            <label for="price_${newIndex}">Price:</label>
            <input type="number" class="form-control" id="price_${newIndex}" name="items[${newIndex}][price]" step="0.01" required>
        </div>
        <div class="form-group">
            <label for="currency_${newIndex}">Currency:</label>
            <select class="form-control" id="currency_${newIndex}" name="items[${newIndex}][currency]">
                <option value="UGX">UGX</option>
                <option value="USD">USD</option>
            </select>
        </div>
        <div class="form-group">
            <label for="availability_${newIndex}">Availability:</label>
            <input type="text" class="form-control" id="availability_${newIndex}" name="items[${newIndex}][availability]">
        </div>
        <div class="form-group">
            <label for="image_${newIndex}">Item Image:</label>
            <input type="file" class="form-control-file" id="image_${newIndex}" name="items[${newIndex}][image]" accept="image/*">
            <small class="form-text text-muted">Max file size: 500KB. Large images will be automatically resized.</small>
        </div>
    `;
    itemsContainer.appendChild(newItem);
}

function removeItem(button) {
    if (confirm('Are you sure you want to remove this item?')) {
        const itemEntry = button.closest('.item-entry');
        itemEntry.remove();
    }
}

function removeRow(button) {
    // Find the row to be removed
    const row = button.parentNode.parentNode;
    // Remove the row from the table
    row.parentNode.removeChild(row);
}

function exportToPDF() {
    // Function to get image data as base64
    function getImageData(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = (e) => reject(e);
            reader.readAsDataURL(file);
        });
    }

    // Gather all the data
    const contactInfo = {
        name: document.getElementById('contact_name').value,
        phone: document.getElementById('phone_number').value,
        email: document.getElementById('email').value,
        location: document.getElementById('location').value
    };

    const itemEntries = document.querySelectorAll('.item-entry');
    const itemPromises = Array.from(itemEntries).map(async (item) => {
        const name = item.querySelector('[name$="[name]"]').value;
        const description = item.querySelector('[name$="[description]"]').value;
        const price = parseFloat(item.querySelector('[name$="[price]"]').value).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        const currency = item.querySelector('[name$="[currency]"]').value;
        const availability = item.querySelector('[name$="[availability]"]').value;
        const imageInput = item.querySelector('[name$="[image]"]');

        let imageData = null;
        if (imageInput.files && imageInput.files[0]) {
            imageData = await getImageData(imageInput.files[0]);
        }

        return { name, description, price, currency, availability, imageData };
    });

    // Wait for all promises to resolve
    Promise.all(itemPromises).then((items) => {
        // Define the document definition
        const docDefinition = {
            content: [
                { text: 'Contact Information', style: 'header' },
                {
                    ul: [
                        `Name: ${contactInfo.name}`,
                        `Phone: ${contactInfo.phone}`,
                        `Email: ${contactInfo.email}`,
                        `Location: ${contactInfo.location}`
                    ]
                },
                { text: 'Items', style: 'header' },
                {
                    table: {
                        headerRows: 1,
                        widths: ['auto', 'auto', 'auto', 'auto', 'auto', 'auto'],
                        body: [
                            ['Name', 'Description', 'Price', 'Currency', 'Availability', 'Image'],
                            ...items.map(item => [
                                item.name,
                                item.description,
                                item.price,
                                item.currency,
                                item.availability,
                                item.imageData ? { image: item.imageData, width: 50 } : 'No Image'
                            ])
                        ]
                    }
                }
            ],
            styles: {
                header: {
                    fontSize: 18,
                    bold: true,
                    margin: [0, 10, 0, 10]
                }
            }
        };

        // Generate the PDF
        pdfMake.createPdf(docDefinition).download('listed_items.pdf');
    }).catch(error => {
        console.error('Error generating PDF:', error);
        alert('An error occurred while generating the PDF. Please try again.');
    });
}

function toggleFullImage(container) {
    var fullImage = container.querySelector('.full-image');
    var thumbnail = container.querySelector('.thumbnail');

    if (fullImage.style.display === 'none' || fullImage.style.display === '') {
        fullImage.style.display = 'block';
        thumbnail.style.display = 'none';
    } else {
        fullImage.style.display = 'none';
        thumbnail.style.display = 'block';
    }
}

function deleteItem(itemId) {
    if (confirm('Are you sure you want to delete this item?')) {
        fetch('/delete_item/' + itemId, {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remove the item from the DOM
                document.querySelector(`#name-${itemId}`).closest('.card').remove();
            } else {
                alert('Failed to delete item. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    }
}

// Function to add a new item entry
function addNewItem() {
    const itemsContainer = document.getElementById('items-container');
    const newIndex = itemsContainer.children.length;
    const newItem = document.createElement('div');
    newItem.className = 'item-entry';
    newItem.innerHTML = `
        <div class="form-group">
            <label for="item_name_${newIndex}">Item Name:</label>
            <input type="text" class="form-control" id="item_name_${newIndex}" name="items[${newIndex}][name]" required>
        </div>
        <div class="form-group">
            <label for="description_${newIndex}">Description:</label>
            <textarea class="form-control" id="description_${newIndex}" name="items[${newIndex}][description]" required></textarea>
        </div>
        <div class="form-group">
            <label for="price_${newIndex}">Price:</label>
            <input type="number" class="form-control" id="price_${newIndex}" name="items[${newIndex}][price]" step="0.01" required>
        </div>
        <div class="form-group">
            <label for="currency_${newIndex}">Currency:</label>
            <select class="form-control" id="currency_${newIndex}" name="items[${newIndex}][currency]">
                <option value="UGX">UGX</option>
                <option value="USD">USD</option>
            </select>
        </div>
        <div class="form-group">
            <label for="availability_${newIndex}">Availability:</label>
            <input type="text" class="form-control" id="availability_${newIndex}" name="items[${newIndex}][availability]">
        </div>
        <div class="form-group">
            <label for="image_${newIndex}">Item Image:</label>
            <input type="file" class="form-control-file" id="image_${newIndex}" name="items[${newIndex}][image]" accept="image/*">
            <small class="form-text text-muted">Max file size: 500KB. Large images will be automatically resized.</small>
        </div>
        <button type="button" class="btn btn-danger remove-item" onclick="removeItem(this)">Remove Item</button>
    `;
    itemsContainer.appendChild(newItem);
}

function showFullImage(element) {
    // Find the full image within the hovered element's container
    var fullImage = element.querySelector('.full-image');
    if (fullImage) {
        fullImage.style.display = 'block';
    }
}

function hideFullImage(element) {
    // Hide the full image
    var fullImage = element.querySelector('.full-image');
    if (fullImage) {
        fullImage.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Existing functionality
    const addItemButton = document.getElementById('add-item');
    if (addItemButton) {
        addItemButton.addEventListener('click', addNewItem);
    }

    const exportPDFButton = document.getElementById('export-to-pdf');
    if (exportPDFButton) {
        exportPDFButton.addEventListener('click', exportToPDF);
    }

    // Existing functionality for modifying listings
    const modifyListingsForm = document.getElementById('modifyListingsForm');
    if (modifyListingsForm) {
        modifyListingsForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            fetch('/modify_listing', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Changes saved successfully!');
                } else {
                    alert('Failed to save changes. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            });
        });
    }

    const shareButtons = document.querySelectorAll('.sharemenu-button');
    shareButtons.forEach(button => {
        button.addEventListener('click', shareToWhatsApp);
    });

    // New functionality for thumbnail containers
    var containers = document.querySelectorAll('.thumbnail-container');
    containers.forEach(function(container) {
        container.addEventListener('mouseover', function() {
            var fullImage = this.querySelector('.full-image');
            var thumbnail = this.querySelector('.thumbnail');
            if (fullImage && thumbnail) {
                fullImage.style.display = 'block';
                thumbnail.style.display = 'none';
            }
        });
        container.addEventListener('mouseout', function() {
            var fullImage = this.querySelector('.full-image');
            var thumbnail = this.querySelector('.thumbnail');
            if (fullImage && thumbnail) {
                fullImage.style.display = 'none';
                thumbnail.style.display = 'block';
            }
        });
    });
});


function shareToWhatsApp() {
    try {
        // The text you want to share
        const text = "Check out these items for sale";
        // The URL you want to share (do not encode it here)
        const url = window.location.href;
        // Encode the text
        const encodedText = encodeURIComponent(text);
        // Combine the encoded text and URL without re-encoding the URL
        const shareText = `${encodedText} ${url}`;
        // Create the WhatsApp sharing link
        const whatsappUrl = `https://wa.me/?text=${shareText}`;
        // Open the WhatsApp sharing link in a new window
        window.open(whatsappUrl, '_blank');
    } catch (error) {
        console.error('Error sharing to WhatsApp:', error);
    }
}
