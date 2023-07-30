'use strict';

window.preferences = {};
var progress_perc = 0;
// var progress_bar = document.querySelector("#progress-bar");

var tinderContainer = document.querySelector('.tinder');
var allCards = document.querySelectorAll('.tinder--card');
var nope = document.getElementById('nope');
var love = document.getElementById('love');

var divResults = document.getElementById("swiped-items");
var swipeResultsWrapper = document.getElementById("swipe-results");
var sendSwipeResultsBtn = document.getElementById("sendSwipeResults");
var tinderWrapper = document.getElementsByClassName("tinder")[0];


function show_results() {
    swipeResultsWrapper.style.display = "block";    
    tinderWrapper.style.display = "none";

    console.log("SHOW-RESULTS:", window.preferences);

    // iterrate over window.preferences keys and show key & value in table,
    // make the value a checkbox (based on 0 and 1)

    Object.keys(window.preferences).forEach(function (key) {
        let row = document.createElement("tr");        

        let interest_cell = document.createElement("td");
        let value_cell = document.createElement("td");
        let super_like_cell = document.createElement("td");        
        
        // INTEREST
        interest_cell.innerHTML = window.preferences[key].text_full;

        // VALUE -> YES/NO
        var is_checked = () => (window.preferences[key].value) == 1 ? "checked" : "";
        let checkbox_html = `
        <div class="pretty p-icon p-toggle p-plain like-icon-div" id='${key}'>
            <input type="checkbox" ${is_checked()}/>
            <div class="state p-off">
                <i class="icon fa fa-heart-o "></i>
                <label>Nope</label>
            </div>
            <div class="state p-on p-info-o">
                <i class="icon fa fa-heart"></i>
                <label>Like</label>
            </div>
        </div>`;        
        // let checkbox = document.createElement("input");
        // checkbox.type = "checkbox";
        // checkbox.checked = d[key];
        // value_cell.appendChild(checkbox);
        value_cell.innerHTML = checkbox_html;

        // SUPER LIKE
        let super_like_html = `
        <div class="pretty p-icon p-round p-plain p-smooth">
            <input type="radio" name="super_like" />
            <div class="state p-success-o">
                <i class="icon fa fa-bolt"></i>
                <label>Superlike</label>
            </div>
        </div>
        `;
        // let super_like_button = document.createElement("input");
        // super_like_button.type = "radio";
        // super_like_button.name = "super_like";
        // super_like_cell.appendChild(super_like_button);
        super_like_cell.innerHTML = super_like_html;

        row.appendChild(interest_cell);
        row.appendChild(value_cell);
        row.appendChild(super_like_cell);

        divResults.appendChild(row);
    });

}

function collect_results() {
    var user_mail = document.getElementById("user_mail").value;
    console.log("USER-MAIL:", user_mail);

    // // var super_like = document.querySelector("input[name='super_like']:checked");    
    var iconHeartDivs = document.getElementsByClassName("like-icon-div");
    var iconHeartDivsArray = Array.from(iconHeartDivs);
    console.log("ICON-HEART-ARRAY:", iconHeartDivsArray);
    

    console.log("BEFORE-RESULTS (COLLECT)", window.preferences);    

    // get the checked checkboxes
    for (var i = 0; i < iconHeartDivsArray.length; i++) {
        var iconHeartDiv = iconHeartDivsArray[i];
        var offDiv = iconHeartDiv.getElementsByClassName("p-off")[0];
        var cardId = iconHeartDiv.id;
    
        // console.log(window.preferences[id]);
        console.log(cardId, offDiv.style.length, offDiv);
    
        var updatedValue = offDiv.style.length == 0 ? 1 : 0;
        window.preferences[cardId].value = updatedValue;
    }
    console.log("AFTER:", window.preferences);


    // var results = {
    //     user_mail: user_mail,
    //     prefs: window.preferences,
    //     super_like: super_like
    // };

    // return results;
    // return window.preferences;
}

// SEND SWIPE RESULTS
sendSwipeResultsBtn.addEventListener("click", (evt) => {

    console.log("BEFORE-RESULTS (SEND)", window.preferences);
    var results = collect_results();
    console.log("COLLECTED-RESULTS:", results);

    // console.log(user_mail);
    // console.log(window.preferences);

    // send window.preferences to server using fetch POST
    fetch('/swipe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(
            { prefs: window.preferences, user_mail: user_mail }
        )
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        });
});

function initCards(card, index) {
    var newCards = document.querySelectorAll('.tinder--card:not(.removed)');

    newCards.forEach(function (card, index) {
        card.style.zIndex = allCards.length - index;
        card.style.transform = 'scale(' + (20 - index) / 20 + ') translateY(-' + 30 * index + 'px)';
        card.style.opacity = (10 - index) / 10;
    });

    tinderContainer.classList.add('loaded');
}

function check_progress() {
    // -2 because of the intro cards (excluded)
    progress_perc = Math.round(Object.keys(window.preferences).length / (allCards.length-2) * 100);
    console.log("PROGRESS: " + progress_perc);

    // progress_bar.style.width = progress_perc + "%";
    // progress_bar.innerHTML = progress_perc + "%";

    if (progress_perc == 100) {
        show_results();
    }
}

function feedback(card, value) {
    var card_id = card.id;

    if (card_id == "research_interest_intro" || card_id == "method_intro") {
        return false;
    }

    var text_full = card.getElementsByClassName("interest-text-full")[0].value;
    var swipe_type = card.getElementsByClassName("swipe-type")[0].value;

    window.preferences[card_id] = {
        text_full, value, swipe_type
    }

    console.log("FEEDBACK:", window.preferences);
}

var action_love = (card) => feedback(card, 1);
var action_nope = (card) => feedback(card, 0);

initCards();

allCards.forEach(function (el, index) {
    var hammertime = new Hammer(el);

    hammertime.on('pan', function (event) {
        el.classList.add('moving');

        check_progress();
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

        check_progress();
    });

    hammertime.on('panend', function (event) {

        if (tinderContainer.classList.contains('tinder_love')) {            
            action_love(el);
        } else if (tinderContainer.classList.contains('tinder_nope')) {
            action_nope(el);
        }

        el.classList.remove('moving');
        tinderContainer.classList.remove('tinder_love');
        tinderContainer.classList.remove('tinder_nope');

        var moveOutWidth = document.body.clientWidth;
        var keep = Math.abs(event.deltaX) < 80 || Math.abs(event.velocityX) < 0.5;
       
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
        
        check_progress();
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
            action_love(card);
        } else {
            card.style.transform = 'translate(-' + moveOutWidth + 'px, -100px) rotate(30deg)';
            action_nope(card);
        }        

        check_progress();
        initCards();
        event.preventDefault();
    };
}

var nopeListener = createButtonListener(false);
var loveListener = createButtonListener(true);

nope.addEventListener('click', nopeListener);
love.addEventListener('click', loveListener);