function showSuccessState() {
  var formContent = document.getElementById("contact-form-content");
  var successState = document.getElementById("success-state");
  if (!formContent || !successState) return;
  formContent.classList.add("hidden");
  successState.classList.add("active");
}

function resetForm() {
  var form = document.getElementById("main-contact-form");
  var formContent = document.getElementById("contact-form-content");
  var successState = document.getElementById("success-state");
  if (form) form.reset();
  if (successState) successState.classList.remove("active");
  if (formContent) formContent.classList.remove("hidden");
}
