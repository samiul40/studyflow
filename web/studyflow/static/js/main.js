function handleSubmit(button) {
  button.disabled = true;

  button.querySelector('.btn-text').classList.add('d-none');
  button.querySelector('.spinner-border').classList.remove('d-none');

  button.form.submit();
}