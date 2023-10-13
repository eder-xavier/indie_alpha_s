// Variáveis para controle de paginação infinita
var page = 2;  // Próxima página a ser carregada
var isLoading = false;  // Evita múltiplas solicitações simultâneas

// Função para verificar se o usuário rolou até o final da seção do feed
function checkScroll() {
    var feedSection = document.getElementById('feed-section');
    var endOfFeed = feedSection.querySelector('#end-of-page');
    var rect = endOfFeed.getBoundingClientRect();

    if (rect.top <= feedSection.clientHeight && !isLoading) {
        loadMorePublications();
    }
}

// Função para carregar mais publicações
function loadMorePublications() {
    isLoading = true;
    
    // Realize uma solicitação AJAX para buscar mais publicações
    // Certifique-se de incluir o número da página na solicitação
    
    $.ajax({
        url: "{% url 'indie_app:main' %}",
        data: { page: page },
        dataType: 'html',
        success: function(data) {
            // Adicione o HTML das novas publicações à lista existente
            var publicationsList = document.querySelector('.publications ul');
            publicationsList.insertAdjacentHTML('beforeend', data);
            page += 1;  // Atualize o número da próxima página
            isLoading = false;  // Permita a próxima solicitação
        }
    });
}

// Adicione um ouvinte de rolagem para verificar quando o usuário rola até o final da seção do feed
var feedSection = document.getElementById('feed-section');
feedSection.addEventListener('scroll', checkScroll);