document.querySelectorAll('[data-featured-carousel]').forEach((carousel) => {
  const track = carousel.querySelector('.featured-track');
  const slides = Array.from(track.children);
  const controls = carousel.querySelector('.featured-controls');
  const counter = carousel.querySelector('.featured-counter');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let index = 0;
  let timer;

  function update() {
    index = Math.max(0, Math.min(slides.length - 1, Math.round(track.scrollLeft / track.clientWidth)));
    counter.textContent = `${index + 1} / ${slides.length}`;
    slides.forEach((slide, position) => {
      slide.querySelector('a').tabIndex = position === index ? 0 : -1;
    });
  }

  function move(direction) {
    index = (index + direction + slides.length) % slides.length;
    track.scrollTo({left: index * track.clientWidth, behavior: reducedMotion.matches ? 'instant' : 'smooth'});
  }

  controls.hidden = slides.length < 2;
  carousel.querySelector('[data-previous]').addEventListener('click', () => move(-1));
  carousel.querySelector('[data-next]').addEventListener('click', () => move(1));
  track.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      move(event.key === 'ArrowRight' ? 1 : -1);
    }
  });
  track.addEventListener('scroll', () => {
    clearTimeout(timer);
    timer = setTimeout(update, 120);
  }, {passive: true});
  new ResizeObserver(() => {
    track.scrollTo({left: index * track.clientWidth, behavior: 'instant'});
  }).observe(track);
  update();
});
