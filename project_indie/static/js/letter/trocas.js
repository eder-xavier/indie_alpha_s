function mostrarContato() {
  document.getElementById("contac").style.display = "block";
  document.getElementById("amizade").style.display = "none";
  document.getElementById("lista_grupos").style.display = "none";
  document.getElementById("criar_grupos").style.display = "none";
}

function mostrarOutros() {
  document.getElementById("amizade").style.display = "block";
  document.getElementById("contac").style.display = "none";
  document.getElementById("lista_grupos").style.display = "none";
  document.getElementById("criar_grupos").style.display = "none";
}

function mostrarGrupos() {
  document.getElementById("contac").style.display = "none";
  document.getElementById("amizade").style.display = "none";
  document.getElementById("criar_grupos").style.display = "none";
  document.getElementById("lista_grupos").style.display = "block";
}

function mostrarCriarGrupos() {
  document.getElementById("lista_grupos").style.display = "none";
  document.getElementById("contac").style.display = "none";
  document.getElementById("amizade").style.display = "none";
  document.getElementById("criar_grupos").style.display = "block";
}
