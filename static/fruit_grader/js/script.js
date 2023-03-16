$(document).bind('dragover', function (e) {
    var dropZone = $('.zone'),
        timeout = window.dropZoneTimeout;
    if (!timeout) {
        dropZone.addClass('in');
    } else {
        clearTimeout(timeout);
    }
    var found = false,
        node = e.target;
    do {
        if (node === dropZone[0]) {
            found = true;
            break;
        }
        node = node.parentNode;
    } while (node != null);
    if (found) {
        dropZone.addClass('hover');
    } else {
        dropZone.removeClass('hover');
    }
    window.dropZoneTimeout = setTimeout(function () {
        window.dropZoneTimeout = null;
        dropZone.removeClass('in hover');
    }, 100);
});

const dropArea = document.querySelector(".drag-area"),
    input = dropArea.querySelector("input"),
    submitButton = dropArea.querySelector("#submitButton");

const initApp = () => {

    const prevents = (e) => e.preventDefault();

    ['dragenter', 'dragover', 'dragleave'].forEach(evtName => {
        dropArea.addEventListener(evtName, prevents);
    });
}

document.addEventListener("DOMContentLoaded", initApp);

dropArea.addEventListener("click", function () {
    input.click();
});

dropArea.addEventListener("drop", (event)=>{
    event.preventDefault();
    input.files = event.dataTransfer.files;
});