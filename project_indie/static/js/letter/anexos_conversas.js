document.addEventListener("DOMContentLoaded", function() {
    const attachImage = document.getElementById("attach-image");
    const attachVideo = document.getElementById("attach-video");
    const attachDocument = document.getElementById("attach-document");
    const attachmentPreview = document.getElementById("attachment-preview");
    const fileInput = document.getElementById("file-input");
    const messageInput = document.getElementById("message-input");
    const messageForm = document.getElementById("message-form");

    attachImage.addEventListener("click", function() {
        // Handle image attachment (display preview)
        fileInput.accept = "image/*";
        fileInput.click();
    });

    attachVideo.addEventListener("click", function() {
        // Handle video attachment (display preview)
        fileInput.accept = "video/*";
        fileInput.click();
    });

    attachDocument.addEventListener("click", function() {
        // Handle document attachment (display file name and icon)
        fileInput.accept = "application/pdf,.doc,.docx,.txt";
        fileInput.click();
    });

    fileInput.addEventListener("change", function() {
        const file = fileInput.files[0];
        if (file) {
            attachmentPreview.innerHTML = `<p>File: ${file.name}</p>`;
        }
    });

    messageForm.addEventListener("submit", function(event) {
        event.preventDefault();
        const message = messageInput.value;
        // Here, you can handle the message and the attached file (if any) and send them to your server.
        // After that, you can clear the input fields and the preview.
        messageInput.value = "";
        fileInput.value = "";
        attachmentPreview.innerHTML = "";
    });
});

document.getElementById('file-input').addEventListener('change', function (e) {
    const fileInput = e.target;
    const attachmentPreview = document.getElementById('attachment-preview');
    
    if (fileInput.files && fileInput.files[0]) {
        const file = fileInput.files[0];
        const reader = new FileReader();

        reader.onload = function (e) {
            const preview = document.createElement('img');
            preview.src = e.target.result;
            attachmentPreview.innerHTML = '';
            attachmentPreview.appendChild(preview);
            attachmentPreview.style.display = 'block';
        };

        reader.readAsDataURL(file);
    } else {
        attachmentPreview.style.display = 'none';
    }
});

// Função para enviar mensagens via WebSocket
function sendMessage(messageData) {
    // Criar um objeto FormData para enviar a mensagem e anexos
    const formData = new FormData();

    // Adicionar texto da mensagem
    formData.append('content', messageData.content);

    // Adicionar anexos (document, video, image)
    if (messageData.document) {
        formData.append('document', messageData.document);
    }
    if (messageData.video) {
        formData.append('video', messageData.video);
    }
    if (messageData.image) {
        formData.append('image', messageData.image);
    }

    // Enviar a mensagem via XMLHttpRequest (ou outra biblioteca de sua escolha)
    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://127.0.0.1:8000/msg/send_message/<str:contact_username>/', true);

    // Manipulador para lidar com a resposta do servidor
    xhr.onload = function () {
        if (xhr.status === 200) {
            // Mensagem enviada com sucesso
            console.log('Mensagem enviada com sucesso!');
        } else {
            // Ocorreu um erro no envio da mensagem
            console.error('Erro ao enviar mensagem:', xhr.status, xhr.statusText);
        }
    };

    // Enviar o objeto FormData
    xhr.send(formData);
}

$(document).ready(function () {
    // Manipulador para enviar mensagens
    $('#env').on('submit', function (e) {
        e.preventDefault();

        // Coletar dados do formulário (texto, documento, vídeo, imagem)
        const content = $('#envmsg').val();
        const document = $('#envdoc')[0].files[0];
        const video = $('#envvideo')[0].files[0];
        const image = $('#envimage')[0].files[0];

        // Verificar se há conteúdo
        if (!content && !document && !video && !image) {
            alert('Por favor, insira uma mensagem ou anexo.');
            return;
        }

        // Montar os dados da mensagem
        const messageData = {
            content: content,
            document: document,
            video: video,
            image: image,
        };

        // Enviar a mensagem
        sendMessage(messageData);

        // Limpar o formulário
        $('#envmsg').val('');
        $('#envdoc').val('');
        $('#envvideo').val('');
        $('#envimage').val('');
    });
});
