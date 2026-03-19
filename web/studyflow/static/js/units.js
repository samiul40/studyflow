function addRow(title = "", duration = "") {
  const table = document.querySelector("#units-table tbody");

  if (!table) return;

  const row = document.createElement("tr");

  row.innerHTML = `
    <td>
      <input type="text" name="title[]" class="form-control" value="${title}">
    </td>
    <td>
      <input type="number" name="duration[]" class="form-control" value="${duration}">
    </td>
    <td>
      <button type="button" class="btn btn-danger btn-sm" onclick="this.closest('tr').remove()">
        Delete
      </button>
    </td>
  `;

  table.appendChild(row);
}

document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("bulkUnitModal");

  if (!modal) return;

  modal.addEventListener("shown.bs.modal", function () {
    const tbody = document.querySelector("#units-table tbody");

    if (!tbody) return;

    tbody.innerHTML = "";

    for (let i = 0; i < 5; i++) {
      addRow();
    }
  });
});
