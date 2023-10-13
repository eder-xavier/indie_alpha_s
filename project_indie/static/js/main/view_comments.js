$(document).ready(function() {
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

    // Função para carregar os comentários e respostas
    function loadComments() {
        // Obtém o ID da publicação do elemento HTML (certifique-se de que o elemento exista)
        var publicationId = $("#publication-id").val();
        
        // Define a URL da chamada AJAX
        var url = `/files/view_comments/${publicationId}/`;

        $.ajax({
            type: "GET",
            url: url,  // Usando a URL direta
            dataType: "json",
            success: function(data) {
                if (data.success) {
                    var commentsContainer = $("#comments-container");
                    commentsContainer.empty();

                    $.each(data.comments, function(index, comment) {
                        var commentDiv = $("<div class='comment'>");
                        commentDiv.append("<p>" + comment.text + "</p>");
                        commentDiv.append("<p>Por: " + comment.author + "</p>");

                        // Botão para exibir/ocultar respostas
                        var showRepliesButton = $("<button class='show-replies-button'>Mostrar Respostas (" + comment.replies_count + ")</button>");
                        showRepliesButton.data("comment-id", comment.id);
                        commentDiv.append(showRepliesButton);

                        // Formulário para adicionar resposta
                        var replyForm = $("<div class='reply-form'>");
                        var replyFormHTML = `
                            <form method="post" class="comment-form">
                                {% csrf_token %}
                                {{ comment_form.as_p }}
                                <input type="hidden" name="parent_comment_id" value="${comment.id}">
                                <button type="submit" class="add-comment-button">Responder</button>
                            </form>
                        `;
                        replyForm.html(replyFormHTML);
                        commentDiv.append(replyForm);

                        // Contêiner para exibir respostas
                        var repliesContainer = $("<div class='replies-container'>");

                        // Adicione respostas se houver
                        if (comment.replies.length > 0) {
                            $.each(comment.replies, function(index, reply) {
                                var replyDiv = $("<div class='reply'>");
                                replyDiv.append("<p>" + reply.text + "</p>");
                                replyDiv.append("<p>Por: " + reply.author + "</p>");
                                
                                // Botão "Like" para a resposta
                                var replyLikeButton = $("<button class='like-button'>Like (" + reply.likes_count + ")</button>");
                                replyLikeButton.data("comment-id", reply.id);
                                replyDiv.append(replyLikeButton);
                                
                                repliesContainer.append(replyDiv);
                            });
                        }

                        // Adicione o contêiner de respostas ao comentário
                        commentDiv.append(repliesContainer);

                        commentsContainer.append(commentDiv);
                    });

                    // Lidar com o clique no botão "Mostrar/ocultar respostas"
                    $(".show-replies-button").click(function() {
                        var commentId = $(this).data("comment-id");
                        var repliesContainer = $(this).closest(".comment").find(".replies-container");
                        
                        // Toggle (exibir/ocultar) respostas
                        repliesContainer.toggle();
                    });
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                console.log("Erro na requisição AJAX: " + textStatus);
            }
        });
    }

    // Carregue os comentários quando a página for carregada
    loadComments();

    // Função para lidar com o envio do formulário de resposta
    $("#comments-container").on("submit", ".reply-comment-form", function(e) {
        e.preventDefault(); // Evite o envio tradicional do formulário

        var form = $(this);
        var commentText = form.find("textarea[name='text']").val();
        var commentId = form.find("input[name='parent_comment_id']").val(); // Obtenha o ID do comentário pai

        // Realize uma solicitação AJAX para enviar a resposta
        $.ajax({
            type: "POST",
            url: `/files/reply_to_comment/${commentId}/`,
            data: {
                'comment_id': commentId,
                'text': commentText,
                'csrfmiddlewaretoken': getCookie('csrftoken')
            },
            dataType: "json",
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            },
            success: function(data) {
                if (data.success) {
                    // Limpe o campo de texto após o envio
                    form.find("textarea[name='text']").val("");

                    // Atualize a lista de respostas com a nova resposta
                    var repliesContainer = form.siblings(".replies-container");
                    repliesContainer.append("<div class='reply'><p>" + data.reply_text + "</p><p>Por: " + data.reply_author + "</p></div>");
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                console.log("Erro na requisição AJAX: " + textStatus);
            }
        });
    });

    
    // Lidar com o clique no botão "Like" para comentários e respostas
    $("#comments-container").on("click", ".like-button", function() {
        var commentId = $(this).data("comment-id");
        likeComment(commentId);
    });

    //Função para dar like a um comentário ou resposta
    function likeComment(commentId) {
        $.ajax({
            type: "POST",
            url: `/files/like_comment/${commentId}/`,
            data: {
                'csrfmiddlewaretoken': getCookie('csrftoken')
            },
            dataType: "json",
            success: function(data) {
                if (data.liked) {
                    // Usuário deu like ao comentário, você pode atualizar a interface do usuário conforme necessário
                    console.log("Usuário deu like ao comentário.");
                } else {
                    // Usuário removeu o like do comentário, você pode atualizar a interface do usuário conforme necessário
                    console.log("Usuário removeu o like do comentário.");
                }
                // Atualize o contador de likes do comentário ou resposta na interface do usuário
                $(".like-button[data-comment-id='" + commentId + "']").text("Like (" + data.likes_count + ")");
            },
            error: function(xhr, textStatus, errorThrown) {
                console.log("Erro na requisição AJAX: " + textStatus);
            }
        });
    }
    


    $(".only_comments").on("click", ".show-replies-button", function() {
        var commentId = $(this).data("comment-id");
        var repliesContainer = $(this).closest("#comments-container").find(".replies-container");
        
        // Toggle (exibir/ocultar) respostas
        repliesContainer.toggle();
        
        // Obter o número real de respostas exibidas
        var displayedRepliesCount = repliesContainer.find(".reply").length;
    
        // Alterar o texto do botão com base no número real de respostas
        var buttonText = repliesContainer.is(":visible")
            ? "Ocultar Respostas (" + displayedRepliesCount + ")"
            : "Mostrar Respostas (" + displayedRepliesCount + ")";
            
        $(this).text(buttonText);
    });
    


});
