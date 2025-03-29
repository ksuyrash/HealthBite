
const body = document.body;
const h3 = document.createElement('h3');
h3.innerText = 'Select Your Preferences:';
body.appendChild(h3);


const options = [
    'vegan',
    'vegetarian',
    'dairy free',
    'sugar free',
    'low calories',
    'high protein',
    'breakfast',
    'lunch',
    'dinner',
    'snack',
    'dessert'
];


options.forEach(option => {
    const label = document.createElement('label');
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.className = 'checkbox';
    checkbox.value = option;

    label.appendChild(checkbox);
    label.appendChild(document.createTextNode(` ${option}`));
    body.appendChild(label);
    body.appendChild(document.createElement('br'));
});


const submitBtn = document.createElement('button');
submitBtn.id = 'submitBtn';
submitBtn.innerText = 'Submit';
body.appendChild(submitBtn);



const resultParagraph = document.createElement('p');
body.appendChild(resultParagraph);

submitBtn.addEventListener('click', () => {
    const checkboxes = document.querySelectorAll('.checkbox');
    let isChecked = false;

    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            isChecked = true;
        }
    });

    if (isChecked) {
        resultParagraph.innerText = 'Preferences submitted successfully!';
    } else {
        resultParagraph.innerText = 'Please select at least one preference.';
    }
});


const recipesContainer = document.createElement('recipes');
recipesContainer.style.display = 'flex';
recipesContainer.style.flexWrap = 'wrap';
recipesContainer.style.justifyContent = 'center';
recipesContainer.style.marginTop = '20px';
body.appendChild(recipesContainer);
