// Mobile menu toggle
        document.addEventListener('DOMContentLoaded', function () {
            const menuToggle = document.getElementById('menuToggle');
            const navLinks = document.getElementById('navLinks');

            menuToggle.addEventListener('click', function () {
                navLinks.classList.toggle('active');
            });

            // Close menu when clicking outside
            document.addEventListener('click', function (event) {
                const isClickInsideNav = navLinks.contains(event.target) || menuToggle.contains(event.target);
                if (!isClickInsideNav && navLinks.classList.contains('active')) {
                    navLinks.classList.remove('active');
                }
            });

            // Smooth scrolling for anchor links
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function (e) {
                    e.preventDefault();

                    const targetId = this.getAttribute('href').substring(1);
                    if (targetId) {
                        const targetElement = document.getElementById(targetId);
                        if (targetElement) {
                            window.scrollTo({
                                top: targetElement.offsetTop - 80,
                                behavior: 'smooth'
                            });
                        }
                    }
                });
            });
        });