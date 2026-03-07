document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("themeToggle");
  const icon = toggle.querySelector("i");

  toggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");

    if (document.body.classList.contains("dark-mode")) {
      icon.classList.replace("fa-moon", "fa-sun");
      toggle.innerHTML = '<i class="fa-solid fa-sun"></i> Light Mode';
    } else {
      icon.classList.replace("fa-sun", "fa-moon");
      toggle.innerHTML = '<i class="fa-solid fa-moon"></i> Dark Mode';
    }
  });
});
