let updateBtns = document.getElementsByClassName("update-cart")

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener("click", function () {
        let product_id = this.dataset.product
        let action = this.dataset.action

        console.log("Product Id:", product_id, " Action: ", action)

        if (user != "AnonymousUser") {
            addItemToCart(product_id, action)
        } else {
            addCookieItem(product_id, action)
        }
    })
}

function addCookieItem(product_id, action) {
    if (cart[product_id] == null) {
        cart[product_id] = {'quantity': 1}
    } else {
        if (action == "add") {
            cart[product_id]['quantity']++;
        } else {
            cart[product_id]['quantity']--;

            if (cart[product_id]['quantity'] <= 0) {
                delete cart[product_id]
            }
        }
    }

    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path/"
    console.log("Cart:", cart)

}


function addItemToCart(product_id, action) {
    url = "/update_item/"
    fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'product_id': product_id,
            'action': action,
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log("Success:", data)
            location.reload()
        })
}