// This is your AJAX script

document.addEventListener("DOMContentLoaded", function () {
  // 1. Get a reference to the modal object
  const detailModal = new bootstrap.Modal(
    document.getElementById("bookDetailModal")
  );
  const modalContent = document.querySelector(
    "#bookDetailModal .modal-content"
  );

  // 2. Add event listener to all 'View Details' buttons
  document.querySelectorAll(".view-details").forEach((button) => {
    button.addEventListener("click", function (event) {
      const url = this.getAttribute("data-detail-url");

      // Show a loading state (optional)
      modalContent.innerHTML =
        '<div class="modal-body text-center py-5">Loading...</div>';

      // 3. Make the AJAX Request (using Fetch API, modern AJAX)
      fetch(url)
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.text();
        })
        .then((html) => {
          // 4. Insert the fetched HTML content into the modal container
          modalContent.innerHTML = html;
          detailModal.show(); // Show the modal once content is loaded
        })
        .catch((error) => {
          console.error("Fetch error:", error);
          modalContent.innerHTML =
            '<div class="modal-body text-danger py-5">Error loading book details.</div>';
          detailModal.show();
        });
    });
  });
});
