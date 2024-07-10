function autoPFupper(valueFieldId, passFailId, threshold) {
    return function() {
        const valueInput = document.getElementById(valueFieldId);
        const passFailSelect = document.getElementById(passFailId);
        const value = parseFloat(valueInput.value);

        if (!isNaN(value)) {
            if (value <= threshold) {
                passFailSelect.value = 'pass';
            } else {
                passFailSelect.value = 'fail';
            }
        } else {
            passFailSelect.value = ''; // If input is not a valid number, reset the select element
        }
    };
}

window.addEventListener('DOMContentLoaded', (event) => {
    console.log("DOM fully loaded and parsed");

    // Add event listener to the runslope input
    const runslopeInput = document.getElementById('runslope-1');
    const runslopepf = document.getElementById('runslope-1-pf');
    if (runslopeInput && runslopepf) {
        runslopeInput.addEventListener('input', autoPFupper('runslope-1', 'runslope-1-pf', 2));
        console.log("Event listener added for runslope-1");
    } else {
        console.log("Runslope input or pass/fail select not found");
    }

    // Add event listener to the cross slope input
    const crossslopeInput = document.getElementById('cross-slope1');
    const crossslopepf = document.getElementById('cross-slope1-pf');
    if (crossslopeInput && crossslopepf) {
        crossslopeInput.addEventListener('input', autoPFupper('cross-slope1', 'cross-slope1-pf', 2));
        console.log("Event listener added for cross-slope1");
    } else {
        console.log("Cross-slope input or pass/fail select not found");
    }
});