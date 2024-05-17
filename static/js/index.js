function downloadFiles(loadTarget) {
    if (loadTarget.hasAttribute('data-download-load-target')) {
        loadTarget.querySelectorAll("[data-download-file]").forEach(element => {
            element.click();
        });
    }
}


document.addEventListener("DOMContentLoaded", (event) => {
    document.addEventListener("htmx:load", e => downloadFiles(e.target));
});
