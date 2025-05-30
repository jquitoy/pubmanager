document.addEventListener('DOMContentLoaded', function() {
  const roleSelect = document.getElementById('id_role');
  const staffSearch = document.getElementById('id_staff_search');
  const staffResults = document.getElementById('staff-results');
  const selectedStaffContainer = document.getElementById('selected-staff-container');
  const selectedStaffInput = document.getElementById('id_selected_staff');

  let selectedStaff = [];

  function renderResults(staffs) {
    staffResults.innerHTML = '';
    if (staffs.length === 0) {
      staffResults.innerHTML = '<div class="p-2 text-gray-500">No staff found.</div>';
      staffResults.classList.remove('hidden');
      return;
    }
    staffs.forEach(staff => {
      const div = document.createElement('div');
      div.className = 'p-2 hover:bg-blue-100 cursor-pointer';
      div.textContent = `${staff.name} (${staff.email})`;
      div.addEventListener('click', function() {
        if (!selectedStaff.some(s => s.id === staff.id)) {
          selectedStaff.push(staff);
          updateSelectedStaff();
        }
        staffResults.classList.add('hidden');
        staffSearch.value = '';
      });
      staffResults.appendChild(div);
    });
    staffResults.classList.remove('hidden');
  }

  function updateSelectedStaff() {
    selectedStaffContainer.innerHTML = '';
    selectedStaff.forEach(staff => {
      const div = document.createElement('div');
      div.className = 'flex items-center gap-2 bg-blue-50 rounded px-2 py-1';
      div.textContent = staff.name;
      const removeBtn = document.createElement('button');
      removeBtn.type = 'button';
      removeBtn.className = 'text-red-500 ml-2';
      removeBtn.textContent = '×';
      removeBtn.addEventListener('click', function() {
        selectedStaff = selectedStaff.filter(s => s.id !== staff.id);
        updateSelectedStaff();
      });
      div.appendChild(removeBtn);
      selectedStaffContainer.appendChild(div);
    });
    // Update hidden input with selected staff IDs (comma-separated)
    if (selectedStaffInput) {
      selectedStaffInput.value = selectedStaff.map(s => s.id).join(',');
    }
  }

  function fetchStaff() {
    const role = roleSelect ? roleSelect.value : '';
    const q = staffSearch.value;
    if (!q && !role) {
      staffResults.classList.add('hidden');
      return;
    }
    fetch(`/api/staff/?role=${role}&q=${encodeURIComponent(q)}`)
      .then(res => res.json())
      .then(data => renderResults(data.results));
  }

  if (staffSearch) {
    staffSearch.addEventListener('input', function() {
      if (staffSearch.value.length > 0) {
        fetchStaff();
      } else {
        staffResults.classList.add('hidden');
      }
    });
    staffSearch.addEventListener('focus', function() {
      if (staffSearch.value.length > 0) {
        fetchStaff();
      }
    });
  }

  if (roleSelect) {
    roleSelect.addEventListener('change', function() {
      if (staffSearch.value.length > 0) {
        fetchStaff();
      }
    });
  }

  document.addEventListener('click', function(e) {
    if (!staffResults.contains(e.target) && e.target !== staffSearch) {
      staffResults.classList.add('hidden');
    }
  });
});
