document.addEventListener('DOMContentLoaded', () => {
    const recipeCards = document.querySelectorAll('.recipe-card');
    const recipeModal = document.getElementById('recipeModal');
    const closeModalBtn = document.getElementById('closeModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalImage = document.getElementById('modalImage');
    const modalIngredients = document.getElementById('modalIngredients');
    const modalInstructions = document.getElementById('modalInstructions');

    recipeCards.forEach(card => {
        card.addEventListener('click', () => {
            const title = card.dataset.title;
            const image = card.dataset.image;
            const ingredients = card.dataset.ingredients.split('||');
            const instructions = card.dataset.instructions.split('||');

            modalTitle.textContent = title;
            modalImage.src = image;
            modalImage.alt = title;

            modalIngredients.innerHTML = '';
            ingredients.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                modalIngredients.appendChild(li);
            });

            modalInstructions.innerHTML = '';
            instructions.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                modalInstructions.appendChild(li);
            });

            recipeModal.classList.remove('hidden');
        });
    });

    closeModalBtn.addEventListener('click', () => {
        recipeModal.classList.add('hidden');
    });

    // Close modal when clicking outside of it
    recipeModal.addEventListener('click', (e) => {
        if (e.target === recipeModal) {
            recipeModal.classList.add('hidden');
        }
    });
});
