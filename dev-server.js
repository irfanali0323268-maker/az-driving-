/* Local test server: serves the site AND runs api/contact.js (so the form can send email on localhost).
   Usage:  1) fill SMTP_HOST / SMTP_USER / SMTP_PASS inside api/contact.js (or put them in a .env.local file)
           2) run   node dev-server.js     3) open http://localhost:3000  */
const http = require('http'), fs = require('fs'), path = require('path');
for (const name of ['.env.local', '.env.local.txt', '.env']) {
  try {
    fs.readFileSync(path.join(__dirname, name), 'utf8').replace(/^\uFEFF/, '').split(/\r?\n/).forEach(l => {
      const m = l.match(/^\s*([A-Za-z_]+)\s*=\s*(.*?)\s*$/); if (m && !(m[1] in process.env)) process.env[m[1]] = m[2].replace(/^["']|["']$/g, '');
    });
    console.log('Loaded settings from ' + name); break;
  } catch (e) { /* try next */ }
}
const contact = require('./api/contact.js');
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.webp': 'image/webp', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.ico': 'image/x-icon', '.mp4': 'video/mp4', '.webm': 'video/webm', '.txt': 'text/plain', '.xml': 'application/xml', '.webmanifest': 'application/manifest+json' };
http.createServer((req, res) => {
  const url = decodeURIComponent(req.url.split('?')[0]);
  if (url.replace(/\/$/, '') === '/api/contact') {
    let raw = ''; req.on('data', c => raw += c); req.on('end', async () => {
      req.body = raw; res.status = c => { res.statusCode = c; return res; };
      res.json = o => { res.setHeader('Content-Type', 'application/json'); res.end(JSON.stringify(o)); return res; };
      try { await contact(req, res); } catch (e) { console.error(e); res.status(500).json({ ok: false, error: 'server' }); }
    }); return;
  }
  let f = path.join(__dirname, path.normalize(url));
  if (!f.startsWith(__dirname)) { res.statusCode = 403; return res.end(); }
  if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
<<<<<<< HEAD
  fs.readFile(f, (err, data) => {
    if (err) { res.statusCode = 404; return fs.readFile(path.join(__dirname, '404.html'), (e, d) => res.end(d || 'Not found')); }
    res.setHeader('Content-Type', TYPES[path.extname(f)] || 'application/octet-stream'); res.setHeader('Accept-Ranges', 'bytes');
    // Range support (like Vercel) - Safari/iOS will not play video from a server that ignores Range requests
    const m = /bytes=(\d*)-(\d*)/.exec(req.headers.range || '');
    if (m) { const a = m[1] ? +m[1] : 0, e = m[2] ? Math.min(+m[2], data.length - 1) : data.length - 1;
      res.statusCode = 206; res.setHeader('Content-Range', `bytes ${a}-${e}/${data.length}`); res.setHeader('Content-Length', e - a + 1); return res.end(data.slice(a, e + 1)); }
    res.setHeader('Content-Length', data.length); res.end(data);
=======
  fs.stat(f, (err, st) => {
    if (err || !st.isFile()) { res.statusCode = 404; return fs.readFile(path.join(__dirname, '404.html'), (e, d) => { res.setHeader('Content-Type', 'text/html; charset=utf-8'); res.end(d || 'Not found'); }); }
    const type = TYPES[path.extname(f)] || 'application/octet-stream';
    res.setHeader('Content-Type', type); res.setHeader('Accept-Ranges', 'bytes'); res.setHeader('Cache-Control', 'no-cache');
    // Range support: browsers need this to play and seek video (mp4 / webm)
    const m = /^bytes=(\d*)-(\d*)$/.exec(req.headers.range || '');
    if (m && (m[1] || m[2])) {
      let start = m[1] === '' ? Math.max(0, st.size - parseInt(m[2], 10)) : parseInt(m[1], 10);
      let end = m[1] === '' || m[2] === '' ? st.size - 1 : Math.min(parseInt(m[2], 10), st.size - 1);
      if (start > end || start >= st.size) { res.statusCode = 416; res.setHeader('Content-Range', 'bytes */' + st.size); return res.end(); }
      res.statusCode = 206; res.setHeader('Content-Range', 'bytes ' + start + '-' + end + '/' + st.size); res.setHeader('Content-Length', end - start + 1);
      return fs.createReadStream(f, { start, end }).pipe(res);
    }
    res.setHeader('Content-Length', st.size);
    fs.createReadStream(f).pipe(res);
>>>>>>> 7db209471ab21315bd2c0c5956c28924a576f193
  });
}).listen(3000, () => console.log('AZ Driving School running at http://localhost:3000'));
