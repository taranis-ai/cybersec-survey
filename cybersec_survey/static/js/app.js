let news_items = [];
let currentIndex = 0;

async function fetchNewsItems() {
  const res = await fetch("/api/news_items");
  const data = await res.json();
  news_items = data.news_items;
  currentIndex = data.index || 0;
  renderText();
}
function renderText() {
    const label = document.getElementById("progress-label");
    const container = document.getElementById("text-container");

    if (currentIndex >= news_items.length) {
      container.innerText = "Done! Thank you very much!";
      label.innerText = `✓ ${news_items.length} / ${news_items.length}`;
      return;
    }

    container.innerText = news_items[currentIndex].content;
    label.innerText = `News Item: ${currentIndex + 1} / ${news_items.length}`;
  }


async function label(value) {
  const current = news_items[currentIndex];
  await fetch("/api/label", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id: current.id, label: value })
  });
  currentIndex++;
  renderText();
}

window.onload = fetchNewsItems;
