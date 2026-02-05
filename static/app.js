const totalInput = document.querySelector("input[name='total']");
const baseField = document.getElementById("base-amount");
const ivaField = document.getElementById("iva-amount");
const totalField = document.getElementById("total-amount");
const taxRate = parseFloat(document.querySelector("input[disabled]")?.value) || 0;

const formatValue = (value) => value.toFixed(2);

const updatePreview = () => {
  if (!totalInput) return;
  const total = parseFloat(totalInput.value) || 0;
  const divider = 1 + taxRate / 100;
  const base = total / divider;
  const iva = total - base;

  if (baseField) baseField.textContent = formatValue(base);
  if (ivaField) ivaField.textContent = formatValue(iva);
  if (totalField) totalField.textContent = formatValue(total);
};

totalInput?.addEventListener("input", updatePreview);
updatePreview();
