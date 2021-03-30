//let qrurl = "otpauth://totp/SecFit:test?secret=ASDFGHJKLKJHGFDS&issuer=SecFit";

async function createQRcode() {

  let response = await sendRequest("GET", `${HOST}/api/two_factor/`);

  if (response.ok) {
    let data = await response.json();

    let messagebox = document.querySelector("#message-box");
    let p = document.createElement("p");
    p.innerHTML = data.message;
    messagebox.append(p)
    // Generate QR-code
    var qrcode = new QRCode("qrcode");
    qrcode.makeCode(data.url);
  } else {
    let data = await response.json();
    let alert = createAlert("Generation of QR-code failed", data);
    document.body.prepend(alert);
  }
}

  document
  .querySelector("#btn-qr")
  .addEventListener("click", async () => await createQRcode());

