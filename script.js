function toggleLanguage() {
    let title = document.getElementById("title");
    let description = document.getElementById("description");
    let button = document.querySelector(".lang-btn");

    if (title.innerText === "من یک برنامه‌نویس پایتون هستم") {
        title.innerText = "I'm a Python Developer";
        description.innerText = "My expertise is in cybersecurity and network hacking.";
        button.innerText = "فارسی";
    } else {
        title.innerText = "من یک برنامه‌نویس پایتون هستم";
        description.innerText = "تخصص من امنیت سایبری و هک شبکه است.";
        button.innerText = "English";
    }
}

function toggleMenu() {
    let menu = document.getElementById("menu");
    if (menu.style.display === "block") {
        menu.style.display = "none";
    } else {
        menu.style.display = "block";
    }
}