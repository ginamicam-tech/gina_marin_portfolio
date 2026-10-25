const players = Array.from(document.querySelectorAll('[data-video-player]'));

players.forEach((player) => {
  const video = player.querySelector('video');
  const button = player.querySelector('.video-play');
  const error = player.querySelector('.video-error');
  const playLabel = button.getAttribute('aria-label');
  let bufferedSource;
  if (player.hasAttribute('data-buffered-video')) video.controls = false;
  button.hidden = !video.paused;

  button.addEventListener('click', async () => {
    error.hidden = true;
    try {
      if (player.hasAttribute('data-buffered-video') && !bufferedSource) {
        button.disabled = true;
        button.setAttribute('aria-label', 'Loading video');
        button.querySelector('span').textContent = '…';
        const response = await fetch(video.querySelector('source').src);
        if (!response.ok) throw new Error('Video download failed');
        // These short reels use a complete local buffer to avoid partial-read
        // failures in the preview browser. Fetch only after an explicit click.
        bufferedSource = URL.createObjectURL(await response.blob());
        video.src = bufferedSource;
      }
      video.controls = true;
      await video.play();
    } catch {
      button.hidden = false;
      error.hidden = false;
    } finally {
      button.disabled = false;
      button.setAttribute('aria-label', playLabel);
      button.querySelector('span').textContent = '▶';
    }
  });

  video.addEventListener('play', () => {
    button.hidden = true;
    error.hidden = true;
    players.forEach((other) => {
      if (other !== player) other.querySelector('video').pause();
    });
  });
  video.addEventListener('pause', () => { button.hidden = false; });
  video.addEventListener('ended', () => { button.hidden = false; });
});
