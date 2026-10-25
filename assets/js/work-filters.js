document.querySelectorAll('.work-filters').forEach((filters) => {
  const section = document.querySelector('main .page-content');
  if (!section) return;
  const cards = Array.from(section.querySelectorAll('[data-work-id]'));
  const buttons = Array.from(filters.querySelectorAll('[data-filter-id]'));
  const status = section.querySelector('.work-filter-status');
  const descriptions = Array.from(section.querySelectorAll('[data-filter-description]'));
  const taggedCards = cards.map((card) => ({card, tags: JSON.parse(card.dataset.workTags), groups: card.dataset.workGroups ? JSON.parse(card.dataset.workGroups) : null}));

  function select(button) {
    const selectedTags = JSON.parse(button.dataset.filterTags);
    let count = 0;
    taggedCards.forEach(({card, tags, groups}) => {
      const matches = button.dataset.filterId === 'all' || (groups
        ? groups.includes(button.dataset.filterId)
        : selectedTags.some((tag) => tags.includes(tag)));
      card.hidden = !matches;
      if (matches) count++;
    });
    buttons.forEach((item) => {
      if (item === button) item.setAttribute('aria-current', 'true');
      else item.removeAttribute('aria-current');
    });
    descriptions.forEach((description) => {
      description.hidden = description.dataset.filterDescription !== button.dataset.filterId;
    });
    status.textContent = `${count} ${count === 1 ? 'entry' : 'entries'} · ${button.textContent.trim()}`;
  }

  function selectFromUrl() {
    const id = new URL(window.location.href).searchParams.get('filter');
    select(buttons.find((button) => button.dataset.filterId === id) || buttons[0]);
  }
  buttons.forEach((button) => button.addEventListener('click', (event) => {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button !== 0) return;
    event.preventDefault();
    const url = new URL(window.location.href);
    if (button.dataset.filterId === 'all') url.searchParams.delete('filter');
    else url.searchParams.set('filter', button.dataset.filterId);
    if (url.href !== window.location.href) window.history.pushState(null, '', url);
    select(button);
  }));
  window.addEventListener('popstate', selectFromUrl);
  selectFromUrl();
});
