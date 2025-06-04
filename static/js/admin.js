function showSection(section) {
  // Hide all content sections
  document.querySelectorAll('.content-section').forEach(sec => {
    sec.classList.add('hidden');
  });

  // Remove active class from all tabs
  document.querySelectorAll('.tab').forEach(tab => {
    tab.classList.remove('active');
  });

  // Show the selected section
  document.getElementById(section + '-section').classList.remove('hidden');

  // Set the active tab
  event.target.classList.add('active');
}
