document.querySelectorAll('.statement-tag').forEach(link => {
 link.title = 'Copy a permanent link to this statement';
 link.addEventListener('click', async () => {
  if (!navigator.clipboard) return;
  try {await navigator.clipboard.writeText(link.href); const old = link.textContent; link.textContent = 'Copied'; setTimeout(() => link.textContent = old, 1200);} catch (_) {}
 });
});
