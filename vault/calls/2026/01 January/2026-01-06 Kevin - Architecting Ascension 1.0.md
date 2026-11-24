---
title: 2026-01-06 Kevin - Architecting Ascension 1.0
date: 2026-01-06
type: other
duration: 158
speakers: 4
---
### 0:00

Speaker 0: Hey, everyone. Welcome to this week's offer fundamentals call. This is the first offer fundamentals call of 2026,

Speaker 0: and I think it's gonna be a great call.

Speaker 0: We we had some questions from people open live launch about

Speaker 0: Ascension

Speaker 0: and, just strategies for that. And we've kinda touched on some of this across multiple calls

Speaker 0: in, as well as the ultimate offer course.

Speaker 0: And I'll have some stuff on

Speaker 0: the market criteria, which would attach some of the stuff he's covered in the market criteria or call would... We'll attach what we're gonna cover here in this call.

Speaker 0: But I I was kinda, like, looking through my notes today and saying, what will I do? And I was asking the guys on live launch, you know, what what would some of the stuff you'd be...

Speaker 0: You'd you'd want most help with was like, yeah. Some stuff on on Ascension would be would be helpful because we've done a lot of work on low ticket front ends. People are getting their act... Their... The front end offers working,

Speaker 0: but

Speaker 0: not as much energy has been ported to back ends yet because, obviously, like, that that first initial

Speaker 0: pipe of sales is is kinda most important. And so, you know, if the front end tends to get more attention initially, and then the back end kinda tends to get, you know, swept to the side until it's like, hey. I'm generating 20 sales a day, and look. It's happening. Right? Because, like, okay. Right. We gotta we gotta we gotta flip flip the energy over here. So that's gonna be kind of the the kind of whole theme of what we're gonna cover here on this call, which is, you know, how do we actually architect Ascension into our products,

Speaker 0: you know, from the... From, you know, as early on in the in the process as possible. So let me get my doc here for everyone.

Speaker 0: And I've

Speaker 0: prepared

Speaker 0: some notes,

Speaker 0: and we're gonna go through those. We're gonna kinda, like, free bullet here for a bit at the start

Speaker 0: to kind of get our foundational thinking going. Sorry. Let me get this doc link.

Speaker 0: Okay.

Speaker 0: So let's drop this in chess.

Speaker 0: Here is the doc for everyone.

Speaker 0: And

Speaker 0: let me share my screen as well.

Speaker 0: So

Speaker 0: can you see this? I believe you can.

Speaker 0: Yeah. So before we kinda, like, dive in... Into into our notes, suppose just some kinda, like, relevant stuff that we've kinda, like, touched on here. And this was one of the strategies I'd shared,

Speaker 0: with, Jen Springer back in

Speaker 0: early in 2025,

Speaker 0: what I call the concierge close. This is a really good post that's just, like, good tangential reading to this.

Speaker 0: This one requires a lot more energy as such to implement as a strategy. But if you have... You know, if you're a self starter and,

Speaker 0: you know, you're running on low volumes and you have, like, energy to give, this is a really great strategy for

Speaker 0: architecting, Ascension.

Speaker 0: Ascension... And, essentially, the

Speaker 0: essentially, the the kind of payoff of this is...

Speaker 0: It's not it's not a scalable strategy as such,

Speaker 0: but if you wanna get to know your audience better and and build rapport with quicker and then learn the things that they're getting the most value out of your product for or where you can improve the product. This is a massive, you know, shortcut... Way of shortcutting that. So this...

Speaker 0: Well,

Speaker 0: not gonna be the foundation of this call. This is definitely a post worth reading and a strategy worth implementing, especially if you're early on in the cycle for product refinement. Right? Because, like, a lot of us, you know,

Speaker 0: a lot of what leads to Ascension is consumption. Right?

Speaker 0: And so, you know, we have, you know, siloed consumption.

Speaker 0: We did a dev... Whole call on this as well,

Speaker 0: where, you know, we'll have pre purchase

Speaker 0: pre purchase

Speaker 0: consumption,

Speaker 0: and then, you know, post post purchase

Speaker 0: consumption. And we'll talk about this as as well on the call.

Speaker 0: And

Speaker 0: so, you know,

Speaker 0: the pre purchase consumption, I suppose, you can think of in kind of simple terms as ads, landing page, checkers,

Speaker 0: maybe upsell path as well.

Speaker 0: And then, you know, after after that, I suppose you could also add in kind of... This would be stuff that would be... Okay. Let's just add this here.

Speaker 0: Bullets.

Speaker 0: The other stuff you could add here was, like, you know, comments on ads on ads, you know, customer reviews

Speaker 0: reviews,

Speaker 0: testimonials,

Speaker 0: this type of stuff. Some of this will be, you know, I'm thinking more trust pilot.

Speaker 0: This wouldn't necessarily be on on page always. Right?

Speaker 0: You know, Better Business Bureau reviews, this type of stuff.

Speaker 0: These these types of things are more...

Speaker 0: They're not kinda, like, architected as part of your sales process, but they're kind of, like, tangential things that will happen through kinda, like, searching or interacting, you know, typically on Google

Speaker 0: or for for your product. Right? And so these will help... These will inject

Speaker 0: inject perception

Speaker 0: into your product,

Speaker 0: b is, you know, positive

Speaker 0: or negative

Speaker 0: in a typical

Speaker 0: typical offer,

Speaker 0: you know, for a new new new offer, what you'll find is,

Speaker 0: you know, the... That you'll have minimum... It really be mainly com... Comments in the ads will be, like, you know, the...

Speaker 0: As you're scaling,

Speaker 0: feedback will start here.

Speaker 0: And then, you know, these

Speaker 0: filter in over time

Speaker 0: Time as well. And they kind of...

Speaker 0: Yeah. These are all filtering over time. So just take this.

Speaker 0: Right. And so some of these will be... Could could inject positive or negative perception. Right?

Speaker 0: And so you could think of this kind of almost as a normal distribution curve of, you know, you'll have no... None of this.

Speaker 0: And then

Speaker 1: we have to fix this afterwards. But let's take this image.

Speaker 0: Open in.

Speaker 0: That one except the full screen shows.

Speaker 0: So you'll have a a normal distribution curve, you know, of...

Speaker 0: Obviously, this is the stuff we're in complete control of, right,

Speaker 0: here.

Speaker 0: We're gonna talk about this more on some some time, dental thoughts here first. But then this this stuff will filter in over time. Right? And it's like you'll have no comment... Minimal comments will start early, and then, you know, customer reviews, testimonials, you know, better business review reviews, these will start filtering in over time based on, you know,

Speaker 0: the the amount of people who are inter... Interacting with your off... Offer and whether they have a,

Speaker 0: you know, positive or negative impact will be largely based on the...

Speaker 0: Largely based on happens in the post purchase consumption,

Speaker 0: which is the actual product quality. Right? So

Speaker 0: Product takes over here.

Speaker 0: And so,

Speaker 0: you know, you're gonna have member for a typical AC offer. You're gonna have members areas.

Speaker 0: And you're going to have email.

Speaker 0: You're have, like, forums or Facebook groups.

Speaker 0: SMS is supposed as well, and,

Speaker 0: you know, any of that any of that type of

Speaker 0: that type of stuff. Right? So...

Speaker 0: As well as the actual product

Speaker 0: product. And under this, you could think of, like, your slides,

Speaker 0: audio,

Speaker 0: video, PDFs, etcetera.

Speaker 0: That's right. And so all of these things, you know, in the pre the pre phase and the post phase,

Speaker 0: the pre purchase consumption creates a percept... Perceptual value. Right?

Speaker 0: Especially this, we're we're we're in control of this.

Speaker 0: This all creates

Speaker 0: exceptional value,

Speaker 0: and the post purchase consumption

Speaker 0: is

Speaker 0: the

Speaker 0: the actual

Speaker 0: consumable value.

Speaker 0: Right? And

Speaker 0: so,

Speaker 0: actually, the flywheel or cycle

Speaker 0: would be

Speaker 0: probably more.

Speaker 0: Yeah. So you can think of just kinda like sick... Sick if you... These things all kind of like feedback

Speaker 0: into each other in a way that either is

Speaker 0: positive reinforcing or negative reinforcing. Right?

Speaker 0: And I'll get better images for this after the call, but we'll just go with these for right now.

Speaker 0: So...

Speaker 0: Alright.

Speaker 0: Search a table.

Speaker 0: And so, yeah, you can kinda have, like, three categories where, you know

Speaker 0: Those four actually. No

Speaker 0: value.

Speaker 0: And then it could be low low or

Speaker 0: high high.

Speaker 0: As was then,

Speaker 0: it's sort of come to the voice.

Speaker 0: And then the... Yeah. This would be high and high.

Speaker 0: High and high. Right? And so in an ideal world, we wanna be in this final category. Right?

Speaker 0: Where you've high high perceived value in the pre purchase cycle and the post per per purchase cycle, the perception value, you know, is... The expectations are met. Right? And this has... This is a positive... Possibly reinforcing.

Speaker 0: Right? And so, yeah, this this is kinda... I have this kinda, like, cycle attaches to this. Right?

Speaker 0: So title role

Speaker 0: is here.

Speaker 0: Yep.

Speaker 0: So

Speaker 0: now...

Speaker 0: So these are the... This is kinda like a basic overview of kind of, like, the solid consumption concept call that we actually did where it was, like, pre and post purchase

Speaker 0: pre and post purchase consumption and how they kind of interact with each other, and some of the kind of, like, downstream negative negative negative effects of, you know,

Speaker 0: you know, over overpromising on delivering, etcetera. Right. Now in terms of

Speaker 0: actual

Speaker 0: secondary transactions and architecting Ascension, the first thing... First concept

Speaker 0: First concept we wanna talk about is... Like, our goal is to be in this...

Speaker 0: Let's go on with this.

Speaker 0: Yeah. Our goal is to be in this positive reinforcing cycle. Right? We want a high perceptual value of the product in the front end, or marketing and sales material, and then the actual product itself.

Speaker 0: It...

Speaker 0: The product itself fulfills in that that

Speaker 0: expectation.

Speaker 0: Right? And so that is actually where this concierge close

Speaker 0: call

Speaker 0: comes in. Right?

Speaker 0: Because what this will help you do is identify

Speaker 0: if you have high perceptual value or low perceptual value prepurchase

Speaker 0: based on people getting on the phone with you. If they won't, that's kind of an indicator that there's some... The expectations are being mismatched somewhere.

Speaker 0: And then through interacting with them, you can see what they what they wanted to have...

Speaker 0: What what they wanted to to interact with in the product. Right? So which bonuses were were were speaking to them or or

Speaker 0: which things were, like, jumping out to them in the sales process that may... You know, had

Speaker 0: higher degrees of appeal to them. And then you can kinda go and say, does this component

Speaker 0: fulfill on that expectation? And have I have I have I done that? And the things that will typically be, it's like, have you overclaimed that the the the product can do something? Is it poorly poorly delivered? You know, is the audio crap? Does it look...

Speaker 0: Do the visuals not look good, etcetera. Right? But the

Speaker 0: the... That's kind of the base

Speaker 0: the base evaluation is is kinda what the benefit of this concierge close

Speaker 0: call will do. This is really

Speaker 0: doing multiple things.

Speaker 0: It's an evaluator

Speaker 0: of what is...

Speaker 0: What customers

Speaker 0: are... Sorry. Okay. So there's three phases. We'll just gonna break them out here. One,

Speaker 0: will they get on the call? Will they get on the call? They get on a call with you as all those.

Speaker 0: Two, are they excited

Speaker 0: to be on the call?

Speaker 0: Three,

Speaker 0: are

Speaker 0: they asking

Speaker 0: you for guidance

Speaker 0: on specific

Speaker 0: components

Speaker 0: of your products

Speaker 0: or those that specific

Speaker 0: component

Speaker 0: of your product

Speaker 0: fulfill

Speaker 0: on their

Speaker 0: expectations

Speaker 0: when

Speaker 0: your...

Speaker 0: This is

Speaker 0: this is a self audit. Right? A self audit.

Speaker 0: You can ask them afterwards potentially as well, but just based on... You've made the product. Right? If that's the assumption, you should kind of know, should that be better or should not. Right?

Speaker 0: And if it's... If if yes,

Speaker 0: you know, great.

Speaker 0: If not... If no,

Speaker 0: what can be done

Speaker 0: to improve

Speaker 0: product. Right?

Speaker 0: Now, the next thing is you can kind of like think of this one as energetics.

Speaker 0: Right?

Speaker 0: When you're guiding

Speaker 0: them

Speaker 0: through the product

Speaker 0: product,

Speaker 0: those...

Speaker 0: Their

Speaker 0: enthusiasm...

Speaker 0: Because the

Speaker 0: enthusiasm

Speaker 0: they came

Speaker 0: to the call with

Speaker 0: increase,

Speaker 0: stay the same

Speaker 0: same, or go down

Speaker 0: based on what you're

Speaker 0: guiding them through.

Speaker 0: This

Speaker 0: indicates

Speaker 0: the perceptual value stuff, perceptual

Speaker 0: value mismatches.

Speaker 0: Right? So if it's going down, you're more likely in this

Speaker 0: low perceptual value post purchase. Right? If it's going up, you may be in low perceived... Perceptual value prepurchase, and then it's becoming higher perceived value inside the actual consumable product.

Speaker 0: Or if it's remaining neutral, you know, I suppose it could just be high high high perceived value. I suppose you you just wanna take the theme. They stay... They're very high energy, and they're they're still excited about us. Nothing's changed. It's just, you know, meeting... So they're meeting their expectations or it's failing their expectations. Right? So you you kinda get a get a sense of that. And so that's kind of,

Speaker 0: you know, just assessing the the the individual on the other side of it. Right? There's some more you could do with that, but that's the

Speaker 0: that's the

Speaker 0: that's the the benefit of discount search calls. Right? You're you're not doing this to simply

Speaker 0: to simply move people to a back end sales call. It's also all of

Speaker 0: all of these other things that are

Speaker 0: are being revealed to you about your product, right, based on on on on these these types of factors. Right?

Speaker 0: Can get a you can get a sense of of

Speaker 0: of the perceptual value of of the product. Right? And so why does this matter?

Speaker 0: You hear this?

Speaker 0: Why does

Speaker 0: why does this matter? Right?

Speaker 0: Because

Speaker 0: consumption

Speaker 0: leads to Ascension.

Speaker 0: Right?

Speaker 0: If people if people

Speaker 0: are not willing

Speaker 0: to...

Speaker 0: Or not consuming

Speaker 0: your product consuming your product,

Speaker 0: having a good experience with us,

Speaker 0: and, like, revealing

Speaker 0: their, you know, personal

Speaker 0: limitations

Speaker 0: via

Speaker 0: the product

Speaker 0: experience,

Speaker 0: or,

Speaker 0: you know, they're

Speaker 0: they're disengaged.

Speaker 0: They will...

Speaker 0: All secondary transactions secondary transact... Secondary

Speaker 0: transactions

Speaker 0: and interaction with the business

Speaker 0: goes down. Right?

Speaker 0: So, like, you know, you're violating the the relationship.

Speaker 0: Right? So without without

Speaker 0: yeah.

Speaker 0: So without without without consumption, this doesn't happen for us.

Speaker 0: And so

Speaker 0: this is kind of the kinda, like, base of why why why why that why

Speaker 0: that concierge close

Speaker 0: concept or call is a really useful one, especially for people who are,

Speaker 0: you know, new

Speaker 0: or or just launching an offer. Right? If you have a new offer and you you you you know, this is not scalable long term in in most instances. Right? You could probably create a group version of this where you guide people through or have, like, you know, VAs do it eventually

Speaker 0: on, like, kinda like Zoom.

Speaker 0: Both the value of this is not necessarily moving people to a sales call, although that can be a secondary benefit of this as well. It's it's definitely... There's definitely some value in that too. What it really is helping you do is evaluate the quality of the actual product and and the expectations

Speaker 0: you're fulfilling on for the audience. Right?

Speaker 0: So...

Speaker 0: And...

Speaker 0: Yeah. So the next thing

Speaker 0: kinda concept I wanna wanna talk talk about, and this is more kind of like... Now that we've done this value... I can't think of this more as an evaluation. Right?

Speaker 0: We have... Let's go back to our... I

Speaker 0: didn't fall back there.

Speaker 0: Yeah.

Speaker 0: Let's go back to our solid consumption concepts.

Speaker 0: Just take all this.

Speaker 0: So the product takes over, obviously, when... Once they get into the members area.

Speaker 0: And

Speaker 0: what is... The the reason this matters is because this is also... It's not even just from a consumable value

Speaker 0: in a

Speaker 0: in a...

Speaker 0: Also too.

Speaker 0: Right.

Speaker 0: But, yeah, concept two is kinda leading to limitations.

Speaker 0: If the... If you get these mismatches wrong, the other thing that happens is because they become disengaged,

Speaker 0: they're not interacting with any of this stuff. Right? They're in... They're they're not interacting with your members there, your email, forms of Facebook groups, SMS, product, any of your any of your deliverables. Right? And what that's... Problem that creates

Speaker 0: creates isn't

Speaker 0: simply

Speaker 0: disengagement...

Speaker 0: Disengaged

Speaker 0: users,

Speaker 0: it's also

Speaker 0: a

Speaker 0: lack of revelation

Speaker 0: for them. Right?

Speaker 0: Because, like, okay.

Speaker 0: By ascension, what we mean for this call or for this section of the call, for sure, we're meaning...

Speaker 0: We mean, you know, high ticket back end. It's just kinda like...

Speaker 0: Think of it

Speaker 0: simply in that that... These terms. Right? The problem this this... Them disengaging

Speaker 0: is it then... There's no revelation fee of the product. Right? So

Speaker 0: we have we

Speaker 0: have...

Speaker 0: You know, this is our goal.

Speaker 0: Their interaction

Speaker 0: with your product

Speaker 0: isn't just consumable

Speaker 0: value consumable value

Speaker 0: value in the, you know, traditional sense.

Speaker 0: It also is a personal

Speaker 0: evaluator

Speaker 0: of their current

Speaker 0: circumstances

Speaker 0: and their

Speaker 0: comparison

Speaker 0: against

Speaker 0: the transformation

Speaker 0: your product

Speaker 0: can have for them. So

Speaker 0: just a kind of simple example.

Speaker 0: Let's say

Speaker 0: someone

Speaker 0: someone...

Speaker 0: We have a weight loss offer weight loss offer. Just keep it simple for us.

Speaker 0: Disengaged customer

Speaker 0: disengaged customer,

Speaker 0: never interacted with the product.

Speaker 0: Product.

Speaker 0: Okay.

Speaker 0: Same

Speaker 0: same same issues as we had above. You have engaged customer,

Speaker 0: We interact with the product.

Speaker 0: Product,

Speaker 0: they they start implementing

Speaker 0: a version of the a version of the outcome the product can generate

Speaker 0: on their own.

Speaker 0: That that

Speaker 0: implementation

Speaker 0: reveals

Speaker 0: limitations

Speaker 0: in

Speaker 0: their

Speaker 0: fields,

Speaker 0: capabilities,

Speaker 0: resources,

Speaker 0: knowledge,

Speaker 0: personal drive,

Speaker 0: and also

Speaker 0: how much...

Speaker 0: How

Speaker 0: hard... How close

Speaker 0: or far away

Speaker 0: the goal

Speaker 0: that they're...

Speaker 0: They want to achieve

Speaker 0: with the product

Speaker 0: deals

Speaker 0: to them first.

Speaker 0: These bullets as well.

Speaker 0: And so... And that... And this this is part of... This

Speaker 0: this creates this creates

Speaker 0: a

Speaker 0: gap

Speaker 0: between

Speaker 0: where they are and where they want to be,

Speaker 0: right, which creates

Speaker 0: desire

Speaker 0: to...

Speaker 0: Creates desire to

Speaker 0: achieve

Speaker 0: the outcome faster

Speaker 0: and get support.

Speaker 0: Huddl also is a regulatory

Speaker 0: in the sense

Speaker 0: that they

Speaker 0: now accept

Speaker 0: that they need help, right,

Speaker 0: versus

Speaker 0: simply

Speaker 0: agree

Speaker 0: they can't do it on their own. Right? So this is this is some of the other stuff that's going on. Right? And so when people

Speaker 0: try and put people onto sales calls and they've never consumed the product, this is one of the things that, you know... Oops. Sorry. Gotta resume the recording. This is one of the things,

Speaker 0: you know, this is one of the things that if you've ever had sales guys... Sorry. What's going on here? If you ever had sales guys

Speaker 0: If you've

Speaker 0: ever had salespeople

Speaker 0: who put... Who have leads

Speaker 0: on the phone,

Speaker 0: who have simply

Speaker 0: bought

Speaker 0: a full time product

Speaker 0: and never interacted with this

Speaker 0: with this or have been disengaged.

Speaker 0: The the... This

Speaker 0: this is at the roof

Speaker 0: of why those sales call those

Speaker 0: sales calls

Speaker 0: become so hard. Right?

Speaker 0: Inter...

Speaker 0: Yeah. This is at the at the real why why those sales calls become so hard. Right? And it's like, also, if the objections come up,

Speaker 0: process questions come up, like, okay, objections come up around price,

Speaker 0: around process.

Speaker 0: How does this work?

Speaker 0: Around credibility.

Speaker 0: Can

### 0:30

Speaker 0: you really help me?

Speaker 0: You know, then they'll want risk reversal.

Speaker 0: So, you know, money back guarantees.

Speaker 0: Ts for better terms.

Speaker 0: Right? And so this this is the

Speaker 0: other way that we we can... The other benefits, again, coming back to that kind of concierge close concept

Speaker 0: from that call, that's one of the other benefits of doing this is that you help simplify

Speaker 0: this this part of part of the process for you, right, in...

Speaker 0: If you if if you if you help refine the product via knowing what people want and if you improve... If you iterate on the product,

Speaker 0: that is...

Speaker 0: That's where that's where

Speaker 0: that's where you get the benefit of that. Oops. Sorry.

Speaker 0: No.

Speaker 0: That's not working. One shift.

Speaker 0: Never mind.

Speaker 0: Yeah. That's it.

Speaker 0: So all of this stuff starts coming up if you're

Speaker 0: if you're doing this. So this can even if you have book a call,

Speaker 0: standard book a call processes, and you don't have a clearly defined

Speaker 0: step by step of of how you kind of, like, create stuff or good processes

Speaker 0: for making clear what... Like, a... If you have a service, what what you actually do for people, you'll get a lot less in there as well, Royce,

Speaker 0: for that. But that's kind of the same type of thing. They haven't consumed...

Speaker 0: They have no conceptualization of the outcome, Royce, that... Or or or of the of the process. And so as a result, all of this

Speaker 0: all of this

Speaker 0: all of this type of stuff starts emerging. Right?

Speaker 0: So that's how... That's the the other important

Speaker 0: components of

Speaker 0: of

Speaker 0: how we can architect Ascension, right, is that part of the Ascension

Speaker 0: via the quality of the product, right, is

Speaker 0: is

Speaker 0: is is is this. This is part of what's going on. It's just that you're letting people,

Speaker 0: you know, learn about their own limitations in the product or create just even even part of it can be just be building appeal to move forward faster. That's, I suppose, even a totally separate concept. But if that never happens, this is this is where you end up with, you know, much more skeptical

Speaker 0: skeptical customers. Right?

Speaker 0: Okay. So that's that's net. Constant three.

Speaker 0: What was this? Yeah. Installing

Speaker 0: criteria.

Speaker 0: Right?

Speaker 0: So... Oh, yeah. I wanna talk with some of the calls. Calls

Speaker 0: that are relevant.

Speaker 0: The product first marketing call.

Speaker 0: Marketing call

Speaker 0: call is

Speaker 0: relevant for this one as well. Now...

Speaker 0: Yeah. It... Also three is kind of installing criteria. Right? So...

Speaker 0: And these kind of all stack on top of each other. Right? You know, if we can't... If we don't have consumption,

Speaker 0: we don't have interaction

Speaker 0: with the product, and then we also don't have...

Speaker 0: There's concept two. They they... As a result, they never get to lead lead to the limitations. But then there's also no...

Speaker 0: Other other things we can do in... Via consumption is kind of install right criteria. So, you know, for example,

Speaker 0: let's define what install criteria is.

Speaker 0: It's the...

Speaker 0: Is when you define

Speaker 0: what success

Speaker 0: or failure

Speaker 0: looks like

Speaker 0: via

Speaker 0: the product

Speaker 0: in some in some some defined way. So... Wait.

Speaker 0: So

Speaker 0: both successful,

Speaker 0: you know, CPAs, let's say, you know, an accounting offer, CPAs do this. Right?

Speaker 0: You know,

Speaker 0: the difference

Speaker 0: between

Speaker 0: people

Speaker 0: who win and lose as, you know,

Speaker 0: learning

Speaker 0: to code

Speaker 0: is this. Right?

Speaker 0: And so you you have

Speaker 0: these...

Speaker 0: And this consumption

Speaker 0: lets you create a a void between...

Speaker 0: If you want

Speaker 0: to be successful,

Speaker 0: you have to do these things,

Speaker 0: versus

Speaker 0: if you fail,

Speaker 0: you do

Speaker 0: these

Speaker 0: things.

Speaker 0: And actually what you're... This is actually derivative of another concept from sociology called linguistic

Speaker 0: intergroup bias.

Speaker 0: We'll go on to this for too much. This is a derivative concept.

Speaker 0: Right? And what linguistic linguistic

Speaker 0: intergroup bias is is when

Speaker 0: people use,

Speaker 0: sorry, use stigmatizing

Speaker 0: language

Speaker 0: for people

Speaker 0: in outside

Speaker 0: outside

Speaker 0: their group

Speaker 0: or certain behaviors.

Speaker 0: And then also use also use,

Speaker 0: you know, positive positive

Speaker 0: language

Speaker 0: or the exact same behavior

Speaker 0: for people within the group price

Speaker 0: group. And so

Speaker 0: these installed

Speaker 0: criteria

Speaker 0: and contrasts

Speaker 0: create a in group and an out group price.

Speaker 0: Create an ingroup

Speaker 0: and an out group.

Speaker 0: And while they won't use language

Speaker 0: necessarily, you might... People might say, well, I'm just too lazy or I didn't do the work. That type of stuff would be if you're in the out group or didn't get success.

Speaker 0: But what will more more likely happen is

Speaker 0: people will

Speaker 0: want to self identify

Speaker 0: self

Speaker 0: with the in group the in group, which is the the ones, you know, who...

Speaker 0: If I wanna be a successful CPA, yeah, I I want I want that for it. So for the the desire for the outcome

Speaker 0: is part of the in group, and then

Speaker 0: as a result, they'll they'll want to adopt

Speaker 0: the behaviors

Speaker 0: of people in the in group.

Speaker 0: And the same then the inversion is kind of for the the group price.

Speaker 0: So again, similar, consumption leads to Ascension.

Speaker 0: Without that, you have no no opportunity

Speaker 0: to install criteria

Speaker 0: that people can kind of, like, contrast, you know, good or bad against. Right? You know, that for...

Speaker 0: You know, if we wanna take it for... To the... All of

Speaker 0: all of the most

Speaker 0: successful

Speaker 0: offer owners

Speaker 0: to

Speaker 0: x,

Speaker 0: y, or z. All the most successful offer owners are on the offer fundamentals call right now. Right?

Speaker 0: And all the ones who aren't are skimming over this. Right? That's an example of a version of installed criteria. So it's letting... You know, it's a very simple basic version, but you can see where we're going with those. At any of that stuff, a lot this stuff will happen even subconsciously.

Speaker 0: A lot of people will create these kind of criteria without even fully be... Fully being aware of them just in the product.

Speaker 0: These things naturally emerge, especially if you're... These will naturally emerge if you have any sort of...

Speaker 0: These naturally emerge

Speaker 0: emerge

Speaker 0: in content

Speaker 0: if you have any

Speaker 0: source of transformation in your product.

Speaker 0: So it doesn't matter

Speaker 0: doesn't matter if it's,

Speaker 0: you know, weight loss. It doesn't matter if it's personal development. It doesn't matter if it's business development. It doesn't matter if it's sports. Like, this will match... This will naturally emerge just when you're talking about how how you, you know, get better or or worse or, like, you talk about anything behavior. Right? This kind of in group ad group stuff kinda naturally emerges. Right? So,

Speaker 0: yeah. That's another key concept that I wanted to to go over. Is is this helpful so far, guys? Is it... You're starting to see how we're building up some of this stuff to think about? We'll we'll we'll... We can actually bring this into an offer shortly as well. But is this is

Speaker 0: any of this landing, or is this helping you kind of see how

Speaker 0: the... What the what the issue with the

Speaker 0: products

Speaker 0: disengaging people would be?

Speaker 0: Feel free to give me any info in chat.

Speaker 0: Next concept. Any feedback in chat? The next concept I wanna cover... Where is this?

Speaker 0: Oh, yeah.

Speaker 0: Stage awareness.

Speaker 0: Yeah. So

Speaker 0: there's

Speaker 0: magnitudes

Speaker 0: problem.

Speaker 0: Magnitude problem.

Speaker 0: So

Speaker 0: So

Speaker 0: this kind of is a derivative of... Or this is... This stacks upon the kind of consumption stuff as well.

Speaker 0: But

Speaker 0: with this other concept from previous calls

Speaker 0: where,

Speaker 0: you know, self evident... Okay. I'll just define these again.

Speaker 0: Self evident offer

Speaker 0: offer is one that is immediately

Speaker 0: obvious

Speaker 0: to the person

Speaker 0: consuming us.

Speaker 0: This is for them.

Speaker 0: The

Speaker 0: value of offer

Speaker 0: is

Speaker 0: an

Speaker 0: offer that

Speaker 0: requires

Speaker 0: evaluation

Speaker 0: to

Speaker 0: see if this offer is right

Speaker 0: for

Speaker 0: me or not. Right?

Speaker 0: Not. And this attaches to a magnitude of problem as well, because if it's a high magnitude problem,

Speaker 0: it's...

Speaker 0: By by its very nature, it's more self evident.

Speaker 0: And so

Speaker 0: the low magnitude problems will typically be more acute

Speaker 0: short term

Speaker 0: problems

Speaker 0: that have

Speaker 0: that have

Speaker 0: many

Speaker 0: available

Speaker 0: alternatives

Speaker 0: that

Speaker 0: solve the problem.

Speaker 0: And so

Speaker 0: as a result,

Speaker 0: you know,

Speaker 0: result, they are, by their nature,

Speaker 0: more valuable price.

Speaker 0: Because, like, do I need x? Do I need y? Do I need z? Right? Or some magnitude problems,

Speaker 0: you know,

Speaker 0: got to solve this fast.

Speaker 0: You know,

Speaker 0: anything that... Anything anything

Speaker 0: any

Speaker 0: plausible solution

Speaker 0: solution

Speaker 0: will

Speaker 0: will be... It'd be more readily accepted. Right?

Speaker 0: And so, you know, take a simple example. Back pain.

Speaker 0: If you have a small backache,

Speaker 0: do I need a pain killer? Do I need a walk? Do I need a massage? Whereas if you've got, you know, chronic back pain and it's been an issue, it's like, give me the surgery, give... Bring me to a chiropractor. Right? The the type of solutions you're more likely to go after are

Speaker 0: more far more, you know...

Speaker 0: You... You're willing... You're more gonna have more more price elasticity, but you're also going to

Speaker 0: you're also going to

Speaker 0: price...

Speaker 0: If if if if you believe in in in that mechanism,

Speaker 0: chiropractic or osteopath or the surgery, you're gonna get on with it. Right? You can do what you can because the the magnitude of the problem because you're in so much pain means that you you will you will you will go and get on with it. Right? And so how does this,

Speaker 0: you know, how does this

Speaker 0: happen via the the product? Right? Well, even if you have a self evident offer

Speaker 0: in the sales cycle,

Speaker 0: there's still

Speaker 0: a post evaluation

Speaker 0: going on

Speaker 0: in the consumption.

Speaker 0: Right? So

Speaker 0: people

Speaker 0: are comparing

Speaker 0: and contrasting

Speaker 0: their timeline

Speaker 0: against

Speaker 0: the product.

Speaker 0: They're also

Speaker 0: they're also getting educated

Speaker 0: educated

Speaker 0: by the product,

Speaker 0: which is partially

Speaker 0: attached to the learning... The limitations

Speaker 0: stuff, limitations and criteria as well.

Speaker 0: And

Speaker 0: they're building

Speaker 0: appeal

Speaker 0: for the

Speaker 0: outcome

Speaker 0: in that consumption.

Speaker 0: And all of this all of this creates desire

Speaker 0: for, you know,

Speaker 0: working

Speaker 0: with someone

Speaker 0: to help help help them

Speaker 0: get the best sold

Speaker 0: possible.

Speaker 0: And so as desire goes up,

Speaker 0: the magnitude of the problem

Speaker 0: goes up

Speaker 0: naturally because that's what's what's... That's where the urgency is coming from. I want this. Right? And the

Speaker 0: the self evident self evident nature

Speaker 0: of the offer goes up as well.

Speaker 0: Well, because they now know what they're getting. Right?

Speaker 0: Goes.

Speaker 0: So these these are kind of, like, downstream effects of the the the consumption as well. So your

Speaker 0: back end becomes higher magnitude, more self evident as the consumption

Speaker 0: goes up, right, with... In in... Inside the product. And so the magnitude of the problem becomes

Speaker 0: bigger for them as well. They'll they'll they'll want

Speaker 0: they'll want that outcome more. Because the gap between the gap between

Speaker 0: where they are now

Speaker 0: versus where they

Speaker 0: want to be

Speaker 0: is is clear to them.

Speaker 0: Okay.

Speaker 0: So

Speaker 0: there's probably more... I definitely have one other concept that's kinda fleeting for me, what I hear. Let's just dive into my notes.

Speaker 0: Oosh.

Speaker 1: Hey, Kevin. Had a couple questions and maybe the concepts that we can talk about. So number one is about presentation.

Speaker 1: So the way I'm thinking about it is,

Speaker 1: you know, as a buyer, as you, you know, you you read the, you know, you read the copy for the front end, you go to the upsells and whatnot, and then the journey begins

Speaker 1: from the from the moment they see the thank you page. Right? Yes. So

Speaker 1: or even... Thank you.

Speaker 1: Then

Speaker 1: they get the Vulcan as soon as they they create their account and stuff. And what is their first impression as soon as they land in the member's area? Right? Because I'm I'm looking back at, stuff courses and stuff I purchased.

Speaker 1: And, you know, as soon as I,

Speaker 1: let's say, like, join a school community or

Speaker 1: purchase something on WAP, the first thing I'm seeing is, okay. What are all the modules in this course? You know, what are their thumbnails look like? Like, how... You know, does it does it mean that dopamine hit as soon as I've, you know,

Speaker 1: made the purchase? Like, is this something that I would wanna invest,

Speaker 1: you know, eight to twelve, like, hours of my time into over the next

Speaker 1: few days, few weeks. What does that introduction

Speaker 1: chapter of my book look like? Because that is something I've been spending a lot of time

Speaker 1: thinking about is, like, how do I write my introduction chapter so it actually makes them wanna read the rest of the book? Yes.

Speaker 1: So just... I think

Speaker 1: it's kinda like a YouTube video. Right? Like, you you go on YouTube and you're deciding, okay. Which video should I click on based on how attractive the thumbnail looks? Yeah. Yeah. Click.

Speaker 1: You wanna you wanna validate...

Speaker 1: You wanna feel validated that, okay, you made the right choice

Speaker 1: by clicking on this video based on the first

Speaker 1: thirty seconds or one minute. Right? Like, what, like, what is the hook of the video? So same way, like, for our product, like, how can we get people,

Speaker 1: yeah. Just hooked.

Speaker 0: Yeah. Yep. So that that, like, a lot of that would fall under, you know, the... A lot of the qualitative factors of the,

Speaker 0: you know, like, fonts, brand colors,

Speaker 0: logos,

Speaker 0: you know, imagery imagery inside... In in... Inside whatever they're consuming.

Speaker 0: Any graphic design graphic design slash slides,

Speaker 0: this type of stuff. Right?

Speaker 0: These things similar... The the same thing happens when you have a,

Speaker 0: you know, any offer, like, okay,

Speaker 0: Choose the showcase.

Speaker 0: You know, there's an immediate set of thoughts that... We've all seen this offer hundreds of times now or for the majority of us have. So this this kinda has zero impact on me now just because I'm banner blind to it. But the very first time someone landed on... Lands on this page, it creates it creates an expectation

Speaker 0: in terms of, like, where this felt... This feels different, in particular for its time when this came out. This came out about 2020.

Speaker 0: You know? And it's the perceptual value. No one was doing any of kind of gradient stuff.

Speaker 0: These, like, you know,

Speaker 0: playing with font colors in in the headlines weren't... Wasn't wasn't a theme or or a thing that people were re... Redoing.

Speaker 0: Graphic design was really, like, not even remotely focused on. No one was doing any

Speaker 0: no one was doing any kind of, like, infographics like this this in a way that we're actually adding consumable value. They were just kind of random random images or pictures of, like, you know, stock footage on the page. So this created a contrast between everything that that came before... That they'd seen before

Speaker 0: and and and

Speaker 0: at... On this on this product when when they saw it. Right? And so that's part of that perceptual value we talked about. Right? And then you've all... Or the majority of you, I'm assuming, have consumed some of the content inside the actual online clients course as well. And, like, Robert did a great job, made a lot of those slides.

Speaker 0: For them as well as what... Of all the guys worked tirelessly on on that product. Right? And so the product fulfilled on that expectation.

Speaker 0: And then we all... Visually,

Speaker 0: so you you had a... The the members area and how the content was laid out in there. You know, now now we have the, obviously, the platform where the... It's currently hosted. But in the in the original platform where, you know, the all of my clients' members area, it had a a great design. It had some

Speaker 0: novelty in the in the user experience in there insofar as it had,

Speaker 0: you know, bonus modules and content they could unlock if they if they... There was some some... Something where if they had they had they had to complete a few modules and then email the team back and then something something

Speaker 0: opened up. I think it was this concept called Moneyball, which was essentially

Speaker 0: the... It's essentially like the catalog model,

Speaker 0: the kind of earlier iterations of that. But that... There was a dedicated training there. That training is probably still inside the platform. But all of these things were, like, micro investments, created micro investments from the user in terms of their their experience. Right? And so if you had come to this product

Speaker 0: and it had...

Speaker 0: You know,

Speaker 0: the second you get into the members area, it fails on those expectations, and it was just a standard. Even the fact that you're you're you're you're you're talking about WAP and School, Ooj, as an example, like WAP School or ClickFunnels. Now we can't... Sometimes we have to just, like, work what we have. But let's say, you know, everyone is using ClickFunnels,

Speaker 0: and it's like your customer has been... Has become... You're in a in a mature market

Speaker 0: and... Or sophisticated market.

Speaker 0: And a lot of people have interacted with that

Speaker 0: members area platform

Speaker 0: from your market. It now... You're now one of the one of the others. Right? You're you're kind of, like, seen among that crowd, and that can be disengaging as well. So that's something you'd have to overcome

Speaker 0: as a potential objections. Like, oh, another ClickFunnels member's area. You know? That that type of thing. Or, you know, doesn't doesn't have to be ClickFunnels. Oh, another ThriveCart member's area. Oh, another Go high level member... Member's area. Oh, another school group. Right? People become jaded with the sales process. And so these will be... You know, this is one that's largely largely

Speaker 0: outside of our control

Speaker 0: other than the fact that we kinda, like, custom build a platform or whatever. But that's an example of these type of immediate reflexive thoughts. Right? And so these are the things we're overcoming

Speaker 0: as they as they as they they go through the product. And so... Or as they as they even onboard. Right? It's like, what does what does your login page look like? All of these little micro details really have have impact. Right?

Speaker 0: And so your... Where you're starting is your book. Right? Where your your kind of initial thought

Speaker 0: picks up. And I suppose, really, what you're actually doing here is creating a narrative.

Speaker 0: Narrative for your offer

Speaker 0: offer in chapter one. Right?

Speaker 0: Essentially, why why

Speaker 0: should

Speaker 0: pay pay attention?

Speaker 0: And so it's like,

Speaker 0: you'll see this in a lot of intros of books.

Speaker 0: And they'll build they'll build they'll build on they'll build on that through some sort of either

Speaker 0: affirming affirming the

Speaker 0: affirming the

Speaker 0: promise of the title,

Speaker 0: or,

Speaker 0: you know, in in a more not a story driven one, it would be like a,

Speaker 0: you know, a hook based

Speaker 0: or or character

Speaker 0: in compromised

Speaker 0: situation. Right? From what kinda like... This is more kinda like fiction.

Speaker 0: That type that type of lead will will will

Speaker 0: come in, or they'll create some sort of like altruistic drive...

Speaker 0: Altruistic

Speaker 0: motivation

Speaker 0: in terms of, you know,

Speaker 0: how this book

Speaker 0: will

Speaker 0: help

Speaker 0: them

Speaker 0: with

Speaker 0: some form of just calls. Right?

Speaker 0: So, you know, let's say you're reading a book on climate change. You're just affirming the beliefs of the of the person there,

Speaker 0: you know, and and why reading this book is, you know, you're part of the solution, not part of the problem. Right? That that kind of a theme. Right? So this is... But this is... That's part of the narrative why anyone wants to to keep going forward. Right?

Speaker 0: So this stuff this stuff ties in...

Speaker 0: Some of the stuff you could you could tie in to the the... You're thinking around what you're actually doing in in the first

Speaker 0: first

Speaker 0: chapter of the book. Right? That's that's that's kinda what's going on.

Speaker 0: But we've

Speaker 0: we've already seen, because we've working on this offer together,

Speaker 0: the impact.

Speaker 0: Like, I did... I've... I did feedback for you yesterday, Royce, and we've... You've just upgraded your logo. You've upgraded to kinda, like, graphic stack. It's a perfect note, but it's, a massive leap forward relative to where it was. That's just initial impact

Speaker 0: in terms of that initial perception of Isaac, man, you you... You're you're... You you wanna lean towards the computer because of... Because of what what that's doing. Right? And that's part of the appeal, desire building process. Right? Like, what what is this? I wanna pay attention. Right?

Speaker 0: And so, like, you can think of those micro investments

Speaker 0: that... They're happening constantly throughout the funnel and constantly throughout the whole sales process and constantly throughout the consumption of the product. Do the... Does this thing make me wanna lean in or move away? Right? Does this... And for what reason? Is it because I'm, you know, reversion? I wanna get away from this thing? I I I feel like it's, you know, a scam or it's,

Speaker 0: you know, it's framing this framing this whatever the content is in a way that's,

Speaker 0: you know,

Speaker 0: you know, judgmental towards me as the user, or am I leaning in because it's like, well, you know, this is this is this is pulling me and this feels right. This feels correct.

Speaker 0: I am... Or it's belief building in some way that that build... Builds appeal to to keep going. Right?

Speaker 0: And a lot of that can happen. Like, that happened...

Speaker 0: You know, it happens up in the Adler first, but, like, the very first way that that happened here on this page, for me at least, when I saw this page, all all all those

Speaker 0: years ago when almost... This this this gradient was like, wow. Like, this was just magic back then. So... Because we haven't seen any of this. This kinda, like, whole gradient vibe was there. So it's like that that that perception

Speaker 0: of care just became immediately obvious. Right? And and so these

Speaker 0: that's a micro micro win

Speaker 0: for for someone once they come to the page. You're immediately, like, your eyes just pulled into the orange, and then you scroll around. It's like, wow. This is... This doesn't feel like any of the other stuff I'm used to seeing. Right?

Speaker 0: And so those... You don't always have to be unique, right, in in the stuff you're creating.

Speaker 0: I'm not gonna install that criteria

Speaker 0: for for you guys, but it... It's just being aware of of, you know, some of the trade offs of of even using some of the bog standard platforms. There are some drawbacks in price insofar

Speaker 0: as it does create a, you know, birds of a feather flocks together type team. I think Charles talked about that a long, long time ago when when referencing a similar a similar concept price. If if if

Speaker 0: if they've been scammed by people using insert platform here,

Speaker 0: you know, and then they'll see you using insert platform here even if it's a different product. It's like, no. I just don't trust this. Right? So it's it's that it's that that type of stuff. Right? Plus,

Speaker 0: Ujj, you, do you have any follow-up questions? Just so you'll unmute the cam... Or or or turn on your camera?

Speaker 1: No. No. That's that's great. Yeah. That makes sense. I I put the link for, the automatic clients, members area login if you wanna Oh, yeah. Yeah. Yeah. Put a do a breakdown on that. I really like ClickFunnels for building the members area because you get a lot of customizability.

Speaker 1: Yeah. I don't know if you have the log. Yeah. I should should have my login. Let me still check.

Speaker 1: But with ClickFunnels two point o, they've they've made it really

Speaker 1: good. Like, I'm I'm working on creating the members area in ClickFunnels.

Speaker 1: That's a very, very good experience.

Speaker 1: You can even add

Speaker 1: upsells, like, after... Like, inside the members area now, so you can control you can control modules and stuff

Speaker 1: even after the purchase if you if you create new new courses and stuff. Do you have login info for this for this members area?

Speaker 3: Yes. Yeah. Can you just send it to me on Discord?

Speaker 1: Yep. And I'll log in here. We'll do we'll do some of this. Actually, I like I like this. It's a good idea.

Speaker 0: Thank you.

Speaker 0: And then the password if you have us. Super.

Speaker 0: Thank you very much.

Speaker 0: Yeah.

Speaker 0: No. It didn't work, unfortunately.

Speaker 0: Alright. Give me a sec.

Speaker 0: The email's alright, just not the not the password?

Speaker 1: Yeah.

Speaker 0: Perfect. Okay. Great.

Speaker 0: Just

Speaker 0: you know, just get out of get out of chat here so we don't see that. Okay. Perfect. Let me share my screen again.

Speaker 0: So,

Speaker 0: yeah, even this this is a custom code of members area back at the time. Right? And so where is this the advanced acquisition theory? So let me click on this.

Speaker 0: And so just a whole theme of this, like, of this graphic design,

### 1:00

Speaker 0: the the quality of the audio,

Speaker 0: it all stacked on top. It all it all stacked on top of each other. For me, that's some, you know, weird corporation.

Speaker 0: In terms of the

Speaker 0: perceptual value. Like, you could just... Like, even even though now, like, with with all we can do with with AI so quickly, Bryce, it this would seem kinda stripped down. But, you know, there's hundreds of slides in here across all of these modules.

Speaker 0: And, like, just the care that went into the product was very, very evident. Right? All of this graphic design. So it's like you couldn't come in here

Speaker 0: and consume this and go, this

Speaker 0: this doesn't feel...

Speaker 0: This does... This feels like these guys have cut corners. In fact, it's it's the the inversion of that. So this help.

Speaker 0: Even this, right, coming back a page.

Speaker 0: So, again, this is the... Attaching back to that novelty in the sales sales

Speaker 0: process call. So... And then this was also this is also an evaluator. Right? We're working. We... Let's let's click launch launch and build my offers. This will probably bring us to book a call page.

Speaker 0: Yeah. No. This is this is here for that. But... No. That was tagging you in the CRM, I imagine, as well.

Speaker 0: Okay. And so then even this stuff for us, join the Facebook group.

Speaker 0: There was something... Yeah. The accelerator,

Speaker 0: book reviews.

Speaker 0: And so, yeah, all of this...

Speaker 0: Other stuff, let's come back here.

Speaker 0: All of this... We have, like, they did all all all the the books as well. Right? So we have people holding the book. So this was, again, more belief building

Speaker 0: where it's like, you know, the... This is a real product. Right?

Speaker 0: And then with the Facebook group link.

Speaker 0: No. Okay. That's been

Speaker 0: been deprecated.

Speaker 0: And then just the same here. Like, clearly very well designed. Right? So if you come in here and, okay, you guess

Speaker 0: this type of a vibe,

Speaker 0: you know,

Speaker 0: in the members area, it's like, why is this stuff broken? It immediately disengaged you. Right? So we don't don't need to go too

Speaker 0: too much deeper into this, but you can just see, like, all the qualitative factors here. Are they perfect? No. Like, would...

Speaker 0: The... Alan would...

Speaker 0: And the the the team now have, you know, leveled up

Speaker 0: kind of all of the

Speaker 0: all of the

Speaker 0: design, you know, for the platform that, like, way above this. Right? It's like leagues beyond. Plus, for its time and even still now, this still... If this was any of our members areas for a a traditional AC offer,

Speaker 0: you know, and and, you know, insert your components here, you'd you'd be very

Speaker 0: you'd be very hard pressed to have customers who didn't feel like there was a lot of care that had gone into this this member's area. Right?

Speaker 0: And yeah.

Speaker 0: This was to book a call. Yeah. Yeah.

Speaker 2: How you doing? It's Robert and Kelly.

Speaker 0: Okay. So we got off a bit of a tangent, but that's something... There's there's a loss. You could strip down a lot of this

Speaker 0: from

Speaker 0: the members area, but all of these little... Or in terms of the impact it has, but I think it's pretty obvious even just glancing around here, the types of things that add real value. Like, the

Speaker 0: the...

Speaker 0: Where is that? Yeah. Here, just watch this now again.

Speaker 0: Like all of all of this design, the thumbnails

Speaker 0: on any of these pages,

Speaker 0: these graphic designs,

Speaker 0: anything you interact with. It's like, there's been care care gone in here. You can't help us feel like it's been taken care of. And we've all had the inverse of this where a product comes in and it's like, you know, random Google slides, zero zero design. The audio sounds like they're speaking to you from 50 miles away, and it's like, you know,

Speaker 0: sorry. Not not gonna call us. Right? Just completely depositions you. And so this created engagement and consumption,

Speaker 0: you know, and and every... Everything that you do that is...

Speaker 0: Anything you do to emulate this will help you. But

Speaker 0: all of the,

Speaker 0: you know, all of the

Speaker 0: all of the

Speaker 0: all of all of the care is very, very obvious and very evident for us. So... Okay. We're gonna move off that for now,

Speaker 0: and we're gonna keep expanding on actually the themes of the call. So,

Speaker 0: yeah, the stages of awareness.

Speaker 0: This is something we've touched on on previous calls.

Speaker 0: And what I would say to this is this should inform your content

Speaker 0: with two calls that are attached to this. So the audio client profiles call

Speaker 0: and

Speaker 0: think that's off for a while, I mean, from memory.

Speaker 0: Certainly,

Speaker 0: the audio audio client profile call for sure.

Speaker 0: And you know, this this...

Speaker 0: The the reason we have this model here is it just being aware

Speaker 0: of

Speaker 0: where your audience sits

Speaker 0: in the awareness

Speaker 0: awareness levels as a cluster. So you'll have... Wait. Unaware.

Speaker 0: Somewhat aware.

Speaker 0: Problem

Speaker 0: aware.

Speaker 0: Solution aware,

Speaker 0: product aware,

Speaker 0: most aware.

Speaker 0: Actually, what I should have done here, which I didn't do my notes as well,

Speaker 0: market sophistication.

Speaker 0: We'll just take this in a simple binary,

Speaker 0: unsophisticated,

Speaker 0: unsophisticated.

Speaker 0: Right?

Speaker 0: And so

Speaker 0: it's very useful to be aware of after someone has purchased your product,

Speaker 0: where they as a cohort or where where your your audience in general as a cohort sits. Like, if they're brand new to this style of offer or style of product, they're probably more in this category, someone aware maybe problem aware,

Speaker 0: and they're in probably more this unsophisticated

Speaker 0: category.

Speaker 0: And so, you know, the type of, you know, contents

Speaker 0: in the product

Speaker 0: should mirror that

Speaker 0: That's

Speaker 0: to some degree.

Speaker 0: And we don't wanna just be focused on problems, both

Speaker 0: problems speaking

Speaker 0: about their speaking,

Speaker 0: about solving

Speaker 0: their problems

Speaker 0: will,

Speaker 0: you know, activate activate

Speaker 0: their appeal because

Speaker 0: that is

Speaker 0: is how they think

Speaker 0: about...

Speaker 0: That's how they think about their issues. Right?

Speaker 0: Stuck in a problem. They're stuck in they're stuck in a problem state state

Speaker 0: in general. Right?

Speaker 0: Whereas if you speak

Speaker 0: to problems for, you know, people who are more to this... To an audience who are more in this category, like, problems are fine for these people, but they they kinda get us. And it's like, just let... Let's get on with us. I want I want I want I want to just

Speaker 0: wanna just solve this. I don't need education or,

Speaker 0: you know, anything to activate me. I just I know what I need, and I want it... Wanna get on with it. Right? So,

Speaker 0: you know, these people...

Speaker 0: You know, you could think of it this way as a very general

Speaker 0: clunky way of thinking about this. This... More people are over here, the more sophisticated they'll be. And the more people are over here, the more unsophisticated they will be as a gen... A generalization.

Speaker 0: And that will inform... Form your content a little bit. Right? And the other kind of mental models we have is, you know, zero to one customers,

Speaker 0: which are kind of beginners,

Speaker 0: One to one hundreds. Right? One to one hundreds,

Speaker 0: which are kind of, like, more, you know, people with momentum.

Speaker 0: This this isn't... This kind of attaches to the same the same kind of color scheme. Right? One to 100 are a little more in the yellow category, and the beginners are kinda more in this this orange orange category. And so,

Speaker 0: you know, you just have to be aware of

Speaker 0: who you're speaking to in the content

Speaker 0: because, you know, I'll see a lot. This happens a ton. Right? And this this actually attaches to criteria in the market as well.

Speaker 0: Both,

Speaker 0: you know, this has happened a lot for work. I've seen this with workshops a lot a lot, where you have sophisticated customers

Speaker 0: customers

Speaker 0: who get a claim

Speaker 0: on a workshop

Speaker 0: to, you know, solve a very specific

Speaker 0: business problem.

Speaker 0: And then they come to the workshop,

Speaker 0: and the workshop morphs into a webinar

Speaker 0: with an inspirational inspirational

Speaker 0: hero's journey

Speaker 0: journey

Speaker 0: type, you know, lead

Speaker 0: and talking talking about, you know,

Speaker 0: the transformation,

Speaker 0: and that can happen

Speaker 0: with zero,

Speaker 0: you know, practical

Speaker 0: elements

Speaker 0: in the workshop

Speaker 0: or,

Speaker 0: you know, ages. Right? Thirty to sixty minutes.

Speaker 0: And so you've you've you've matched beginner

Speaker 0: problem style content with a sophisticated market who have momentum, and they just completely reject it. It's like, this is not for me. I don't wanna be I don't wanna be like... You've... You're you're violating the criteria in another... And for... Through a number of lenses. Right?

Speaker 0: You know, because they have limitations. Right? Mainly be time.

Speaker 0: Right? So this is an example of,

Speaker 0: you know, they're in this category.

Speaker 0: And this... The the the workshop claims to do this. So you're pre pre consumption,

Speaker 0: you know who your avatar was. Your pre... Your pre consumption created an expectation.

Speaker 0: And when they get to the workshop, the expectation gets violated

Speaker 0: by kind of giving giving someone who is not... Giving them unsophisticated content essentially. Right? And, you know, it violates the criteria mainly around time and and skills

Speaker 0: and capabilities. Right?

Speaker 0: And, like, these people are much more outcome focused

Speaker 0: versus

Speaker 0: versus, you know,

Speaker 0: inspiration focused. Right?

Speaker 0: And so, like, I will stop you at this. This is another concept of, like, education educational

Speaker 0: versus motivational copy.

Speaker 0: Copy and even actually, we cover this as well on the unconscious in the unconscious mechanisms of conversion.

Speaker 0: So this concept of ratios, like, you can still have a bit of, like, you know, inspirational stuff early, but it's like for this sophisticated crowd,

Speaker 0: it needs to be, like, thirty to sixty

Speaker 0: seconds. Right? That meets their criteria. Okay. Cool. You've pumped me up for the workshop. Let's get on with us. Not, you know,

Speaker 0: not ours. And you any... You hear anyone who complain about webinars

Speaker 0: in terms of, like, get get to the...

Speaker 0: Point, they're the more sophisticated crowd. They're aware of the sales process. Right? So it's it's that type of stuff. Right? So expectations

Speaker 0: mismatches.

Speaker 0: And yeah, so this kind of, like,

Speaker 0: educational motivational

Speaker 0: copy

Speaker 0: attaches to us. And then actually, even just the concept of unconscious mechanisms of conversion,

Speaker 0: how that attaches to this is just in terms of ratios. Right? We do need a little inspiration always, but it's like just a small sprinkle. It's like seasoning for these people versus for more problems take people.

Speaker 0: The motivational stuff may need to be, you know, 80% of what's what's going on there because that's belief building. Their limitations are around, you know, limiting beliefs. Right? So the limitations of the kind of... The generalized limitations here will be more...

Speaker 0: Yeah. Actually, let's do this. Insert a table.

Speaker 0: One sec. Yeah.

Speaker 0: Generalized limitations of

Speaker 0: the orange crowd, the unsophisticated. We'll use unsophisticated unsophisticated just as a as a as a simple pointer here versus sophistic... Sophisticated.

Speaker 0: It's not this black and white, by the way, but just it's it's very market dependent. Plus, you people who are more of this unaware or someone aware, problem aware, zero to one beginner on sophisticated crowd, they're generally have one of the limiting beliefs of worthless,

Speaker 0: hopeless,

Speaker 0: or helpless.

Speaker 0: And so and

Speaker 0: so they're tip... Gonna typically be in a more low emotional state

Speaker 0: state. And the sophisticated market are gonna feel more worthy.

Speaker 0: The inversion was worthy, hopeful,

Speaker 0: and capable.

Speaker 0: And these are in a high high emotional state

Speaker 0: in general as well. Right?

Speaker 0: It's not always as black and white, but that's a good kind of gross generalization that you can you can take here from this. And so that... That's kind of attaching to that same that same thing as well. It's like, you know, don't waste my time. I'm worthy of my time not being wasted.

Speaker 0: Right? I'm capable enough. Let's get on with this. A little bit inspiration to hype me up is great, boss.

Speaker 0: I want I want a little bit more

Speaker 0: a little bit more

Speaker 0: outcome focused type stuff. Right? And so these people will be more

Speaker 0: outcome focused,

Speaker 0: and

Speaker 0: these people will be more

Speaker 0: emotionally focused. Right?

Speaker 0: In terms of like,

Speaker 0: you

Speaker 0: know, language.

Speaker 0: I suppose, you know, like this is like make me feel good.

Speaker 0: Feel good or they probably won't say that.

Speaker 0: Yeah.

Speaker 0: Whereas, you know, these people will say this if you mismatch the criteria,

Speaker 0: is like, you know, get on with this, get on with this, get on with this.

Speaker 0: When are we doing x,

Speaker 0: etcetera. Right? This type of stuff. So this would be

Speaker 0: this would be kind of an audit for your content

Speaker 0: as a

Speaker 0: as a...

Speaker 0: Based on my... On sophistication levels. Right?

Speaker 0: And so that's why I wanted to talk... I'm sorry. And based on, you know, stages of awareness because you'll have a, you know, you'll know if you're dealing with a beginner crowd in general or a more knowledgeable crowd. Right? And it's not always black and white, but this this is a good kind of binary

Speaker 0: way of thinking about how

Speaker 0: you're... You should be thinking of your content for them. Right? So, typically, this will wanna be more focused to the point content, and you have a little bit more space with these these crowds

Speaker 0: because, you know, they... They'll they'll they'll have they'll have bit more time to give in general.

Speaker 0: Okay.

Speaker 0: And so...

Speaker 0: Yeah. Some of this messaging stuff's good. Done with the self self evident versus a value of offers. We already dealt with that. Nature needs,

Speaker 0: that's more one time transient cyclical ever present. It's good. We've dealt with the microfluid problem. We don't wanna talk about nature need in regards to consumption.

Speaker 0: That, again, would slight, like, slightly attached to market criteria.

Speaker 0: Yeah. Then we can have kind of... Okay. Biom... Biopsychology.

Speaker 0: Yeah. This is good.

Speaker 0: Okay. So then you'll have towards in a way motivated. This is kind of actually

Speaker 0: nicely attached to

Speaker 0: nicely attached to this stuff as well. Right? These sophisticated markets will typically be more towards.

Speaker 0: These will be more away focused

Speaker 0: as well.

Speaker 0: K. I'm actually gonna zoom in here on this. I'll just start expanding this.

Speaker 0: Yep. And so, yeah, again, this this this this actually maps quite nicely at what we're just talking about as well

Speaker 0: in terms of, like, this would be the orange group,

Speaker 0: and this would be

Speaker 0: the yellow group. Right?

Speaker 0: Maps maps of of

Speaker 0: quite nicely onto us.

Speaker 0: Yeah.

Speaker 0: Yeah. The the convincing models are good to be aware of as well. This this would inform content for me as well in the... In in a similar way, mainly through time, Bryce.

Speaker 0: If you've... If you kind of have

Speaker 0: people who sit in this this cohort more naturally, you're... The... In the automatic channel, impulsive channel, you're gonna want content that's short to the point, direct, Bryce,

Speaker 0: whereas,

Speaker 0: you know, the the consistency and duration stuff will tend to be more more longer form content in general.

Speaker 0: And then the convince your channels, yeah, visual or auditory kinesthetic. This is kinda some of the unconscious mechanisms of conversion we talked about, as well as the kind of graphic design stuff in the members area. So that that kinda links into this as well

Speaker 0: and very loosely.

Speaker 0: Okay. Internal external reference option option versus procedural.

Speaker 0: No. These are these are market criteria.

Speaker 0: So,

Speaker 0: again, this would be more mismatching. Right? So

Speaker 0: if, like,

Speaker 0: the...

Speaker 0: Let me see if I still have the link to the members area here.

Speaker 0: I do.

Speaker 0: What's inside?

Speaker 0: No. You're kidding me.

Speaker 0: Yeah. Perfect.

Speaker 0: So this... The... These... This this is an example of, like, sociological factors that are, like, you know, extrinsically motivated,

Speaker 0: right, or externally... People who are externally referenced. Right? We have the other people using us. Right?

Speaker 0: So your

Speaker 0: your factors in your in your members area around other people using it, the five star reviews. These are more the things that are related to the externally referenced

Speaker 0: type of evaluators.

Speaker 0: And the internally referenced stuff is more the kind of, like, you know, claims and outcome based stuff. So even the...

Speaker 0: Like, this is more... I care about this if I'm more in the the internal reference stuff. It's like, what's the outcome of the product? Right? So this

Speaker 0: would be the same inside the consumption. Right? You know, it's a... There's a very fine line to straddle here

Speaker 0: on the... Because this Marcus

Speaker 0: is a mix of

Speaker 0: this market was a mix of

Speaker 0: of kind of low emotional, high emotional state customers. Probably,

Speaker 0: the ratio was kinda, like, seven to three, maybe the low emotional states state stuff, but the high emotional state customers in general were the the the bigger spenders.

Speaker 0: And so it's like, the problem you run into with those people is that they're... They tend to be very outcome focused and time constrained. And so you you come in here and you see a,

Speaker 0: you know,

Speaker 0: a seven day fast start series, and it's like, first video of this fast start is two hours long. So it's like this this kind of violated

Speaker 0: violated that criteria,

Speaker 0: but the way it was overwhelmed was through the quality of content. Right? The the the information being so so high value, that kind of overwhelmed this. Right?

Speaker 0: And so that's that's

Speaker 0: another example of, like, you know, this trade off where it's like, there are times where you'll want

Speaker 0: you'll want longer form content to be part of the the mix of what you're doing in your members area, but it violates, you know, the

Speaker 0: the the criteria

Speaker 0: of that audience. Right? They're more automatic, impulsive,

Speaker 0: and then internally reference people, and so they're more outcome focused, but it's... You know? And so if you if you if you give them long form content or you're gonna make them consume their time, you gotta be really aware of, like,

Speaker 0: is this adding value to them or not, or am I, you know, getting... Is this gonna... Are they gonna perceive this as boring and repetitive? How can I condense this? Right? So this would be another type of thing that you wanna be considering inside your members area for people in each of these these blocks. Right?

Speaker 0: Optional procedural as well. Like, if you have... You know, you can do this any way you want. Right?

Speaker 0: Type language for procedural people who want, like, the step by step. You know, what do I do on day one? What do I do on day two? Where's my checklists? Right? Here's here's here's

Speaker 0: an offer naming generator. So this is kinda like a widget that'll help them figure figure it out. Right? So all of the resources underneath of the the the fast start were kind of... These were... This was the kind of process stuff,

Speaker 0: and this this helps get people in action as well and moving them forward. Right?

Speaker 0: And so these these these resources here throughout the seven day fast start, in this example,

Speaker 0: they're not on every page, but they are they are they are designed to help this kind of, like, procedural people

Speaker 0: feel like they have a process, but also the optional people come in and kinda play with these things

Speaker 0: and get a sense of get

Speaker 0: a sense of

Speaker 0: just, you know, ideas. Right? And and so they they don't even they don't even need to get... They don't even necessarily define an outcome with with, you know, a naming generator. It's just like it's a source of inspiration.

Speaker 0: Whereas,

Speaker 0: you know, the same for the ads. The the value to them is just having the option. Oh, I have that ad there if I wanna come back to it. For the procedural crowd, it's... I want an ad so I can I can copy it? Right? Or have a a framework to work for. And so

Speaker 0: the

Speaker 0: the... You're you're probably gonna get... You know, your market will see it in one of these or the other as well. And so the... Also, the stuff we'll want to do,

Speaker 0: we talked about this at the very start of the call

Speaker 0: in the...

Speaker 0: Leading to limitations.

Speaker 0: Things that help with that leading... With the leading to limitations are around these kind of kind of attached to this optional procedural stuff as well in, like, worksheets,

Speaker 0: workbooks.

Speaker 0: Right?

Speaker 0: Worksheets.

Speaker 0: Like, I'm optional by my nature. Right? And and

Speaker 0: that's that's how my my work style is. Like,

Speaker 0: no two calls are the same. I tend to just, like, freely associate because that's how my brain works.

Speaker 0: And

Speaker 0: and and so even if... Whenever I buy products that have kind of any of these worksheets,

Speaker 0: I would more... I will be more of a scanner and looking for, like, key ideas outside of it. That's how I will derive the value out of it. Whereas procedural people will take the exact same consumable I will get, and they'll go through it line by line. They'll fill every single detail in. They'll miss nothing, And that will help, you know, ground ground ground them in. But that also will lead to

Speaker 0: a revelation

Speaker 0: and then

Speaker 0: personal personal limitations as well.

Speaker 0: Limitations

Speaker 0: that

Speaker 0: make them

Speaker 0: want to, you know, get get more support more support.

Speaker 0: Right? So this is kinda like how how some of the kinda like resources you add in here can do that. Like this naming generator, as an example... Let's just come back to this. I hope it's still live. I imagine it is.

Speaker 0: The economics calculator. Again, another one. Some people wanna know if they come to the economics calculator. They wanna have every single

Speaker 0: metric

Speaker 0: planned out. I wanna know what my CTR is, etcetera.

Speaker 0: I wanna know what my CPC is. I wanna know what my CPA is. I wanna know my my AOV.

Speaker 0: And this gives me math logic that makes me feel grounded in numerical data that my offer is gonna work. Right?

Speaker 0: And and that's more the kind of procedural crowd that will give them a sense of security. Right?

Speaker 0: Whereas the optional crowd will just be like, they'll come in, they'll look at the exact same thing, and it will just give them a sense of what's the possibility with this opportunity. Okay. I'll plug all my numbers in, but it's not necessarily I need this to believe this possible and probably already as an optional... The people who are more optional will tend to be more,

Speaker 0: you know, dreamer type characters who'll be kinda more future focused, maybe in a way that's unrealistic.

Speaker 0: But this... Whereas the procedural people will be more skeptical as, again, a bit of a generalization.

Speaker 0: But the the way the optional crowd will will will look at this will be more of a...

Speaker 0: What's possible with this, you know, if I if I sell 200 units a day and with an an AOV of, like, $80 and my CPA is, like, 50, well, that's, you know, that's $6 a day net on the front, that type of stuff. Right? Or if my ascension is this, well, I could really scale to 50 or $60 a month if I figure this out. Right? That's that's the way they'll use it. They won't need this fully to say my offer will work or won't. They'll just kinda get a sense. I'm building my offer. I just wanna see what what it could look like. Right? So the way people derive value will will vary massively based on on who they are, but they will...

Speaker 0: That's also appeal being built as well. Right?

Speaker 0: Appeal,

Speaker 0: revelation, or personal limitations will

Speaker 0: emerge. Right? And so one of the things that the...

Speaker 0: One of the personal limitations that can emerge from this automatic influence calculator is, let's say, someone has some previous

Speaker 0: experience running ads, and they know, well, my CPMs are a $180, and my CPC is $12.

Speaker 0: You know? And I can't make my my numbers my numbers work because that that... They just have anchoring to that. That will install an invitation, right,

Speaker 0: based on their their their lived experience. So, like, that's an example of how this component could potentially invalidate

Speaker 0: some of that

Speaker 0: some of that

Speaker 0: thinking, but the the point holds true is

Speaker 0: the point holds true in that it's

Speaker 0: it is... Something is happening. They're either they're either using it to to get a sense of

Speaker 0: revelation of this is what's possible in my off... Offer or the appeal of this. This is what will happen for for me if I do do this process or will reveal some sort of, like, personal limitation to them as well, which is kinda like what happens with, like, calculators, worksheets, etcetera.

Speaker 0: Yeah. Next would be the kinda hidden factors and constraints.

Speaker 0: Yeah. We've already touched on the hopeless, hopeless, worthless.

Speaker 0: It's good.

Speaker 0: Yeah.

Speaker 0: Yeah. This is this is more...

Speaker 0: You could use this actual what's... That what's possible call could be even used in in the content as part of your seven seven day fast start. This could be, like, day one. Right? You know, what's possible with insert your product, why it's possible, what made it possible, which is kinda, like, show proof proof of

Speaker 0: stuff in similar... People in similar situations.

Speaker 0: And and...

Speaker 0: Or show, you know, show that the... This actually could could can show proof of the changes in the environment that made it possible, and then what that means for you is show people in similar suit... What that means.

Speaker 0: You... And then what else?

Speaker 0: Yeah.

Speaker 0: That would be the way I'd price this.

Speaker 0: But, yeah, you could make this as part of your seven day fast start, and this would help

Speaker 0: this would help

Speaker 0: a lot of that kind of...

Speaker 0: You could do this quick and and have it fit both

Speaker 0: the kind of automatic convince or, you know,

Speaker 0: short short people

Speaker 0: who need... Or or high emotional state and also the low emotional state crowd can get... Still get some value out of this as well.

Speaker 0: Hidden limitations and constraints.

Speaker 0: Yes. Okay. So you have this time, money limitations, knowledge limitation, support limitations.

Speaker 0: These are... We've kind of touched on some of these,

Speaker 0: and this will kinda, like, vary vary based on the avatar. And so this...

Speaker 0: Again, with the whole team of this is architecting Ascension. You should be aware of what these limitations are in your product and that you don't speak to... This is gonna take a ton of time if they they only have thirty minutes a day. Right? You need to be aware of who the avatar is and how your... The the language you're in... You're having...

Speaker 0: The language you're injecting in there

Speaker 0: for them inside the content and how that can create, again, perceived limitations or have them reject

Speaker 0: the sales process by saying this or the... Even the the consumption of the product by saying, this isn't for me. I don't have time for this. This isn't for me. I'm not smart enough. This isn't for me. I I don't have the money to, you know, run ads as an example or whatever it is. Right? It's it's that that type of stuff. And so you you wanna be aware of these limitations

Speaker 0: and how you may be injecting

Speaker 0: injecting

Speaker 0: skepticism or doubt

Speaker 0: into the audience

Speaker 0: or

Speaker 0: personal limitation based on their their their circumstances,

Speaker 0: based on who they are, right, and the the way you're phrasing your content. So that's kinda where this is coming from in terms of how you should be thinking about this for Architecting Ascension.

Speaker 0: Okay. Then, yeah, the hidden goals, desires, objections, belief. You know? So this is kind of attached to the primary and secondary payoff stuff we talked about as well. So the the the surface, you know, I wanna lose 20 pounds as a weight loss exam... Example.

Speaker 0: That may be the... That's the overt... The primary the primary outcome. But the secondary payoff is so that I can be more desirable to the opposite sex, so that I can, you know, get a promotion, so that I can feel worthy, so that I can be... You know, feel like I did when I was, you know, 20 again, like, whatever whatever it is.

### 1:30

Speaker 0: And these are the kinda, like, downstream things that they won't always necessarily

Speaker 0: articulate.

Speaker 0: But being aware of what these are are things you can inject into the content. Right? If you go have a weight loss product

Speaker 0: and

Speaker 0: and you...

Speaker 0: You're you're you're purely focusing on the on the the the weight loss components,

Speaker 0: if you sprinkle a little bit of this, you know, how they'll how they'll how they'll become more,

Speaker 0: you know, be seen as, I think, one of them safer,

Speaker 0: smarter,

Speaker 0: sexier,

Speaker 0: or seen is... Seen this phrase

Speaker 0: phrase used before

Speaker 0: as a way of kind of articulating

Speaker 0: ebbs your offer, makes someone feel safer, smarter, sexier, or seen. Whereas, it's kind of

Speaker 0: attached to the secondary payoffs as well. Right?

Speaker 0: And so if your content is very functional and stuck here in the the the primary outcome and doesn't have any of this belief building stuff, because this this, you know, these are... These build appeal

Speaker 0: and our belief builders

Speaker 0: builders,

Speaker 0: you know, depending on depending

Speaker 0: on what what the actual content

Speaker 0: context is you're talking about some of the the secondary payouts are, but they're doing one of... They're doing some of this. Right? And so if you have a very functional, you know, flat product

Speaker 0: with with

Speaker 0: with

Speaker 0: minimal,

Speaker 0: you know, belief building type stuff going into us around the secondary payoffs,

Speaker 0: that's... That doesn't kind of stimulate

Speaker 0: that desire

Speaker 0: to keep going or to do... To to to to work with you or, you know, work with the business

Speaker 0: and work and with the business and

Speaker 0: engage in any secondary transactions. Right?

Speaker 0: So

Speaker 0: that's just how you would implement that.

Speaker 0: Yeah.

Speaker 0: Oh, yeah. We had core beliefs. So this kind of identity stuff as well, Bryce.

Speaker 0: Just... This is this is...

Speaker 0: If you violate if you violate,

Speaker 0: you know, people's nonnegotiable stuff,

Speaker 0: you know, where religious or spiritual con... Convictions in the product,

Speaker 0: professional ethics, cultural beliefs, you know, they will

Speaker 0: they will reject reject the

Speaker 0: they will reject the

Speaker 0: consumption. This is, like, dis... A disengaging factor. Right? So it's like, you just be aware of the identity of the of the person you're making stuff for in the audience as well.

Speaker 0: That's that's really important as well.

Speaker 0: Yeah. Let me really sort of touch that to us.

Speaker 0: Yeah. And so then this is the pre and post purchase stuff. We've already talked about this.

Speaker 0: Yeah. Now Heather... Or sorry. Hendra asked this question here

Speaker 0: in the live launch lounge before we got started.

Speaker 0: This this is what...

Speaker 0: This is one thing you wanna be aware of. Or sorry. This is the kinda, like, three the three schools of thought on back end cannibalization. It's like there's always a trade off. It's like, do I want...

Speaker 0: You know, this is the kind of like...

Speaker 0: This is the two thousand

Speaker 0: two two thousand and ten model. Right? Where, you know, on ClickBank.

Speaker 0: Where it's like, what can we do to, you know, architect friction in the product so the people just get bored, get lost, and don't refund and come back late... And and say they'll come back to this later when they have time. Right? And so, like, you know, that's that's that's how that's how that entire

Speaker 0: model worked with regards to

Speaker 0: with regards to product development for front end for front end products.

Speaker 0: And this disengages people from from

Speaker 0: Ascension. It does make them

Speaker 0: work through the kind of challenges they have, but, you know, this is really the the bigger risk. They get frustrated, they abandon the product. Right?

Speaker 0: Then the second kind of, like, school of thought, this is give them enough for pro...

Speaker 0: For progress. So, like, what do they need to do to get measurable movement in the right direction and give them momentum towards the goal? So, like, the AC example is perfect to this. This gives them a sense of momentum.

Speaker 0: It gives them mental and numeric... Numerical evaluators.

Speaker 0: The the ads does as well. It gives them something that makes them feel like, hey. I could use this as well. Right? I now have ad copy that I can model.

Speaker 0: And so, you know, that that doesn't seem as intimidating anymore.

Speaker 0: The same with the economics calculator.

Speaker 0: What was the old one? The economics calculator.

Speaker 0: The market selection matrix. Right? The offer naming convention.

Speaker 0: Of our name generator.

Speaker 0: So

Speaker 0: lots of... These things all

Speaker 0: these things all

Speaker 0: built up the

Speaker 0: built up the...

Speaker 0: I gave them a sense of progress, right, which builds up appeal and lets them take ownership of the the product and the outcome we can generate for them. Right?

Speaker 0: So

Speaker 0: that's the the same. You could apply the same same type of thinking in in,

Speaker 0: you know, anything, you know, health related stuff where it's like, you know,

Speaker 0: this type of stuff where it's just like, okay. The the simplest example of this is,

Speaker 0: you know,

Speaker 0: if you had, like, I don't know, health offer, diabetes offer, let's say, an example, and you have a quiz. Right? That's an evaluator for their current situation.

Speaker 0: And so it it it gives them a sense of just ownership of the problem by getting some sort of, like, die... Diagnostic. And and that's even though they haven't done anything, it does give them a sense of progress towards taking ownership of the problem, which also builds appeal. Right? I have diabetes. I've got a diagnosis for now, etcetera. Right?

Speaker 0: And then there's the other kind of school of thought where you just, like, you you

Speaker 0: give everything possible away through the through the core product and then

Speaker 0: get get people moving moving forward

Speaker 0: and

Speaker 0: less air quality and relationship drive essential. And that's actually kind of more where we're operating here inside of NHP, I suppose. Like, we're trying not to hold anything back. It's like, let's let's give it all away.

Speaker 0: And it really is... It's... This is a trust building process. Right? You you were... We're not we're

Speaker 0: not holding

Speaker 0: things back, but you guys... You know, this is a sophisticated market.

Speaker 0: This sophisticated market.

Speaker 0: And then this would be, you know, unsophisticated.

Speaker 0: And so that gets kinda like part of the part of the reason we're we're in this kind of like, we're certainly here at bare minimum,

Speaker 0: but we're debt... We're at... We're more we're more likely here. Like, we'll workshop with people. We'll, like, do hot seats. There's hot seats every week. We'll help you move things forward. We'll look at ad copy, whatever you need. Right? It's like we're giving you as much value as we can, and then the people who come into the coaching programs really are just like, I wanna go faster. I want more help, or I enjoyed your coaching style, Kevin or Lauren or Charles or Brandon or, you know, Robert or whoever.

Speaker 0: And, you know, they they... You guys move up based on that, not based on us holding it holding it back. It's just getting more faster. Right? It's that type of stuff. Right?

Speaker 0: So

Speaker 0: then this kind of, like, failure mechanism as a catalyst. This kind of is attached

Speaker 0: to... Alan has talked about this in the...

Speaker 0: Is it the... What call is this?

Speaker 0: I think he called about this specifically. Where is it? Wherever... How long is it? This. Alan talked about this. Alan talked about this

Speaker 0: in the...

Speaker 0: It's the name of the call. It's the one that

Speaker 0: was shared by Nick in the lounge. Is this call a normal serve?

Speaker 0: Well, I can't remember what you call.

Speaker 0: It's the name of...

Speaker 0: It's calls for argument call. I think that's... Yeah. It's the calls for argument call.

Speaker 0: Yeah. I'm almost sure it's that call.

Speaker 0: And this

Speaker 0: isn't about, you know, architecting,

Speaker 0: you know,

Speaker 0: architecting failure for them, but it is... It's essentially

Speaker 0: it's essentially very similar to the the... What we talked with here at the very start, which is the

Speaker 0: unsolved criteria through the...

Speaker 0: Here.

Speaker 0: Leading to limitations. Right? They

Speaker 0: they will... By naturally interacting with the product and because they're engaged,

Speaker 0: they have a

Speaker 0: they have a...

Speaker 0: They they... Their their limitations will will be revealed to them. Right? And so

Speaker 0: you're not you're

Speaker 0: not...

Speaker 0: Where is this?

Speaker 0: It's here.

Speaker 0: Yeah.

Speaker 0: Yeah. You're not you're not architecting failure for them in the product, but it just kind of... It it... It's a it's a byproduct of of of working. So they'll they'll they'll have some some lack of skill or lack of capabilities, lack of knowledge, lack of expertise, whatever it is. And it it it gets it gets exposed by things like worksheets. Right? Exercises,

Speaker 0: check

Speaker 0: points.

Speaker 0: Yeah. This this type of stuff, and then you can position the back back end as a natural kind of

Speaker 0: way out of that. Right? So this this helps architect Ascension as well via things like worksheets. Right?

Speaker 0: Yeah. And so part of what's going on, if they're not... The the way the the way people will ascend

Speaker 0: is through again a psychological journey. Right? And again, this is the the kind of the importance of consumption

Speaker 0: leading to ascension.

Speaker 0: And, like, the people who just have, you know, functional products with no care gone into them, this... They did... And they disengage people. That's the problem they create. They don't get any awareness, understanding, experience of the problem, and then knowing that

Speaker 0: they've

Speaker 0: that they've...

Speaker 0: You know, they they can't do do things on their own. And so, you know, they they... As a result, they'll... They won't...

Speaker 0: They they can't they can't come up to the back end because they're disengaged from disengaged from the process. So this

Speaker 0: the psychological journey gets cut off, you know, even though they know the problem or opportunity exists, they land in your member's area. They don't they don't trust the the content they're consuming, and they leave as a result. Right?

Speaker 0: Okay.

Speaker 0: Installing criteria leading to limitations is similar to what we've already touched on.

Speaker 0: Yeah. Yeah. Exactly. So this is actually said better than what it... The way it's said earlier, but position your back end as as the standard by by something what what good looks like. So language pattern, the best x y z look like this and this. Professionals in the field always do this. The difference between amateurs and experts is, right, you install

Speaker 0: criteria

Speaker 0: in in the content that creates a natural

Speaker 0: gap between

Speaker 0: having the the outcome or not, and that that builds appeal. And then it creates, you know, positions the back back in the standard, creates self self qualification mechanism. I want to be in this group similar to the in group, out group stuff we talked talked talked about, And then let's conclude they need more help rather than being sold. Right?

Speaker 0: And then, yeah, lean limitations.

Speaker 0: Yeah. Yeah.

Speaker 0: Yeah. Yeah. Yeah. Yeah. Yeah.

Speaker 0: But this is the... Oh, this is more... Yeah. This is more in checking thoughts.

Speaker 0: Yeah. Yeah. Yeah. Similar to what we talked about already, but that's that's good.

Speaker 0: Yeah. The mechanism stuff, I wouldn't wanna lean on too much.

Speaker 0: These are fine as well.

Speaker 0: More more... Yeah. More content stuff. No.

Speaker 0: We're starting to get to the...

Speaker 0: Some stuff here towards the end I definitely wanna touch on. I feel like this is... So this I have...

Speaker 0: What I did was I took initial notes, and I kinda spoken to

Speaker 0: I spoken to,

Speaker 0: you know, like, Whisper Transcribe

Speaker 0: and dump this into...

Speaker 0: Clawed against my own notes. And so it's hallucinated a little bit of some stuff that I wouldn't necessarily wanna fully include in this, but it's got me a good

Speaker 0: good framework to work from. This is fine.

Speaker 0: Oh, yeah. This

Speaker 0: this is really useful. And it's not even from the catalog model. Just being aware of this,

Speaker 0: thinking about this through,

Speaker 0: you know, what you could think of it in the catalog model.

Speaker 0: Transformational journey, Bryce.

Speaker 0: The the transformational journey, Bryce, before they start solving the problem while they're in motion via your product.

Speaker 0: And then after after

Speaker 0: the the product new problems exist, and this this will give you an exam...

Speaker 0: Ideas for secondary products.

Speaker 0: But this will kinda give you

Speaker 0: sim... Similar to what we talk talk with. This is, like, problem solution and then transformation. It's another way of thinking about this. But when they're interacting with your product,

Speaker 0: thinking about the the the obstacles they run into in in motion

Speaker 0: also creates that

Speaker 0: personal awareness of

Speaker 0: their lack of capability to maybe do do things on their own. So, like, the craving to... An energy, for example, in a weight loss context are great, but it's also, like, let's say they have to do weight training and they don't have good technique, or let's say they're getting, like, muscle delayed onset muscle soreness as well, or just generally, like, you know, feeling low low energy.

Speaker 0: It's covered here.

Speaker 0: That type of stuff kind of what... Like, what I need a coach or maybe am I not eating enough or am I eating too much? And so then then all of those lingering doubts start start creeping in in terms of their own thinking. And so that that that creates, you know, a a post evaluation where it's like, don't I don't know if I'm doing this correct or not. I need expert help. Right? So being aware of the kind of obstacles they run into inside the product can be useful

Speaker 0: in terms of

Speaker 0: how... Understanding how that builds

Speaker 0: appeal to get help. And...

Speaker 0: Yeah. Yeah. Just... So sometimes you can help reveal some of this through that kind of worksheets worksheets

Speaker 0: or even components of the product that we we talked about earlier as well.

Speaker 0: Sorry.

Speaker 0: Yeah. That we talked about earlier

Speaker 0: in terms of

Speaker 0: how you create content

Speaker 0: that

Speaker 0: helps to to to to

Speaker 0: make them meet these obstacles quicker. Right? So for example,

Speaker 0: the ad template here inside

Speaker 0: the AC

Speaker 0: offer page,

Speaker 0: this actually gets them interacting with the obstacle of I don't know how to run ads. I only have one ad. Right?

Speaker 0: So it's like, they were given an ad. It gets them in motion, but it also the secondary consequence of that as well. I need more. Right? Or is this one working? Or it's not working for me? Or have I set it up correctly? Right? All of these new obstacles start emerging when they get in in motion with that component. Right?

Speaker 0: And not because you've done anything wrong to architect

Speaker 0: this obstacle. It's just a natural consequence of of of of moving forward. Right?

Speaker 0: And yeah. These... Yeah. This this is good. These these these are... This is the the kind of the the bump bump concepts. So you've four types of bumps. You can have optional bumps. You can have additive bumps. You can have adjacent bumps. Or you can have accelerants.

Speaker 0: And the option are kinda more of nice to have category. Additive enhances the core outcome of the core product. Adjacent solves a related problem. So, like, if you had a weight loss problem and you had something for excess skin, the excess skin is kind of a... An adjacent problem. And then accelerants would just be stuff that gets them gets them there faster.

Speaker 0: These

Speaker 0: these are...

Speaker 0: You can think of your your back end

Speaker 0: as having some of these these function... Functions to it as well.

Speaker 0: I think of upsells and through this through this lens as well. One of the upsells I was working on recently in live launch

Speaker 0: for... I won't name won't name who we're working on. Anyway,

Speaker 0: they were they

Speaker 0: were framing the content in an optional way in the... For upsell too, the way way we were talking about it, and I was trying to make it more of an accelerant or additive in terms of the framing. So

Speaker 0: speaking in broad terms, they were talking about it being, like, a daily email that we were gonna send to them while I was saying, no. This is, like, daily tactics and skills for insert whatever, you know, problem we're solving. And so it became more additive and compounding to the to the

Speaker 0: to the out... The the the core outcome of the front end product

Speaker 0: rather than it being, you know, an optional daily notification,

Speaker 0: which is the way it was kind of being done with the framing and the copy. So that made it feel more, like, additive or an accelerant to a better version of the outcome

Speaker 0: in in the way I'd framed it rather than just simply being, do I want to subscribe to this random email list that I'm not really sure how it works. Right? So that was that was the that was the kind of the

Speaker 0: the the con... The contrast of how you can think about that. And you can think of any of the components you add to your programs in... Through the same lens. So your back end and and anyhow you frame it. You know, we're gonna work with you for x, y, zed weeks. These are the things we're gonna achieve.

Speaker 0: It's like, are you are you framing these things in a way that are

Speaker 0: optional out of... Adjacent

Speaker 0: or accelerants to the the core outcome they want. Right? And that's... This is another one that it can be kind of very hidden in plain sight where you'll have a lot of this... You know, people will use... Even just... It can be the same deliverable, but you just use language that's...

Speaker 0: You use language that

Speaker 0: language that doesn't doesn't have a clear outcome focus or just, again, feels optional. And so it makes the product feel feel more nice to have. And so it's like, well, why do I need this? An example would be, you know

Speaker 0: you know, we have, you know,

Speaker 0: we have... As part of your program, we have, you know, twenty four four seven round the clock support.

Speaker 0: And it's like, there's no specifics about what that support will do for you,

Speaker 0: what what what that what that means. I have to kinda, like, fill in the gaps. So it feels like an optional add on, whereas it's like, no. We have twenty four seven, you know,

Speaker 0: technical support on how to use the software where someone will, like, you know,

Speaker 0: guide you to the exact resources you need when you're when you're setting something up. Now it's like, okay. This is gonna make make things easier. So it reduces limitation,

Speaker 0: whereas same same deliverable

Speaker 0: just in the initial framing, it's just not articulated properly, and so it makes it feel more more more optional for us.

Speaker 0: And so it doesn't enhance enhance the perceptual value of the actual outcome.

Speaker 0: And then the identity upgrades.

Speaker 0: Yeah. Yeah.

Speaker 0: And then this... Actually, this would attach us to the void call as well.

Speaker 0: And so, yeah, current identity,

Speaker 0: aspirational identity, who they want to become through the product. So just being aware of that, like, who who this person is becoming

Speaker 0: through through your back end

Speaker 0: is extremely useful as well as that's... You can... Again, seeding this in content. Like, a lot of how you do this is is through seeding this in content. It's like,

Speaker 0: you know,

Speaker 0: again, similar in this in this...

Speaker 0: Yeah. Meeting the need versus fulfilling the need.

Speaker 0: Like, a lot a lot a lot of this a lot of this content

Speaker 0: here is create... Is installing the identity of being an offer owner. Right? And so that becomes the aspirational identity when you're consuming

Speaker 0: the the product

Speaker 0: for for all my clients. Right? And so they then want that outcome, and they want they want all of the the capabilities of someone who knows how to create offers, write ads,

Speaker 0: etcetera.

Speaker 0: And and because they're now moving towards towards that, that builds again the the appeal for the back end. If you miss some of that aspirational identity

Speaker 0: transformation,

Speaker 0: and then these these attach,

Speaker 0: yeah, the secondary payoffs as well.

Speaker 0: And so you just gotta be aware of what that is. So, like, Ooj, the offer you're working on, the secondary payoffs are really what's driving a lot of it. Right?

Speaker 0: And it's, you know, you

Speaker 0: can even think about the the... Some of it's wanting to go back and feel like, you know, young again, and some of it's also getting back a sense of control. Right? And so that's that's kinda like that that transformational identity. And so the functional description of the primary outcome that the product can deliver,

Speaker 0: while

Speaker 0: some guys will fill in the gaps if, you know, if you leave out these kinda, like, secondary downstream consequences

Speaker 0: of of who they become after they've taken back control of this in the content. If you just ignore that and let them fill in the gaps without themself,

Speaker 0: then they'll be lost. And remember the way we were working on your sales copy

Speaker 0: for your your... This... That was the same type of problem that was missing there. It was just like a quick bullet point type line, and then onto the next one, they had to, like, fill in all the thoughts. Whereas we... When we expanded it, the story kinda, like, had a lot more bite to it because

Speaker 0: you you were sucked in based on on having more of a narrative about that transformation. Right? You could see what the... Why why are we talking about this became more obvious. Right? So the same problem has the potential to emerge in the product if you're not mindful of it. Right?

Speaker 0: That makes sense?

Speaker 0: Then, yes, timelines as well are very important.

Speaker 0: Yeah.

Speaker 0: Yeah. So, again, in anything that gets people interacting with the product is extremely important. So worksheets, checklists,

Speaker 0: progress tracking,

Speaker 0: stuff, milestones, celebrations are great, quizzes, assessments,

Speaker 0: anything...

Speaker 0: Checklists is... That... That's already there. Anything that anything that gets them taking all of what these are doing, right, is getting them

Speaker 0: Right? And so what's happening here is is, like, people are taking ownership of their their personal version of the problem and how it looks and pay for in some seem... Seemingly measurable way. And so that kind of is almost like putting them in a more associative state

Speaker 0: States, they're engaged with the... They're engaged

Speaker 0: they're engaged

Speaker 0: and self identify with

Speaker 0: the with

Speaker 0: the

Speaker 0: the transformation for themselves, for us.

Speaker 0: For yourself,

Speaker 0: through the offer, price. They'll they'll they'll want us or they'll they'll realize how far they are away away from it based on on on that.

Speaker 0: Yeah. We kind of talked on this avatar specific delivery with the orange and yellow stuff for it earlier.

Speaker 0: Yeah. We kinda hit on all this already.

Speaker 0: Yeah. Yeah. Some some some... If you're dealing with stuff that has kinda like, you know, stigma attached to us or like, you know,

Speaker 0: that type of stuff.

Speaker 0: Yeah. Yeah. This this is small stuff.

Speaker 0: Yeah. So then there's some, like, tactical stuff, which is good. You know, seeding, you can see this here, Bryce.

Speaker 0: Back to course previous lesson. Next.

Speaker 0: There was... It worked... This work with those buttons is kinda here floating around. You could even have under here, like, you know, want more help with, you know, insert your problem, click here, and then it just brings them over to whatever the page is. Right?

Speaker 0: So it's, like, strategic strategically seeing that, and then you can see that inside the content. You can talk about transformations inside the content that that help that help do those. Over mention of the back end offers where where relevant in the content is extremely important.

Speaker 0: Bonus training that locks when they take the next action, kinda already hinted on some of those, and then case studies

Speaker 0: as well, you know, near key decision points like late in the seven day fast start.

Speaker 0: You could talk about scaling and optimizing your offer and have a case study attached to this. In this example, I'm I'm I'm not even sure if there is one.

Speaker 0: No. But you... This would... This... You could have quite easily have a case to the example here and speak speak to some of that, and that would help build appeal as they're coming to the end of the... Of that. It builds builds more desire to kinda get more support and help us. Right? And then outside the members area, there's retargeting ads to buyers driving them to the login. These will be really basic. I've talked with these before, but this can be, like, $5 link click ads

Speaker 0: for, you know,

Speaker 0: any purchasers

Speaker 0: within kind of, like,

Speaker 0: you know, fourteen to thirty days.

Speaker 0: And the objective is just get them back in... Back back back into the members area. You can also have video ads,

Speaker 0: you know, like, 30 to 50 of them, 50 of them, and you can attach the kinda like problem

Speaker 0: problem

Speaker 0: problems

Speaker 0: or or, you know, market sophistication stuff, the yellow and orange stuff we talked about earlier.

Speaker 0: Problem or solution,

Speaker 0: a component here,

Speaker 0: thinking here.

Speaker 0: And so, like, you know, if you have a more sophisticated market, you'll still have lots of ads, but it's more teaching them how to make micro micro progress forward via the offer

Speaker 0: in the in the retargeting.

Speaker 0: Whereas the problem state crowd, you would just speak to get more of the problems and the symptoms they're having as well as any co occurrences

Speaker 0: that might be coming along with this as well of not solving the the the the offer or things like the cost of an action price.

Speaker 0: So for problem crowds... Yeah. Let's do this.

Speaker 0: And then for the solution crowd,

Speaker 0: more direct.

Speaker 0: Again, the goal here is just getting them to consume more more con... Goal here is getting them to consume more, like, contextually relevant stuff attached to the purchase that kind of, like, gets them either coming back to the product or even if they've consumed the product for enough of it. Just keeps building appeal. So maybe when they see one of your emails, it's like, oh, I do wanna work. Let me go and see what that call booking page is all about. Maybe I wanna work with people. Right? Same with email sequences and then... Yeah.

Speaker 0: Yeah. Testimonials.

Speaker 0: Yes. Yeah. Yeah. You can actually... That's that's good. Testimonial request to us

Speaker 0: success.

Speaker 0: You know, you can actually, like, celebrate them via the email, etcetera, that type of stuff too. Concierge closed, we talked about this as well.

Speaker 0: You know, the whole... The kind of theme is let me guide you through the product.

Speaker 0: Promises, this isn't a sales call, so we're making you you you... I'm sure you get results or get kind of the value you want, total value to do that... To to doing that, compresses time to value, builds trust and relationship, creates belief in the outcome. They'll see the path, and, naturally, it's the secondary transactions.

Speaker 0: Also, it helps you evaluate all of the other stuff we talked about right up at the start of the call. We'll go back back over, plus,

Speaker 0: you know, how... Where you can improve the product and that

Speaker 0: type of stuff

Speaker 0: that,

Speaker 0: you know you know, how

Speaker 0: willing people are are to get on the phone with you or, you know, just their energy go up or down, that the energetic stuff, all of that type of stuff attaches to that as well.

Speaker 0: Yeah.

Speaker 0: These these these metrics are hallucinated. I would ignore those.

Speaker 0: What you wanna be looking for is activity. After after doing these onboarding calls, you wanna be, like, they'll reach out via email. They'll reach out via DM. They'll start interacting in your communities more. They'll start asking questions based on specific content. Right? If you're not seeing that,

Speaker 0: that type of stuff, reach out.

Speaker 0: Yeah. Ems.

Speaker 0: Reach

Speaker 0: out reach out in communities.

Speaker 0: They'll start they'll start

Speaker 0: asking

Speaker 0: for support

Speaker 0: based on content

Speaker 0: that you guided them to

Speaker 0: or

Speaker 0: they asked

Speaker 0: where it was.

Speaker 0: Right? And so

Speaker 0: this is the the... You want you want to see secondary interaction. It's essentially the the the downstream payoff of the success success

Speaker 0: metrics wise, you know, of of this onboarding call or just call bookings. Right? Maybe they they enjoy the onboarding call so much. Hey. Do you wanna work with us as a soft sell? They'll come over because they kind of believe in believe in believe in you based

### 2:00

Speaker 0: on that experience. That's one of the other benefits of it, boss. The

Speaker 0: the...

Speaker 0: You know, you you want to be seeing

Speaker 0: high energy secondary secondary interaction

Speaker 0: somewhere within, you know, two... You know, twenty... Twelve to forty eight hours of that onboarding call from a large percentage of the people who've gone through that. Because you've you've... What... What's happening here with this is you're giving them moments

Speaker 0: and belief builders

Speaker 0: builders

Speaker 0: on the call,

Speaker 0: you know, mainly around, oh, you know, the belief builders, this is a real business. These people care about us. So it's like, they should then care more about the product because you you send over it so the product can generate real results based on the fact that they're willing to send over us. So they engage with the product, and then as a result, this this stuff should start happening. This stuff's not not happening. You you have product issue more than likely. Right?

Speaker 0: Yeah. Yeah. Some of these email campaign stuff is good.

Speaker 0: We already talked about this ad ad ad campaign stuff. Yeah. This is video volume. Yeah. Yeah. This is the video of your campaign's good. It's great.

Speaker 0: And then, yeah, these these content... Top questions, doubts from sales calls, handle any objections, case studies,

Speaker 0: client testimonials, and reiterate the unique mechanism of your product across multiple videos as well. That's that's useful. These are all these are all good ideas for ads for video content.

Speaker 0: Yeah. This... Ignore this.

Speaker 0: This is

Speaker 0: hallucinated.

Speaker 0: Okay.

Speaker 0: Yeah. So we had a couple of questions as well in the live launch lounge about this. So it's like, hey. You know, you... You're... If you're choosing the right full format for just offers in general,

Speaker 0: self evident offers, more short form.

Speaker 0: These will be more high emotional state people.

Speaker 0: And then for the value of low emotional state crowd, you're gonna want more long form long form audiences. Right?

Speaker 0: Long form... Long to long form page.

Speaker 0: Yeah. How do you create a great first impression? I think this was your question, wasn't it?

Speaker 0: I think we've we've largely covered this. This, right, where it's like, you know, mismatch between claims, qualitative factors, design elements,

Speaker 0: anything we can do to compress them to value that that concierge

Speaker 0: close, any moments,

Speaker 0: or anything you can guide them to will help them stop is is is is great. Product quality stuff and anything you do to kind of, like, exceed expectations. Right? This is is how we create create good expectations. If you come to a clunky, weird,

Speaker 0: poorly thought out members area,

Speaker 0: That's, you know, that's what'll happen. Right? So it's like, we do... This is so common in direct response. All the care goes into the sales cycle, zero care on the product. Right? And it's like those days are

Speaker 0: not coming to an end. There'll always there'll always be a a place for that because there's just always people who will be short term thinkers and, you know, will just, you know, push marketing to... Marketing claims. But the more you focus on the other stuff,

Speaker 0: the easier the whole... What... If you're good good marketing and sales and you have great product, your life's gonna be a 100 times easier than without it for us.

Speaker 0: Yeah. And then what creates more is more low low low production values, chaotic UX, no brand continuity, content doesn't match the sophistication of the sales messaging we touched on this as well, the webinar example we talked about earlier, missing components or bonuses. Right?

Speaker 0: Yeah.

Speaker 0: Yeah. Yeah. Yeah. And so, yeah, refund rates is actually going... Yeah. If you're getting 3% of people who are saying, actually, give me my money back, there's another eight to 15% who are considering doing this, and I've equally been invalidated. So the 3% refund rate is not a 3% rejection rate. You're having a significant number of people who are disengaging.

Speaker 0: And these are... Then...

Speaker 0: Anyway, it's just a good good useful, you know, refund rates are are are also a proxy for satisfaction and, like,

Speaker 0: what... Like, a one to 2% isn't just a 1% change. It's, a 100%

Speaker 0: more people are unsatisfied is the way you can think about it. Right?

Speaker 0: Yeah.

Speaker 0: Yeah. Okay. And then these exercises are definitely useful. In particular,

Speaker 0: you know, what problems we come before your solution, what obstacle emerge while implementing, what new problems arise after success with the product, what scales and limitations do they they have, what co occurrences can you address that they have, and what accelerants can you offer. This is...

Speaker 0: These are very useful to think about before

Speaker 0: making your content because you can kinda speak to some of this stuff. This references their lived experience

Speaker 0: before

Speaker 0: meeting... Before, you know, doing anything.

Speaker 0: This

Speaker 0: will reference their momentum with the product.

Speaker 0: This will reference the

Speaker 0: life after the product,

Speaker 0: after the transformation.

Speaker 0: And then this... These will these

Speaker 0: will highlight, you know, reasons they'll want support

Speaker 0: or just... The concurrences are useful because

Speaker 0: the... I I would think of this more as...

Speaker 0: You can... These are more, like, symptoms that you can potentially speak to in the Adler. It's probably not as useful for actual Ascension, although you can put... Potentially hit on some of that for for

Speaker 0: your, like, book a call pages about some of the other stuff that they're having problems with. Right?

Speaker 0: And then, yeah, this this this can... This is this...

Speaker 0: Now that you're aware of, like, some of these co occurrences or limitations or any of these problems, it's like, what can we do to address these in the product or via secondary products? That's kind of what what comes out of this. And so this... These these are again...

Speaker 0: There's monetization opportunities here.

Speaker 0: And there's also

Speaker 0: there's also

Speaker 0: product enhancement opportunities here.

Speaker 0: And you're probably... You're thinking on that should really be, I should monetize this if they're largely hap... Happy with the product.

Speaker 0: I should be thinking about this as monetization. I could sell something new. If they're all happy with the product, it's... I wanna be thinking more on enhancements. Right? That's probably the the the way you should be thinking about it. So, you know, what accelerants or, you know, product reworks

Speaker 0: enhancements

Speaker 0: and your offer.

Speaker 0: Yeah. Then even this, you know, the consumption stuff, where are they disengaging?

Speaker 0: Yeah. And then the the failure mechanisms which we talked about earlier, it's like not designing that they fail, but it's like, what exercises are are you doing that helps them naturally expose to limitations. Right? How do you position your back end offer

Speaker 0: at those moments as a... In a way that, you know, helps them overcome those limitations,

Speaker 0: and then the concierge urge close stuff is is there. So that's

Speaker 0: this AVK.

Speaker 0: Yeah. I wouldn't worry about this.

Speaker 0: All that exercise out.

Speaker 0: This is good.

Speaker 0: Yeah. This would be useful as well.

Speaker 0: Yeah. This is this is just useful around thinking around some of the content. I don't think these these are probably the two,

Speaker 0: three, four, and five are probably the most valuable ones of this. This is more just kinda, like, generalized thinking.

Speaker 0: Okay.

Speaker 0: Any questions, guys? I kinda went through this in a bit of a whistle stop tour. Has this been useful? I kinda feel like this was a

Speaker 0: this was a

Speaker 0: philosophical

Speaker 0: call. I don't know. I think I'm gonna probably

Speaker 0: I don't know. Maybe maybe maybe we should do a design version of this call as well.

Speaker 0: Like, where it's like, how how would we design content or members area around that for a specific offer?

Speaker 0: That may be the expansion of this.

Speaker 0: But,

Speaker 0: conceptually, this is a lot of what what goes on. This is a lot of what I'm thinking about about how we

Speaker 0: how we,

Speaker 0: you know, architect Ascension. These are the types of things that you need to be be mindful of. And,

Speaker 0: again, a lot of this... I don't have all of this top of mind at all times. It's like a library of things I'm thinking about. They kind of, like, emerge subconsciously as I'm interacting with the offer.

Speaker 0: And and...

Speaker 0: But but if you want a a

Speaker 0: good checklist of kind of things to think about, this is a lot of what's going on. And so it's like... You know,

Speaker 0: to reach Architected Ascension, it starts, you know,

Speaker 0: it starts with kind of the the foundational thing that needs to happen is consumption. Right? And that's really where where, you know, coming back to where

Speaker 0: we where we started. Without this

Speaker 0: without this, they cannot

Speaker 0: ascend to other other other product components

Speaker 0: or

Speaker 0: back end offers. They just... They can't they can't do it.

Speaker 0: And so, really, this is the kinda, like, nucleus. All of this thinking is built around, and everything else is kind of, like, a revelation of the benefits

Speaker 0: of of

Speaker 0: getting

Speaker 0: increasing... Of of increased consumption price.

Speaker 0: And

Speaker 0: what what what what actually happens when we we get to to to to to

Speaker 0: to... When people engage with the product. Right? So that's that's really what what the whole the whole theme of the call was about. There's questions here in chat.

Speaker 0: Sorry. Be cool to show us. Yeah. Yeah. I think I think some design stuff we we would do. I think I might just get some samples of, like, how I would structure members areas with maybe, like, ClickFunnels or

Speaker 0: and maybe some scripts for, like, email and book a call stuff. I think I might do that for Architecting Ascension two point o, where it's, like, one point o is theoretical and two point o is tactical practical.

Speaker 0: So I think that's what I'll do. I'll do a two point o version of this call, and I'll get some scripts and

Speaker 0: screenshots of stuff that I think would be useful to include for everyone across whatever platform platform we're building.

Speaker 0: Okay.

Speaker 0: Any other questions?

Speaker 1: Having like, a... An intro video where,

Speaker 1: you know, where you talk about how to use this course, how to go through this course, where you actually

Speaker 1: kinda set the premise for for consumption. Right? Like, making sure they actually consume it. Yep. And maybe even telling them, like, hey, you know, maybe maybe lock up the book call options until they complete all the modules because I think...

Speaker 0: I think I think... Actually, the way I the way I tend to structure book a call

Speaker 0: pages

Speaker 0: is through the lens of a...

Speaker 0: You're figuring it out lead. Right? So it's like if you look at a book a call page

Speaker 0: and you make it so, like, you know, hey. Welcome to, you know, whatever it is.

Speaker 0: Welcome to your your product,

Speaker 0: you know, elite. We just call it an elite version of it. This is... Where you are now is on your own, figuring this all out. Now we gave you everything you needed inside

Speaker 0: whatever the core product's name was,

Speaker 0: but you have to piece it all together yourself. And so when you use that type of a lead, it it doesn't really matter if they've consumed

Speaker 0: all the product or ten seconds of it. Your framing in that book a call page has has created a

Speaker 0: agreement that they have to figure it out and assemble it themselves. Right? So you're naturally kind of introducing the limitation of go piece it back together on your own. Right? We've got it for you. It's all there, but you gotta go and assemble it. And it's just the truth. Right? That's the natural constraint of of of a book or a course is that they'll have to consume it and and and synthesize

Speaker 0: the information and then, you know, implement it on their own. Whereas, you know, a back end service for whatever it is, doesn't matter what it is, will help close that, you know, knowledge gap or implementation gap. You... Is it done with me or done for me, right, in in terms of of of what that back end offer is?

Speaker 0: But that that natural... That is a natural limitation of of any product, right, is the the self implementation. So you can use that kind of a lead on the book of call stuff to

Speaker 0: to...

Speaker 0: It it it... To

Speaker 0: not make it seem like you've created an obstacle course for them because you haven't... Even... No matter who... That's actually irrelevant to how good or bad the product Right?

Speaker 0: Even if the... Even if it was a... You know, okay. I suppose the only... With the advent of AI and all these vibe code... Vibe vibe coding tools that can, like... You know, you can pro... You can talk to and it'll build your software. Maybe that's one of the few examples where it's like the product really is getting to a point where it's, you know, why would I need the secondary transaction? It's like the only the only secondary transactions for that type of offer are, like, a bigger database after I launch. Right? It's not about figuring out how to build the thing anymore or, you know, iteratively secondary prompting, but they'll figure that out eventually as well. But you see what I'm getting at. It's it's a... The... There's a natural limitation that emerges from the product in some way, shape, or form. Right? You know, with the vibe coding example, it's like, how do get users is the next limitation. Right? It's like, when you you made your your website or whatever you vibe coded, next constraint becomes, you know, traffic or users or,

Speaker 0: you know, optimizing the page. But, like, a constraint emerges irrespective of how easy... Whatever the product is. Right?

Speaker 0: But... Yeah. So that's how I tend to, like, those book a call page leads, and so I wouldn't mess... I don't think you have to lock it. I think you just... If you frame it right early

Speaker 0: and just speak to that natural constraint that's emerged, you can kinda have your cake and eat it too there on that sales message.

Speaker 0: Cool.

Speaker 1: I guess, I'll throw one

Speaker 1: more question. What are your thoughts in terms of, like, personalization?

Speaker 1: You know, as as we go forward, you know, I think with with information becoming more and more easily available Yep. What are your thoughts on, you know, having personalization elements? I saw you you wrote about, like, quizzes and

Speaker 1: trackers and things like that. You can... This concierge

Speaker 0: team

Speaker 0: is essentially a version of personalization if you think about it. It's like, let me guide you to the product

Speaker 0: over the over the shoulder is essentially what that is. Right? And it's... You're, like, establishing a rapport and relationship with it. So it it is a version of that. Right? The human touch is is is...

Speaker 0: The human touch is the

Speaker 0: is the

Speaker 0: final piece that's missing... Or sorry. It's it's the one thing that's gonna be hard to fully automate out of any business. Right? We're getting closer and closer with lot of this AI stuff, but it's it's

Speaker 0: it's not to a point where you can you can you you can remove that. And and that really is a version of per... Personalization. So I got someone to interact with to talk about my specific problems. That is personalization even if it's... You're guiding the

Speaker 0: same question... The same person with the same question gets sent to the exact same chapter of your book, maybe with some slightly different context, but that that is that is the personalization. Right? So that... That's... That... This is the the first version of it.

Speaker 0: But then you can have, like, other stuff attached to the product where it's... Don't know. The... If you have a community, that's a version of personalization because they can come in and have,

Speaker 0: you know, interact and and ask questions based on their current circumstances.

Speaker 0: So

Speaker 0: personalization

Speaker 0: personalization is actually where a lot of the value is unlocked.

Speaker 1: Now this one this this one, if you're doing 200 sales a day, this is gonna become a bit of a challenge. Great problem to have. Right? Plus, if you get into that category, this is gonna become a constraint for you. Right? It flips to you.

Speaker 0: Both in the in the early stages, you the leverage this thing gives you if you're willing to do it is massive. Massive.

Speaker 1: I think I think this can be done via

Speaker 1: the ends as well. Right? And you can have...

Speaker 1: If you can have a team of, you know Yay. Maybe you have a team of VAs.

Speaker 0: Yep. You know, who who reach out to people who join, you know, the Yep. Same day.

Speaker 1: How, like, you know, give them welcome and, like, hey, you know, is there anything specific you were looking for when you, you know, bought this program?

Speaker 1: Yep. You know, get feedback. Yeah.

Speaker 0: Definitely definitely there is that. Or or you could have a group onboarding call via Zoom as well, which is not to be done one to one. You could do it one to many and pair that with the VAs as well. Maybe they're all on that. So every day at 3PM, we're doing one or whatever. Right? Like, a a rolling time. But, yeah, there's definitely, like, you can always find a way... Like, is that as good as a one to one personalized? No. But it's, like, maybe 95% there, and that would be scalable. So it would still still be valuable to do that type of stuff. And, yeah, definitely, DMs is is a way of doing it or group Zooms for sure.

Speaker 0: Hassan?

Speaker 3: Hi, Kevin.

Speaker 3: Sorry that I actually joined late.

Speaker 3: Was I was sort of side of... Yeah. So a bit of context.

Speaker 3: So we're running cybersecurity

Speaker 3: program. Okay. And all throughout last year... I don't know if you remember the call that we had around February where I showed my funnel.

Speaker 3: So we're currently... Yeah. That's that's been a while. So

Speaker 3: back then, we were not actually making any profits on the front end.

Speaker 3: But all through 2025,

Speaker 3: we

Speaker 3: we spent around $8.00... $804,000

Speaker 3: ad spent and total revenue on that front end. So we run, like, a challenge, five days challenge. Mhmm. So we made about 812

Speaker 3: on that front end. And then on the back end, that's sort of, like, propelled us to

Speaker 3: about

Speaker 3: $3,000,000,

Speaker 3: right, like, from January to December.

Speaker 3: Now this type of funnels that we've been running

Speaker 3: is just pretty much, you know, webinar and VSL.

Speaker 3: Yeah. So... Which, obviously,

Speaker 3: with the AC model, it sort of leaves out some of these

Speaker 3: audiences that we really, really need to cater to because we are trying to

Speaker 3: on this figure up to about $11,000,000

Speaker 3: a month.

Speaker 3: So

Speaker 3: this Ascension model

Speaker 3: that you mentioned, right, so the... I'm trying to see how that's gonna actually work for us because we run a five days challenge. So we have a low ticket offer.

Speaker 3: We're having an upsell to book a call. Is that is that what would normally be the right thing to do? Because we've, you know, we've always run a webinar

Speaker 3: that sells the $69.07

Speaker 3: offer to the five days challenge.

Speaker 3: Right? So I'm trying to see how that would work for our type of business because, majorly, we want to sell the $69.07 offer. And the VSL that we ran also last year,

Speaker 3: I created it in February, know, it's been working ever since then. So I'm trying to see where we can install that in a proper AC model. That's why I... Once I saw that

Speaker 3: that you have... Actually, haven't just called. I just had to jump in even though it was it's already late. So... Yeah. Yeah. No. No. You're good. One one of the things I...

Speaker 0: Yeah. I have a vague memory. We did a we did a we did a good teardown of that that offer that we had looked at for. We were probably talking for about forty five minutes, I think, maybe even an hour on that from memory, and we looked across a lot of pages.

Speaker 0: And so I can't remember the specifics of the offer, but I do kind of, like...

Speaker 0: With what you filled in the gaps for me here now, here's what I would say, is that your five day challenge and even your webinars,

Speaker 0: what you're getting is a lot of attentional isolation and time invested from the user upfront.

Speaker 0: And that is

Speaker 0: just whether the... If the the people who hang around have no choice but to interact with that. Right? And so that is that is

Speaker 0: that that is kind of... I'm not sure how much of this call you consume. I think you're pretty late to us, like, maybe in the last ten minutes. I think you only opt on. But you're gonna get a lot of kinda like moments

Speaker 0: and natural revelation

Speaker 0: revelation

Speaker 0: for the... For them in

Speaker 0: terms of what's possible for them or their own limitations or whatever it is in those those environments. Right? Because they... They're they're consuming Uh-huh. And and there's belief building stuff. Now your... You could still have that via an AC offer as well. Right?

Speaker 0: Boss Mhmm. Your your... This is an intimate environment you... You're you're naturally drawing people to. Right?

Speaker 0: Intimate environment.

Speaker 0: And so whereas an AC an AC

Speaker 0: follow-up

Speaker 0: with the product

Speaker 0: can apps can be as well, but there's more optionality of... Optionality in consumption.

Speaker 0: Consumption versus versus a webinar. Right? It's like, I signed up for this webinar. Well, did you attend or not? I I did. I'm consuming. I didn't. I'm not consuming. It's very... It's a very binary event. They have to show that they did. With an AC phone or an AC offer, it's not that binary. It's like I came in, I logged in, I clicked her in the book, I left, and I came back next week, or I plan to come back next week. Right? And so there's a different... It... They can skip the skip the consumption or have more optionality in in in how they consume. Right?

Speaker 0: And so

Speaker 0: with that in mind and and given how you're currently ascending successfully off workshop webinar,

Speaker 0: what I would do with an AC offer for this would be I would use this primarily as retargeting

Speaker 0: to start off the back of the webinar

Speaker 0: or before the workshop. I I would start there and have this be a

Speaker 0: other path... An optional path,

Speaker 0: and I would do it for the people who weren't leads. Right? So the way I would do it is I would... Any clicks I drove through webinar page, anyone who became a lead,

Speaker 0: I would I would I would leave in the webinar funnel, and maybe I would send them an email after the... Our webinar cycle. Let's say you're running in a weekly cycle. I think that was was from memory or something like this. After weeks over, you can push them to that offer if they haven't bought. Right? Push them to the low tickets. Maybe they'll they'll pull them in. But for what... If you're running the webinar in general,

Speaker 0: you know, you're probably get... Don't know. If you're getting a 20% up to rate, 80% of people are rejecting that that that. Are they rejecting...

Speaker 0: They're either rejecting the outcome or the mechanism. I I don't wanna go to a webinar. I don't I don't have time for a workshop.

Speaker 0: Now a low ticket may fit those people we're targeting. So that you've... That's what I would... Where I would start. You're already spending your media spend on your webinar. So I'd just leave that as is, but I would pixel the people who didn't opt in and hit them with retargeting for the low tickets to start. And that, I think, is a good

Speaker 0: first version of of of how to do it. And what I would do as well in your upsell path, I would have axe... I don't know what the challenge is in terms of price point, but I might try and get the the challenge as part of the upsell path as well in that in that AC funnel or certainly in the content there. I would I would see the webinar inside that content as well. Right? But you have a very... You've you've you've optionality in in consumption. Right? And so the... Where I would start, given that you're successful in your current format, is I would add make some funnel for sure, but I would start with the the retargeting of people who are not becoming leads because

Speaker 0: the people... You know, the the the reason they're saying no is not clear to us is we just know they're not opting in. And so I don't have webinars. I don't have time for this, you know, or I don't believe you. Right? We don't know. But if we start retargeting,

Speaker 0: you... We... If they're in either of the first two categories, I don't have time for this or I don't like webinars, well, there's a product here. This may seem easier or I could buy it on impulse. Right? So... See, I guess.

Speaker 3: Then in actual parts to an upsell would be a VSL selling the six nine seven. Right?

Speaker 0: Yeah. You could you could you could do a a six nine seven upsell of that. What do you think it for the front end? $47 front end, I think?

Speaker 3: Yes. Yes. Thereabouts. Because we've never done anything like that before. So Yeah. You could you

Speaker 0: could try a you could try a

Speaker 0: you could try a a a six nine seven upsell. It's probably a bit of a stretch, I'm being honest. Like, if

Speaker 3: Yes. That's that's what I'm thinking. That's what I'm thinking after the first

Speaker 3: after the first page, obviously.

Speaker 3: Then the next one is going to pretty pretty much sell the the call with the closeouts.

Speaker 3: Because what we do is... Remember the the webinar funnel and then the VSL. They watch the VSL and they book a call with our closers. Yeah. Or they... When they watch the webinar and they do not, you know, buy our $6.97 right there on the webinar, those that saw the offer, the closeouts also reach out to them, you know, to get them to actually convert to the $6.97.

Speaker 3: So I'm I'm here thinking,

Speaker 3: okay. If we have an Ascension for now, they buy the book or whatever material we actually put in front for consumption.

Speaker 3: Then after that, what's the next path? Would it be

Speaker 3: a VSL telling them to actually book a call,

Speaker 3: which would still pretty much

Speaker 3: work as a VSL funnel, but then we have

Speaker 3: we have an option for them to actually consume a lower price tickets

Speaker 3: on the front end. Don't know if that makes sense. I think you got a lot of value out of you watching this call. We kinda hit on a lot of this thread through edits. So I'll just give you a little bit,

Speaker 0: you know,

Speaker 0: just because I bought a $47 offer. Right? Mhmm. One thing that happens after the... I've purchased that offer is all

Speaker 0: your marketing and sales material for everything else,

Speaker 0: the value of it goes to zero if that product is bad. Right? So Yeah. For any people who come in... So so actually, the the the primary focus is on the consumable side of this. Because the very first thing... What's happening... What you're getting in your current sales process

Speaker 0: is consumption. Right? You have... They have to. They can't attend the workshop or the webinar, and consumption not be part of it. Right? So the people who are are engaging are having that happen. And consumption is what leads to them purchasing the the second... The, you know, the Ascension to the other products. Now in your low ticket, you know, the risk that that happens here is we slap something together.

Speaker 0: We have a deep functional

Speaker 0: in terms of, you know, getting started,

Speaker 0: you know, as a micro validation, and then we don't do enough in the product to actually make it feel, you know, have high perceptual value in and of itself. Right? So let me just get this grid we built here.

Speaker 0: Let's just zoom in for one second.

Speaker 0: Make this easier to see.

Speaker 0: There's the four four level grid.

Speaker 0: Yeah. This... So you're gonna have a pre purchase.

Speaker 0: Let's say you have a high perceptual... We'll do... Let's say you get high conversions on this offer. So you've pre purchased high perceptual value, but your post purchase, you've a low low perceptual value in the in the in the in the product. And what this creates is negative negative negative feedback cycle from from, you know, people who've interacted with that product. They disengage from your emails. They disengage from from this, that, or the other. Right? They maybe even start commenting negatively on your ads if you're running on Facebook, etcetera. Right? So that is that is where the first level of focus would need to be on this this offer. Not the next step. We push them to a book of call because it's like they bought something from you. They paid money for it. It's not like an optional sales process where they've opted in for webinar or a free challenge where it's like they're just here as a guest and, like, they're having a good time. It's like, I've given you money. And so it's like, we gotta we gotta fulfill on that expectation. Right? So we need to have the high perceived... High

Speaker 0: perceptual

Speaker 0: value on the the the sales cycle, but then also in the consumption. Well, this feels great. I really feel like this product's been had... Has been taken care of.

Speaker 0: Mhmm. But what do we push into next is a function of that. Right? Okay. Now you could still have that happen automatically in your upsell path or whatever. Like, you could try and do it immediately,

Speaker 0: but you gotta be mindful that they'll opt in, but then they'll go to the product. If the product doesn't feel right, then they'll disengage. Right? So it's... Yeah. But we gotta be aware of that. I think you get a lot of value if you, rewatch this call with that Definitely. Top of mind theme

Speaker 0: Yeah. About what's going on because that was a lot of what we talked about here in terms of of of how of how this works.

Speaker 0: Okay. So so... Yeah. No. You... Yes is the answer to a lot of what you've asked, but it's like, yes, but we gotta be mindful of Yeah. Of this because your

Speaker 0: your bias for move them to the next page

Speaker 0: is based on your experience of having them in a high consumption environment before you move them to the next page. Yeah. You're...

Speaker 0: Yeah. They're now in an optional consumption environment

Speaker 0: with... If they purchased it from you, but they've also paid for it. So the the the perception is different. It's like the the the the

Speaker 0: the quality that leads higher

Speaker 0: from the off rip, but in the same breath,

Speaker 0: if they have a bad experience with the prob... Product,

Speaker 0: the tactics and strategies you try and use to move them here, there, and everywhere is... Yeah. It doesn't work. So we have to be a good one. Yeah. I totally understand. Doesn't matter what... What's in this kind of... I open it and it tastes like shit.

Speaker 0: I ain't buying it again. They market it to me Yeah. A 100 different ways and never pick them up again. Right? Same same thing the rest. And... Okay. Yeah. I think you get a lot of value rewatching this call. Yeah. Definitely. I'm going to watch it. Thank you very much. Excellent. Excellent. Yeah. My pleasure. Will?

Speaker 2: Hey. How's it going, Kevin?

Speaker 0: Good. Good. I'd say you got a lot of audio to this one. Yeah. Yeah. Yeah. Yeah. I

Speaker 2: think I think it's really good. I think some of it, though, is it's a little bit beyond my current

Speaker 2: Situation. How far I can see. Yes. So

Speaker 2: as far as, like, conceptually, I understand it all, but how I'm going to practically implement it, there's a little bit of a, like, gap in that process. Yeah. Yeah. Yeah. Yeah. I I... Like, look, I don't even implement all this stuff perfectly into into an offers I build. It's like... It's just like

Speaker 0: the first step of solving any problem is just being simply aware that that that it's... This is a potential issue, and it's like, how do I wanna handle this? And you'll do your your first version. It's like, no. It's not right. And then need to fix this, but I'll go with that for now. Right? It's just like... That's what business is. It's a constant iterative process. Right? Yeah. Yeah. Exactly. Yeah. Yeah.

Speaker 0: Ahead. I... No. No. No. You're good. You're good. No. So so so good. My

Speaker 2: question was more so for

Speaker 2: our offer. I don't... For the Ascension,

Speaker 2: I wasn't planning on after having them buying the product, sending them to a book call. I was gonna have it more be, like, a post consumption thing. Yes. Because I I I remember seeing a while back that you were saying that for some offers,

Speaker 2: having to book a call right after going through the funnel is just gonna create a lot of buyer's remorse, and it's like, what did I buy all this Yes. $4.04.

Speaker 0: Yeah. There's

Speaker 0: so It's it's it's it's it's kinda market dependent. For your market, for sure, I think it massively... For female markets, it will massively invalidate their belief from what they've purchased. And, like, I think it's a violation.

Speaker 0: So it's like it's it's too soon. So I think they'll they'll have a much much harder harder criteria and... Around that where it's like, you know, I I... My... The the trust side will be be lost. Guys, I think, are a little more open to, you know, being kind of moved through a...

### 2:30

Speaker 0: The the the the sales process quicker in terms of, like, yeah. Let me see this. I know that they're trying to sell me something, boss, whatever. Whereas for the for the for the women, at least from my experience, that tends to be a bit more of a

Speaker 0: a bit more of a binary, you know, violation.

Speaker 0: Right? It's either that that that just feels like very, very violating for them.

Speaker 0: So, yeah, what do... If I was... If I had to do it for your market, I would do the concierge one where it's like, me welcome you around the product. Right? I would I would use this strategy

Speaker 0: rather than trying to book them in on the call. It's like, let let us show you how to use this the best way possible. Right? Book in with our team, not a sales call.

Speaker 0: Here's here's how you can use the product, and you guide them around us. They go, hey. What do you wanna do with this? I wanna earn, you know you know, $500 extra a month to kinda pay for my summer vacation. I wanna earn,

Speaker 0: you know, $5 a month because I'm sick of my job. You can kinda start getting a sense of that. Oh, you need this. You need this, but you'll also get a sense of who the avatar is. Right? All that type of stuff. Right?

Speaker 0: Right. Mhmm.

Speaker 0: So I think I think I would... This this concierge close strategy, I think, would be it would be how I would use it. And so you you could put this as o two zero three, and and it's it's not an o two o. It's just like a part of your welcome page where it's like, hey. You know, welcome to

Speaker 0: our our products.

Speaker 0: You know, we have a... You know, we're so excited for to get started, etcetera. If you wanna get on with a member of our team and have us guide you around the product and help you get the most... The absolute most of everything you've purchased, you know, there's a link directly below this. This isn't a sales call. We're just... We're here to help you get get the maximum value and get on get on the fast track to getting the results you want from from what we've purchased. Anyway, we can help you do that. We we wanna we wanna figure out, and that's what this that's that's what this call is for. It's a short fifteen minutes, no pressure environment where we'll, you know, ask you what you wanna achieve and guide you to the resources that will best help you and... Or help answer any kind of micro questions you have about how you can do this, you know, for your situation. Something like that. At

Speaker 0: the back of it, low intimidation,

Speaker 0: very, very high trust types type structure would work really, really well.

Speaker 2: Okay. Awesome. I can I can definitely implement that? One thing that I've noticed, though, maybe it's just, like, a limitation of GoHighLevel.

Speaker 2: Right now, we have our whole membership area in there. Mhmm. And it's not very customizable.

Speaker 2: But one thing that we're noticing is a lot of people just aren't accessing their product in general. Yeah. Like, we have people joining... I I think everybody so far that's joined the community on the back end has yet to join it. Yeah. Yeah. Yeah. We're sending them e... Sending them emails. We're Are you sure are you sure you send them opening us?

Speaker 2: They just... We send them an email, and then there's also on the thank you page buttons for them to click to get... Yeah. Yeah. Yeah. Yeah.

Speaker 0: So it's it's... We've gotta architect that. So they're, like, logging in, getting what they need. It's obvious, Bryce. So that that might be something we'll need to have a look at as well. We can we can go through the hot seats as well if you want. Just micro micro... Go through everything.

Speaker 2: Yeah.

Speaker 2: Like, I think we're talking about just completely tearing down the entire funnel. Yeah. But this this is also, like, you know, a $5, you know... Eventually, when we start scaling this up for you based on even just your...

Speaker 0: I think, like, the video ad strategy and the the retargeting the members area stuff

Speaker 0: where... With some context. Hey. You bought this. You know? Here... Here's here's where your login is. That that type of stuff for, like, just link click ads. They should be spending, like, $5 a day on that type of stuff to get people back in. Right? Like, hey. We're, like... We believe in our product so much. We're gonna pay to get you to come back to a price. That's that's the that's the that's the theme for that.

Speaker 0: Right. But, yeah, it's... We need to we need to evaluate is this because of user overwhelm and confusion or because they're just like, I'll come back to this later. It's like it's kind of... And it's probably a little bit of both, but we need to figure that out. And this is kinda what I was getting at for Hassan where it's like there's no optionality in the the consumption. You're... That that exact same stuff I was saying there. There's optionality in terms of how they can choose when they'll they'll consume the next thing. So it's obviously the ease of which we can get them to to... Into the members area is extremely important or just making sure it's not a user overwhelm issue.

Speaker 0: But that's that's part of it. I'll buy... I'll come back to this later. They buy us on an impulse, and and they they never they never come back. Right?

Speaker 0: Whereas for webinar, if they opt in, it's a very binary event. They either kept watching or they didn't. Right? Or they showed up or they didn't. It's... You know, they're...

Speaker 0: The...

Speaker 0: So that's one of the trade offs to the low ticket.

Speaker 0: But, you know, if you architect the rights, that you're very high consumption. It's just that there's

Speaker 0: some some things that... I have a sneaking suspicion for your offer.

Speaker 0: They're more likely to... Well, actually, it's an older demo that that are fine. The 60 plus that are... The ones who are primary bar in the tool. It's 35 plus. Like, prime... Primarily,

Speaker 2: it's

Speaker 2: 45 to 65 plus. I bet I bet it's more technological bullshit for them. I'd say it's something something's going wrong with the technology. They're just, like, giving up and all. I'll figure this out later, and then they just stop.

Speaker 0: So... Yeah.

Speaker 0: I got that.... Concierge that concierge thing if they booked in if that was at the very end.

Speaker 0: Then they say, I can't log in. Right?

Speaker 2: Would you recommend putting that before the thank you page so they have to see that before there's even a chance for them to, like, have a sense of completeness? Because I I think Yeah. Also what's happening is they hit the thank you page, and it's like, thank you for your purchasing. Like, oh, I'm done. And then I wanna watch that video. Yeah. Yeah. Definitely. Definitely. Yeah. 100%. Yeah. I'll have it before that.

Speaker 2: Okay.

Speaker 2: Awesome. I can build that out. And then one last small thing. Do you have any things where I can find, like, UI, UX things for funnels?

Speaker 2: Because I know you want me to work on that, but I... Like, I'm not sure. I don't have the context to know if the changes I'm making are the right changes. Yeah. Yeah. Yeah. Do you

Speaker 0: let's talk about that more on Hot Seats tomorrow. Okay. Yeah. Figma will be where we'll start. Yep.

Speaker 0: And then Freebook for just, like, icons and stuff, but I'll I'll get you some samples. Have a sample for you that I want for that... For the the rest of the page just to to to to the bottom bottom of your upsell one page. I have a I have a better sample. I just need to go and find it. I just... I have it in my head and, like Okay. As part of... For fast feedback, I'm, like, getting getting frustrated, not at you or... It's like, where is that? The example. Do you know what I mean? I have it.

Speaker 0: And I can't see it my head. So it's like I just wanna give that to you. So I'll find that for you. That'll solve the bottom of the page. It'll be very clear what you need to do there. It'll it'll it'll be obvious.

Speaker 0: And then, yeah, we'll we'll just... We'll we'll rework it in Figma.

Speaker 0: You know, we'll just import it very simply into a Figma page and and tweak the design, and it'll it'll be it'll be very straightforward how we we we can we can enhance it.

Speaker 2: Okay. Awesome. Thank you so much, Kevin. Okay. Super.

Speaker 0: Okay. Great call, everyone. Any last questions? Or I'm gonna round this up. Hassan, I'll get this open to the members ASAP so you can watch it.

Speaker 0: Other than that, great call, everyone. I really enjoyed this one. And,

Speaker 0: yeah, we went through a two point o version of this where it's like, I'll go back through this and just, like, add image... Imagery

Speaker 0: to the whole...

Speaker 0: To anything we covered or, like, contextual examples, a comparative, like, just do comparisons. I think I need to start doing a little bit more example in because I'm very...

Speaker 0: I'm a I'm a visual thinker as well. Like, I see pictures in my head. I'm... I I think... Or, like, you know, even just explaining things to people. Like, if people are just, like, words word processors, they might need a visual example. So I think we might do a a two point o version of this call where we just go back through and add visuals to everything.

Speaker 0: But... Yeah. Yeah. And, Heather, yeah, the design stuff would be good as well. Yeah. Okay. So we'll we'll probably do that in the future. I'll figure out how we get that done. But, yeah, this was a really, really great call. Really enjoyed this one.

Speaker 0: Okay. Thanks, everyone.

*Speaker labels below are algorithmically derived clusters, not identified people: one label on a long call usually means diarisation failed, not that one person spoke. Speakers observed: 4.*
