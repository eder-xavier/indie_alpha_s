// Função para obter o token CSRF do cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function() {
    $(".comment-form").submit(function(e) {
        e.preventDefault(); // Evita que o formulário seja enviado tradicionalmente

        var form = $(this);
        var publicationId = form.find("button[type='submit']").data("publication-id");
        //var publicationId = $(this).data("publication-id");
        var commentText = form.find("textarea[name='text']").val();

        console.log("Publication ID:", publicationId); // Log de depuração

        $.ajax({
            type: "POST",
            url: "/files/add_comment/" + publicationId + "/",
            data: {
                'publication_id': publicationId,
                'text': commentText,
                'csrfmiddlewaretoken': getCookie('csrftoken')  // Obtém o valor do token CSRF do cookie
            },
            dataType: "json",
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            },
            success: function(data) {
                if (data.success) {
                    // Limpa o campo de texto após o envio
                    form.find("textarea[name='text']").val("");

                    // Atualiza o número de comentários
                    var commentCountElement = $("#comment-count-" + publicationId);
                    console.log("Current Comment Count:", commentCountElement.text()); // Log de depuração
                    var newCommentCount = parseInt(commentCountElement.text()) + 1;
                    console.log("New Comment Count:", newCommentCount); // Log de depuração
                    commentCountElement.text(newCommentCount);

                    // Atualiza a lista de comentários com os novos comentários (se necessário)
                    var commentList = $("#comment-list-" + publicationId);
                    $.each(data.comments, function(index, comment) {
                        commentList.append("<li>" + comment.author + ": " + comment.text + "</li>");
                    });
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                console.log("Erro na requisição AJAX: " + textStatus);
            }
        });
    });

    // Redirecionar o usuário ao clicar no número de comentários
    $(".comment-count").click(function(e) {
        e.preventDefault();
        var publicationId = $(this).data("publication-id");
        window.location.href = `files/view_comments/${publicationId}/`;
    });

        // Lidar com o clique no link "Comentários"
        $("a[href^='{% url 'storage_app:view_comments' %}']").on("click", function(e) {
            e.preventDefault(); // Impede o comportamento padrão de seguir o link
    
            var publicationId = $(this).data("publication-id"); // Se necessário, você pode adicionar um atributo de dados (data-publication-id) ao link
    
            // Redirecione o usuário para a página de visualização de comentários
            window.location.href = "{% url 'storage_app:view_comments' %}" + publicationId;
        });
});

function updateCommentCount(publicationId) {
    $.ajax({
        type: "GET",
        url: `/get_comment_count/${publicationId}/`,  // Use a nova URL criada
        dataType: "json",
        success: function(data) {
            // Atualize o número de comentários na página
            var commentCountElement = $("#comment-count-" + publicationId);
            commentCountElement.text(data.comment_count);
        },
        error: function(xhr, textStatus, errorThrown) {
            console.log("Erro na requisição AJAX: " + textStatus);
        }
    });
}

// Use esta função para atualizar o número de comentários quando necessário
updateCommentCount(publicationId);  // Chame esta função inicialmente para carregar o número de comentários na página
