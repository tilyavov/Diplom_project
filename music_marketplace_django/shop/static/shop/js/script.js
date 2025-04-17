document.addEventListener('DOMContentLoaded', function() {
    const userMenu = document.getElementById('userMenu');
    const dropdownMenu = document.getElementById('dropdownMenu');

    if (userMenu && dropdownMenu) {
        userMenu.addEventListener('click', function(event) {
            event.stopPropagation();
            dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
        });

        document.addEventListener('click', function(event) {
            if (dropdownMenu.style.display === 'block' && !userMenu.contains(event.target)) {
                dropdownMenu.style.display = 'none';
            }
        });
    }
});