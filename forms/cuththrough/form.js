function downloadCSV() {
    const inputs = document.querySelectorAll('input[type="text"]');
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
