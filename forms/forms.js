function downloadXLSX() {
    const inputs = document.querySelectorAll('input[type="text"], input[type="number"], input[type="date"], select');
    const data = [];

    // Collect headers
    const headers = ['type'];
    inputs.forEach(input => {
        headers.push(input.name);
    });
    headers.push('Photo 1', 'Photo 2', 'Photo 3'); // Add headers for photos
    data.push(headers);

    // Collect values
    const values = ['parallel'];
    inputs.forEach(input => {
        values.push(input.value);
    });
    values.push(
        document.getElementById('fileName1').textContent,
        document.getElementById('fileName2').textContent,
        document.getElementById('fileName3').textContent
    ); // Add photo file names
    data.push(values);

    // Convert data to worksheet and then to XLSX
    const worksheet = XLSX.utils.aoa_to_sheet(data);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');
    const xlsxData = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
    const blob = new Blob([xlsxData], { type: 'application/octet-stream' });

    // Get file name from input
    const fileName = document.getElementById('fileName').value || 'data';

    // Create download link
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `${fileName}.xlsx`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    localStorage.removeItem('formData');

    inputs.forEach(input => {
        input.value = input.defaultValue;
    });

    document.getElementById('fileName1').textContent = 'No file chosen';
    document.getElementById('fileName2').textContent = 'No file chosen';
    document.getElementById('fileName3').textContent = 'No file chosen';
}

    window.addEventListener('message', function(event) {
            // Validate the origin of the event for security purposes
            if (event.origin !== window.location.origin) {
                return;
            }

            const { nextObjectId } = event.data;
            const fileNameInput = document.getElementById('fileName');
            fileNameInput.value = `${nextObjectId}`;
        });

document.getElementById('curb-avg-button').addEventListener('click', function() {
    // Prompt the user for 5 numbers
    let numbers = [];
    for (let i = 0; i < 5; i++) {
        let num = parseFloat(prompt(`Enter number ${i + 1}:`));
        if (isNaN(num)) {
            alert('Please enter a valid number.');
            return;
        }
        numbers.push(num);
    }

    // Calculate the average
    let sum = numbers.reduce((a, b) => a + b, 0);
    let average = sum / numbers.length;

    // Output the average to the input element
    document.getElementById('curb-slope').value = average;
});

function resetForm() {
    if (confirm('Are you sure you would like to reset the form?')) {
      const inputs = document.querySelectorAll('input[type="text"], input[type="number"], select');
      
      inputs.forEach(input => {
        input.value = input.defaultValue;
      });

      document.getElementById('fileName1').textContent = 'No file chosen';
      document.getElementById('fileName2').textContent = 'No file chosen';
      document.getElementById('fileName3').textContent = 'No file chosen';
    }
  }

  document.getElementById('photoButton1').addEventListener('click', function() {
    document.getElementById('fileInput1').click();
});

document.getElementById('photoButton2').addEventListener('click', function() {
    document.getElementById('fileInput2').click();
});

document.getElementById('photoButton3').addEventListener('click', function() {
    document.getElementById('fileInput3').click();
});

document.getElementById('fileInput1').addEventListener('change', function() {
    const fileName = this.files[0].name;
    document.getElementById('fileName1').textContent = fileName;
});

document.getElementById('fileInput2').addEventListener('change', function() {
    const fileName = this.files[0].name;
    document.getElementById('fileName2').textContent = fileName;
});

document.getElementById('fileInput3').addEventListener('change', function() {
    const fileName = this.files[0].name;
    document.getElementById('fileName3').textContent = fileName;
});