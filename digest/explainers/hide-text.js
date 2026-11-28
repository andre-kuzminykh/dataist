// Прячет весь текст на странице сайта, кроме селекторов keep: мелкие подписи в ролике всё равно не читаются.
// Иконки и фигуры (SVG) остаются. Текст, который сайт добавляет по ходу анимации, прячется тоже (MutationObserver).
// Подключается в record.js через page/context.addInitScript(hideText, keep).
function hideText(keep) {
  const start = () => {
    const css = document.createElement('style');
    css.textContent = '.vt-x{visibility:hidden!important;opacity:0!important}svg text,svg tspan{visibility:hidden!important}' +
      'input,textarea{color:transparent!important;caret-color:transparent!important}::placeholder{color:transparent!important}';
    document.head.appendChild(css);
    const skip = t => { const p = t.parentElement; return !p || !t.nodeValue.trim() || p.closest('script,style,noscript,svg,.vt-x' + (keep ? ',' + keep : '')); };
    const wrap = root => {
      if (root.nodeType === 3) { if (!skip(root)) hide(root); return; }
      if (root.nodeType !== 1) return;
      const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT), list = [];
      let n; while ((n = w.nextNode())) if (!skip(n)) list.push(n);
      list.forEach(hide);
    };
    const hide = t => { const s = document.createElement('span'); s.className = 'vt-x'; t.parentNode.insertBefore(s, t); s.appendChild(t); };
    wrap(document.body);
    new MutationObserver(ms => ms.forEach(m => m.addedNodes.forEach(wrap))).observe(document.body, { childList: true, subtree: true });
  };
  if (document.body) start(); else document.addEventListener('DOMContentLoaded', start);
}
module.exports = { hideText };
