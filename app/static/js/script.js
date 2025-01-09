document.addEventListener('DOMContentLoaded', () => {
    // Получаем кнопки и секции
    const buttons = document.querySelectorAll('.subject-buttons button');
    const sections = document.querySelectorAll('.book-section');

    // Добавляем обработчик события на каждую кнопку
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            // Получаем значение data-subject из кнопки
            const subject = button.getAttribute('data-subject');

            // Скрываем все секции
            sections.forEach(section => {
                section.classList.remove('active');
            });

            // Показываем только нужную секцию
            const activeSection = document.querySelector(`.book-section[data-subject="${subject}"]`);
            if (activeSection) {
                activeSection.classList.add('active');
            }
        });
    });
});


