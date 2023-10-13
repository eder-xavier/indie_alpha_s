// JavaScript para lidar com a funcionalidade de adicionar membros
const contactSearchInput = document.getElementById('contact-search-input');
const contactsList = document.getElementById('contacts-list');
const contactCheckboxes = document.querySelectorAll('.contact-checkbox');
const addSelectedContactsButton = document.getElementById('add-selected-contacts');

// Event listener para pesquisar contatos à medida que o usuário digita no campo de pesquisa
contactSearchInput.addEventListener('input', function () {
    const searchTerm = contactSearchInput.value.toLowerCase();
    const contactItems = contactsList.querySelectorAll('li');

    contactItems.forEach((contactItem) => {
        const contactName = contactItem.querySelector('span').textContent.toLowerCase();
        if (contactName.includes(searchTerm)) {
            contactItem.style.display = 'block';
        } else {
            contactItem.style.display = 'none';
        }
    });
});

// Event listener para adicionar contatos selecionados ao grupo
addSelectedContactsButton.addEventListener('click', function () {
    const selectedContacts = [];

    contactCheckboxes.forEach((checkbox) => {
        if (checkbox.checked) {
            const contactId = checkbox.closest('li').getAttribute('data-contact-id');
            selectedContacts.push(contactId);
        }
    });

    // Enviar a lista de contatos selecionados para o servidor (use AJAX).
    // O servidor deve adicionar esses contatos ao grupo.

    // Redirecionar ou atualizar a página após a ação ser concluída.
    location.reload(); // Recarregar a página como exemplo.
});

// Função para filtrar membros do grupo com base na pesquisa
function filterMembers() {
    var input = document.getElementById("member-search-input").value.toLowerCase();
    var memberList = document.getElementById("member-list");
    var members = memberList.getElementsByTagName("li");

    for (var i = 0; i < members.length; i++) {
        var member = members[i];
        var username = member.textContent.toLowerCase();
        if (username.includes(input)) {
            member.style.display = "";
        } else {
            member.style.display = "none";
        }
    }
}

// Adicione um event listener ao campo de pesquisa
document.getElementById("member-search-input").addEventListener("input", filterMembers);