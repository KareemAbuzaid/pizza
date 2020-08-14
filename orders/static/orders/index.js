// Get references to the dom elements, the scroller in which
// we will append the templates and the templates that represent
// menuitems
var scroller = document.querySelector('#scroller');
var template = document.querySelector('#menuitem_template');
var sentinel = document.querySelector('#sentinel');

// add order to the local storage
localStorage.setItem('orders', JSON.stringify([]));

// add onclick to the checkout button
var checkoutButton = document.querySelector('#checkout-btn');
checkoutButton.addEventListener('click', function(event) {
    orders = localStorage.getItem('orders');

    // Put the orders in an object that can be sent in AJAX request
    data = {'orders': orders};

    // Send the AJAX request
    $.ajax({
        "url": 'checkout/',
        "type": 'post',
        "data": data,
    });
});

// Order list to be showen on the orders card
var orderList = document.getElementById("cart-card").getElementsByClassName("card-body")[0].getElementsByTagName("ul")[0];

// get the button in the model to add an event listener to it
var modalButton = document.getElementById("Mymodal").getElementsByClassName("btn")[0];
modalButton.addEventListener('click', function(event){

    // get all checkboxes
    checkboxes = document.getElementsByTagName("input");

    // loop over them to get the size and toppings, and store the
    // selected values in object order
    var orderItem = {'toppings': []};
    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked == true) {
            if ((checkboxes[i].id == "small") || (checkboxes[i].id == "large")) {
                orderItem['size'] = checkboxes[i].id;
                orderItem['name'] = checkboxes[i].value;
                orderItem['price'] = checkboxes[i].name;
                orderItem['id'] = checkboxes[i].itemId;
                orderItem['pricing_id'] = checkboxes[i].pricingId;
            }
            else {
                orderItem['toppings'].push(checkboxes[i].name);
            }
        }
    }

    // add the item data to the cart card
    var li = document.createElement("li");
    li.appendChild(document.createTextNode(`${orderItem['name']}...${orderItem['size']}...${orderItem['price']}`));
    orderList.appendChild(li);

    // add the orders to local storage
    var oldOrders = JSON.parse(localStorage.getItem('orders'));
    oldOrders.push(orderItem);
    localStorage.setItem('orders', JSON.stringify(oldOrders));
    });

// Function to load the menuitems from the backend
function loadItems() {

    // Use fetch to request data
    fetch('/load').then((response) => {

        // Convert the response data to JSON
        response.json().then((data) => {

            // If empty JSON, exit the function
            if (!data) {

                // Replace the spinner with "That's all the food"
                sentinel.innerHTML = "That's all the food";
                return;
            }

            // Get the menu categories and menuitems from the response
            const categories = Object.keys(data['menu']);

            // loop over the categories
            for (const category of categories) {

                // Get the menuitems list
                menuitems = data['menu'][category];

                // Create an h2 header that says the name of the category
                // and append it to the DOM
                var categoryHeader = document.createElement("h2");
                categoryHeader.style.textAlign = "left";
                categoryHeader.innerHTML = category;
                scroller.appendChild(categoryHeader);

                // add line break
                var lineBreak = document.createElement("br");
                scroller.appendChild(lineBreak);

                // Loop over the menuitems to show them to user
                for (var i = 0; i < menuitems.length; i++){

                    // Clone the HTML template
                    let templateClone = template.content.cloneNode(true);

                    // Update the template with values recieved from server
                    templateClone.querySelector('#menuitem-name').innerHTML = menuitems[i]['name'];

                    // Add the id of the Item to the button
                    templateClone.querySelector('#add-btn').dataset.item_id = menuitems[i]['id']

                    // Add listener to the button in each template
                    templateClone.querySelector('#add-btn').addEventListener('click', function(event){
                    getItem(this.dataset.item_id)
                });

                    // Append the template to the dom
                    scroller.appendChild(templateClone);
                }
                // add line breaks
                var lineBreak = document.createElement("br");
                scroller.appendChild(lineBreak);
                var lineBreak = document.createElement("br");
                scroller.appendChild(lineBreak);
            }

        });

    });

}

function getItem(n) {
    // Get item details and view them in the modal

    // Use fetch to request data
    fetch(`/item/${n}`).then((response) => {

        // Convert the response data to JSON
        response.json().then((data) => {

            // If empty JSON, exit the function
            if (!data){

                // Should show an error message
                return;
            }

            // Get the item data from the response
            const itemName = data['item']['name'];
            const maxToppings = data['item']['max_toppings'];
            const pricing = data['item']['pricing'];
            const toppings = data['item']['toppings'];

            // Store information in local storage to be used
            // by the modal onclick
            localStorage.setItem('itemName', itemName);
            localStorage.setItem('maxToppings', maxToppings);
            localStorage.setItem('pricing', pricing);

            // Also add all toppings to the local storage
            localStorage.setItem('toppings', toppings);

            // add the item options to the modal body
            var modalBody = document.getElementsByClassName("modal-body")[0];
            modalBody.innerHTML = 'Item options<br>';

            // add line break
            var lineBreak = document.createElement("br");
            modalBody.appendChild(lineBreak);

            // add title for sizes of there are sizes
            if (pricing.length != 0) {
                var sizeTitle = document.createTextNode("Sizes");
                modalBody.appendChild(sizeTitle);
            }
            for(var i = 0; i < pricing.length; i++){

                // add line break
                var lineBreak = document.createElement("br");
                modalBody.appendChild(lineBreak);
                // add checkbox
                var checkbox = document.createElement("input");
                checkbox.type = "checkbox";
                checkbox.value = itemName;
                checkbox.name = pricing[i][1];
                checkbox.id = pricing[i][0];
                checkbox.itemId = n;
                checkbox.pricingId = pricing[i][2];

                // add the checkbox label
                var label = document.createElement('label');
                label.htmlFor = pricing[i][0];
                label.appendChild(document.createTextNode(pricing[i][0]));

                modalBody.appendChild(checkbox);
                modalBody.appendChild(label);
            }

            var lineBreak = document.createElement("br");
            modalBody.appendChild(lineBreak);
            if (maxToppings != 0) {
                // add toppings to the modal body
                // add toppings title
                var toppingsTitle = document.createTextNode('Toppings');
                modalBody.appendChild(toppingsTitle);
                for(var i = 0; i < toppings.length; i++){
                    // add line break
                    var lineBreak = document.createElement("br");
                    modalBody.appendChild(lineBreak);

                    // add checkbox
                    var checkbox = document.createElement("input");
                    checkbox.type = "checkbox";
                    checkbox.name = toppings[i];
                    checkbox.value = toppings[i];

                    // add the checkbox label
                    var label = document.createElement('label');
                    label.htmlFor = toppings[i];
                    label.appendChild(document.createTextNode(toppings[i]));

                    modalBody.appendChild(checkbox);
                    modalBody.appendChild(label);
                }
            }
            $('#Mymodal').modal('show');
        });
    });

}

// Call the load items method
loadItems()
