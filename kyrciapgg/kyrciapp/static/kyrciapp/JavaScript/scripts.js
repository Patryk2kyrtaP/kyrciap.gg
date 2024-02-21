document.getElementById('menuToggle').addEventListener('click', function() {
    var menu = document.getElementById('navMenu');
    if (menu.style.display === 'none') {
        menu.style.display = 'block';
    } else {
        menu.style.display = 'none';
    }
});



function setTheme(theme) {
localStorage.setItem('theme', theme);
}

function applySavedTheme() {
const theme = localStorage.getItem('theme');
const themeToggleBtn = document.getElementById('theme-toggle');

if (theme === 'light') {
document.body.classList.remove('bg-dark');
document.body.classList.add('light-theme');

if (themeToggleBtn) themeToggleBtn.innerHTML = '<i class="bi bi-moon"></i>';
} else {

document.body.classList.add('bg-dark');
document.body.classList.remove('light-theme');

if (themeToggleBtn) themeToggleBtn.innerHTML = '<i class="bi bi-brightness-alt-high"></i>';
}
}

document.addEventListener("DOMContentLoaded", applySavedTheme);

document.getElementById('theme-toggle').addEventListener('click', function() {
const isLightTheme = document.body.classList.contains('light-theme');

if (isLightTheme) {
    setTheme('dark'); 
} else {
    setTheme('light'); 
}

applySavedTheme(); 
});