window.addEventListener('message', function(event) {
        if (event.origin !== window.location.origin) {
            return;
        }

        const { nextObjectId } = event.data;
        const fileNameInput = document.getElementById('fileName');
        fileNameInput.value = `${nextObjectId}`;
    });

// document.getElementById('curb-avg-button').addEventListener('click', function() {
//     // Prompt the user for 5 numbers
//     let numbers = [];
//     for (let i = 0; i < 5; i++) {
//         let num = parseFloat(prompt(`Enter number ${i + 1}:`));
//         if (isNaN(num)) {
//             alert('Please enter a valid number.');
//             return;
//         }
//         numbers.push(num);
//     }

//     // Calculate the average
//     let sum = numbers.reduce((a, b) => a + b, 0);
//     let average = sum / numbers.length;

//     // Output the average to the input element
//     document.getElementById('curb-slope').value = average;
// });

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

function resetFormNoIntersections() {
    if (confirm('Are you sure you would like to reset the form?')) {
        const inputs = document.querySelectorAll('input[type="text"], input[type="number"], select');
        
        inputs.forEach(input => {
            if (input.id != "ew-road" && input.id != "ns-road") {
                input.value = input.defaultValue;
            } else {
                console.log("Intersection fields remain in place");
            }
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

// Create autosave file, cleared when downloading or hitting reset button
function autoSave() {
    const inputs = document.querySelectorAll('input[type="text"], input[type="number"], select');
    const formData = {};

    inputs.forEach(input => {
        formData[input.name] = input.value;
    });

    localStorage.setItem('formData', JSON.stringify(formData));
}

function restoreData() {
    const savedData = localStorage.getItem('formData');
    if (savedData) {
        const formData = JSON.parse(savedData);
        Object.keys(formData).forEach(key => {
            const input = document.querySelector(`[name="${key}"]`);
            if (input) {
                input.value = formData[key];
            }
        });
    }
}

document.getElementById('curb-avg-button').addEventListener('click', function() {
    document.getElementById('tableModal').style.display = 'block';
});

document.querySelector('.close').addEventListener('click', function() {
    document.getElementById('tableModal').style.display = 'none';
});

document.getElementById('calculateAverage').addEventListener('click', function() {
    let numbers = [];
    let total = 0;
    let count = 0;

    for (let i = 1; i <= 10; i++) {
        let value = parseFloat(document.getElementById(`tablenum${i}`).value);
        if(!isNaN(value)) {
            numbers.push(value);
            total += value;
            count++;
        } 
    }

    if (count > 0) {
        let average = total / count;
        document.getElementById('curb-slope').value = average.toFixed(2);
    } else {
        alert('No valid numbers found');
    }

    document.getElementById('tableModal').style.display = 'none';
});

setInterval(autoSave, 500);

window.addEventListener('load', restoreData);

// Confirm before leaving the page
window.addEventListener('beforeunload', function (event) {
    event.preventDefault();
    event.returnValue = '';
});