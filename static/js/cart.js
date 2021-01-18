let updateBtns = document.getElementsByClassName("update-cart")

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener("click", function () {
        let product_id = this.dataset.product
        let action = this.dataset.action

        console.log("Product Id:", product_id, " Action: ", action)

        if (user != "AnonymousUser") {
            addItemToCart(product_id, action)
        }
    })
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