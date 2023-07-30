'use strict';

var preferences = {};
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

    console.log("SHOW-RESULTS:", preferences);

    // iterrate over preferences keys and show key & value in table,
    // make the value a checkbox (based on 0 and 1)

    Object.keys(preferences).forEach(function (key) {
        let row = document.createElement("tr");        

        let interest_cell = document.createElement("td");
        let value_cell = document.createElement("td");
        let super_like_cell = document.createElement("td");        
        
        // INTEREST
        interest_cell.innerHTML = preferences[key].text_full;

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
            <input type="radio" name="super_like" id='SL-${key}'/>
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
    /**
     * Collect the results from the swipe cards and return them as a JSON object
     * + collect superlike
     */

    var userMail = document.getElementById("user_mail").value;
    var userName = document.getElementById("user_name").value;
    var effort = document.getElementById("effort").value;
    var meth_pref = document.getElementById("preference").value;

    var superLikeDiv = document.querySelector("input[name='super_like']:checked");    
    var iconHeartDivs = document.getElementsByClassName("like-icon-div");
    var iconHeartDivsArray = Array.from(iconHeartDivs);   

    // get the checked checkboxes
    for (var i = 0; i < iconHeartDivsArray.length; i++) {
        var iconHeartDiv = iconHeartDivsArray[i];
        var offDiv = iconHeartDiv.getElementsByClassName("p-off")[0];
        var cardId = iconHeartDiv.id;
    
        var updatedValue = offDiv.checkVisibility() ? 0 : 1;
        preferences[cardId].value = updatedValue;

        var isSuperLike;
        if (superLikeDiv == null) {
            isSuperLike = 0;
        } else {
            isSuperLike = superLikeDiv.id.split("-")[1] == cardId ? 1 : 0;
        }

        preferences[cardId].super_like = isSuperLike;
    }

    var results = {
        user_mail: userMail,
        user_name: userName,
        swipes: preferences,
        effort: effort,
        preference: meth_pref
    };

    return results;
}

function sendResults() {
    /**
     * Collect & send the results to the server using fetch POST
     */

    var results = collect_results();
    console.log("SEND-RESULTS:", results);

    console.log(JSON.stringify(results));

    fetch('/swipe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(
            results
        )
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        });
}

function initCards(card, index) {
    /**
     * Initialize the cards
     * 
     * @param {object} card
     * @param {number} index
     */
    var newCards = document.querySelectorAll('.tinder--card:not(.removed)');

    newCards.forEach(function (card, index) {
        card.style.zIndex = allCards.length - index;
        card.style.transform = 'scale(' + (20 - index) / 20 + ') translateY(-' + 30 * index + 'px)';
        card.style.opacity = (10 - index) / 10;
    });

    tinderContainer.classList.add('loaded');
}

function checkProgress() {
    /**
     * Check the progress of the swipe cards
     * if 100% -> show results
     * Optional: show progress bar
     */

    // -2 because of the intro cards (excluded)
    progress_perc = Math.round(Object.keys(preferences).length / (allCards.length-2) * 100);
    // console.log("PROGRESS: " + progress_perc);

    // progress_bar.style.width = progress_perc + "%";
    // progress_bar.innerHTML = progress_perc + "%";

    if (progress_perc == 100) {
        show_results();
    }
}

function feedback(card, value) {
    /**
     * save the feedback of the card in the preferences object
     * 1 or 0 for like or nope, skip intro cards
     * 
     * @param {object} card
     * @param {number} value
     */
    var card_id = card.id;

    if (card_id == "research_interest_intro" || card_id == "method_intro") {
        return false;
    }

    var text_full = card.getElementsByClassName("interest-text-full")[0].value;
    var swipe_type = card.getElementsByClassName("swipe-type")[0].value;

    preferences[card_id] = {
        text_full, value, swipe_type
    }

    // console.log("FEEDBACK:", preferences);
}

// name the functions for the swipe actions
var action_love = (card) => feedback(card, 1);
var action_nope = (card) => feedback(card, 0);

initCards();

// add the swipe functionality
allCards.forEach(function (el, index) {
    var hammertime = new Hammer(el);

    // keep track of the pan
    hammertime.on('pan', function (event) {
        el.classList.add('moving');

        checkProgress();
    });

    // reset the pan on release of the card
    hammertime.on('pan', function (event) {
        if (event.deltaX === 0) return;
        if (event.center.x === 0 && event.center.y === 0) return;

        tinderContainer.classList.toggle('tinder_love', event.deltaX > 0);
        tinderContainer.classList.toggle('tinder_nope', event.deltaX < 0);

        var xMulti = event.deltaX * 0.03;
        var yMulti = event.deltaY / 80;
        var rotate = xMulti * yMulti;

        event.target.style.transform = 'translate(' + event.deltaX + 'px, ' + event.deltaY + 'px) rotate(' + rotate + 'deg)';

        checkProgress();
    });

    // decide if the card is removed or not
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

        // if the card is removed, move it out of the screen
        if (keep) {
            event.target.style.transform = '';
        } else {
            // animate the card out of the screen
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
        
        checkProgress();
    });
});

function createButtonListener(love) {
    /**
     * Create a button listener for the swipe buttons
     * 
     * @param {boolean} love
     * @returns {function}
     * 
     */
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

        checkProgress();
        initCards();
        event.preventDefault();
    };
}

// event listeners
var nopeListener = createButtonListener(false);
var loveListener = createButtonListener(true);

nope.addEventListener('click', nopeListener);
love.addEventListener('click', loveListener);
sendSwipeResultsBtn.addEventListener('click', sendResults);