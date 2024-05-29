document.addEventListener("DOMContentLoaded", function () {
  let id = document.getElementById("username");
  let pw = document.getElementById("password");
  let btn = document.getElementById("btn");

  btn.addEventListener("click", function () {
    if (id.value === "") {
      id.nextElementSibling.classList.add("warning");
      setTimeout(function () {
        var labels = document.querySelectorAll("label");
        labels.forEach(function (label) {
          label.classList.remove("warning");
        });
      }, 1500);
    } else if (pw.value === "") {
      pw.nextElementSibling.classList.add("warning");
      setTimeout(function () {
        var labels = document.querySelectorAll("label");
        labels.forEach(function (label) {
          label.classList.remove("warning");
        });
      }, 1500);
    }
  });
});


