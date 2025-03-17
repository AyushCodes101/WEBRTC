document.addEventListener("DOMContentLoaded", function () {
    const navLinks = document.querySelectorAll("nav a");

    // Function to update active link
    function updateActiveLink() {
        const currentPath = window.location.pathname.split("/").pop();

        navLinks.forEach(link => {
            if (link.getAttribute("href") === currentPath) {
                link.classList.add("active");
            } else {
                link.classList.remove("active");
            }
        });
    }

    // Run on page load
    updateActiveLink();
});
