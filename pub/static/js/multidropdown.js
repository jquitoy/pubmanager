var tagSelector = new MultiSelectTag('role', {
	required: true,               // default false.
	placeholder: 'Search roles',   // default 'Search'.
	onChange: function(selected) { // Callback when selection changes.
		console.log('Selection changed:', selected);
	}
});