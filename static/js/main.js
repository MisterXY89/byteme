
document.addEventListener("DOMContentLoaded", evt => {

    // var confettiCanvas = document.createElement('canvas');
    // document.body.appendChild(confettiCanvas);

    // var confetti = confetti.create(confettiCanvas, {
    //     resize: true,
    //     useWorker: true
    // });

    // confetti({
    //     particleCount: 100,
    //     spread: 70,
    //     origin: { y: 0.6 }
    // });

    const nextStepBtn = document.querySelector("#next-step-btn");
    const step1 = document.querySelector("#step-1-form");
    const step2 = document.querySelector("#step-2-form");

    nextStepBtn.addEventListener("click", evt => {

        step1.style.display = "none";
        step2.style.display = "block";         

    });


}); 