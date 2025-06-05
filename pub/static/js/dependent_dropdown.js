const staffData = {{ staff_by_role_json|safe }}; // Pass this from your Django view as a JSON dict: {role_id: [{id, name}, ...]}
function updateStaffOptions(roleSelect) {
  const staffSelect = roleSelect.closest('.staff-role-row').querySelector('.staff-select');
  const roleId = roleSelect.value;
  staffSelect.innerHTML = '<option value="">Select Staff</option>';
  if (roleId && staffData[roleId]) {
    staffData[roleId].forEach(staff => {
      const opt = document.createElement('option');
      opt.value = staff.id;
      opt.textContent = staff.name;
      staffSelect.appendChild(opt);
    });
  }
}

document.addEventListener('change', function(e) {
  if (e.target.classList.contains('role-select')) {
    updateStaffOptions(e.target);
  }
});

document.getElementById('add-staff-role-btn').addEventListener('click', function() {
  const container = document.getElementById('staff-role-container');
  const firstRow = container.querySelector('.staff-role-row');
  const newRow = firstRow.cloneNode(true);
  // Reset selects
  newRow.querySelector('.role-select').selectedIndex = 0;
  const staffSelect = newRow.querySelector('.staff-select');
  staffSelect.innerHTML = '<option value="">Select Staff</option>';
  container.appendChild(newRow);
});
