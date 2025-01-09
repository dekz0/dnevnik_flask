document.addEventListener('DOMContentLoaded', () => {
    // Показ заголовка при нажатии на кнопку "6"
    document.getElementById('class-6').addEventListener('click', () => {
        const header = document.getElementById('class-6-header');
        header.style.display = 'block'; // Показываем заголовок
    });

    // Показ списка литературы при нажатии на кнопку "Показать список"
    document.getElementById('show-list').addEventListener('click', () => {
        const bookList = document.getElementById('class-6-books');
        bookList.style.display = 'block'; // Показываем список
    });
});


// Пример обработки события для кнопки
document.getElementById('show-list').addEventListener('click', () => {
    alert('Список литературы будет отображён!');
});
