function downloadCSV() {
    const inputs = document.querySelectorAll('input[type="text"], input[type="number"], select');
    const csvRows = [];

    // Collect headers
    const headers = [];
    inputs.forEach(input => {
        headers.push(input.name);
    });
    csvRows.push(headers.join(','));

    // Collect values
    const values = [];
    inputs.forEach(input => {
        values.push(input.value);
    });
    csvRows.push(values.join(','));

    // Convert to CSV format
    const csvString = csvRows.join('\n');
    const blob = new Blob([csvString], { type: 'text/csv' });

    // Get file name from input
    const fileName = document.getElementById('fileName').value || 'data';
    
    // Create download link
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `${fileName}.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function setDefaultDate() {
    const dateInput = document.getElementById('cal-date');
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0'); // Months are zero-based
    const dd = String(today.getDate()).padStart(2, '0');
    const formattedDate = `${mm}-${dd}-${yyyy}`;
    dateInput.value = formattedDate;
}

window.addEventListener('DOMContentLoaded', (event) => {
    // Set default date when the page loads
    setDefaultDate();
});