document.addEventListener("DOMContentLoaded", function () {
    // Selecione todas as mensagens de sucesso e erro
    const successMessages = document.querySelectorAll(".success-message");
    const errorMessages = document.querySelectorAll(".error-message");

    // Função para mostrar as mensagens e removê-las após um atraso
    function showAndHideMessages(messages) {
        messages.forEach(function (message) {
            message.classList.add("show-message");
            setTimeout(function () {
                message.classList.remove("show-message");
            }, 3000); // Defina o tempo em milissegundos (5 segundos neste exemplo)
        });
    }

    // Chame a função para as mensagens de sucesso e erro
    showAndHideMessages(successMessages);
    showAndHideMessages(errorMessages);
});
