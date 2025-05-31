// Add this at the top of the file to ensure HTMX is loaded
console.log('MultiDropdown script loaded');

function initMultiSelectTag(containerId) {
    console.log('Initializing MultiSelectTag for container:', containerId);
    const container = document.getElementById(containerId);
    if (!container) {
        console.log('Container not found:', containerId);
        return;
    }
    
    const select = container.querySelector('select[name="role[]"]');
    console.log('Found select:', select);
    
    if (select) {
        // Clean up any existing MultiSelectTag in this container
        const existingWrapper = select.nextElementSibling;
        if (existingWrapper && existingWrapper.classList.contains('mult-select-tag')) {
            existingWrapper.remove();
        }
        
        // Initialize new MultiSelectTag
        new MultiSelectTag(select.id, {
            required: true,
            placeholder: 'Search roles',
            onChange: function(selected) {
                console.log('Selection changed:', selected);
            }
        });
        console.log('MultiSelectTag initialized for', select.id);
    }
}

// For Add Staff modal (on page load)
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded fired');
    initMultiSelectTag('add-staff-modal-content');
});

// For Edit Staff modal (after HTMX swap)
document.body.addEventListener('htmx:afterSettle', function(evt) {
    if (evt.detail.target && evt.detail.target.id === "edit-staff-modal-content") {
        console.log('Modal content settled, initializing dropdown');
        initMultiSelectTag('edit-staff-modal-content');
        document.getElementById('edit_staff_modal').showModal();
    }
});

