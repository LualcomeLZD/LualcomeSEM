const itemsContainer = document.getElementById("items");
const addRowButton = document.getElementById("add-row");

const createRow = () => {
  const row = document.createElement("div");
  row.classList.add("table-row");
  row.innerHTML = `
    <input name="item_desc[]" type="text" placeholder="Producto" />
    <input name="item_qty[]" type="number" inputmode="decimal" min="0" step="0.01" value="1" />
    <input name="item_price[]" type="number" inputmode="decimal" min="0" step="0.01" placeholder="0.00" />
    <input name="item_discount[]" type="number" inputmode="decimal" min="0" step="0.01" value="0" />
    <span class="row-total">0.00</span>
  `;
  itemsContainer.appendChild(row);
};

const updateTotals = () => {
  const rows = itemsContainer.querySelectorAll(".table-row");
  rows.forEach((row) => {
    const qty = parseFloat(row.querySelector("input[name='item_qty[]']").value) || 0;
    const price = parseFloat(row.querySelector("input[name='item_price[]']").value) || 0;
    const discountRate =
      parseFloat(row.querySelector("input[name='item_discount[]']").value) || 0;
    const subtotal = qty * price;
    const discountAmount = (subtotal * discountRate) / 100;
    const total = subtotal - discountAmount;
    row.querySelector(".row-total").textContent = total.toFixed(2);
  });
};

addRowButton?.addEventListener("click", () => {
  createRow();
});

itemsContainer?.addEventListener("input", updateTotals);
updateTotals();
