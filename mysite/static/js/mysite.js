document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuButton = document.querySelector('[aria-controls="mobile-menu"]');
    const mobileMenu = document.getElementById('mobile-menu');

    mobileMenuButton.addEventListener('click', function() {
        const isExpanded = mobileMenuButton.getAttribute('aria-expanded') === 'true';
        mobileMenuButton.setAttribute('aria-expanded', !isExpanded);
        mobileMenu.classList.toggle('hidden');
    });
});