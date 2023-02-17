export function useFormatDateTime(dateIsoFormatString) {
  // Format date like "06.02.2023 20:05" from python `date.isoformat` string.
  let date = new Date(dateIsoFormatString);
  return date.toLocaleDateString("ru-RU") + " " + date.toLocaleTimeString("ru-RU", {
    hour: "2-digit",
    minute: "2-digit"
  });
}