/*
  AZ Driving School - contact form -> email (built in, no third-party service, no npm packages)
  Vercel serverless function. Receives the enquiry as JSON and emails it to info@azdriving.co.uk
  by logging in to YOUR OWN mailbox over SMTP (the same login you use in Outlook / Apple Mail / Gmail app).

  ONE-TIME SETUP: fill in the 3 values below (SMTP_HOST, SMTP_USER, SMTP_PASS) and deploy. That is all.
  Where to find them: your email host's "SMTP settings" page (cPanel, Hostinger, GoDaddy, Microsoft 365, Google Workspace...).
    Common hosts:  Hostinger smtp.hostinger.com | GoDaddy smtpout.secureserver.net | Gmail/Workspace smtp.gmail.com (use an App Password)
                   cPanel mail.yourdomain.co.uk | Microsoft 365 smtp.office365.com (port 587)
  Port 465 (secure) is the default. Use 587 if your host says so.

  Keep your GitHub repository PRIVATE because the mailbox password lives in this file (server side only, never sent to browsers).
  Optional: the same names can be set as Vercel environment variables instead, which override the values here.
*/
'use strict';
const net = require('net');
const tls = require('tls');

// ================= BUILT-IN SETTINGS =================
const BUILT_IN = {
  SMTP_HOST: 'smtp.hostinger.com',      // Hostinger
  SMTP_PORT: 465,                      // 465 (secure) or 587
  SMTP_USER: 'info@azdriving.co.uk',   // full mailbox login
  SMTP_PASS: '',                       // that mailbox's password (or app password)
  MAIL_TO: 'info@azdriving.co.uk'      // where enquiries are delivered (comma separated for several)
};
// =====================================================

const cfg = k => (process.env[k] !== undefined && process.env[k] !== '' ? process.env[k] : BUILT_IN[k]);
const getConfig = () => ({
  host: String(cfg('SMTP_HOST') || '').trim(),
  port: parseInt(cfg('SMTP_PORT'), 10) || 465,
  user: String(cfg('SMTP_USER') || '').trim(),
  pass: String(cfg('SMTP_PASS') || ''),
  secure: parseInt(cfg('SMTP_PORT'), 10) === 465 || String(cfg('SMTP_SECURE') || '') === 'true',
  to: String(cfg('MAIL_TO') || '').split(',').map(s => s.trim()).filter(Boolean)
});

const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const clean = (v, max) => (typeof v === 'string' ? v : '').replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '').trim().slice(0, max);
const oneLine = v => v.replace(/\s+/g, ' ');
const b64 = s => Buffer.from(s, 'utf8').toString('base64');
const wrap64 = s => b64(s).replace(/(.{76})/g, '$1\r\n');
const header = s => (/^[\x20-\x7e]*$/.test(s) ? s : '=?UTF-8?B?' + b64(s) + '?=');

/* ---------- minimal SMTP client (implicit TLS on 465, STARTTLS on 587) ---------- */
function smtpSend({ host, port, user, pass, secure }, from, rcpts, raw) {
  return new Promise((resolve, reject) => {
    let sock, buf = '', waiter = null, done = false;
    const fail = e => { if (done) return; done = true; try { sock && sock.destroy(); } catch (x) { /* ignore */ } reject(e); };
    const timer = setTimeout(() => fail(Object.assign(new Error('timeout'), { code: 'timeout' })), 15000);
    const finish = () => { if (done) return; done = true; clearTimeout(timer); try { sock.end(); } catch (x) { /* ignore */ } resolve(); };

    function onData(d) {
      buf += d.toString('utf8');
      pump();
    }
    function pump() {
      // a reply is complete when a line matches "NNN " (space, not dash)
      const lines = buf.split('\r\n');
      for (let i = 0; i < lines.length - 1; i++) {
        if (/^\d{3} /.test(lines[i])) {
          const text = lines.slice(0, i + 1).join('\n');
          buf = lines.slice(i + 1).join('\r\n');
          const w = waiter; waiter = null;
          if (w) w({ code: parseInt(lines[i].slice(0, 3), 10), text });
          return;
        }
      }
    }
    const read = () => new Promise((res, rej) => { waiter = res; pump(); sock.once('error', rej); });
    const cmd = async (line, ok) => {
      if (line !== null) sock.write(line + '\r\n');
      const r = await read();
      if (!ok.includes(r.code)) throw Object.assign(new Error('smtp ' + r.code + ' ' + r.text.slice(0, 200)), { code: 'smtp_' + r.code, smtp: r.code });
      return r;
    };

    const attach = s => { sock = s; sock.setEncoding && 0; sock.on('data', onData); sock.on('error', fail); sock.on('close', () => { if (!done) fail(new Error('closed')); }); };

    (async () => {
      sock = await new Promise((res, rej) => {
        const s = secure ? tls.connect({ host, port, servername: host }, () => res(s)) : net.connect({ host, port }, () => res(s));
        s.once('error', rej);
      });
      sock.removeAllListeners('error');
      attach(sock);
      await cmd(null, [220]);
      let ehlo = await cmd('EHLO azdriving.co.uk', [250]);
      if (!secure) {
        await cmd('STARTTLS', [220]);
        sock.removeAllListeners('data'); sock.removeAllListeners('close'); sock.removeAllListeners('error');
        buf = '';
        sock = await new Promise((res, rej) => { const s = tls.connect({ socket: sock, host, servername: host }, () => res(s)); s.once('error', rej); });
        sock.removeAllListeners('error');
        attach(sock);
        ehlo = await cmd('EHLO azdriving.co.uk', [250]);
      }
      if (user && pass) {
        if (/AUTH[^\n]*PLAIN/i.test(ehlo.text) && !/AUTH[^\n]*LOGIN/i.test(ehlo.text)) {
          await cmd('AUTH PLAIN ' + Buffer.from('\0' + user + '\0' + pass).toString('base64'), [235]);
        } else {
          await cmd('AUTH LOGIN', [334]);
          await cmd(b64(user), [334]);
          await cmd(b64(pass), [235]);
        }
      }
      await cmd('MAIL FROM:<' + from + '>', [250]);
      for (const r of rcpts) await cmd('RCPT TO:<' + r + '>', [250, 251]);
      await cmd('DATA', [354]);
      const body = raw.replace(/\r?\n/g, '\r\n').replace(/^\./gm, '..');
      await cmd(body + '\r\n.', [250]);
      try { sock.write('QUIT\r\n'); } catch (x) { /* ignore */ }
      finish();
    })().catch(fail);
  });
}

function parseBody(req) {
  const b = req.body;
  if (b && typeof b === 'object' && !Buffer.isBuffer(b)) return b;
  if (typeof b === 'string' || Buffer.isBuffer(b)) {
    try { return JSON.parse(b.toString()); } catch (e) { /* fall through */ }
  }
  return {};
}

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  const c = getConfig();

  if (req.method === 'GET') {
    // Health check: open https://azdriving.co.uk/api/contact/ to see whether email is configured. Never reveals the password.
    return res.status(200).json({ ok: true, configured: !!(c.host && c.user && c.pass && c.to.length), host: c.host || null, port: c.port, user: c.user || null });
  }
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'GET, POST');
    return res.status(405).json({ ok: false, error: 'method_not_allowed' });
  }

  const d = parseBody(req);

  // Spam trap: real visitors never see/fill this field. Pretend success so bots move on.
  if (clean(d.website, 200)) return res.status(200).json({ ok: true });

  const name = oneLine(clean(d.name, 100));
  const phone = oneLine(clean(d.phone, 30));
  const email = oneLine(clean(d.email, 160));
  const course = oneLine(clean(d.course, 120));
  const location = oneLine(clean(d.location, 120));
  const method = oneLine(clean(d.method, 40));
  const message = clean(d.message, 2000);

  const errors = {};
  if (name.length < 2) errors.name = true;
  if (!/^[+\d][\d\s()-]{7,}$/.test(phone)) errors.phone = true;
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) errors.email = true;
  if (Object.keys(errors).length) return res.status(400).json({ ok: false, error: 'invalid', fields: errors });

  if (!(c.host && c.user && c.pass && c.to.length)) {
    console.error('contact: SMTP is not configured (fill SMTP_HOST / SMTP_USER / SMTP_PASS in api/contact.js)');
    return res.status(500).json({ ok: false, error: 'not_configured' });
  }

  const rows = [
    ['Name', name], ['Phone', phone], ['Email', email], ['Course', course || '-'],
    ['Location', location || '-'], ['Preferred contact', method || '-'], ['Message', message || '-']
  ];
  const text = 'New enquiry from azdriving.co.uk\r\n\r\n' + rows.map(r => r[0] + ': ' + r[1]).join('\r\n') + '\r\n';
  const html =
    '<div style="font-family:Arial,Helvetica,sans-serif;max-width:560px;margin:0 auto;color:#0a1a40">' +
    '<div style="background:#0b1f4d;color:#fff;padding:18px 22px;border-radius:12px 12px 0 0"><b style="font-size:18px">New driving lesson enquiry</b>' +
    '<div style="color:#e9b93a;font-size:13px;margin-top:2px">azdriving.co.uk contact form</div></div>' +
    '<table style="width:100%;border-collapse:collapse;border:1px solid #e3e6ee;border-top:0" cellpadding="10">' +
    rows.map(r => '<tr><td style="width:150px;background:#f5f3ec;border-bottom:1px solid #e3e6ee;font-weight:bold;vertical-align:top">' + esc(r[0]) +
      '</td><td style="border-bottom:1px solid #e3e6ee;vertical-align:top;white-space:pre-wrap">' + esc(r[1]) + '</td></tr>').join('') +
    '</table><p style="font-size:12px;color:#667;margin-top:14px">Press Reply to answer ' + esc(name) + ' directly.</p></div>';

  const subject = 'New enquiry: ' + name + (course ? ' - ' + course : '');
  const bnd = '=_azd_' + Date.now().toString(36) + Math.random().toString(36).slice(2);
  const raw = [
    'From: ' + header('AZ Driving School Website') + ' <' + c.user + '>',
    'To: ' + c.to.map(t => '<' + t + '>').join(', '),
    'Reply-To: ' + header(name) + ' <' + email + '>',
    'Subject: ' + header(subject),
    'Date: ' + new Date().toUTCString().replace('GMT', '+0000'),
    'Message-ID: <' + Date.now().toString(36) + '.' + Math.random().toString(36).slice(2) + '@' + (c.user.split('@')[1] || 'azdriving.co.uk') + '>',
    'MIME-Version: 1.0',
    'Content-Type: multipart/alternative; boundary="' + bnd + '"',
    '',
    '--' + bnd,
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: base64',
    '',
    wrap64(text),
    '--' + bnd,
    'Content-Type: text/html; charset=UTF-8',
    'Content-Transfer-Encoding: base64',
    '',
    wrap64(html),
    '--' + bnd + '--',
    ''
  ].join('\r\n');

  try {
    await smtpSend(c, c.user, c.to, raw);
    return res.status(200).json({ ok: true });
  } catch (e) {
    console.error('contact: SMTP failed:', e && e.message);
    const code = e && e.smtp === 535 ? 'bad_login' : 'send_failed';
    return res.status(502).json({ ok: false, error: code });
  }
};
