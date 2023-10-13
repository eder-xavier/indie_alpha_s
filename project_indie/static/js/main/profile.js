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

    // Função para atualizar os detalhes do perfil
    function updateProfileDetails(userId) {
        $.ajax({
            type: "GET",
            url: `/files/userprofile/${userId}/`,
            dataType: "json",
            success: function(data) {
                if (data.success) {
                    // Atualizar o botão
                    var button = $(".toggle-follow-button[data-user-id='" + userId + "']");
                    if (data.is_following) {
                        button.text("Parar de Seguir");
                    } else {
                        button.text("Seguir");
                    }
            
                    // Atualizar o número de seguidores
                    $(".follower-count").text(data.follower_count);
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                console.log("Erro na requisição AJAX: " + textStatus);
            }
        });
    }
    function updateFollowingCount(userId) {
        $.ajax({
            type: "GET",
            url: `/files/userprofile/${userId}/`,
            dataType: "json",
            success: function(data) {
                if (data.success) {
                    // Atualizar o número de pessoas que o usuário está seguindo
                    $(".following-count").text(newFollowingCount);
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                console.log("Erro na requisição AJAX: " + textStatus);
            }
        });
    }

    $(".toggle-follow-button").click(function() {
        var userId = $(this).data("user-id");
        var button = $(this);

        // Realize uma solicitação AJAX para seguir ou parar de seguir o usuário
        $.ajax({
            type: "POST",
            url: `/files/toggle_follow/${userId}/`,
            dataType: "json",
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken')); // Inclua o token CSRF
            },
            success: function(data) {
                if (data.success) {
                    // Atualize o botão na interface do usuário
                    if (data.is_following) {
                        button.text("Parar de Seguir");
                    } else {
                        button.text("Seguir");
                    }

                    // Atualize o número de seguidores na interface do usuário
                    updateFollowingCount(userId, data.following_count);
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                console.log("Erro na requisição AJAX: " + textStatus);
            }
        });
    });
});
