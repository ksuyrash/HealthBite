const body = document.body;
body.style.fontFamily = 'Times New Roman, sans-serif';
body.style.backgroundColor = '#f4f4f4';
body.style.margin = '0';
body.style.padding = '20px';
body.style.display = 'flex';
body.style.flexDirection = 'column';
body.style.alignItems = 'center';

const h3 = document.createElement('h3');
h3.innerText = 'Select Your Preferences:';
h3.style.color = '#333';
body.appendChild(h3);

const options = [
    'high protein',
    'breakfast',
    'lunch',
    'dinner',
    'snack',
    'dessert',
    'vegan',
    'sugar-free',
    'gluten-free',
    'soup',
    'salad',
    'vegetarian'
];

options.forEach(option => {
    const label = document.createElement('label');
    label.style.display = 'flex';
    label.style.alignItems = 'center';
    label.style.margin = '5px 0';
    label.style.background = '#fff';
    label.style.padding = '10px';
    label.style.borderRadius = '5px';
    label.style.boxShadow = '0 2px 5px rgba(0, 0, 0, 0.1)';
    label.style.width = '200px';
    label.style.transition = 'background 0.3s';

    label.onmouseover = () => {
        label.style.background = '#e0e0e0';
    };
    label.onmouseout = () => {
        label.style.background = '#fff';
    };

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.className = 'checkbox';
    checkbox.value = option;
    checkbox.style.marginRight = '10px';

    label.appendChild(checkbox);
    label.appendChild(document.createTextNode(` ${option}`));
    body.appendChild(label);
});

const recipes = [
    {"title": "Vegan Chili", "link": "https://www.bbcgoodfood.com/recipes/vegan-chilli", "tags": ["vegan", "dinner", "soup"]},
    {"title": "Sugar-Free Banana Bread", "link": "https://www.bbcgoodfood.com/recipes/sugar-free-banana-cake", "tags": ["sugar-free", "dessert"]},
    {"title": "High Protein Greek Yogurt Parfait", "link": "https://www.ibreatheimhungry.com/high-protein-yogurt-parfait/", "tags": ["high-protein", "breakfast"]},
    {"title": "Chickpea Salad Sandwich", "link": "https://www.loveandlemons.com/chickpea-salad-sandwich/", "tags": ["vegan", "lunch", "salad"]},
    {"title": "Zucchini Noodles with Avocado Pesto", "link": "https://www.eatyourselfskinny.com/zucchini-noodles-with-creamy-avocado-pesto/", "tags": ["vegan", "lunch", "vegetarian"]},
    {"title": "Vegan Lentil Soup", "link": "https://www.noracooks.com/vegan-lentil-soup/", "tags": ["vegan", "dinner", "soup"]},
    {"title": "Sugar-Free Pancakes", "link": "https://homecooknblog.com/sugar-free-pancakes/", "tags": ["sugar-free", "breakfast"]},
    {"title": "Quinoa & Black Bean Salad", "link": "https://detoxinista.com/the-best-quinoa-black-bean-salad/", "tags": ["vegan", "lunch", "salad"]},
    {"title": "Almond Flour Muffins", "link": "https://thebigmansworld.com/almond-flour-muffins/", "tags": ["gluten-free", "snack"]},
    {"title": "Vegan Buddha Bowl", "link": "https://www.loveandlemons.com/buddha-bowl-recipe/", "tags": ["vegan", "dinner"]},
    {"title": "Sugar-Free Granola", "link": "https://www.lazycatkitchen.com/healthy-granola-no-sugar-oil/", "tags": ["sugar-free", "snack"]},
    {"title": "Protein-Packed Smoothie", "link": "https://www.eatingwell.com/gallery/7910825/high-protein-smoothie-recipes/", "tags": ["high-protein", "breakfast"]},
    {"title": "Vegan Stuffed Peppers", "link": "https://www.wellplated.com/vegan-stuffed-peppers/", "tags": ["vegan", "dinner"]},
    {"title": "Chickpea Flour Omelette", "link": "https://thehiddenveggies.com/chickpea-omelette-the-best-vegan-omelette/", "tags": ["vegan", "breakfast"]},
    {"title": "High Protein Egg Muffins", "link": "https://www.wellplated.com/healthy-breakfast-egg-muffins/", "tags": ["high-protein", "breakfast"]},
    {"title": "Vegan Tacos", "link": "https://www.loveandlemons.com/vegan-tacos/", "tags": ["vegan", "dinner"]},
    {"title": "Avocado Toast with Chickpeas", "link": "https://nadiashealthykitchen.com/spicy-chickpea-avocado-toast/", "tags": ["vegan", "lunch"]},
    {"title": "Sugar-Free Sweet Potato Casserole", "link": "https://www.eatingwell.com/recipe/268408/no-sugar-added-sweet-potato-casserole/", "tags": ["sugar-free", "dinner"]},
    {"title": "High Protein Quinoa Bowl", "link": "https://healthylittlevittles.com/protein-packed-creamy-tahini-quinoa-bowls/", "tags": ["high-protein", "dinner"]},
    {"title": "Vegetable Stir-Fry", "link": "https://www.loveandlemons.com/stir-fry-recipe/", "tags": ["vegan", "dinner"]},
    {"title": "Vegan Pizza", "link": "https://minimalistbaker.com/my-favorite-vegan-pizza/", "tags": ["vegan", "dinner"]},
    {"title": "Sugar-Free Chocolate Avocado Mousse", "link": "https://sugarfreelondoner.com/chocolate-avocado-mousse/", "tags": ["sugar-free", "dessert"]},
    {"title": "Overnight Oats with Chia Seeds", "link": "https://www.loveandlemons.com/overnight-oats-recipe/", "tags": ["vegan", "breakfast"]},
    {"title": "Vegan Smoothie Bowl", "link": "https://minimalistbaker.com/favorite-smoothie-bowl-5-minutes/", "tags": ["vegan", "snack"]},
    {"title": "Sugar-Free Carrot Cake", "link": "https://sugarfreelondoner.com/sugar-free-carrot-cake/", "tags": ["sugar-free", "dessert"]},
    {"title": "High Protein Turkey Meatballs", "link": "https://www.erinliveswhole.com/healthy-greek-turkey-meatballs-with-tzatziki/", "tags": ["high-protein", "dinner"]},
    {"title": "Vegan Mushroom Stroganoff", "link": "https://rainbowplantlife.com/creamy-vegan-mushroom-stroganoff/", "tags": ["vegan", "dinner"]},
    {"title": "Sugar-Free Peanut Butter Cookies", "link": "https://www.allrecipes.com/recipe/158403/sugar-free-peanut-butter-cookies/", "tags": ["sugar-free", "dessert"]},
];

const selectedPreferences = [];
document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        if (checkbox.checked) {
            selectedPreferences.push(checkbox.value);
        } else {
            const index = selectedPreferences.indexOf(checkbox.value);
            if (index > -1) {
                selectedPreferences.splice(index, 1);
            }
        }
    });
});

function displayMatchedRecipes() {
    const matchedRecipes = recipes.filter(recipe => {
        return recipe.tags.some(tag => selectedPreferences.includes(tag));
    });

    const resultWindow = window.open('', 'Recipe Recommendations', 'width=400,height=400');
    if (matchedRecipes.length > 0) {
        resultWindow.document.write('<h2>Recommended Recipes:</h2>');
        matchedRecipes.forEach(recipe => {
            resultWindow.document.write(`<p>${recipe.title}</p>`);
            resultWindow.document.write(`<p><a href="${recipe.link}" target="_blank">${recipe.link}</a></p>`);
            resultWindow.document.write(`<p>${recipe.ingredients}</p>`);
        });
    } else {
        resultWindow.document.write('<h2>No recipes match your preferences.</h2>');
    }
    resultWindow.document.close();

    const resultParagraph = document.getElementById('result');
    if (matchedRecipes.length > 0) {
        resultParagraph.innerText = 'Recommended Recipes: ' + matchedRecipes.map(recipe => recipe.title).join(', ');
        resultParagraph.style.color = '#5cb85c'; // green for success
    } else {
        resultParagraph.innerText = 'No recipes match your preferences.';
        resultParagraph.style.color = '#d9534f'; // red for error
    }
}

// Add the submit button
const submitButton = document.createElement('button');
submitButton.id = 'submitButton';
submitButton.innerText = 'Submit';
submitButton.style.marginTop = '20px';
submitButton.style.padding = '10px 20px';
submitButton.style.fontSize = '16px';
submitButton.style.backgroundColor = '#007bff';
submitButton.style.color = '#fff';
submitButton.style.border = 'none';
submitButton.style.borderRadius = '5px';
submitButton.style.cursor = 'pointer';
submitButton.onmouseover = () => {
    submitButton.style.backgroundColor = '#0056b3';
};
submitButton.onmouseout = () => {
    submitButton.style.backgroundColor = '#007bff';
};
body.appendChild(submitButton);

submitButton.addEventListener('click', displayMatchedRecipes);

// Add a paragraph to display the result
const resultParagraph = document.createElement('p');
resultParagraph.id = 'result';
resultParagraph.style.marginTop = '20px';
body.appendChild(resultParagraph);
