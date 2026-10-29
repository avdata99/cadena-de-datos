/* Cadena de datos - reproductor y utilidades. JavaScript plano, sin dependencias. */
(function () {
  'use strict';

  var $ = function (id) { return document.getElementById(id); };
  var audio = $('player-audio');
  var bar = $('player');
  var toggle = $('player-toggle');
  var seek = $('player-seek');
  var speeds = [1, 1.25, 1.5, 1.75, 2, 0.75];
  var current = null; // {src, title, img, url}
  var lastSave = 0;

  function fmt(s) {
    if (!isFinite(s)) return '0:00';
    s = Math.floor(s);
    var h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), sec = s % 60;
    var mm = h ? String(m).padStart(2, '0') : m;
    return (h ? h + ':' : '') + mm + ':' + String(sec).padStart(2, '0');
  }

  // localStorage puede fallar (modo privado): todo envuelto en try/catch
  function store(key, val) {
    try {
      if (val === undefined) return localStorage.getItem(key);
      localStorage.setItem(key, val);
    } catch (e) { return null; }
  }
  var posKey = function (src) { return 'cd-pos:' + src; };

  function syncButtons() {
    var playing = !audio.paused;
    toggle.innerHTML = playing ? '<i class="bi bi-pause-fill"></i>' : '<i class="bi bi-play-fill"></i>';
    toggle.setAttribute('aria-label', playing ? 'Pausar' : 'Reproducir');
    document.querySelectorAll('.js-play').forEach(function (b) {
      var on = playing && current && b.dataset.src === current.src;
      b.classList.toggle('is-playing', on);
      b.querySelector('i').className = on ? 'bi bi-pause-fill' : 'bi bi-play-fill';
    });
  }

  function load(ep) {
    current = ep;
    audio.src = ep.src;
    $('player-title').textContent = ep.title;
    $('player-title').href = ep.url;
    $('player-cover').src = ep.img;
    bar.hidden = false;
    document.body.classList.add('has-player');
    var saved = parseFloat(store(posKey(ep.src)));
    if (saved > 5) {
      audio.addEventListener('loadedmetadata', function once() {
        audio.removeEventListener('loadedmetadata', once);
        if (saved < audio.duration - 10) audio.currentTime = saved;
      });
    }
    if ('mediaSession' in navigator) {
      navigator.mediaSession.metadata = new MediaMetadata({
        title: ep.title, artist: 'Cadena de datos',
        artwork: [{ src: ep.img, sizes: '512x512' }]
      });
    }
    store('cd-last', JSON.stringify(ep));
  }

  function play(ep) {
    if (!current || current.src !== ep.src) load(ep);
    audio.play();
    if (window.tag_analytics) tag_analytics('audio_start', 'engagement', 'escucha episodio ' + ep.title);
  }

  document.addEventListener('click', function (e) {
    var b = e.target.closest('.js-play');
    if (!b) return;
    var ep = { src: b.dataset.src, title: b.dataset.title, img: b.dataset.img, url: b.dataset.url };
    if (current && current.src === ep.src && !audio.paused) audio.pause();
    else play(ep);
  });

  toggle.addEventListener('click', function () { audio.paused ? audio.play() : audio.pause(); });
  $('player-back').addEventListener('click', function () { audio.currentTime = Math.max(0, audio.currentTime - 15); });
  $('player-fwd').addEventListener('click', function () { audio.currentTime = Math.min(audio.duration || 0, audio.currentTime + 30); });

  var speedBtn = $('player-speed');
  function setSpeed(r) { audio.playbackRate = r; speedBtn.textContent = r + 'x'; store('cd-speed', r); }
  speedBtn.addEventListener('click', function () {
    var i = speeds.indexOf(audio.playbackRate);
    setSpeed(speeds[(i + 1) % speeds.length]);
  });
  setSpeed(parseFloat(store('cd-speed')) || 1);
  audio.addEventListener('loadedmetadata', function () { audio.playbackRate = parseFloat(store('cd-speed')) || 1; });

  function paintSeek() {
    var pct = audio.duration ? (audio.currentTime / audio.duration) * 100 : 0;
    seek.style.setProperty('--pct', pct + '%');
  }
  audio.addEventListener('loadedmetadata', function () {
    seek.max = Math.floor(audio.duration);
    $('player-duration').textContent = fmt(audio.duration);
  });
  audio.addEventListener('timeupdate', function () {
    if (!seek.matches(':active')) seek.value = Math.floor(audio.currentTime);
    $('player-current').textContent = fmt(audio.currentTime);
    paintSeek();
    var now = Date.now();
    if (current && now - lastSave > 5000) { store(posKey(current.src), audio.currentTime); lastSave = now; }
  });
  seek.addEventListener('input', function () { audio.currentTime = seek.value; paintSeek(); });
  audio.addEventListener('play', syncButtons);
  audio.addEventListener('pause', function () { syncButtons(); if (current) store(posKey(current.src), audio.currentTime); });
  audio.addEventListener('ended', function () { if (current) store(posKey(current.src), 0); syncButtons(); });

  if ('mediaSession' in navigator) {
    navigator.mediaSession.setActionHandler('seekbackward', function () { audio.currentTime -= 15; });
    navigator.mediaSession.setActionHandler('seekforward', function () { audio.currentTime += 30; });
  }

  // atajos: espacio = play/pausa (fuera de campos de texto)
  document.addEventListener('keydown', function (e) {
    if (e.code !== 'Space' || !current || /INPUT|TEXTAREA|BUTTON/.test(e.target.tagName)) return;
    e.preventDefault();
    audio.paused ? audio.play() : audio.pause();
  });

  // retomar el ultimo episodio escuchado (sin reproducir solo)
  try {
    var last = JSON.parse(store('cd-last'));
    if (last && last.src) load(last);
  } catch (e) { /* nada */ }

  // buscador de episodios en la home
  var buscar = $('buscar');
  if (buscar) {
    var items = document.querySelectorAll('.js-episodio');
    var norm = function (s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); };
    var textos = Array.prototype.map.call(items, function (el) { return norm(el.dataset.texto); });
    buscar.addEventListener('input', function () {
      var q = norm(buscar.value.trim()), vis = 0;
      items.forEach(function (el, i) {
        var ok = !q || textos[i].indexOf(q) !== -1;
        el.hidden = !ok;
        if (ok) vis++;
      });
      $('sin-resultados').hidden = vis > 0;
    });
  }

  // convertir URLs sueltas en links (ideas de la charla)
  document.querySelectorAll('.js-linkify li').forEach(function (li) {
    if (li.querySelector('a')) return;
    li.innerHTML = li.innerHTML.replace(/(https?:\/\/[^\s<]+)/g, '<a href="$1" rel="noopener">$1</a>');
  });

  // copiar codigo de insercion
  document.querySelectorAll('.js-copy').forEach(function (b) {
    b.addEventListener('click', function () {
      var t = $(b.dataset.target);
      navigator.clipboard.writeText(t.value).then(function () {
        var old = b.innerHTML;
        b.innerHTML = '<i class="bi bi-check2"></i> Copiado';
        setTimeout(function () { b.innerHTML = old; }, 1500);
      });
    });
  });

  // compartir nativo si el navegador lo soporta, si no copia el link
  document.querySelectorAll('.js-share').forEach(function (b) {
    b.addEventListener('click', function () {
      var data = { title: b.dataset.title, url: b.dataset.url };
      if (navigator.share) navigator.share(data).catch(function () {});
      else navigator.clipboard.writeText(data.url).then(function () { b.innerHTML = '<i class="bi bi-check2"></i> Link copiado'; });
    });
  });
})();
