  const fileInput = document.querySelector('input[type="file"]');
  const previewImage = document.getElementById('image-placeholder');

  if (fileInput) {
    fileInput.addEventListener('change', function() {
      const file = this.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
          previewImage.setAttribute('src', e.target.result);
        }
        reader.readAsDataURL(file);
      }
    });
  }
