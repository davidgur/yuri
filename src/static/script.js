var myDropzone = new Dropzone("div#dropzone", {url: "/upload"});
Dropzone.options.dropzone = {
    paramName: "file",
    maxFilesize: 5,
}