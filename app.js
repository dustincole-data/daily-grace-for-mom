async function loadDailyGrace() {
  try {
    const response = await fetch(`data/today.json?ts=${Date.now()}`, { cache: 'no-store' });
    if (!response.ok) throw new Error(`Unable to load daily content: ${response.status}`);
    const data = await response.json();

    document.getElementById('display-date').textContent = data.display_date;
    document.getElementById('prayer-title').textContent = data.prayer.title;
    document.getElementById('prayer-text').textContent = data.prayer.text;

    const source = document.getElementById('prayer-source');
    source.textContent = data.prayer.source;
    source.href = data.prayer.link;

    document.getElementById('thought-headline').textContent = data.thought.headline;
    document.getElementById('thought-body').textContent = data.thought.body;
    document.getElementById('verse').textContent = data.thought.verse;
    document.getElementById('practice').textContent = data.practice;
    document.getElementById('blessing').textContent = data.blessing;
    document.getElementById('readings-note').textContent = data.daily_readings.note;
    document.getElementById('readings-link').href = data.daily_readings.url;
  } catch (error) {
    console.error(error);
    document.getElementById('display-date').textContent = 'A prayer is ready for today';
    document.getElementById('prayer-title').textContent = 'Jesus, I trust in You';
    document.getElementById('prayer-text').textContent = 'Lord, be close today. Bring comfort, hope, and healing. Amen.';
    document.getElementById('thought-headline').textContent = 'You are not alone.';
    document.getElementById('thought-body').textContent = 'God is near in this moment, and love is holding you.';
  }
}

loadDailyGrace();
