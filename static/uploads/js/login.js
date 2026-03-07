function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = "block";
    document.body.classList.add("modal-open");
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = "none";
    document.body.classList.remove("modal-open");
  }
}

document.addEventListener("DOMContentLoaded", function () {
  // Toggle password visibility on click of eye icon
  document.querySelectorAll(".toggle-password").forEach(function (toggle) {
    toggle.addEventListener("click", function () {
      const input = toggle.closest(".input-group").querySelector("input");
      const icon = toggle.querySelector("i");
      if (input.type === "password") {
        input.type = "text";
        icon.classList.replace("fa-eye", "fa-eye-slash");
      } else {
        input.type = "password";
        icon.classList.replace("fa-eye-slash", "fa-eye");
      }
    });
  });

  // Close modal when clicking outside modal content
  window.addEventListener("click", function (event) {
    document.querySelectorAll(".custom-modal").forEach((modal) => {
      if (event.target === modal) {
        closeModal(modal.id);
      }
    });
  });
});
