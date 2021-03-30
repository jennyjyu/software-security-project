async function register2fa() {
  // Activate 2FA if checkbox is checked
  var twoFA = document.getElementById("enable2fa").checked;

  if (twoFA) {
    window.location.replace("qr.html");
  }
}

document
  .querySelector("#btn-2fa")
  .addEventListener("click", async () => await register2fa());
