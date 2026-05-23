// Global Utilities
function handleSubmit(button) {
  button.disabled = true;

  button.querySelector(".btn-text")?.classList.add("d-none");
  button.querySelector(".spinner-border")?.classList.remove("d-none");

  button.form.submit();
}

// Bulk Unit Modal Logic
function addRow(title = "", duration = "", contentKind = "") {
  const table = document.querySelector("#units-table tbody");
  if (!table) return;

  const row = document.createElement("tr");

  const durationCell =
    contentKind !== "reading"
      ? `
        <td>
          <input type="number" name="duration[]" class="form-control" value="${duration}">
        </td>
      `
      : "";

  row.innerHTML = `
    <td>
      <input type="text" name="title[]" class="form-control" value="${title}">
    </td>
    ${durationCell}
    <td>
      <button type="button" class="btn btn-danger btn-sm">
        Delete
      </button>
    </td>
  `;

  row.querySelector("button")?.addEventListener("click", () => {
    row.remove();
  });

  table.appendChild(row);
}

function initBulkModal() {
  const modal = document.getElementById("bulkUnitModal");
  if (!modal) return;

  const contentKind = modal.dataset.contentKind;

  modal.addEventListener("shown.bs.modal", function () {
    const tbody = document.querySelector("#units-table tbody");
    if (!tbody) return;

    tbody.innerHTML = "";

    for (let i = 0; i < 5; i++) {
      addRow("", "", contentKind);
    }
  });
}

// Toggle password
function togglePassword() {
  const toggle = document.getElementById("togglePass");
  const icon = document.getElementById("togglePassword");
  const password = document.getElementById("password");

  if (!toggle || !password || !icon) return;

  toggle.addEventListener("click", () => {
    const isPassword = password.type === "password";
    password.type = isPassword ? "text" : "password";

    icon.classList.toggle("fa-eye");
    icon.classList.toggle("fa-eye-slash");
  });
}

// Init All
document.addEventListener("DOMContentLoaded", function () {
  initBulkModal();
  togglePassword();
});
