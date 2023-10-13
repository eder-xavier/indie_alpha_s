document.querySelectorAll('.custom-file-input input[type="file"]').forEach(function(input) {
    input.addEventListener('change', function() {
      var files = Array.from(this.files).map(function(file) {
        return file.webkitRelativePath ? file.webkitRelativePath + '/' + file.name : file.name;
      });
      this.closest('.custom-file-input').setAttribute('data-files', files.join(', '));
    });
  });
  