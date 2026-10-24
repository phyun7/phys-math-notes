document.querySelectorAll('.statement-tag').forEach(link => {
 link.title = 'Copy a permanent link to this statement';
 link.addEventListener('click', async () => {
  if (!navigator.clipboard) return;
  try {await navigator.clipboard.writeText(link.href); const old = link.textContent; link.textContent = 'Copied'; setTimeout(() => link.textContent = old, 1200);} catch (_) {}
 });
});

(() => {
  function addProofSquares() {
    const mj = window.MathJax;
    if (!mj?.startup?.promise || !mj.typesetPromise) return;

    mj.startup.promise = mj.startup.promise.then(async () => {
      const added = [];
      const proofSelector = "details.proof, .admonition.proof";

      document.querySelectorAll(proofSelector).forEach(proof => {
        if (proof.classList.contains("manual-qed")) return;
        if (proof.querySelector(".proof-qed")) return;

        const paragraphs = [...proof.querySelectorAll("p")].filter(p =>
          !p.classList.contains("admonition-title") &&
          p.closest(proofSelector) === proof
        );

        const last = paragraphs[paragraphs.length - 1];
        if (!last) return;

        const square = document.createElement("span");
        square.className = "proof-qed arithmatex";
        square.textContent = "\\(\\square\\)";
        last.appendChild(square);
        added.push(square);
      });

      if (added.length) await mj.typesetPromise(added);
    }).catch(error => console.error("Proof squares:", error));
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", addProofSquares);
  } else {
    addProofSquares();
  }

  window.addEventListener("load", addProofSquares);

  if (typeof document$ !== "undefined") {
    document$.subscribe(addProofSquares);
  }
})();