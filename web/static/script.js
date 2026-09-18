// Persist ?lang= across internal links
(function () {
  const p = new URLSearchParams(location.search);
  const lang = p.get('lang');
  if (!lang) return;
  document.querySelectorAll('a[href^="/"]').forEach(a => {
    const u = new URL(a.href, location.origin);
    if (!u.searchParams.get('lang')) u.searchParams.set('lang', lang);
    a.href = u.toString();
  });
})();
