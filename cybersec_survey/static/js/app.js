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

  const current = news_items[currentIndex];

  container.innerText = current.content;
  label.innerText = `News Item: ${currentIndex + 1} / ${news_items.length}`;

  document.querySelectorAll('.label-button').forEach(btn => {
    btn.classList.remove('selected');
  });

  if (current.label === "yes") {
    document.getElementById('btn-yes').classList.add('selected');
  } else if (current.label === "no") {
    document.getElementById('btn-no').classList.add('selected');
  } else if (current.label === "unsure") {
  document.getElementById('btn-unsure').classList.add('selected');
  }
}


async function label(value) {
  const current = news_items[currentIndex];

  current.label = value;

  await fetch("/api/label", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id: current.id, label: value })
  });
  renderText();
}

function showCommentForm() {
  document.getElementById("comment-section").style.display = "block";
}

function hideCommentForm() {
  const section = document.getElementById("comment-section");
  const textarea = document.getElementById("comment-input");
  section.style.display = "none";
  textarea.value = "";
}

function move(direction) {
  if (direction === 'next' && currentIndex < news_items.length - 1) {
    currentIndex++;
  } else if (direction === 'prev' && currentIndex > 0) {
    currentIndex--;
  }
  renderText();
}


window.onload = () => {
  fetchNewsItems();

  const commentForm = document.getElementById("comment-form");
  if (commentForm) {
    commentForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const current = news_items[currentIndex];
      const comment = document.getElementById("comment-input").value.trim();
      if (!comment) {
        return;
      }

      current.label = "unsure";
      current.comment = comment;

      await fetch("/api/label", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          id: current.id,
          label: "unsure",
          comment: comment
        })
      });

      document.querySelectorAll('.label-button').forEach(btn => {
        btn.classList.remove('selected');
      });

      document.getElementById('btn-unsure').classList.add('selected');

      hideCommentForm();
      renderText();
    });

  }
};
