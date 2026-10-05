function toggleMenu() {
    const nav = document.getElementById("mainNav");

    if (nav) {
        nav.classList.toggle("mobile-open");
    }
}


document.addEventListener("DOMContentLoaded", function () {

    const messages = document.querySelectorAll(".message");

    messages.forEach(function (message) {

        setTimeout(function () {
            message.classList.add("hide");
        }, 4000);

    });

});