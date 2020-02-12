let mousePosition;
let offset = [0,0];
let hid = document.getElementById('hid');
let mover = document.getElementById('mover');
let isDown = false;
let cards = document.querySelectorAll('.card-heading'); 

mover.addEventListener('mousedown', function(e) {
    isDown = true;
    offset = [
        hid.offsetLeft - e.clientX,
        hid.offsetTop - e.clientY
    ];
    for (let card of cards) {
        card.style.backgroundColor = 'grey';
    }
}, true);

document.addEventListener('mouseup', function() {
    isDown = false;
    for (let card of cards) {
        card.style.backgroundColor = 'rgb(0, 0, 150)';
    }
}, true);

document.addEventListener('mousemove', function(event) {
    event.preventDefault();
    if (isDown) {
        mousePosition = {

            x : event.clientX,
            y : event.clientY

        };
        hid.style.left = (mousePosition.x + offset[0]) + 'px';
        hid.style.top  = (mousePosition.y + offset[1]) + 'px';
    }
}, true);
