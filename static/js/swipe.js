'use strict';

var preferences = {};
// var progress_bar = document.querySelector("#progress-bar");

var tinderContainer = document.querySelector('.tinder');
var allCards = document.querySelectorAll('.tinder--card');
var nope = document.getElementById('nope');
var love = document.getElementById('love');


var divResults = document.getElementById("swiped-items");
var swipeResultsWrapper = document.getElementById("swipe-results");
var sendSwipeResultsBtn = document.getElementById("sendSwipeResults");
var tinderWrapper = document.getElementsByClassName("tinder")[0];

var progress_perc = 0;

function show_results() {
    swipeResultsWrapper.style.display = "block";    
    tinderWrapper.style.display = "none";

    // iterrate over preferences keys and show key & value in table,
    // make the value a checkbox (based on 0 and 1)

    Object.keys(preferences).forEach(function (key) {
        let row = document.createElement("tr");

        let interest_cell = document.createElement("td");
        let value_cell = document.createElement("td");
        let super_like_cell = document.createElement("td");        
        
        // INTEREST
        interest_cell.innerHTML = key;

        // VALUE -> YES/NO
        let checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.checked = preferences[key];
        value_cell.appendChild(checkbox);

        // SUPER LIKE
        let super_like_button = document.createElement("input");
        super_like_button.type = "radio";
        super_like_button.name = "super_like";
        super_like_cell.appendChild(super_like_button);

        row.appendChild(interest_cell);
        row.appendChild(value_cell);
        row.appendChild(super_like_cell);

        divResults.appendChild(row);
    });

}

function send_results() {
    let user_mail = document.getElementById("user_mail").value;

    console.log(user_mail);
    console.log(preferences);

    // send preferences to server using fetch POST
    fetch('/swipe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(
            { preferences, user_mail }
        )
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        });
}

function initCards(card, index) {
    var newCards = document.querySelectorAll('.tinder--card:not(.removed)');

    newCards.forEach(function (card, index) {
        card.style.zIndex = allCards.length - index;
        card.style.transform = 'scale(' + (20 - index) / 20 + ') translateY(-' + 30 * index + 'px)';
        card.style.opacity = (10 - index) / 10;
    });

    tinderContainer.classList.add('loaded');
}

initCards();

allCards.forEach(function (el, index) {
    var hammertime = new Hammer(el);

    hammertime.on('pan', function (event) {
        el.classList.add('moving');

         // if last card is removed, redirect to results page
         if (progress_perc == 100) {
            show_results();
        }
    });

    hammertime.on('pan', function (event) {
        if (event.deltaX === 0) return;
        if (event.center.x === 0 && event.center.y === 0) return;

        tinderContainer.classList.toggle('tinder_love', event.deltaX > 0);
        tinderContainer.classList.toggle('tinder_nope', event.deltaX < 0);

        var xMulti = event.deltaX * 0.03;
        var yMulti = event.deltaY / 80;
        var rotate = xMulti * yMulti;

        event.target.style.transform = 'translate(' + event.deltaX + 'px, ' + event.deltaY + 'px) rotate(' + rotate + 'deg)';

        // if last card is removed, redirect to results page
        if (progress_perc == 100) {
            show_results();
        }
    });

    hammertime.on('panend', function (event) {
        if (tinderContainer.classList.contains('tinder_love')) {
            preferences[el.id] = 1;
        } else if (tinderContainer.classList.contains('tinder_nope')) {
            preferences[el.id] = 0;
        }

        el.classList.remove('moving');
        tinderContainer.classList.remove('tinder_love');
        tinderContainer.classList.remove('tinder_nope');

        var moveOutWidth = document.body.clientWidth;
        var keep = Math.abs(event.deltaX) < 80 || Math.abs(event.velocityX) < 0.5;

        progress_perc = Math.round(Object.keys(preferences).length / allCards.length * 100);
        // progress_bar.style.width = progress_perc + "%";
        // progress_bar.innerHTML = progress_perc + "%";

        console.log(preferences);
        console.log(progress_perc);
        console.log(allCards.length);

        console.log(progress_perc);

        event.target.classList.toggle('removed', !keep);

        if (keep) {
            event.target.style.transform = '';
        } else {
            var endX = Math.max(Math.abs(event.velocityX) * moveOutWidth, moveOutWidth);
            var toX = event.deltaX > 0 ? endX : -endX;
            var endY = Math.abs(event.velocityY) * moveOutWidth;
            var toY = event.deltaY > 0 ? endY : -endY;
            var xMulti = event.deltaX * 0.03;
            var yMulti = event.deltaY / 80;
            var rotate = xMulti * yMulti;

            event.target.style.transform = 'translate(' + toX + 'px, ' + (toY + event.deltaY) + 'px) rotate(' + rotate + 'deg)';
            initCards();
        }

        // if last card is removed, redirect to results page
        if (progress_perc == 100) {
            show_results();
        }
    });
});

function createButtonListener(love) {
    return function (event) {
        var cards = document.querySelectorAll('.tinder--card:not(.removed)');
        var moveOutWidth = document.body.clientWidth * 1.5;

        if (!cards.length) return false;

        var card = cards[0];

        card.classList.add('removed');

        if (love) {
            card.style.transform = 'translate(' + moveOutWidth + 'px, -100px) rotate(-30deg)';
            // TODO: store the user's choice in the database
            preferences[card.id] = 1;
        } else {
            card.style.transform = 'translate(-' + moveOutWidth + 'px, -100px) rotate(30deg)';
            // TODO: store the user's choice in the database
            preferences[card.id] = 0;
        }

        console.log(preferences);
        progress_perc = Math.round(Object.keys(preferences).length / (allCards.length) * 100);

        console.log("BTN: " + progress_perc)
        

        if (progress_perc == 100) {
            show_results();
        }

        initCards();

        event.preventDefault();
    };
}

var nopeListener = createButtonListener(false);
var loveListener = createButtonListener(true);

nope.addEventListener('click', nopeListener);
love.addEventListener('click', loveListener);

sendSwipeResultsBtn.addEventListener("click", send_results);