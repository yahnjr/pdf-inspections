window.addEventListener("load", function () {
  var url = "docs/ADAInspectorsGuide.pdf";

  // The workerSrc property should be specified.
  pdfjsLib.GlobalWorkerOptions.workerSrc =
    "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";

  // Create the iframe viewer
  var viewer = document.createElement("iframe");
  viewer.src =
    "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/web/viewer.html?file=" +
    encodeURIComponent(url);
  viewer.id = "pdf-viewer";

  // Replace the div with the iframe
  document.getElementById("pdf-viewer").replaceWith(viewer);

  // Handle orientation change
  window.addEventListener("orientationchange", function () {
    setTimeout(function () {
      viewer.contentWindow.location.reload();
    }, 100);
  });
});
