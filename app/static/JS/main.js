    document.addEventListener("DOMContentLoaded", function() {


            var triggerButton = document.getElementById("triggerButton");
            var imageModal = new bootstrap.Modal(document.getElementById("imageModal"));

            triggerButton.onclick = function() {
                imageModal.show();
            }
        });


       document.addEventListener("DOMContentLoaded", function() {
            var triggerButton2 = document.getElementById("triggerButton2");
            var imageModal2 = new bootstrap.Modal(document.getElementById("imageModal2"));

            triggerButton2.onclick = function() {
                imageModal2.show();
            }
        });