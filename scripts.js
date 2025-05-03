document.addEventListener("DOMContentLoaded", function () {
    // Mobile Menu Toggle
    const menuButton = document.querySelector(".md\\:hidden");
    const mobileMenu = document.querySelector(".hidden.md\\:hidden");
    
    if (menuButton && mobileMenu) {
      menuButton.addEventListener("click", function () {
        mobileMenu.classList.toggle("hidden");
      });
    }
  
    // Theme Toggle
    const themeToggle = document.getElementById("themeToggle");
    if (themeToggle) {
      const themeIcon = themeToggle.querySelector("i");
      let isDark = true;
      
      themeToggle.addEventListener("click", function () {
        isDark = !isDark;
        
        if (isDark) {
          document.body.classList.remove("light-theme");
          themeIcon.classList.remove("ri-moon-line");
          themeIcon.classList.add("ri-sun-line");
        } else {
          document.body.classList.add("light-theme");
          themeIcon.classList.remove("ri-sun-line");
          themeIcon.classList.add("ri-moon-line");
        }
      });
    }
  });