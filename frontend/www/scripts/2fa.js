async function register2fa() {
  // Activate 2FA if checked
  console.log("HEIHEIEHI");
  let form = document.querySelector("#form-activate-2fa");
  console.log(form);
  var twoFA = document.getElementById("enable2fa").checked;

  console.log("TWOfa", twoFA);
  if (twoFA) {
    window.location.replace("qr.html");
  }
}

document
  .querySelector("#btn-2fa")
  .addEventListener("click", async () => await register2fa());
