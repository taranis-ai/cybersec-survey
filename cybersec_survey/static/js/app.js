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
  const nextBtn   = document.getElementById("btn-next");
  const prevBtn   = document.getElementById("btn-prev");

  // Conditionally show "Next" button
  if (currentIndex >= news_items.length) {
    document.getElementById("btn-next").style.display = "none";
  } else {
    document.getElementById("btn-next").style.display = "inline-block";
  }

  // Turn "Next" into "Finish" if last News Item was reached
  if (currentIndex === news_items.length - 1) {
    nextBtn.textContent = "Finish";
    nextBtn.classList.add("finish-button");
    nextBtn.classList.remove("move-button");
  } else {
    nextBtn.textContent = "Next";
    nextBtn.classList.remove("finish-button");
    nextBtn.classList.add("move-button");
  }

  // Disable Next for "unsure" until there is a saved comment
  if (news_items[currentIndex]) {
    const current = news_items[currentIndex];
    if (current.label === "unsure" && !current.comment) {
      nextBtn.disabled = true;
      prevBtn.disabled = true;
    document.getElementById('comment-hint').style.display = 'none';
    } else {
      nextBtn.disabled = false;
      prevBtn.disabled = false;
      document.getElementById('comment-hint').style.display = 'block';
    }
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

  // (re-run the disable‐logic in case we needed to re-enable after save+render)
  if (current.label === "unsure" && !current.comment) {
    nextBtn.disabled = true;
    prevBtn.disabled = true;
    document.getElementById('comment-hint').style.display = 'block';
  } else {
    nextBtn.disabled = false;
    prevBtn.disabled = false;
    document.getElementById('comment-hint').style.display = 'none';
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
  const current = news_items[currentIndex];
  current.label = 'unsure';

  document.querySelectorAll('.label-button').forEach(btn => {
    btn.classList.remove('selected');
  });
  document.getElementById('btn-unsure').classList.add('selected');

  const section = document.getElementById('comment-section');
  section.style.display = 'block';
  section.scrollIntoView({ behavior: 'smooth' });

  document.getElementById('btn-next').disabled = true;
  document.getElementById('btn-prev').disabled = true;
  document.getElementById('comment-hint').style.display = 'block';
}


function hideCommentForm() {
  const section = document.getElementById("comment-section");
  const textarea = document.getElementById("comment-input");
  section.style.display = "none";
  textarea.value = "";
  document.getElementById('comment-hint').style.display = 'none';
}

function hideSaveComment() {
    document.getElementById('comment-hint').style.display = 'none';
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
