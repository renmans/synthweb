function fetch_post(card_id, route_url) {
    fetch('/' + route_url + '/' + card_id, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        data: JSON.stringify(card_id)
    }).then(response => console.log(response));
}

function change_status(event) {
    let card_id = event.target.parentNode.parentNode.parentNode.id;
    fetch_post(card_id, 'change');
}

function delete_task(event) {
    let card_id = event.target.parentNode.parentNode.parentNode.id;
    fetch_post(card_id, 'delete')
}

function showForm() {
    let hide = document.getElementById('hid');
    hide.style.display = (hide.style.display == 'block') ? 'none' : 'block';
}