$(document).ready(function() {
    // Adicione um manipulador de eventos de clique ao botão de "like"
    $(".like-button").click(function(e) {
        e.preventDefault();
        var postId = $(this).data("post-id");
        var csrftoken = getCookie('csrftoken');
        var userLiked = $(this).hasClass("liked");

            // Alterne o estado visual da lâmpada imediatamente
        $(this).toggleClass("liked");
            if ($(this).hasClass("liked")) {
                $(this).find(".lamp").text("lightbulb");
            } else {
                $(this).find(".lamp").text("lightbulb_outline");
            }


        // Alterne o estado do "like" com AJAX
        $.ajax({
            type: "POST",
            url: "/files/like_post_ajax/" + postId + "/",
            data: {},
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(data) {
                // Atualize a classe CSS e o ícone da lâmpada com base na resposta do servidor
                if (data.liked) {
                    $(this).data("user-liked", true);
                    $(this).find(".lamp").addClass("liked");
                    $(this).find(".lamp").text("lightbulb");
                } else {
                    $(this).data("user-liked", false);
                    $(this).find(".lamp").removeClass("liked");
                    $(this).find(".lamp").text("lightbulb_outline");
                }
                // Atualize o contador de likes, se necessário
                $("#likes-count-" + postId).text(data.likes_count + " Insights");
            },
            error: function(xhr, textStatus, errorThrown) {
                console.log("Erro na requisição AJAX: " + textStatus);
            }
        });
    });

    // Função para obter o token CSRF do cookie
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
