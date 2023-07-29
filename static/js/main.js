
document.addEventListener("DOMContentLoaded", evt => {

    const nextStepBtn = document.querySelector("#next-step-btn");
    const step1 = document.querySelector("#step-1-form");
    const step2 = document.querySelector("#step-2-form");

    nextStepBtn.addEventListener("click", evt => {

        step1.style.display = "none";
        step2.style.display = "block";  

    });


}); 