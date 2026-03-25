function handleSubmit(button) {
  button.disabled = true;

  button.querySelector('.btn-text').classList.add('d-none');
  button.querySelector('.spinner-border').classList.remove('d-none');

  button.form.submit();
}

document.addEventListener("DOMContentLoaded", function () {
    const typeField = document.getElementById("id_resource_type");
    const unitField = document.getElementById("id_unit_count");
    const wrapper = document.getElementById("unit-count-wrapper");

    if (!typeField || !unitField) return;

    const labelMap = {
      book: "Number of chapters",
      udemy: "Number of sections",
      youtube: "Number of videos",
    };

    function updateUI() {
      const selected = typeField.value;

      const validTypes = ["book", "udemy", "youtube"];

      if (!validTypes.includes(selected)) {
        unitField.value = "";
      }

      // Show only for valid types
      if (wrapper) {
        wrapper.style.display = validTypes.includes(selected)
          ? "block"
          : "none";
      }

      // Update label
      const label = document.querySelector(`label[for="${unitField.id}"]`);
      if (label) {
        label.textContent = labelMap[selected] || "Number of units";
      }
    }

    updateUI();
    typeField.addEventListener("change", updateUI);
  });