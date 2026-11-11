/* Local test server: serves the site AND runs api/contact.js (so the form can send email on localhost).
   Usage:  1) create a file named .env.local containing   RESEND_API_KEY=re_xxxxxxxx
           2) run   node dev-server.js     3) open http://localhost:3000
   Optional in .env.local: MAIL_FROM=AZ Driving School <onboarding@resend.dev>   (for testing before your domain is verified)  */
const http = require('http'), fs = require('fs'), path = require('path');
for (const name of ['.env.local', '.env.local.txt', '.env']) {
  try {
    fs.readFileSync(path.join(__dirname, name), 'utf8').replace(/^\uFEFF/, '').split(/\r?\n/).forEach(l => {
      const m = l.match(/^\s*([A-Za-z_]+)\s*=\s*(.*?)\s*$/); if (m && !(m[1] in process.env)) process.env[m[1]] = m[2].replace(/^["']|["']$/g, '');
    });
    console.log('Loaded settings from ' + name); break;
  } catch (e) { /* try next */ }
}
console.log(process.env.RESEND_API_KEY ? 'RESEND_API_KEY: found' : 'RESEND_API_KEY: NOT FOUND - create a file named .env.local next to dev-server.js containing RESEND_API_KEY=re_xxxx');
const contact = require('./api/contact.js');
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.webp': 'image/webp', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.ico': 'image/x-icon', '.mp4': 'video/mp4', '.txt': 'text/plain', '.xml': 'application/xml', '.webmanifest': 'application/manifest+json' };
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
  fs.readFile(f, (err, data) => {
    if (err) { res.statusCode = 404; return fs.readFile(path.join(__dirname, '404.html'), (e, d) => res.end(d || 'Not found')); }
    res.setHeader('Content-Type', TYPES[path.extname(f)] || 'application/octet-stream'); res.end(data);
  });
}).listen(3000, () => console.log('AZ Driving School running at http://localhost:3000'));
