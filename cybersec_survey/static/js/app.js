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

  // Conditionally show "Next" button
  if (currentIndex >= news_items.length) {
    document.getElementById("btn-next").style.display = "none";
  } else {
    document.getElementById("btn-next").style.display = "inline-block";
  }

  // Check if clicked "Next" on last News item
  if (currentIndex >= news_items.length) {
    container.innerText = "";
    label.innerText = `${news_items.length} / ${news_items.length}`;

    document.querySelectorAll('.label-button').forEach(btn => {
      btn.style.display = 'none';
    });

    hideCommentForm();

    const allLabelled = news_items.every(item =>
      ['yes', 'no', 'unsure'].includes(item.label)
    );

    if (!allLabelled) {
      const msg = document.createElement('p');
      msg.style.color = 'red';
      msg.style.fontWeight = 'bold';
      msg.innerText = '⚠️ Not all items have been classified. Please go back and complete them.';
      container.appendChild(msg);
    } else {
        container.innerText = "Done! Thank you very much!";
        label.innerText = `✓ ${news_items.length} / ${news_items.length}`;
    }

    return;
  }

  const current = news_items[currentIndex];
  container.innerText = current.content;
  label.innerText = `News Item: ${currentIndex + 1} / ${news_items.length}`;

  document.querySelectorAll('.label-button').forEach(btn => {
    btn.classList.remove('selected');
    btn.style.display = 'inline-block';
  });

  if (current.label === "yes") {
    document.getElementById('btn-yes').classList.add('selected');
  } else if (current.label === "no") {
    document.getElementById('btn-no').classList.add('selected');
  } else if (current.label === "unsure") {
  document.getElementById('btn-unsure').classList.add('selected');
  }

  const commentInput = document.getElementById("comment-input");
  if (commentInput) {
    commentInput.value = current.comment || "";
  }

  if (current.label === "unsure" && current.comment) {
    showCommentForm();
  } else {
    hideCommentForm();
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
  if (direction === 'next' && currentIndex < news_items.length) {
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
      if (!comment) return;

      await fetch("/api/label", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          id: current.id,
          label: "unsure",
          comment: comment
        })
      });

      current.label = "unsure";
      current.comment = comment;

      hideCommentForm();
      renderText();
    });

  }
};
