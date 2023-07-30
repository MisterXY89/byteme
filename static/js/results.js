
document.addEventListener('DOMContentLoaded', () => {

    const round1 = document.querySelector('#groups-round-1');
    const round2 = document.querySelector('#groups-round-2');
    const round3 = document.querySelector('#groups-round-3');
    const round4 = document.querySelector('#groups-round-4');

    // ping server for results every 5 seconds
    setInterval(() => {
        fetch('/checkResults')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            document.querySelector('#results').innerHTML = data.results;
        });
    }, 5000);
    
});