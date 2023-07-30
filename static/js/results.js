
document.addEventListener('DOMContentLoaded', () => {

    // var confettiCanvas = document.createElement('canvas');
    // document.body.appendChild(confettiCanvas);

    // var confetti = confetti.create(confettiCanvas, {
    //     resize: true,
    //     useWorker: true
    // });

    const round1 = document.querySelector('#groups-round-1');
    const round2 = document.querySelector('#groups-round-2');
    const round3 = document.querySelector('#groups-round-3');
    const round4 = document.querySelector('#groups-round-4');
    const rounds = [round1, round2, round3, round4];

    // parse user_name from url by ?user_name=
    let user_name = window.location.search.split("=")[1];

    // header-user-name 
    document.querySelector("#header-user-name").innerHTML = user_name;

    console.log(user_name);

    function getRounds(round) {       
        
        console.log(round);

        // hide all rounds that are not the current round
        for (let i = 0; i < rounds.length; i++) {
            if (i != round - 1) {
                rounds[i].style.display = "none";
            } else {
                rounds[i].style.display = "block";
            }
        }

        // add loading msg to 'user-group' div
        rounds[round - 1].querySelector(".user-group").innerHTML = "Loading...";

        let url = (round, user_name) => `/getResults/round/${round}/user/${user_name}`
        fetch(url(round, user_name))
            .then(response => response.json())
            .then(data => {

                console.log(data);

                rounds[round - 1].querySelector(".user-group").innerHTML = data.user_group;
                
                // confetti({
                //     particleCount: 100,
                //     spread: 70,
                //     origin: { y: 0.6 }
                // });

                // enable next round button
                rounds[round - 1].querySelector("button").disabled = false;
                rounds[round - 1].addEventListener('click', () => {
                    getRounds(round + 1);
                });

            });
    }

    function checkForResults() {
        fetch('/checkResults')
            .then(response => response.json())
            .then(data => {

                console.log(data);

                if (data.ready) {
                    clearInterval(refreshIntervalId);
                    getRounds(1);
                }

            });
    }

    // ping server for results every 5 seconds
    var refreshIntervalId = setInterval(checkForResults, 5000);

});