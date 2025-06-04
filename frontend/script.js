// Tab switching functionality
document.addEventListener('DOMContentLoaded', function() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const contentSections = document.querySelectorAll('.content-section');

    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // Remove active class from all buttons and sections
            tabButtons.forEach(btn => btn.classList.remove('active'));
            contentSections.forEach(section => section.classList.remove('active'));
            
            // Add active class to clicked button and corresponding section
            this.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });

    // Search functionality
    const searchInputs = document.querySelectorAll('.search-input');
    
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const tableId = this.id.replace('Search', 'Table');
            const table = document.getElementById(tableId) || this.closest('.content-section').querySelector('tbody');
            
            if (table) {
                const rows = table.querySelectorAll('tr');
                
                rows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    if (text.includes(searchTerm)) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                });
            }
        });
    });

    // Action button functionality
    const actionButtons = document.querySelectorAll('.action-btn');
    
    actionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const action = this.classList.contains('view') ? 'view' : 
                          this.classList.contains('edit') ? 'edit' : 'delete';
            const row = this.closest('tr');
            const name = row.querySelector('td').textContent;
            
            handleAction(action, name, row);
        });
    });

    // Add button functionality
    const addButtons = document.querySelectorAll('.add-btn');
    
    addButtons.forEach(button => {
        button.addEventListener('click', function() {
            const buttonText = this.textContent.trim();
            const actionType = buttonText.replace('+ Add ', '');
            handleAdd(actionType);
        });
    });

    // Sign out functionality
    const signOutBtn = document.querySelector('.sign-out-btn');
    signOutBtn.addEventListener('click', function() {
        if (confirm('Are you sure you want to sign out?')) {
            alert('Signed out successfully!');
            // Redirect logic would go here
        }
    });
});

// Handle action buttons (view, edit, delete)
function handleAction(action, itemName, row) {
    switch(action) {
        case 'view':
            alert(`Viewing details for: ${itemName}`);
            // Open modal or navigate to detail page
            break;
        case 'edit':
            alert(`Editing: ${itemName}`);
            // Open edit modal or navigate to edit page
            break;
        case 'delete':
            if (confirm(`Are you sure you want to delete ${itemName}?`)) {
                row.style.opacity = '0.5';
                setTimeout(() => {
                    row.remove();
                    alert(`${itemName} has been deleted.`);
                }, 300);
            }
            break;
    }
}

// Handle add buttons
function handleAdd(type) {
    switch(type) {
        case 'User':
            showAddUserModal();
            break;
        case 'Course':
            showAddCourseModal();
            break;
        case 'Quiz':
            showAddQuizModal();
            break
    
    }
}