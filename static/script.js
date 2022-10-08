function showImage(elem) {
    elem.classList.add("gallery-img")

    // Disable scrolling
    var sx = window.scrollX;
    var sy = window.scrollY;
    document.onscroll = function() {
        window.scrollTo(sx, sy);
    }
    document.body.style.overflowY = "hidden";

    // Display image info
    const url = new URL(elem.src);
    const relUrl = url.toString().substring(url.origin.length+1);
    document.getElementById("gallerybg").innerText
        = "Name: "+relUrl
        + "\nDimensions: "+elem.width.toString()+"x"+elem.height.toString();
}

function hideImage(elem) {
    elem.classList.remove("gallery-img")

    // Enable scrolling
    document.onscroll = null;
    document.body.style.overflowY = "visible";
}

function toggleImage(elem) {
    if (elem.style.position != "fixed") {
        showImage(elem);
    }}

function closeGallery() {
    for (const elem of Array.from(document.getElementsByTagName("img"))) {
        hideImage(elem)
    }
    document.getElementById("gallerybg").style.display = "none";
}

function main() {
    for (const elem of Array.from(document.getElementsByTagName("img"))) {
        elem.onclick = function() {
            toggleImage(elem);
            document.getElementById("gallerybg").style.display = "inline";
        }
    }

    document.getElementById("gallerybg").onclick = closeGallery;
}
