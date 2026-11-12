/*
  AZ Driving School - contact form -> email
  Vercel serverless function (Node). Receives the enquiry form as JSON and emails it to info@azdriving.co.uk
  through Resend (https://resend.com). No npm packages needed.

  Environment variables (Vercel > Project > Settings > Environment Variables):
    RESEND_API_KEY  (required)  API key from resend.com
    MAIL_FROM       (optional)  default: "AZ Driving School Website <enquiries@azdriving.co.uk>"
                                the domain must be verified in Resend (Domains > Add azdriving.co.uk)
    MAIL_TO         (optional)  default: info@azdriving.co.uk  (comma separated for several inboxes)
*/
'use strict';

const MAIL_TO = (process.env.MAIL_TO || 'info@azdriving.co.uk').split(',').map(s => s.trim()).filter(Boolean);
const MAIL_FROM = process.env.MAIL_FROM || 'AZ Driving School Website <enquiries@azdriving.co.uk>';

const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const clean = (v, max) => (typeof v === 'string' ? v : '').replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '').trim().slice(0, max);
const oneLine = v => v.replace(/\s+/g, ' ');

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
  // Health check: open https://azdriving.co.uk/api/contact/ in a browser to see whether email sending is configured (no secrets shown).
  if (req.method === 'GET') {
    const ok = !!process.env.RESEND_API_KEY;
    return res.status(200).json({
      ok, configured: ok, to: MAIL_TO.map(a => a.replace(/^(.).*(@.*)$/, '$1***$2')), from: MAIL_FROM,
      hint: ok ? 'RESEND_API_KEY is set. If enquiries still fail, check Vercel > Logs for lines starting with "contact:".'
               : 'RESEND_API_KEY is NOT set. Add it in Vercel > Project > Settings > Environment Variables, then redeploy.'
    });
  }
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
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

  if (!process.env.RESEND_API_KEY) {
    console.error('contact: RESEND_API_KEY is not set');
    return res.status(500).json({ ok: false, error: 'not_configured' });
  }

  const rows = [
    ['Name', name], ['Phone', phone], ['Email', email], ['Course', course || '-'],
    ['Location', location || '-'], ['Preferred contact', method || '-'], ['Message', message || '-']
  ];
  const text = 'New enquiry from azdriving.co.uk\n\n' + rows.map(r => r[0] + ': ' + r[1]).join('\n') + '\n';
  const html =
    '<div style="font-family:Arial,Helvetica,sans-serif;max-width:560px;margin:0 auto;color:#0a1a40">' +
    '<div style="background:#0b1f4d;color:#fff;padding:18px 22px;border-radius:12px 12px 0 0"><b style="font-size:18px">New driving lesson enquiry</b>' +
    '<div style="color:#e9b93a;font-size:13px;margin-top:2px">azdriving.co.uk contact form</div></div>' +
    '<table style="width:100%;border-collapse:collapse;border:1px solid #e3e6ee;border-top:0" cellpadding="10">' +
    rows.map(r => '<tr><td style="width:150px;background:#f5f3ec;border-bottom:1px solid #e3e6ee;font-weight:bold;vertical-align:top">' + esc(r[0]) +
      '</td><td style="border-bottom:1px solid #e3e6ee;vertical-align:top;white-space:pre-wrap">' + esc(r[1]) + '</td></tr>').join('') +
    '</table><p style="font-size:12px;color:#667;margin-top:14px">Press Reply to answer ' + esc(name) + ' directly.</p></div>';

  const send = from => fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + process.env.RESEND_API_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from,
      to: MAIL_TO,
      reply_to: email,
      subject: 'New enquiry: ' + name + (course ? ' - ' + course : ''),
      text,
      html
    })
  });

  try {
    let r = await send(MAIL_FROM);
    let body = await r.text();
    // Domain not verified yet in Resend (403/422)? Retry once with Resend's shared test sender so the enquiry is not lost.
    if (!r.ok && (r.status === 403 || r.status === 422) && /domain|verif|from/i.test(body) && !/onboarding@resend\.dev/.test(MAIL_FROM)) {
      console.error('contact: sender domain not verified, retrying with onboarding@resend.dev. Resend said:', body.slice(0, 300));
      r = await send('AZ Driving School Website <onboarding@resend.dev>');
      body = await r.text();
    }
    if (!r.ok) {
      console.error('contact: Resend error', r.status, body.slice(0, 500));
      const error = r.status === 401 || r.status === 403 ? 'mail_auth' : 'send_failed';
      return res.status(502).json({ ok: false, error });
    }
    return res.status(200).json({ ok: true });
  } catch (e) {
    console.error('contact: request failed', e && e.message);
    return res.status(502).json({ ok: false, error: 'send_failed' });
  }
};
