document.querySelectorAll('[data-featured-carousel]').forEach((carousel) => {
  const track = carousel.querySelector('.featured-track');
  const slides = Array.from(track.children);
  const controls = carousel.querySelector('.featured-controls');
  const counter = carousel.querySelector('.featured-counter');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let index = 0;
  let navigating = false;
  let timer;

  function render() {
    counter.textContent = `${index + 1} / ${slides.length}`;
    slides.forEach((slide, position) => {
      slide.querySelector('a').tabIndex = position === index ? 0 : -1;
    });
  }

  function updateFromScroll() {
    index = Math.max(0, Math.min(slides.length - 1, Math.round(track.scrollLeft / track.clientWidth)));
    render();
  }

  function move(direction) {
    clearTimeout(timer);
    navigating = true;
    index = (index + direction + slides.length) % slides.length;
    render();
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
    if (!navigating) updateFromScroll();
    timer = setTimeout(() => {
      navigating = false;
      updateFromScroll();
    }, 120);
  }, {passive: true});
  // Let a swipe or wheel gesture take over from an arrow-triggered animation.
  ['pointerdown', 'wheel'].forEach((type) => {
    track.addEventListener(type, () => {
      navigating = false;
      updateFromScroll();
    }, {passive: true});
  });
  new ResizeObserver(() => {
    track.scrollTo({left: index * track.clientWidth, behavior: 'instant'});
  }).observe(track);
  updateFromScroll();
});
