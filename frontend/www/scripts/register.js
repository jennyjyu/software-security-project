async function createNewUser(event) {
  let form = document.querySelector("#form-register-user");
  let formData = new FormData(form);
  let response = await sendRequest("POST", `${HOST}/api/users/`, formData, "");

  if (!response.ok) {
    let data = await response.json();
    let alert = createAlert("Registration failed!", data);
    document.body.prepend(alert);

  } else {
    let body = { username: formData.get("username"), password: formData.get("password") };
    let data = await response.json();
    let alert = createAlert("Registration", data);
    document.body.prepend(alert);
    form.reset();
  }
}

document.querySelector("#btn-create-account").addEventListener("click", async (event) => await createNewUser(event));