function addRow(title = "", duration = "", resourceType = "") {
  const table = document.querySelector("#units-table tbody");

  if (!table) return;

  const row = document.createElement("tr");
  const durationCell =
    resourceType !== "book"
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

  const resourceType = modal.dataset.resourceType;

  modal.addEventListener("shown.bs.modal", function () {
    const tbody = document.querySelector("#units-table tbody");

    if (!tbody) return;

    tbody.innerHTML = "";

    for (let i = 0; i < 5; i++) {
      addRow("", "", resourceType);
    }
  });
});
