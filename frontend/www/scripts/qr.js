let qrurl = "otpauth://totp/SecFit:test?secret=ASDFGHJKLKJHGFDS&issuer=SecFit";

async function createQRcode(qrurl) {
  let response = await sendRequest("GET", `${HOST}api/two_factor/`);
  if (response.ok) {
    let data = await response.json();
    // Generate QR-code
    var qrcode = new QRCode("qrcode");
    qrcode.makeCode(data.url);
  } else {
    let data = await response.json();
    let alert = createAlert("Generation of QR-code failed", data);
    document.body.prepend(alert);
  }
}

function makeCode(url) {
  var qrcode = new QRCode("qrcode");
  qrcode.makeCode(url);
}

makeCode(qrurl);
