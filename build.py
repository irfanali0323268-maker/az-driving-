"""AZ Driving School - static site generator.
Edit the CONTENT section, then run:  python3 build.py
Pages are written as clean URLs: /about-us/index.html -> https://azdriving.co.uk/about-us/
"""
import os, re, json, html, shutil, glob
from urllib.parse import quote

BASE = 'https://azdriving.co.uk'
PHONE_D, PHONE = '+447380323268', '+44 7380 323268'
EMAIL = 'info@azdriving.co.uk'
TODAY, TODAY_H = '2026-11-09', '9 November 2026'
AREAS = ['Gloucester', 'Stroud', 'Tewkesbury', 'Cheltenham']
ADDR = 'Diamond Jubilee Close, Gloucester, GL1\u00a04LR'
WA = 'https://wa.me/447380323268'
WA_ICON = '<svg viewBox="0 0 24 24" width="28" height="28" fill="currentColor" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.39-1.47-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48 0 1.46 1.07 2.88 1.21 3.07.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.69.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.17-1.41-.07-.12-.27-.2-.57-.35m-5.42 7.4h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.88 9.89-9.88 2.64 0 5.12 1.03 6.99 2.9a9.82 9.82 0 0 1 2.89 6.99c0 5.45-4.44 9.88-9.88 9.88m8.41-18.3A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.89 0-3.18-1.24-6.17-3.48-8.41z"/></svg>'
FOOT_Q = [('How much are lessons?', 'Hi AZ Driving School, how much are your driving lessons?'), ('Manual or automatic?', 'Hi, do you offer both manual and automatic lessons?'),
          ('Which areas do you cover?', 'Hi, which areas do you cover for driving lessons?'), ('Do you teach beginners?', 'Hi, do you teach complete beginners?'), ('How do I book?', 'Hi, how do I book my first lesson?')]
MAPS = 'https://www.google.com/maps/search/?api=1&query=Diamond+Jubilee+Close+Gloucester+GL1+4LR'
V = '34'  # cache-bust for css/js

esc = html.escape
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

# ----------------------------------------------------------------- CONTENT
NAV = [('about-us', 'About Us'), ('driving-courses', 'Courses'), ('driving-theory-test', 'Theory Test'),
       ('success-stories', 'Success Stories'), ('pricing', 'Pricing'), ('faqs', 'FAQs'), ('contact', 'Contact')]
NAMES = dict(NAV); NAMES['index'] = 'Home'

COURSES = [
 ('Manual Driving Lessons', 'Learn in a manual car and earn a full licence that lets you drive both manual and automatic cars.', 'Learners wanting maximum flexibility.'),
 ('Automatic Driving Lessons', 'Focus on the road without gear changes. A relaxed, confidence-building way to learn.', 'Nervous learners or anyone wanting simplicity.'),
 ('Beginner Driving Lessons', 'Start from lesson one at your own pace, with clear explanations and plenty of practice.', 'Anyone who has never driven.'),
 ('Intensive Driving Lessons', 'Concentrated learning when time is short. Ask about availability and durations.', 'Learners with a deadline.'),
 ('Refresher Driving Lessons', 'Rebuild confidence after a break with lessons that start where you are today.', 'Licence holders who have not driven recently.'),
 ('Pass Plus', 'Extra training after you pass to build experience in a wider range of conditions.', 'Newly qualified drivers.'),
 ('Motorway Driving Lessons', 'Learn to join, lane-change and exit motorways calmly and safely.', 'Learners and new drivers.'),
 ('Eco Driving Lessons', 'Drive smoothly and efficiently to use less fuel and reduce wear.', 'Any driver.'),
]
COURSE_ALT = ['Driver’s hands on a steering wheel on an open road', 'Automatic gear selector inside a car',
 'Red L plate on top of a learner car', 'Open road at sunset', 'Car driving along a coastal road at sunset',
 'Graduation cap with gold tassel', 'Cars driving on a motorway', 'Small white car beside a young green plant']

PRICES = {
 'gl': ('Gloucester', 40, [('First 2 Lessons', 60, '2 Hours'), ('Standard Lesson', 40, '1 Hour'), ('Block of 5 Lessons', 190, '5 Hours'),
        ('Block of 10 Lessons', 370, '10 Hours'), ('Pass Plus', 250, 'Approximately 5 Hours'), ('Motorway & Refresher', 85, '2 Hours'), ('Eco Driving', 90, '2 Hours')]),
 'st': ('Stroud, Tewkesbury & Cheltenham', 45, [('First 2 Lessons', 60, '2 Hours'), ('Standard Lesson', 45, '1 Hour'), ('Block of 5 Lessons', 215, '5 Hours'),
        ('Block of 10 Lessons', 430, '10 Hours'), ('Pass Plus', 250, 'Approximately 5 Hours'), ('Motorway & Refresher', 90, '2 Hours'), ('Eco Driving', 90, '2 Hours')]),
}

FAQ = [
 ('General Driving Lessons', [
  ('Where do you teach?', 'We teach in Gloucester, Stroud, Tewkesbury and Cheltenham.'),
  ('Does AZ Driving School cover Cheltenham and Stroud?', 'Yes. We offer lessons in Gloucester, Stroud, Tewkesbury and Cheltenham.'),
  ('How many lessons will I need?', 'It varies for each learner. Your instructor will assess your progress and advise honestly.'),
  ('Do you teach complete beginners?', 'Yes. Our beginner lessons start from lesson one, at your own pace.'),
  ('I have not driven for a while. Can you help?', 'Yes. Refresher lessons are designed to rebuild your confidence after a break.')]),
 ('Manual & Automatic Lessons', [
  ('Do you offer both manual and automatic lessons?', 'Yes, manual and automatic lessons are available.'),
  ('Should I learn in a manual or an automatic car?', 'An automatic car has fewer controls, so you can concentrate on the road. A manual licence lets you drive both types of car. Your instructor can talk through which suits you best.')]),
 ('Pricing & Payments', [
  ('How much does a lesson cost?', 'A standard hour is £40 in Gloucester and £45 in Stroud, Tewkesbury and Cheltenham. Please confirm availability and pricing before booking.'),
  ('How much do driving lessons cost in Gloucester?', 'A standard one-hour lesson is £40 and your first two lessons (2 hours) are £60. Blocks of 5 and 10 lessons cost £190 and £370.'),
  ('Do you offer block bookings?', 'Yes. In Gloucester a block of 5 lessons is £190 and a block of 10 is £370. In Stroud, Tewkesbury and Cheltenham they are £215 and £430.')]),
 ('Booking & Scheduling', [
  ('How do I book?', f'Call or WhatsApp {PHONE}, email {EMAIL} or use the contact form.'),
  ('Where can I book driving lessons in Gloucester?', f'Use our contact page, or call or WhatsApp {PHONE}.')]),
 ('Courses & Extra Training', [
  ('Do you offer Pass Plus and motorway lessons?', 'Yes. Pass Plus, motorway, refresher and eco driving lessons are all available. See our pricing page for current rates.'),
  ('Can I take intensive lessons?', 'Intensive lessons are available for learners with a deadline. Please ask about availability.')]),
 ('Driving Theory Tests', [
  ('What is in the car theory test?', '50 multiple-choice questions in 57 minutes (pass mark 43), then hazard perception: 14 clips (pass mark 44 out of 75).'),
  ('How can I prepare for my UK driving theory test?', 'Study the Highway Code, practise multiple-choice and hazard perception questions, then book through GOV.UK. Our theory test page has a practice quiz.')]),
 ('Practical Driving Tests', [
  ('How do I book a practical test?', 'Practical tests are booked through GOV.UK. Your instructor can advise when you are ready.')]),
 ('Driving Instructor Training', [
  ('Do you train instructors?', f'For information about instructor training, please call {PHONE} or email {EMAIL}.')]),
]

GALLERY_ALT = {
 1: 'Learner holding a document beside a red lesson car, door open', 2: 'Learner holding a document in front of a grey lesson car',
 3: 'Learner in a maroon t-shirt holding a document beside a grey car with an L plate', 4: 'Learner standing in a parking bay behind a blue car with an L plate',
 5: 'Learner holding a document beside a white hybrid lesson car', 6: 'Learner holding a document behind a white car on a sunny day',
 7: 'Learner holding a document beside a grey lesson car', 8: 'Learner holding a document beside a black car with an L plate',
 9: 'Learner in a blue t-shirt holding a document beside a white lesson car', 10: 'Learner holding a document beside a grey lesson car',
 11: 'Learner in a light blue t-shirt holding a document beside a white car with an L plate', 12: 'Learner holding a document in front of a grey car with an L plate',
 13: 'Learner in a teal t-shirt holding a document beside a white lesson car', 14: 'Learner in a maroon t-shirt holding a document beside a white hybrid car',
 15: 'Learner holding a document in front of a black lesson car', 16: 'Learner holding a document beside a black car with an L plate',
 17: 'Learner standing beside a black lesson car on a residential street', 18: 'Learner standing beside a black lesson car in a parking bay',
 19: 'Learner holding a document beside a grey lesson car', 20: 'Learner in a white t-shirt holding a document behind a silver lesson car', 21: 'Learner in a light blue shirt holding a document beside a silver lesson car', 22: 'Learner in sunglasses holding a document beside a silver lesson car with the door open', 23: 'Learner in a grey t-shirt holding a document beside a silver lesson car', 24: 'Learner in a white t-shirt holding a document beside a silver lesson car with an L plate', 25: 'Learner in a red top holding a document beside a silver lesson car with an L plate', 26: 'Learner in a grey hoodie holding a document beside a silver lesson car', 27: 'Learner in a black hoodie holding a document beside a lesson car with an L plate'}
GALLERY_DIM = {n: ((640, 853) if n not in (5, 13, 8, 9, 12) else ((640, 640) if n in (5, 13) else (484, 860))) for n in GALLERY_ALT}

PAGES = {  # key: (title, meta description)
 'index': ('Driving School Gloucester | Manual & Automatic Lessons', 'AZ Driving School offers manual and automatic driving lessons in Gloucester, Stroud, Tewkesbury and Cheltenham. Friendly instructors. Book your first lesson.'),
 'about-us': ('About AZ Driving School | Gloucester Driving Instructors', 'Learn about AZ Driving School, a Gloucester driving school with 15+ years of experience, friendly instructors and a safety-first, personalised approach.'),
 'driving-courses': ('Driving Lessons Gloucester | Manual, Automatic & Intensive', 'Manual, automatic, beginner, intensive, refresher, motorway, Pass Plus and eco driving lessons in Gloucester. See who each course suits and book.'),
 'driving-theory-test': ('Theory Test Practice Quiz & Guide | AZ Driving School', 'Prepare for the UK car theory test: 50 questions, hazard perception, road signs, a free practice quiz and the official GOV.UK booking link.'),
 'success-stories': ('Learner Success Stories | AZ Driving School Gloucester', 'See photos of AZ Driving School learners in Gloucester, Stroud, Tewkesbury and Cheltenham, and start your own driving journey with us.'),
 'pricing': ('Driving Lesson Prices Gloucester | From £40 an Hour', 'Driving lesson prices in Gloucester from £40 an hour, with block bookings, Pass Plus and refresher lessons. Separate rates for Stroud, Tewkesbury, Cheltenham.'),
 'faqs': ('Driving Lessons FAQs | AZ Driving School Gloucester', 'Answers about driving lessons in Gloucester: prices, booking, manual and automatic lessons, theory tests, practical tests and the areas we cover.'),
 'contact': ('Book Driving Lessons Gloucester | Contact AZ Driving School', f'Book driving lessons in Gloucester. Call or WhatsApp {PHONE}, email {EMAIL} or send an enquiry. Covering Stroud, Tewkesbury and Cheltenham.'),
}
PAGE_IMAGES = {'index': [f'/assets/gallery/photo-{i}.webp' for i in list(range(1, 9)) + [20, 21, 22, 23]],
 'about-us': [f'/assets/gallery/photo-{i}.webp' for i in (2, 5, 9)],
 'driving-courses': [f'/assets/courses/course-{i}.webp' for i in range(1, 9)],
 'success-stories': [f'/assets/gallery/photo-{i}.webp' for i in range(1, 28)]}
RELATED = {
 'about-us': [('driving-courses', 'Explore our driving lessons in Gloucester'), ('pricing', 'See driving lesson prices'), ('contact', 'Contact AZ Driving School')],
 'driving-courses': [('pricing', 'Driving lesson prices in Gloucester'), ('driving-theory-test', 'Driving theory test preparation'), ('contact', 'Book driving lessons in Gloucester')],
 'pricing': [('driving-courses', 'Compare manual and automatic driving lessons'), ('faqs', 'Driving lesson FAQs'), ('contact', 'Book your first lesson')],
 'driving-theory-test': [('faqs', 'Driving test questions answered'), ('driving-courses', 'Driving lessons in Gloucester'), ('contact', 'Book a lesson')],
 'success-stories': [('driving-courses', 'Driving courses we offer'), ('pricing', 'Driving lesson prices'), ('contact', 'Book a lesson')],
 'faqs': [('driving-theory-test', 'Theory test preparation'), ('pricing', 'Lesson prices'), ('contact', 'Contact AZ Driving School')],
 'contact': [('driving-courses', 'Driving courses'), ('pricing', 'Driving lesson prices'), ('faqs', 'Driving lesson FAQs')]}
UPDATED = {'pricing', 'faqs', 'driving-theory-test'}

# ----------------------------------------------------------------- HELPERS
def U(k): return BASE + ('/' if k == 'index' else f'/{k}/')
def L(k): return '/' if k == 'index' else f'/{k}/'

def hero_cta(label='Book Your First Lesson', href='/contact/'):
    return f'<a class="btn p" href="{href}">{label}</a>'

def CTA(t='Your Driving Journey Starts Here.', s='Call, WhatsApp or send an enquiry and we will help you choose the right lessons.'):
    return (f'<section class="w rv"><div class="gl cta"><span class="eyebrow">Get started</span><h2>{t}</h2><p>{s}</p>'
            f'<div class="row c"><a class="btn p" href="/contact/">Book Your First Lesson</a><a class="btn" href="tel:{PHONE_D}">Call {PHONE}</a></div></div></section>')

def crumbs(name, k):
    return (f'<nav class="cr w" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li aria-current="page">{name}</li></ol></nav>')

def head(eyebrow, h1, sub, k):
    return crumbs(NAMES[k], k) + f'<header class="w ph"><span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p class="lead">{sub}</p></header>'

def sec_head(eyebrow, h2, sub=''):
    return f'<div class="sh rv"><span class="eyebrow">{eyebrow}</span><h2>{h2}</h2>{"<p class=lead>"+sub+"</p>" if sub else ""}</div>'

ICON3D = {'Gloucester': 'pin', 'Stroud': 'car', 'Tewkesbury': 'wheel', 'Cheltenham': 'cap'}
PE = '<i class="fx" aria-hidden="true"></i><i class="fold" aria-hidden="true"></i>'

def card(i, link=True):
    n, d, s = COURSES[i]
    return (f'<article class="gl pe rv cp" id="{slug(n)}">{PE}<img src="/assets/courses/course-{i+1}.webp" alt="{esc(COURSE_ALT[i])}" width="420" height="236" loading="lazy">'
            f'<div class="cb"><h3>{n}</h3><p>{d}</p><p class="su"><b>Suitable for:</b> {s}</p>'
            f'<a class="more" href="/contact/?course={n.replace(" ", "+")}">Book this course <span aria-hidden="true">→</span></a></div></article>')

def info(items, tag='div'):
    return ''.join(f'<{tag} class="gl pe rv">{PE}<h3>{t}</h3><p>{d}</p></{tag}>' for t, d in items)

def gallery(n, h2='Our learners', sub='Photos of AZ Driving School learners, shared with the school. Click a photo or use the arrows.'):
    figs = ''.join(f'<figure class="cc"><img src="/assets/gallery/photo-{i}.webp" alt="{esc(GALLERY_ALT[i])}" width="{GALLERY_DIM[i][0]}" height="{GALLERY_DIM[i][1]}" loading="lazy" draggable="false"></figure>' for i in (n if isinstance(n, (list, tuple)) else range(1, n + 1)))
    return (f'<section class="w rv" aria-labelledby="gal-h">{sec_head("Gallery", h2.replace("<h2", "<h2"), sub).replace("<h2>", "<h2 id=gal-h>")}'
            f'<div class="cf" id="cf" data-slides="{n}" role="group" aria-roledescription="carousel" aria-label="AZ Driving School learner photos">{figs}</div>'
            f'<div class="row c" style="margin-top:18px"><button class="btn ic" id="cp" aria-label="Previous photo">←</button><button class="btn ic" id="cn" aria-label="Next photo">→</button></div></section>')

def per_hour(name, price, hrs):
    m = re.match(r'^(\d+) Hours?$', hrs)
    return round(price / int(m.group(1)), 2) if m and name not in ('Standard Lesson',) else None

def price_panel(key, data):
    area, std, items = data
    out = f'<div class="grid pg" id="{key}" role="tabpanel" aria-labelledby="tab-{key}">'
    for name, p, hrs in items:
        extra = ''; feat = ''
        ph = per_hour(name, p, hrs)
        mb = re.match(r'Block of (\d+)', name)
        if mb:
            n = int(mb.group(1)); save = std * n - p
            extra = f'<p class="sv">≈ £{ph:g} per hour · save £{save} against the standard rate</p>'
            if n == 10: feat = ' feat'
        elif ph:
            extra = f'<p class="sv">≈ £{ph:g} per hour</p>'
        badge = '<span class="bdg">Best value</span>' if feat else ''
        out += (f'<div class="gl pe rv{feat}">{PE}{badge}<h3>{name}</h3><div class="pr">£{p}</div><p class="du">{hrs}</p>{extra}'
                f'<a class="btn p" href="/contact/?course={name.replace(" ", "+").replace("&", "%26")}">Book Now</a></div>')
    return out + '</div>'

def inp(i, l, t='text', ac=''):
    return f'<div class="fld"><label for="{i}">{l}</label><input id="{i}" name="{i}" type="{t}" required{(" autocomplete=%s" % ac) if ac else ""}><div class="er" aria-live="polite"></div></div>'
def sel(i, l, o):
    return f'<div class="fld"><label for="{i}">{l}</label><select id="{i}" name="{i}">' + ''.join(f'<option>{x}</option>' for x in o) + '</select></div>'

VID = ('<div class="vd"><video id="lv" autoplay muted loop playsinline preload="auto" poster="/assets/logo-poster.webp" width="720" height="427" '
       'aria-label="AZ Driving School animated logo"><source src="/assets/logo-animated.mp4" type="video/mp4"></video></div>')

# ----------------------------------------------------------------- PAGE BODIES
def body_index():
    stats = ''.join(f'<div class="st"><div class="big">{n}</div><span>{t}</span></div>' for n, t in
        [('<span data-n="15">15</span>+', 'Years of experience'), ('<span data-n="3000">3,000</span>+', 'Students trained'),
         ('<span data-n="4">4</span>', 'Locations served'), ('<span aria-hidden="true">✓</span><span class="sr">Yes</span>', 'Experienced instructors')])
    steps = ''.join(f'<div class="gl pe rv step">{PE}<span class="num">0{i+1}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate([
        ('Get in touch', f'Call, WhatsApp, email or use the enquiry form. Tell us about your experience and which area you are in.'),
        ('Start with two lessons', 'Your first two lessons (2 hours) are £60, so you can meet your instructor and see how you get on.'),
        ('Learn at your pace', 'Your instructor assesses your progress and gives you honest advice on what to practise next.'),
        ('Take your tests', 'Book your theory and practical tests through GOV.UK. Your instructor can advise when you are ready.')]))
    areas = ''.join(f'<a class="gl pe rv area" href="/pricing/#{"gl" if a=="Gloucester" else "st"}">{PE}<span class="ico3d"><img src="/assets/areas/{ICON3D[a]}.webp" alt="" width="288" height="288" loading="lazy" decoding="async"></span><h3>Driving lessons in {a}</h3>'
        f'<p>{d}</p><span class="more">See {a} prices <span aria-hidden="true">→</span></span></a>' for a, d in [
        ('Gloucester', 'Our home base in Gloucester. Standard lessons from £40 per hour.'),
        ('Stroud', 'Manual and automatic lessons from £45 per hour.'),
        ('Tewkesbury', 'Flexible lesson times from £45 per hour.'),
        ('Cheltenham', 'Friendly, patient instruction from £45 per hour.')])
    why = info([('Affordable pricing', 'Clear hourly rates from £40, with block bookings that work out cheaper per hour.'),
        ('Experienced instructors', 'More than 15 years of teaching and over 3,000 students trained.'),
        ('Professional instruction', 'Structured lessons and honest feedback at every stage.'),
        ('Modern teaching techniques', 'Up-to-date methods that help you understand, not just memorise.'),
        ('Flexible lesson scheduling', 'Lesson times planned around your work, study and family life.'),
        ('Personalised learning', 'Manual or automatic, beginner or refresher: lessons tailored to you.')])
    faq3 = ''.join(f'<details class="gl rv"><summary>{q}</summary><p>{a}</p></details>' for q, a in [FAQ[2][1][1], FAQ[0][1][1], FAQ[3][1][0]])
    return (f'''<section class="w hero"><div class="hc"><span class="eyebrow">Gloucester · Stroud · Tewkesbury · Cheltenham</span>
<h1><span class="g1">Learn to Drive.</span><br><span class="gr">Drive with</span><br><span class="brv" data-blob="14" data-words="Control.|Skill.|Calm.">Confidence.</span></h1>
<p class="lead">Your journey to becoming a confident, safe and independent driver starts with AZ Driving School in Gloucester. Friendly, experienced instructors, manual and automatic cars, and lessons planned around you.</p>
<div class="row"><a class="btn p" href="/contact/">Book Your First Lesson</a><a class="btn" href="/driving-courses/">Explore Our Courses</a></div>
<p class="fine">First two lessons (2 hours) £60 · Call or WhatsApp <a href="tel:{PHONE_D}">{PHONE}</a></p></div>
<div class="hv">{VID}<div class="chip gl" style="top:-4%;left:-3%">Manual &amp; Automatic</div><div class="chip gl" style="top:44%;right:-4%;animation-delay:-2s">From £30 / hour</div><div class="chip gl" style="bottom:-19%;left:34%;animation-delay:-4s">4 areas covered</div></div></section>
<section class="w rv"><div class="gl stats">{stats}</div></section>
<section class="w two"><div class="rv"><span class="eyebrow">About us</span><h2>Your trusted driving school in <span class="brv" data-blob="9" data-words="Stroud|Tewkesbury|Cheltenham">Gloucester</span></h2>
<p>AZ Driving School pairs more than 15 years of experience with friendly, professional instruction. Whether you have never sat behind the wheel or you are returning after a break, every lesson is planned around you: your pace, your confidence and your goals.</p>
<p>We teach in Gloucester, Stroud, Tewkesbury and Cheltenham, in both manual and automatic cars, with modern teaching techniques and flexible scheduling that fits around work, study and family life.</p>
<a class="more" href="/about-us/">More about us <span aria-hidden="true">→</span></a></div>
<ul class="gl nv ticks rv"><li>Manual and automatic lessons</li><li>Beginner, intensive and refresher courses</li><li>Pass Plus, motorway and eco driving</li><li>Flexible lesson scheduling</li><li>Clear, transparent pricing</li></ul></section>
<section class="w">{sec_head("Driving courses", "Lessons for every <span class=gr>learner</span>", "From your very first lesson to extra training after you pass.")}<div class="grid">{''.join(card(i) for i in (0, 1, 2))}</div>
<p class="rv" style="margin-top:22px"><a class="more" href="/driving-courses/">View all driving courses <span aria-hidden="true">→</span></a></p></section>
<section class="w">{sec_head("How it works", "From first call to <span class=gr>confident driver</span>")}<div class="grid steps">{steps}</div></section>
'''
    + gallery(list(range(1, 9)) + [20, 21, 22, 23]) +
    f'''<section class="w">{sec_head("Areas we cover", "Driving lessons across <span class=gr>Gloucestershire</span>")}<div class="grid">{areas}</div></section>
<section class="w">{sec_head("Why AZ Driving School", "Why choose <span class=gr>AZ Driving School?</span>")}<div class="grid">{why}</div></section>
<section class="w">{sec_head("Quick answers", "Common <span class=gr>questions</span>")}<div class="faq">{faq3}</div><p class="rv" style="margin-top:18px"><a class="more" href="/faqs/">Read all FAQs <span aria-hidden="true">→</span></a></p></section>'''
    + CTA())

def body_about():
    cards_ = info([
     ('Our story', 'AZ Driving School has over 15 years of experience and has trained more than 3,000 students across Gloucester, Stroud, Tewkesbury and Cheltenham.'),
     ('Our mission', 'To help every learner become a safe, confident and independent driver.'),
     ('Teaching philosophy', 'Patient, personalised instruction that moves at your pace, using modern teaching techniques.'),
     ('Road safety', 'Safety is at the heart of every lesson, from your first drive to your test and beyond.'),
     ('Our instructors', 'Friendly, experienced instructors who teach in both manual and automatic cars.'),
     ('Where we teach', 'Gloucester, Stroud, Tewkesbury and Cheltenham.')])
    pics = ''.join(f'<img src="/assets/gallery/photo-{n}.webp" alt="{esc(GALLERY_ALT[n])}" width="{GALLERY_DIM[n][0]}" height="{GALLERY_DIM[n][1]}" loading="lazy">' for n in (2, 5, 9))
    return (head('About us', 'Helping Gloucester Become More Confident Drivers', 'A friendly, professional Gloucester driving school built around the learner.', 'about-us')
      + f'<section class="w two"><div class="rv"><h2>A driving school built around <span class="gr">you</span></h2><p>Learning to drive is a big step. We aim to make it enjoyable, clear and stress-free, with instructors who explain things patiently and give honest feedback.</p><p>Whether you are learning in a manual or an automatic car, starting from scratch or rebuilding confidence, your lessons are planned around your progress, not a fixed script.</p></div>'
        f'<ul class="gl nv ticks rv"><li>15+ years of experience</li><li>3,000+ students trained</li><li>4 locations served</li><li>Manual and automatic cars</li></ul></section>'
      + f'<section class="w"><div class="grid">{cards_}</div></section>'
      + f'<section class="w rv">{sec_head("Our learners", "Meet some of our <span class=gr>learners</span>")}<div class="pics">{pics}</div></section>'
      + CTA('Ready to start learning?'))

def body_courses():
    tbl = ('<div class="gl rv tw"><table><caption class="sr">Manual and automatic lessons compared</caption><thead><tr><th></th><th scope="col">Manual</th><th scope="col">Automatic</th></tr></thead><tbody>'
     '<tr><th scope="row">Licence you earn</th><td>Full licence for manual and automatic cars</td><td>Licence for automatic cars</td></tr>'
     '<tr><th scope="row">Controls</th><td>Clutch and gears to learn</td><td>No clutch or gear changes</td></tr>'
     '<tr><th scope="row">Focus</th><td>Extra skill to master alongside road awareness</td><td>Concentrate fully on the road</td></tr>'
     '<tr><th scope="row">Often chosen by</th><td>Learners wanting maximum flexibility</td><td>Nervous learners or anyone wanting simplicity</td></tr></tbody></table></div>')
    return (head('Driving courses', 'Driving Lessons in Gloucester', 'Courses for every learner, in manual and automatic cars, across Gloucester, Stroud, Tewkesbury and Cheltenham.', 'driving-courses')
      + f'<section class="w"><div class="grid">{"".join(card(i) for i in range(8))}</div></section>'
      + f'<section class="w">{sec_head("Choosing a car", "Manual or <span class=gr>automatic?</span>", "Not sure which to choose? Here is a quick comparison. Your instructor can talk it through with you.")}{tbl}<p class="rv" style="margin-top:14px">Durations and availability are confirmed when you enquire.</p></section>'
      + CTA())

def body_theory():
    facts = info([('Multiple-choice', '50 questions in 57 minutes. Pass mark: 43 out of 50.'), ('Hazard perception', '14 video clips. Pass mark: 44 out of 75.'),
        ('Book your test', '<a href="https://www.gov.uk/book-theory-test" target="_blank" rel="noopener">Official GOV.UK booking →</a>')])
    signs = ''.join(f'<div class="gl pe rv sgc">{PE}<img class="sg" src="/assets/sign-{k}.webp" alt="{alt}" width="310" height="257" loading="lazy"><h3>{h}</h3><p>{p}</p></div>' for k, alt, h, p in
        [('stop', 'Red octagonal STOP road sign', 'Stop', 'Stop and give way.'), ('warning', 'Yellow triangular warning road sign with an exclamation mark', 'Warning', 'Triangles warn of hazards ahead.'),
         ('orders', 'Red circular road sign showing a car, a prohibition order', 'Orders', 'Circles give orders or prohibitions.'), ('information', 'Blue square information road sign with a letter i', 'Information', 'Rectangles give information.')])
    tips = info([('Study the Highway Code', 'The Highway Code is the foundation of the theory test. Read it little and often.'),
        ('Practise regularly', 'Short, regular practice sessions help the answers stick far better than last-minute cramming.'),
        ('Train your hazard perception', 'Practise spotting developing hazards early, and use lessons to notice them on real roads.'),
        ('Book through GOV.UK', 'Only book through the official GOV.UK service, and check what you need to bring on the day.')])
    return (head('Theory test', 'Prepare for Your Driving Theory Test with Confidence.', 'What the UK car theory test involves, and how to prepare.', 'driving-theory-test')
      + f'<section class="w"><div class="grid">{facts}</div></section>'
      + f'<section class="w">{sec_head("Preparation", "How to <span class=gr>prepare</span>")}<div class="grid">{tips}</div></section>'
      + f'<section class="w">{sec_head("Road signs", "Road signs <span class=gr>at a glance</span>")}<div class="grid">{signs}</div></section>'
      + f'<section class="w rv">{sec_head("Practice quiz", "Test your <span class=gr>knowledge</span>", "Sample questions by AZ Driving School. Not official DVSA content. See the <a href=https://www.gov.uk/guidance/the-highway-code target=_blank rel=noopener>Highway Code</a>.")}<div class="grid" id="qz"></div><p id="qs" class="fine" role="status"></p></section>')

def body_success():
    return (head('Success stories', 'Real Learners. Real Progress. Real Success.', 'Photos of learners we have taught across Gloucester, Stroud, Tewkesbury and Cheltenham.', 'success-stories')
      + gallery(list(range(1, 28)), 'Learners from across <span class=gr>Gloucestershire</span>', 'Photos of AZ Driving School learners, shared with the school. Click a photo or use the arrows.')
      + '<section class="w rv"><div class="gl"><h3>Genuine reviews only</h3><p>We only ever publish real learner feedback. Reviews will appear here as they are added.</p></div></section>'
      + CTA('Be our next success story.'))

def body_pricing():
    tabs = ''.join(f'<button role="tab" id="tab-{k}" aria-controls="{k}" aria-selected="{"true" if k=="gl" else "false"}" data-t="{k}" class="{"on" if k=="gl" else ""}">{v[0]}</button>' for k, v in PRICES.items())
    return (head('Pricing', 'Driving Lesson Prices in Gloucester', 'Clear, transparent pricing. Choose your area.', 'pricing')
      + f'<section class="w"><div class="seg" role="tablist" aria-label="Choose your area">{tabs}</div>' + ''.join(price_panel(k, v) for k, v in PRICES.items())
      + '<p class="rv" style="margin-top:22px">Please confirm availability and pricing before booking. Per-hour figures are approximate and shown for comparison.</p></section>'
      + CTA('Ready to book?', 'Tell us your area and the course you want, and we will confirm availability and pricing.'))

def body_faqs():
    out = ''
    for g, qs in FAQ:
        out += f'<h2 class="fh">{g}</h2>' + ''.join(f'<details class="gl rv"><summary>{q}</summary><p>{a}</p></details>' for q, a in qs)
    return (head('FAQs', 'Driving Lessons FAQs', 'Quick answers to common questions about lessons, prices, booking and tests.', 'faqs')
      + f'<section class="w faq">{out}</section>' + CTA('Still have questions?', 'We are happy to help. Call, WhatsApp or send us a message.'))

IC = {
 'phone': '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
 'wa': '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8z"/>',
 'mail': '<path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/><path d="m22 6-10 7L2 6"/>',
 'pin': '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>'}
def ico(n): return f'<span class="ci" aria-hidden="true"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{IC[n]}</svg></span>'

def body_contact():
    rows = (f'<a class="cl" href="tel:{PHONE_D}">{ico("phone")}<span><small>Call us</small><b>{PHONE}</b></span></a>'
            f'<a class="cl" href="https://wa.me/{PHONE_D[1:]}" target="_blank" rel="noopener">{ico("wa")}<span><small>WhatsApp</small><b>Message us directly</b></span></a>'
            f'<a class="cl" href="mailto:{EMAIL}">{ico("mail")}<span><small>Email</small><b>{EMAIL}</b></span></a>'
            f'<a class="cl" href="{MAPS}" target="_blank" rel="noopener">{ico("pin")}<span><small>Visit us</small><b>{ADDR}</b></span></a>')
    info_card = (f'<div class="gl nv cn rv"><span class="eyebrow">Get in touch</span><h2>Talk to <span class="gr">AZ Driving School</span></h2>'
                 f'<p>Call, WhatsApp or email us, or send an enquiry. We teach in Gloucester, Stroud, Tewkesbury and Cheltenham.</p><div class="cls">{rows}</div>'
                 f'<div class="row"><a class="btn p" href="https://wa.me/{PHONE_D[1:]}" target="_blank" rel="noopener">WhatsApp us</a><a class="btn" href="{MAPS}" target="_blank" rel="noopener">Open in Maps</a></div></div>')
    form = ('<form class="gl rv" id="f" novalidate><h2 style="font-size:1.7rem">Send an enquiry</h2><p>Tell us a little about what you need. Fields marked required help us reply faster.</p>'
      f'<div class="fr">{inp("n","Full Name","text","name")}{inp("p","Phone Number","tel","tel")}</div>'
      f'<div class="fr">{inp("e","Email Address","email","email")}{inp("e2","Confirm Email","email","email")}</div>'
      f'<div class="fr">{sel("c","Select Course",[c[0] for c in COURSES])}{sel("l","Preferred Location",AREAS)}</div>'
      f'{sel("m","Preferred Contact Method",["Phone","WhatsApp","Email"])}'
      '<div class="fld"><label for="g">Message</label><textarea id="g" rows="4" placeholder="Tell us about your experience, preferred days or any questions"></textarea></div>'
      '<div class="hp" aria-hidden="true"><label for="web">Leave this field empty</label><input id="web" name="web" type="text" tabindex="-1" autocomplete="off"></div>'
      '<p id="st" role="status" class="fine"></p><button class="btn p wide" type="submit">Send My Enquiry</button></form>')
    nxt = ''.join(f'<div class="gl pe rv step">{PE}<span class="num">0{i+1}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate([
        ('Send your enquiry', 'Use the form, call, WhatsApp or email. Tell us your area and the course you are interested in.'),
        ('We get back to you', 'We reply using your preferred contact method and confirm availability and pricing.'),
        ('Book your first lesson', 'Your first two lessons (2 hours) are £60, so you can meet your instructor and get started.')]))
    return (head('Contact', 'Let’s Get You on the Road.', 'Call, WhatsApp, email or send an enquiry. We will get back to you.', 'contact')
      + f'<section class="w cg">{info_card}{form}</section>'
      + f'<section class="w">{sec_head("What happens next", "Three simple <span class=gr>steps</span>")}<div class="grid">{nxt}</div></section>')

BODIES = {'index': body_index, 'about-us': body_about, 'driving-courses': body_courses, 'driving-theory-test': body_theory,
          'success-stories': body_success, 'pricing': body_pricing, 'faqs': body_faqs, 'contact': body_contact}

# ----------------------------------------------------------------- SCHEMA
BIZ = {"@type": ["EducationalOrganization", "LocalBusiness"], "@id": BASE + "/#business", "name": "AZ Driving School", "alternateName": "AZ Driving",
 "description": "Manual and automatic driving lessons in Gloucester, Stroud, Tewkesbury and Cheltenham.", "url": BASE + "/", "telephone": PHONE_D, "email": EMAIL,
 "logo": {"@type": "ImageObject", "url": BASE + "/assets/icon-512.png", "width": 512, "height": 512}, "image": BASE + "/assets/og-image.jpg", "hasMap": MAPS, "priceRange": "£40-£45 per hour",
 "address": {"@type": "PostalAddress", "streetAddress": "Diamond Jubilee Close", "addressLocality": "Gloucester", "postalCode": "GL1 4LR", "addressCountry": "GB"},
 "contactPoint": {"@type": "ContactPoint", "telephone": PHONE_D, "email": EMAIL, "contactType": "customer service"},
 "areaServed": [{"@type": "City", "name": a} for a in AREAS],
 "availableLanguage": "English", "currenciesAccepted": "GBP", "slogan": "Learn to Drive. Drive with Confidence.", "knowsAbout": ["Driving lessons", "Manual driving lessons", "Automatic driving lessons", "Pass Plus", "Motorway driving", "Driving theory test"]}

def ld(k, t, d):
    g = [BIZ]
    if k == 'index':
        g.append({"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/", "name": "AZ Driving School", "publisher": {"@id": BASE + "/#business"}, "inLanguage": "en-GB"})
    ty = {'about-us': 'AboutPage', 'contact': 'ContactPage', 'faqs': 'FAQPage'}.get(k, 'WebPage')
    pg = {"@type": ty, "@id": U(k) + "#page", "url": U(k), "name": t, "description": d, "inLanguage": "en-GB", "dateModified": TODAY, "isPartOf": {"@id": BASE + "/#website"}, "about": {"@id": BASE + "/#business"}, "publisher": {"@id": BASE + "/#business"}}
    if k != 'index': pg["breadcrumb"] = {"@id": U(k) + "#breadcrumb"}
    if k in PAGE_IMAGES: pg["primaryImageOfPage"] = {"@type": "ImageObject", "url": BASE + PAGE_IMAGES[k][0]}
    if k == 'faqs':
        pg["mainEntity"] = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for _, qs in FAQ for q, a in qs]
    g.append(pg)
    if k != 'index':
        g.append({"@type": "BreadcrumbList", "@id": U(k) + "#breadcrumb", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"}, {"@type": "ListItem", "position": 2, "name": NAMES[k], "item": U(k)}]})
    if k == 'pricing':
        for key, (area, std, items) in PRICES.items():
            g.append({"@type": "Service", "name": "Driving lessons – " + area, "serviceType": "Driving lessons", "provider": {"@id": BASE + "/#business"},
              "areaServed": [{"@type": "City", "name": a.strip()} for a in area.replace(' & ', ', ').split(',')],
              "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Driving lesson prices – " + area,
                "itemListElement": [{"@type": "Offer", "name": n, "price": str(p), "priceCurrency": "GBP", "description": h, "url": U('pricing'), "availability": "https://schema.org/InStock", "priceValidUntil": "2027-12-31", "seller": {"@id": BASE + "/#business"}, "itemOffered": {"@type": "Service", "name": n, "serviceType": "Driving lessons", "provider": {"@id": BASE + "/#business"}}} for n, p, h in items]}})
    if k == 'driving-courses':
        g.append({"@type": "ItemList", "name": "AZ Driving School courses", "itemListElement": [
          {"@type": "ListItem", "position": i + 1, "item": {"@type": "Service", "name": n, "description": dsc, "serviceType": "Driving lessons", "provider": {"@id": BASE + "/#business"}, "url": U('driving-courses') + '#' + slug(n)}}
          for i, (n, dsc, _) in enumerate(COURSES)]})
    return json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

# ----------------------------------------------------------------- LAYOUT
def page(k, t, d, body, robots='index,follow,max-image-preview:large,max-snippet:-1', canon=True, schema=''):
    t, d = esc(t), esc(d)
    nv = ''.join(f'<a href="{L(u)}"{" class=on aria-current=page" if u == k else ""}>{n}</a>' for u, n in [('index', 'Home')] + NAV)
    nv += f'<div class="mc"><a class="btn" href="tel:{PHONE_D}">Call</a><a class="btn p" href="/contact/">Book Your Lesson</a></div>'
    ft = ''.join(f'<a href="{L(u)}">{n}</a>' for u, n in [('index', 'Home')] + NAV)
    og = (f'<meta property="og:type" content="website"><meta property="og:site_name" content="AZ Driving School"><meta property="og:locale" content="en_GB">'
          f'<meta property="og:title" content="{t}"><meta property="og:description" content="{d}"><meta property="og:url" content="{U(k)}">'
          f'<meta property="og:image" content="{BASE}/assets/og-image.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
          f'<meta property="og:image:alt" content="AZ Driving School logo"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{t}">'
          f'<meta name="twitter:description" content="{d}"><meta name="twitter:image" content="{BASE}/assets/og-image.jpg">') if canon else ''
    cn = f'<link rel="canonical" href="{U(k)}"><link rel="alternate" hreflang="en-GB" href="{U(k)}"><link rel="alternate" hreflang="x-default" href="{U(k)}">' if canon else ''
    sc = f'<script type="application/ld+json">{schema}</script>' if schema else ''
    pre = '<link rel="preload" as="image" href="/assets/logo-poster.webp" fetchpriority="high">' if k == 'index' else ''
    areas = ''.join(f'<a href="/pricing/#{"gl" if a == "Gloucester" else "st"}">{a}</a>' for a in AREAS)
    wa_widget = ('<div class="wa" id="wa"><div class="wp" id="wp" role="dialog" aria-label="Chat with AZ Driving School on WhatsApp" hidden>'
      '<div class="wh"><img src="/assets/favicon.png" alt="" width="44" height="44" loading="lazy"><div><b>AZ Driving School</b><small>Chat on WhatsApp</small></div>'
      '<button class="wx" id="wx" aria-label="Close chat panel" type="button">×</button></div>'
      '<div class="wbd"><p class="wm">Hello! 👋 How can we help you with your driving lessons?</p><p class="wl">Choose a question to start:</p>'
      + ''.join(f'<a class="wq" href="{WA}?text={quote(m)}" target="_blank" rel="noopener">{q}<span aria-hidden="true">→</span></a>' for q, m in FOOT_Q) +
      f'<a class="wgo" href="{WA}?text={quote("Hi AZ Driving School, I would like to ask about driving lessons.")}" target="_blank" rel="noopener">{WA_ICON}<span>Start chat on WhatsApp</span></a></div></div>'
      '<button class="wf" id="wf" type="button" aria-expanded="false" aria-controls="wp" aria-label="Chat with us on WhatsApp">' + WA_ICON + '<span class="wt">Chat with us</span></button></div>')
    return f'''<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><script>document.documentElement.className="js";try{{if(!sessionStorage.getItem("azi")&&!matchMedia("(prefers-reduced-motion:reduce)").matches&&!/bot|crawl|spider|lighthouse/i.test(navigator.userAgent))document.documentElement.className+=" intro"}}catch(e){{}}</script>
<title>{t}</title><meta name="description" content="{d}"><meta name="robots" content="{robots}">{cn}<meta name="theme-color" content="#0b1f4d"><meta name="author" content="AZ Driving School"><meta name="geo.region" content="GB-GLS"><meta name="geo.placename" content="Gloucester"><link rel="manifest" href="/site.webmanifest"><link rel="sitemap" type="application/xml" title="Sitemap" href="/sitemap.xml"><meta name="format-detection" content="telephone=no"><meta name="googlebot" content="index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1"><meta name="bingbot" content="index,follow,max-snippet:-1,max-image-preview:large"><meta name="color-scheme" content="light"><meta name="application-name" content="AZ Driving School"><meta name="apple-mobile-web-app-title" content="AZ Driving"><meta name="msapplication-TileColor" content="#0b1f4d"><link rel="alternate" type="text/plain" title="LLMs" href="/llms.txt">{og}
<link rel="icon" href="/favicon.ico?v={V}" sizes="48x48"><link rel="icon" type="image/png" sizes="32x32" href="/assets/icon-32.png?v={V}"><link rel="icon" type="image/png" sizes="96x96" href="/assets/icon-96.png?v={V}"><link rel="icon" type="image/png" sizes="192x192" href="/assets/icon-192.png?v={V}"><link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png?v={V}">{pre}<link rel="stylesheet" href="/style.css?v={V}">
<!-- Google Search Console: add google-site-verification meta tag here --><!-- Bing Webmaster: add msvalidate.01 meta tag here --><!-- Google Analytics 4: add your gtag snippet (G-XXXXXXXXXX) here -->{sc}</head>
<body><div id="intro"><div class="ib" aria-hidden="true"><video id="iv" muted playsinline preload="auto" poster="/assets/logo-poster.webp" width="720" height="428"></video><i class="ibar"></i></div><button class="is" type="button">Skip</button></div><script>if(document.documentElement.classList.contains("intro")){{var iv=document.getElementById("iv");iv.muted=true;iv.src="/assets/logo-animated.mp4";var ip=iv.play();if(ip&&ip.catch)ip.catch(function(){{}})}}</script><svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><filter id="lg" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB"><feTurbulence type="fractalNoise" baseFrequency=".012 .02" numOctaves="2" seed="7" result="n"/><feGaussianBlur in="n" stdDeviation="1.2" result="nb"/><feDisplacementMap in="SourceGraphic" in2="nb" scale="14" xChannelSelector="R" yChannelSelector="G"/></filter></svg><a class="skip" href="#main">Skip to content</a><div class="aurora" aria-hidden="true"><i></i><i></i><i></i></div><canvas id="sp" aria-hidden="true"></canvas><div id="pb" aria-hidden="true"></div>
<header class="top"><nav id="nav" aria-label="Main"><a class="lg" href="/" aria-label="AZ Driving School home"><img src="/assets/logo.webp" alt="AZ Driving School" width="67" height="34"></a><div class="ln" id="ln">{nv}</div><a class="btn p nb" href="/contact/">Book Your Lesson</a><button class="bg" id="bg" aria-label="Menu" aria-expanded="false" aria-controls="ln"><span></span><span></span></button></nav></header>
<main id="main">{body}</main>
<footer><div class="w fg"><div><img class="fl" src="/assets/logo.webp" alt="" width="120" height="61" loading="lazy"><p>Friendly, professional driving lessons in Gloucester, Stroud, Tewkesbury and Cheltenham. Manual and automatic, beginner to refresher.</p><div class="fcta"><a class="btn p fb1" href="/contact/">Book Your First Lesson</a><a class="btn fb2" href="tel:{PHONE_D}">Call us</a></div></div>
<div><h3>Quick links</h3><div class="fqk">{ft}</div></div><div><h3>Areas</h3>{areas}<a class="fpr" href="/pricing/">Lesson prices →</a></div>
<div><h3>Contact</h3><a class="fc" href="tel:{PHONE_D}">{ico("phone")}<span>{PHONE}</span></a><a class="fc" href="{WA}" target="_blank" rel="noopener">{ico("wa")}<span>WhatsApp</span></a><a class="fc" href="mailto:{EMAIL}">{ico("mail")}<span>{EMAIL}</span></a><a class="fc" href="{MAPS}" target="_blank" rel="noopener">{ico("pin")}<span>{ADDR}</span></a></div></div>
<div class="w fb"><span>© 2026 AZ Driving School. All rights reserved.</span><span class="fr"><a class="sm" href="/sitemap/">Sitemap</a><a class="pw" href="https://www.aureviasolution.art/" target="_blank" rel="noopener">Powered by <b>AureviaSolution</b><span aria-hidden="true">↗</span></a><a class="tp" href="#main" aria-label="Back to top">↑</a></span></div></footer>
{wa_widget}
<div class="dock" aria-label="Quick contact"><a href="tel:{PHONE_D}">Call</a><a class="bk" href="/contact/">Book Your Lesson</a></div>
<script src="/app.js?v={V}" defer></script></body></html>'''

def write(path, s):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    open(path, 'w', encoding='utf-8').write(s)

# ----------------------------------------------------------------- BUILD
for old in glob.glob('*.html'): os.remove(old)
for k, (t, d) in PAGES.items():
    b = BODIES[k]()
    if k in RELATED:
        b += ('<section class="w rv"><div class="rel"><b>Related:</b> ' + ''.join(f'<a href="{L(x)}">{lbl}</a>' for x, lbl in RELATED[k]) + '</div>'
              + (f'<p class="fine">Page last updated: {TODAY_H}.</p>' if k in UPDATED else '') + '</section>')
    write('index.html' if k == 'index' else f'{k}/index.html', page(k, t, d, b, schema=ld(k, t, d)))
write('404.html', page('404', 'Page not found | AZ Driving School', 'Sorry, we could not find that page.',
  '<section class="w" style="padding:110px 20px;text-align:center"><div class="gl cta"><h1>404</h1><p>Sorry, we could not find that page.</p><div class="row c"><a class="btn p" href="/">Back to home</a><a class="btn" href="/contact/">Contact us</a></div></div></section>',
  robots='noindex,follow', canon=False))

def sm_img(k):
    return ''.join(f'<image:image><image:loc>{BASE}{u}</image:loc></image:image>' for u in PAGE_IMAGES.get(k, []))
NAMES['sitemap'] = 'Sitemap'
SM_T, SM_D = 'Sitemap | AZ Driving School Gloucester', 'Every page on the AZ Driving School website: courses, prices, theory test help, FAQs and contact details for Gloucester, Stroud, Tewkesbury and Cheltenham.'
sm_body = ('<section class="w"><div class="gl"><span class="eyebrow">Sitemap</span><h1>Site<span class="gr">map</span></h1><p class="lead">Every page on our website in one place.</p><ul class="al smp">'
  + ''.join(f'<li><a href="{L(k)}"><b>{NAMES[k]}</b></a> <span class="fine">- {PAGES[k][1]}</span></li>' for k in PAGES) + '</ul></div></section>')
write('sitemap/index.html', page('sitemap', SM_T, SM_D, sm_body, schema=ld('sitemap', SM_T, SM_D)))
ALL = list(PAGES) + ['sitemap']
def sm_alt(k): return f'<xhtml:link rel="alternate" hreflang="en-GB" href="{U(k)}"/><xhtml:link rel="alternate" hreflang="x-default" href="{U(k)}"/>'
def pri(k): return "1.0" if k == "index" else ("0.9" if k in ("driving-courses", "pricing", "contact") else ("0.3" if k == "sitemap" else "0.7"))
write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?><?xml-stylesheet type="text/xsl" href="/sitemap.xsl"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" xmlns:xhtml="http://www.w3.org/1999/xhtml">'
  + ''.join(f'<url><loc>{U(k)}</loc>{sm_alt(k)}<lastmod>{TODAY}</lastmod><changefreq>{"weekly" if k in ("index","pricing") else "monthly"}</changefreq><priority>{pri(k)}</priority>{sm_img(k)}</url>' for k in ALL) + '</urlset>')
write('sitemap.xsl', '<?xml version="1.0" encoding="UTF-8"?><xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:s="http://www.sitemaps.org/schemas/sitemap/0.9"><xsl:output method="html" encoding="UTF-8"/><xsl:template match="/"><html lang="en-GB"><head><meta charset="utf-8"/><meta name="robots" content="noindex"/><title>XML Sitemap | AZ Driving School</title><style>body{font:16px/1.6 -apple-system,Segoe UI,Arial,sans-serif;background:#f5f3ec;color:#0a1a40;margin:0;padding:32px}main{max-width:860px;margin:auto;background:#fff;border-radius:20px;padding:28px;box-shadow:0 20px 50px -20px rgba(11,31,77,.3)}h1{color:#0b1f4d;margin-top:0}a{color:#1f4fb5}li{padding:6px 0;border-bottom:1px solid #eee}small{color:#667}</style></head><body><main><h1>AZ Driving School - XML Sitemap</h1><p>This sitemap helps search engines find every page.</p><ul><xsl:for-each select="s:urlset/s:url"><li><a href="{s:loc}"><xsl:value-of select="s:loc"/></a> <small>updated <xsl:value-of select="s:lastmod"/></small></li></xsl:for-each></ul></main></body></html></xsl:template></xsl:stylesheet>')
write('robots.txt', f"""# AZ Driving School
User-agent: *
Allow: /
Disallow: /404.html

# AI / answer-engine crawlers are welcome to read the public pages
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /

Sitemap: {BASE}/sitemap.xml
""")
write('site.webmanifest', json.dumps({"name": "AZ Driving School", "short_name": "AZ Driving", "description": "Manual and automatic driving lessons in Gloucester, Stroud, Tewkesbury and Cheltenham.", "start_url": "/", "scope": "/", "display": "browser", "lang": "en-GB", "background_color": "#f5f3ec", "theme_color": "#0b1f4d", "icons": [{"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"}, {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"}, {"src": "/assets/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}, indent=1))
write('llms.txt', f"""# AZ Driving School
> Friendly, professional manual and automatic driving lessons in Gloucester, Stroud, Tewkesbury and Cheltenham (UK). Beginner, intensive, refresher, motorway, Pass Plus and eco driving courses. First two lessons (2 hours) £60.

Contact: {PHONE} (call or WhatsApp) | {EMAIL} | {ADDR}

## Pages
""" + ''.join(f'- [{NAMES[k]}]({U(k)}): {PAGES[k][1]}\n' for k in PAGES) + f"""
## Sitemap
- [XML sitemap]({BASE}/sitemap.xml)
- [HTML sitemap]({BASE}/sitemap/)
""")
write('.well-known/security.txt', f'Contact: mailto:{EMAIL}\nExpires: 2027-11-09T00:00:00.000Z\nPreferred-Languages: en\nCanonical: {BASE}/.well-known/security.txt\n')
IKEY = 'a7c3e91d5b2f48e6a0d4c8f1b3e57290'
write(IKEY + '.txt', IKEY)
write('humans.txt', '/* TEAM */\nSchool: AZ Driving School, Gloucester, UK\nContact: ' + EMAIL + '\n\n/* SITE */\nLanguage: English (UK)\nBuilt as a fast static site with clean URLs.\n')
write('_redirects', '\n'.join([f'/{k}.html /{k}/ 301' for k in PAGES if k != 'index'] + ['/index.html / 301', '/home / 301', '/home/ / 301']) + '\n')
write('_headers', '/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n  Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()\n  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload\n  Cross-Origin-Opener-Policy: same-origin-allow-popups\n  Cache-Control: public, max-age=0, must-revalidate\n/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n/style.css\n  Cache-Control: public, max-age=31536000, immutable\n/app.js\n  Cache-Control: public, max-age=31536000, immutable\n/sitemap.xml\n  Content-Type: application/xml; charset=utf-8\n  Cache-Control: public, max-age=3600\n/robots.txt\n  Cache-Control: public, max-age=3600\n/llms.txt\n  Content-Type: text/plain; charset=utf-8\n/site.webmanifest\n  Content-Type: application/manifest+json\n')
# ---- Vercel ----
_sec = [{"key": "X-Content-Type-Options", "value": "nosniff"}, {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"}, {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
        {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=(), interest-cohort=()"}, {"key": "Strict-Transport-Security", "value": "max-age=31536000; includeSubDomains; preload"},
        {"key": "Cross-Origin-Opener-Policy", "value": "same-origin-allow-popups"}]
_imm = [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]
_vc = {"$schema": "https://openapi.vercel.sh/vercel.json", "cleanUrls": True, "trailingSlash": True,
  "rewrites": [{"source": "/api/contact/", "destination": "/api/contact"}],
  "redirects": [{"source": f"/{k}.html", "destination": f"/{k}/", "permanent": True} for k in PAGES if k != 'index']
    + [{"source": "/index.html", "destination": "/", "permanent": True}, {"source": "/home", "destination": "/", "permanent": True}, {"source": "/home/", "destination": "/", "permanent": True}],
  "headers": [{"source": "/(.*)", "headers": _sec},
    {"source": "/assets/(.*)", "headers": _imm}, {"source": "/style.css", "headers": _imm}, {"source": "/app.js", "headers": _imm},
    {"source": "/sitemap.xml", "headers": [{"key": "Content-Type", "value": "application/xml; charset=utf-8"}, {"key": "Cache-Control", "value": "public, max-age=3600"}]},
    {"source": "/sitemap.xsl", "headers": [{"key": "Content-Type", "value": "application/xslt+xml; charset=utf-8"}]},
    {"source": "/favicon.ico", "headers": [{"key": "Cache-Control", "value": "public, max-age=86400"}]}, {"source": "/robots.txt", "headers": [{"key": "Cache-Control", "value": "public, max-age=3600"}]},
    {"source": "/llms.txt", "headers": [{"key": "Content-Type", "value": "text/plain; charset=utf-8"}]},
    {"source": "/site.webmanifest", "headers": [{"key": "Content-Type", "value": "application/manifest+json; charset=utf-8"}]}]}
write('vercel.json', json.dumps(_vc, indent=2) + '\n')
write('.vercelignore', 'build.py\ndev-server.js\n.env.local\nREADME.txt\n_headers\n_redirects\n__pycache__\n*.zip\n.DS_Store\n')
write('.gitignore', '__pycache__/\n.DS_Store\n.vercel\n.env.local\n')
print('built', len(PAGES) + 2, 'pages')
