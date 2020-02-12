function change_status(event) {
    let card_id = event.target.parentNode.parentNode.parentNode.id;
    $.ajax({
        type: "POST",
        url: "/change/" + card_id,
        headers: { "Content-Type": "application/json" },
        data: JSON.stringify(card_id),
        success: function(response) {
            document.getElementById(card_id).childNodes[1].childNodes[11].innerHTML =
                (document.getElementById(card_id).childNodes[1].childNodes[11].innerHTML == 'Complete!') ?
                "Incomplete" : "Complete!";
            document.getElementById(card_id).childNodes[1].childNodes[11].style.color =
                (document.getElementById(card_id).childNodes[1].childNodes[11].innerHTML == 'Complete!') ?
                "green" : "red";
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function delete_task(event) {
    let card_id = event.target.parentNode.parentNode.parentNode.id;
    $.ajax({
        type: "POST",
        url: "/delete/" + card_id,
        headers: { "Content-Type": "application/json" },
        data: JSON.stringify(card_id),
        success: function (response) {
            document.getElementById(card_id).remove();
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function showForm() {
    let hide = document.getElementById('hid');
    hide.style.display = (hide.style.display == 'block') ? 'none' : 'block';
}