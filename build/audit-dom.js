/* Paste into the browser console on either page to catch text that was meant to
   be markup but got rendered literally (raw tags, unparsed entities, stray
   backticks). On the lab page it walks every fugue with the drawer and help
   panel open. Expect [] . */
(async () => {
  const w = ms => new Promise(r => setTimeout(r, ms));
  const BAD = /<\/?[a-z][a-z0-9]*\b[^>]*>|&(amp|lt|gt|quot|nbsp|#\d+);|(^|\s)`[^`]|\*[^*\s][^*]*\*/i;
  const scan = () => {
    const out = [], wk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let n;
    while ((n = wk.nextNode())) {
      const t = n.nodeValue;
      if (!t || !t.trim()) continue;
      if (n.parentElement && /SCRIPT|STYLE/.test(n.parentElement.tagName)) continue;
      if (BAD.test(t)) out.push(n.parentElement.tagName + ' :: ' + t.trim().slice(0, 90));
    }
    return out;
  };
  const found = [];
  const help = document.querySelector('#help'), drawer = document.querySelector('#drawer');
  if (help) help.hidden = false;
  if (drawer) drawer.hidden = false;
  const cards = [...document.querySelectorAll('.pcard')];
  if (cards.length) {
    for (const c of cards) {
      document.querySelector('#pieceBtn').click();
      c.click(); await w(800);
      scan().forEach(x => found.push(c.dataset.id + ' | ' + x));
    }
    document.querySelector('#picker').hidden = true;
  } else {
    scan().forEach(x => found.push(x));
  }
  console.log([...new Set(found)]);
  return [...new Set(found)];
})();
