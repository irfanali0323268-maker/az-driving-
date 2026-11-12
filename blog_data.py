# -*- coding: utf-8 -*-
"""Blog content for AZ Driving School. Edit here, then run: python3 build.py
Each post: slug, title (h1), seo (title tag), desc (meta description), img, date, mins, excerpt, tag, body (HTML), related (slugs).
Facts are taken from GOV.UK / DVSA guidance and the school's own price list. Fees can change, so posts point readers to GOV.UK."""

DATE = '2026-11-12'

POSTS = [
 dict(
  slug='how-many-driving-lessons-do-you-need',
  title='How Many Driving Lessons Do You Need to Pass?',
  seo='How Many Driving Lessons Do You Need? | AZ Driving School',
  desc='How many driving lessons will you need to pass your test? What the DVSA average means, what changes it, and how to plan your lessons in Gloucester.',
  img='/assets/courses/course-4.webp', tag='Learning to drive', mins=5,
  excerpt='The honest answer to the question every learner asks, and what actually changes the number.',
  related=['cost-of-learning-to-drive', 'nervous-learner-driver-tips', 'driving-test-day-what-to-expect'],
  body='''<p>It is the first question almost every new learner asks, and the honest answer is: it depends. Nobody can promise an exact number before you have sat behind the wheel, but there are useful guidelines and a few things that genuinely change how many lessons you will need.</p>
<h2>What the DVSA says</h2>
<p>The DVSA, the government agency that runs the driving test, has said that learners need around 45 hours of lessons with a professional instructor, plus about 22 hours of practice with family or friends. That is an average across many learners. Some pass with far fewer hours, and others need more. Treat it as a planning figure, not a target.</p>
<h2>What changes the number of lessons</h2>
<ul>
<li><b>Your starting point.</b> A complete beginner has more to learn than someone who has driven abroad or is returning after a break. If you have driven before, a <a href="/driving-courses/">refresher course</a> may be a better fit.</li>
<li><b>How often you have lessons.</b> One lesson a week works well for many people, but long gaps mean you spend the start of each lesson remembering what you did last time. Two shorter lessons a week can build skills faster.</li>
<li><b>Private practice.</b> Extra practice between lessons, in a car you are insured to drive, makes a big difference. Ask your instructor what to practise next.</li>
<li><b>Confidence.</b> Nerves are normal. Calm, steady progress beats rushing. Our guide on <a href="/blog/nervous-learner-driver-tips/">feeling calmer behind the wheel</a> may help.</li>
<li><b>Where you drive.</b> Busy junctions, roundabouts and dual carriageways take practice. Learning in the area where you will take your test helps.</li>
<li><b>Manual or automatic.</b> Many learners find automatics easier at first because there is no clutch to master. See <a href="/blog/manual-or-automatic-driving-lessons/">manual or automatic: which should you choose?</a></li>
</ul>
<h2>How do you know you are ready for the test?</h2>
<p>Your instructor will tell you honestly. Signs you are close include driving without prompts from your instructor, handling unfamiliar roads calmly, making good decisions at junctions and roundabouts, and carrying out your reversing manoeuvres smoothly. If you are making the same mistakes every lesson, a little more practice is better than booking a test too early.</p>
<h2>Plan, but stay flexible</h2>
<p>A good way to plan is to book a first block, check your progress with your instructor after a few lessons, then decide the next steps together. Our <a href="/pricing/">block bookings</a> can save money compared with paying lesson by lesson, and you can book your <a href="/driving-theory-test/">theory test</a> early so it is out of the way.</p>
<p>Not sure where to start? <a href="/contact/">Send us an enquiry</a> and we will recommend a sensible plan for your situation.</p>'''),

 dict(
  slug='manual-or-automatic-driving-lessons',
  title='Manual or Automatic Driving Lessons: Which Should You Choose?',
  seo='Manual or Automatic Driving Lessons? Which to Choose | AZ Driving School',
  desc='Manual or automatic driving lessons? Compare the licence you earn, learning curve, cost and who each suits, then choose with confidence in Gloucester.',
  img='/assets/courses/course-2.webp', tag='Choosing lessons', mins=5,
  excerpt='A plain comparison of manual and automatic lessons, and the licence rules that matter.',
  related=['how-many-driving-lessons-do-you-need', 'cost-of-learning-to-drive', 'motorway-lessons-and-pass-plus'],
  body='''<p>One of the first decisions you will make is whether to learn in a manual or an automatic car. Both are good routes to a full licence. The difference is mainly about the licence you end up with and how you want to drive in future.</p>
<h2>The licence rule that matters</h2>
<p>If you pass your test in a <b>manual</b> car, you get a full licence that lets you drive both manual and automatic cars. If you pass in an <b>automatic</b> car, your licence is for automatic cars only. You can take a manual test later to remove that restriction.</p>
<h2>Manual lessons</h2>
<p>You will learn to use a clutch and gears as well as steering, braking and observation. That is more to coordinate at first, but it gives you the most flexibility afterwards, including borrowing or buying any type of car and often a wider choice of used cars.</p>
<ul>
<li>Best if you want the widest choice of cars and the most flexible licence.</li>
<li>Often takes more lessons for the first few weeks while you learn clutch control.</li>
</ul>
<h2>Automatic lessons</h2>
<p>With no clutch or gears to change, you can focus on road positioning, hazards and junctions from the start. Many nervous learners find this less stressful. Electric and hybrid cars are automatic, and automatics are increasingly common.</p>
<ul>
<li>Best if you want to concentrate on road skills, or you expect to drive automatic or electric cars.</li>
<li>Your licence will be limited to automatic cars unless you later pass a manual test.</li>
</ul>
<h2>Which is quicker or cheaper?</h2>
<p>Learners often find automatics easier to pick up, which can reduce the number of lessons, but everyone is different and we do not promise a set number. Lesson prices may differ by course and area, so check our <a href="/pricing/">pricing page</a>.</p>
<h2>How to decide</h2>
<ol>
<li>Think about the car you expect to drive after you pass.</li>
<li>Consider how confident you feel. If you are very nervous, an automatic can be a calmer start.</li>
<li>Ask about trying a lesson in each. Our <a href="/driving-courses/">manual and automatic courses</a> both suit complete beginners.</li>
</ol>
<p>Still unsure? <a href="/contact/">Contact us</a> and we will talk it through with no pressure. See also <a href="/faqs/">our FAQs</a>.</p>'''),

 dict(
  slug='driving-test-day-what-to-expect',
  title='Practical Driving Test: What to Expect on the Day',
  seo='Practical Driving Test: What to Expect on the Day | AZ Driving School',
  desc='What happens in the UK practical driving test: eyesight check, show me tell me, independent driving, manoeuvres, faults and what to bring on test day.',
  img='/assets/courses/course-5.webp', tag='Test day', mins=6,
  excerpt='From the eyesight check to the result, a clear walk-through of the car driving test.',
  related=['theory-test-tips', 'how-many-driving-lessons-do-you-need', 'nervous-learner-driver-tips'],
  body='''<p>Knowing what will happen on test day takes away a lot of the fear. Here is a plain guide to the UK car practical test, based on GOV.UK guidance. Always check the latest details on GOV.UK before your test.</p>
<h2>Before you set off</h2>
<p>Bring your photocard driving licence. The examiner will check your details and ask you to read a number plate from a distance of 20 metres (for a new-style plate). If you cannot read it, you will not be able to take the test.</p>
<h2>Show me, tell me</h2>
<p>You will be asked two vehicle safety questions. For the &ldquo;tell me&rdquo; question you explain how you would check something, such as the tyres or the brake lights. For the &ldquo;show me&rdquo; question you demonstrate it, usually while driving, for example how to clear the windscreen. A wrong answer is one minor fault, not an automatic fail, but your instructor can help you learn the answers well.</p>
<h2>The driving</h2>
<p>The test usually lasts about 40 minutes and includes general driving on a mix of roads. Expect:</p>
<ul>
<li><b>Independent driving</b> for around 20 minutes, where you follow directions from a sat nav or traffic signs.</li>
<li><b>One reversing manoeuvre</b>, such as parallel parking at the roadside, parking in a bay, or pulling up on the right and reversing for two car lengths.</li>
<li><b>An emergency stop</b>, which is asked on some tests.</li>
</ul>
<p>You are allowed to ask the examiner to repeat or clarify an instruction. Take your time, and do not worry if you make a small mistake; carry on calmly.</p>
<h2>How the test is marked</h2>
<p>You can make up to 15 driving faults (minors) and still pass. You will fail if you make 16 or more, or if you make a serious or dangerous fault. Examiners are looking for safe, confident driving, not perfection.</p>
<h2>How to prepare</h2>
<ul>
<li>Practise the roads and junction types used around your test centre with your instructor.</li>
<li>Do a mock test so the format feels familiar.</li>
<li>Get a good night&rsquo;s sleep and arrive early.</li>
<li>Have a warm-up lesson before the test if you can.</li>
</ul>
<p>If nerves are the main worry, read our tips on <a href="/blog/nervous-learner-driver-tips/">feeling calmer behind the wheel</a>. Ready to book lessons? See our <a href="/driving-courses/">courses</a> or <a href="/contact/">get in touch</a>.</p>'''),

 dict(
  slug='theory-test-tips',
  title='Theory Test Tips: How to Pass First Time',
  seo='Theory Test Tips: How to Pass First Time | AZ Driving School',
  desc='Practical UK car theory test tips: format, pass marks, hazard perception, how to revise, and why you should only book through GOV.UK.',
  img='/assets/courses/course-6.webp', tag='Theory test', mins=5,
  excerpt='The format, the pass marks and a revision plan that works, plus the booking trap to avoid.',
  related=['driving-test-day-what-to-expect', 'provisional-licence-guide', 'how-many-driving-lessons-do-you-need'],
  body='''<p>The theory test is the first big hurdle on the way to your licence, and it is very passable with a bit of steady preparation. Here is what it involves and how to get ready.</p>
<h2>The format</h2>
<p>The car theory test has two parts, taken in one sitting:</p>
<ul>
<li><b>Multiple choice:</b> 50 questions in 57 minutes. You need 43 out of 50 to pass. It includes a short case study with five questions.</li>
<li><b>Hazard perception:</b> 14 video clips with a pass mark of 44 out of 75.</li>
</ul>
<p>You must pass both parts in the same sitting. Your pass is valid for two years, so you need to pass your practical test within that time.</p>
<h2>Tips that work</h2>
<ol>
<li><b>Read the Highway Code.</b> It is free on GOV.UK and the questions are based on it. Little and often beats a last-minute cram.</li>
<li><b>Practise daily.</b> Ten or fifteen minutes a day helps answers stick. Try our free <a href="/driving-theory-test/">practice quiz</a> and use the official practice resources on GOV.UK.</li>
<li><b>Learn the road signs by shape and colour.</b> Triangles warn, circles give orders, rectangles inform.</li>
<li><b>Read each question twice.</b> Many marks are lost to rushing, and some questions ask what you should <em>not</em> do.</li>
<li><b>Use your lessons.</b> Noticing real hazards from the passenger seat or behind the wheel helps with hazard perception.</li>
<li><b>Practise the hazard clips.</b> You score for spotting a developing hazard early, so click when you see it start to develop. Do not click constantly, as that can score zero for the clip.</li>
<li><b>Take a mock test.</b> Time yourself so the real thing feels familiar.</li>
</ol>
<h2>Booking: use GOV.UK only</h2>
<p>The theory test is booked on the official GOV.UK service. At the time of writing the fee is &pound;23. Some unofficial websites add extra charges for the same booking, so always start from <a href="https://www.gov.uk/book-theory-test" target="_blank" rel="noopener">the official GOV.UK page</a>. If you do not pass, you can rebook after a short wait, so do not be discouraged.</p>
<p>Once your theory test is behind you, you can focus on the road. Browse our <a href="/driving-courses/">driving courses</a> or <a href="/contact/">book your first lesson</a>. Need a provisional licence first? See our <a href="/blog/provisional-licence-guide/">provisional licence guide</a>.</p>'''),

 dict(
  slug='cost-of-learning-to-drive',
  title='How Much Does It Cost to Learn to Drive in Gloucester?',
  seo='Cost of Learning to Drive in Gloucester | AZ Driving School',
  desc='What learning to drive costs in Gloucester: lessons from £40 an hour, block discounts, provisional licence, theory and practical test fees explained.',
  img='/assets/courses/course-8.webp', tag='Costs', mins=5,
  excerpt='Lessons, block bookings and government fees, added up in plain English.',
  related=['how-many-driving-lessons-do-you-need', 'manual-or-automatic-driving-lessons', 'provisional-licence-guide'],
  body='''<p>Learning to drive is an investment, so it helps to know where the money goes. The total is made up of your lessons plus a small number of government fees. Here is how it adds up.</p>
<h2>1. Driving lessons</h2>
<p>Lessons are the biggest part of the cost, and the number you need varies from learner to learner (see <a href="/blog/how-many-driving-lessons-do-you-need/">how many lessons do you need?</a>). Our current prices are:</p>
<ul>
<li><b>Gloucester:</b> from &pound;40 an hour.</li>
<li><b>Stroud, Tewkesbury and Cheltenham:</b> from &pound;45 an hour.</li>
<li><b>First two lessons (2 hours):</b> &pound;60, so you can meet your instructor and get started.</li>
<li><b>Block bookings:</b> buying lessons in blocks of 5 or 10 costs less than paying one lesson at a time.</li>
</ul>
<p>Always check our <a href="/pricing/">pricing page</a> for the latest rates, including Pass Plus, motorway and refresher lessons.</p>
<h2>2. Government fees</h2>
<p>At the time of writing, GOV.UK lists these fees:</p>
<ul>
<li><b>Provisional licence:</b> &pound;34 online.</li>
<li><b>Theory test:</b> &pound;23.</li>
<li><b>Practical test:</b> &pound;62 on weekdays, &pound;75 evenings, weekends and bank holidays.</li>
</ul>
<p>That is &pound;119 for a weekday practical test if everything goes first time. Fees can change, so confirm them on GOV.UK. Re-taking a test means paying the fee again.</p>
<h2>3. Extras to budget for</h2>
<ul>
<li>Using your instructor&rsquo;s car for the test, if charged.</li>
<li>Private practice insurance, if you practise in a family car.</li>
<li>Theory revision materials, though many good resources are free.</li>
</ul>
<h2>A simple way to estimate</h2>
<p>Multiply your expected number of lessons by the hourly rate, then add the government fees. As an example only, 30 hours at &pound;40 is &pound;1,200, plus &pound;119 in fees. Your own number will depend on your progress, so treat it as a rough guide.</p>
<h2>Ways to keep costs down</h2>
<ul>
<li>Choose block bookings for a lower price per hour.</li>
<li>Practise privately between lessons if you can.</li>
<li>Pass your theory test early and revise properly to avoid paying twice.</li>
<li>Only book your practical test when your instructor says you are ready.</li>
</ul>
<p>Want a clear quote for your situation? <a href="/contact/">Contact us</a> and we will explain the options.</p>'''),

 dict(
  slug='nervous-learner-driver-tips',
  title='Nervous About Driving? 7 Ways to Feel Calmer Behind the Wheel',
  seo='Nervous Learner Driver? 7 Tips to Feel Calmer | AZ Driving School',
  desc='Feeling anxious about driving lessons or your test? Seven practical, supportive tips for nervous learner drivers, from pacing to breathing.',
  img='/assets/courses/course-1.webp', tag='Confidence', mins=4,
  excerpt='Feeling nervous is normal. These seven steps help you build confidence at your own pace.',
  related=['how-many-driving-lessons-do-you-need', 'manual-or-automatic-driving-lessons', 'driving-test-day-what-to-expect'],
  body='''<p>If the thought of driving makes your stomach flip, you are in good company. Many learners feel nervous, and many go on to become calm, confident drivers. These tips can help.</p>
<h2>1. Tell your instructor how you feel</h2>
<p>A good instructor adjusts the lesson to you. Say what worries you, whether it is junctions, roundabouts or other traffic, and agree a pace that feels manageable. You are always allowed to say &ldquo;I need a moment&rdquo;.</p>
<h2>2. Start in quiet places</h2>
<p>Quiet roads let you get used to the controls without pressure. Build up to busier roads step by step as your confidence grows.</p>
<h2>3. Consider an automatic</h2>
<p>With no clutch to manage, some nervous learners find an automatic car calmer to begin with. Read our comparison of <a href="/blog/manual-or-automatic-driving-lessons/">manual and automatic lessons</a>.</p>
<h2>4. Break skills into small steps</h2>
<p>Practise one thing at a time, such as moving off smoothly, then mirrors, then a roundabout. Small wins add up quickly.</p>
<h2>5. Slow your breathing</h2>
<p>Before you set off, take a few slow breaths in through the nose and out through the mouth. If you feel tense while driving, relax your grip on the wheel and drop your shoulders.</p>
<h2>6. Prepare, but do not over-rehearse</h2>
<p>Knowing the route type and what the test involves reduces fear of the unknown. Our guide to <a href="/blog/driving-test-day-what-to-expect/">what to expect on test day</a> explains each part. Get a good night&rsquo;s sleep and eat before lessons and tests.</p>
<h2>7. Be kind to yourself</h2>
<p>A stalled engine or a missed gear is part of learning, not a sign you cannot drive. Everyone makes mistakes, and every lesson builds experience.</p>
<p>If anxiety feels overwhelming or affects your daily life, it is worth speaking to your GP as well. When you are ready, <a href="/contact/">get in touch</a> and tell us what would help, or look at our <a href="/driving-courses/">beginner lessons</a>.</p>'''),

 dict(
  slug='provisional-licence-guide',
  title='How to Get Your Provisional Driving Licence',
  seo='How to Get a Provisional Driving Licence (UK) | AZ Driving School',
  desc='Step by step guide to applying for your first UK provisional driving licence: age rules, what you need, the fee and what to do next.',
  img='/assets/courses/course-3.webp', tag='Getting started', mins=4,
  excerpt='Age rules, what you need and how to apply, so you can book your first lesson.',
  related=['theory-test-tips', 'cost-of-learning-to-drive', 'how-many-driving-lessons-do-you-need'],
  body='''<p>Before you can drive on the road, you need a provisional driving licence. It is simple to get if you have the right details ready. This guide follows GOV.UK; always apply through the official site.</p>
<h2>When can you apply?</h2>
<p>You can apply for a provisional licence from 15 years and 9 months old. You can usually start driving a car on your 17th birthday. If you receive the enhanced rate of the mobility part of Personal Independence Payment (PIP), you can drive from 16.</p>
<h2>What you need</h2>
<ul>
<li>Proof of identity, such as a valid passport.</li>
<li>Your National Insurance number, if you know it.</li>
<li>Your addresses for the last three years.</li>
<li>A way to pay the fee. At the time of writing it is &pound;34 online.</li>
</ul>
<h2>How to apply</h2>
<ol>
<li>Go to the official GOV.UK page to apply for your first provisional driving licence.</li>
<li>Fill in your details and upload or confirm your identity.</li>
<li>Pay the fee and submit your application.</li>
<li>Wait for your photocard licence to arrive by post. Allow a couple of weeks and apply in good time.</li>
</ol>
<p>Be careful to use the official GOV.UK service. Unofficial sites may charge extra for the same application.</p>
<h2>Check your eyesight</h2>
<p>You must be able to read a number plate from 20 metres, with glasses or contact lenses if you wear them. You will also need to meet the legal medical requirements for driving, and you must tell the DVLA about any condition that could affect your driving.</p>
<h2>What to do next</h2>
<ol>
<li>Start your <a href="/driving-theory-test/">theory test</a> revision. You need your licence number to book it.</li>
<li>Book your <a href="/contact/">first lessons</a>. Our first two lessons (2 hours) are &pound;60, so you can meet your instructor.</li>
<li>Read our tips on <a href="/blog/theory-test-tips/">passing the theory test first time</a>.</li>
</ol>
<p>You must have your provisional licence with you whenever you drive as a learner. Questions? Check our <a href="/faqs/">FAQs</a> or <a href="/contact/">contact us</a>.</p>'''),

 dict(
  slug='motorway-lessons-and-pass-plus',
  title='Motorway Lessons and Pass Plus: Are They Worth It?',
  seo='Motorway Lessons & Pass Plus: Worth It? | AZ Driving School',
  desc='Motorway lessons and Pass Plus explained: who they suit, what you learn, and how they build confidence after you pass your driving test.',
  img='/assets/courses/course-7.webp', tag='After you pass', mins=5,
  excerpt='Why many new drivers add motorway practice or Pass Plus once they have their licence.',
  related=['nervous-learner-driver-tips', 'cost-of-learning-to-drive', 'manual-or-automatic-driving-lessons'],
  body='''<p>Passing your test is a big achievement, but it is only the start of real-world driving. Many new drivers feel unsure about motorways, night driving or bad weather. Two options can help: motorway lessons and Pass Plus.</p>
<h2>Motorway lessons</h2>
<p>Learner drivers in England, Scotland and Wales can have lessons on motorways, but only with an approved driving instructor in a car fitted with dual controls. Motorway driving is not part of the standard driving test, so many people pass without ever having driven on one.</p>
<p>A motorway lesson typically covers joining and leaving safely, lane discipline, overtaking, keeping a safe following distance, reading the signs and signals, and what to do if something goes wrong. It is also useful as a <a href="/driving-courses/">refresher</a> if you passed a while ago and have avoided motorways since.</p>
<h2>Pass Plus</h2>
<p>Pass Plus is a practical training course for newly qualified drivers, run by approved instructors. It covers six modules: town driving, all-weather driving, out-of-town driving, night driving, dual carriageways and motorways. It is not a test, but you are assessed through the modules and receive a certificate on completion.</p>
<h2>Is it worth it?</h2>
<ul>
<li><b>Confidence:</b> structured practice in situations you may not have met before.</li>
<li><b>Safety:</b> new drivers benefit from extra supervised experience in challenging conditions.</li>
<li><b>Insurance:</b> some insurers may offer a discount to drivers who hold a Pass Plus certificate, but this varies and is not guaranteed. Ask your insurer before deciding.</li>
</ul>
<p>It may not be necessary for everyone, but if you feel unsure about driving alone in certain conditions, the extra training can be good value.</p>
<h2>Prices at AZ Driving School</h2>
<p>We offer Pass Plus and motorway and refresher lessons. See the current prices on our <a href="/pricing/">pricing page</a>, and read more about <a href="/driving-courses/">our courses</a>.</p>
<p>Not sure which suits you? <a href="/contact/">Send us an enquiry</a> and we will recommend the best option. If nerves are the issue, see <a href="/blog/nervous-learner-driver-tips/">our tips for feeling calmer behind the wheel</a>.</p>'''),
]
