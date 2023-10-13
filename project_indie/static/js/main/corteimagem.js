document.addEventListener("DOMContentLoaded", function () {
    const imageUploadInput = document.getElementById("id_profile_picture");
    const editProfilePictureForm = document.getElementById("edit-profile-picture-form");
    const imagePreview = document.getElementById("image-preview");
    const saveProfilePictureButton = document.getElementById("save-profile-picture");
    const discardProfilePictureButton = document.getElementById("discard-profile-picture");

    let cropper;

    // Manipulador de evento para abrir a imagem no Cropper.js
    imageUploadInput.addEventListener("change", function () {
        const file = this.files[0];

        if (file) {
            // Crie um objeto FileReader para ler o arquivo de imagem
            const reader = new FileReader();
            reader.onload = function (e) {
                // Remova o cropper existente, se houver
                if (cropper) {
                    cropper.destroy();
                }

                // Crie um novo elemento de imagem para a visualização
                const img = document.createElement("img");
                img.id = "cropper-image";
                img.src = e.target.result;

                // Adicione a imagem à visualização
                imagePreview.innerHTML = "";
                imagePreview.appendChild(img);

                // Inicialize o Cropper.js com a imagem
                cropper = new Cropper(img, {
                    aspectRatio: 1,  // Define a proporção desejada (1:1 para imagem de perfil)
                    viewMode: 1,
                });
            };
            reader.readAsDataURL(file);
        }
    });

    // Manipulador de evento para salvar a imagem recortada
    saveProfilePictureButton.addEventListener("click", function () {
        // Obtenha a imagem recortada em base64
        const croppedDataUrl = cropper.getCroppedCanvas().toDataURL();

        // Crie um novo elemento de imagem para a imagem recortada
        const croppedImg = document.createElement("img");
        croppedImg.src = croppedDataUrl;

        // Adicione a imagem recortada ao formulário de edição de perfil (opcional)
        const formData = new FormData(editProfilePictureForm);
        formData.append("cropped_image", croppedDataUrl);

        // Envie o formulário (você pode usar AJAX aqui, se preferir)
        fetch(editProfilePictureForm.action, {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            // Lide com a resposta do servidor, se necessário
            console.log(data);
        })
        .catch(error => {
            console.error("Erro ao enviar o formulário:", error);
        });
    });

    // Manipulador de evento para descartar a imagem recortada
    discardProfilePictureButton.addEventListener("click", function () {
        // Remova o cropper existente
        if (cropper) {
            cropper.destroy();
        }

        // Limpe a visualização e o campo de upload
        imagePreview.innerHTML = "";
        editProfilePictureForm.reset();
    });
});
