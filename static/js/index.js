function autoDownloadLink(elt) {
    elt.querySelectorAll("[data-auto-download]").forEach(element => {
        element.click();
    });
}

document.addEventListener("DOMContentLoaded", (event) => {
    document.addEventListener("htmx:load", e => autoDownloadLink(e.target));
});
