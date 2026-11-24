---
title: 02 16 2026 Robert OpenClaw 2x Your Productivity With an AI Assistant
date: unknown
type: other
duration: 125
speakers: 7
---
### 0:00

Speaker 0: My man. How are you? Yes,

Speaker 1: brother. Blessed. Blessed. Are you well? I'm doing very well. Just cold as fuck, dude, but

Speaker 0: surviving.

Speaker 1: Well, Open Claw, man. They can put your heaters on, Kai.

Speaker 0: Probably.

Speaker 1: I've seen I've seen the guy talking about use case scenarios. People using it for, like,

Speaker 1: turning their lights on and the heaters on. Yeah. I'm sure. It's the the sit... The... But, yeah, man. Looking forward to today's call, man. Seeing what he's doing. I've I've I've I've not even got got chance to, like, get Open Claw going, so I'm really excited to see what what you've what you've been cooking up.

Speaker 0: Yeah. It's been really interesting because I...

Speaker 0: Hello to everybody else as well, Wayne, Nick, and Alex.

Speaker 0: I installed Open Claw when it first came out, but I just put it on my computer. So it was just on when my computer was on.

Speaker 0: And

Speaker 0: as everybody knows, probably, like, what you're supposed to do is put it on a VPS or put it on a Mac mini, right, that's running all the time. And when I did that, it was like... That's when I realized the real value and the real magic in it. So

Speaker 0: so, yeah,

Speaker 0: we'll get into all of that. But that's it. So what you... You buy a Mac mini and then you install it on that. Is that the best way to do it? Well, we're gonna dive into that. I haven't done it that way, but I'm gonna go through all the options. So we'll we'll crack into all that in a bit. So I guess we'll just wait a little bit for people to come on

Speaker 0: so everybody can get the same info. Yeah. I agree with Joseph. Fuck buying a Mac mini. I'm just using a VPS, but, yeah, we're gonna dive into it. I think some of the newbies as well are kinda... They hear all these terms, and they don't even know what it means and the difference between them. So we'll kinda do a walk through of all that.

Speaker 0: Welcome. Welcome, everybody.

Speaker 0: Dominic, Joseph,

Speaker 0: Jacob.

Speaker 0: Good

Speaker 0: to have you guys here.

Speaker 0: Yes, sir. Cooper.

Speaker 0: Hope you guys are doing well. Who... Let me know in the chat who's already running their

Speaker 0: Open Claw,

Speaker 0: and who isn't.

Speaker 0: Dominic,

Speaker 0: no. I think Joe said he wasn't.

Speaker 0: Joseph, no. Wayne, yes. Nicholas, no. Okay.

Speaker 0: Don't have it. We've got a Mac Mini secure to see how to set it up on that. Okay.

Speaker 0: Nice.

Speaker 0: Well, we're we're we're gonna we're gonna wait a few minutes to let everybody else join. So,

Speaker 0: yeah, this thing has just been blowing my mind. So

Speaker 0: I'm very pumped to

Speaker 0: to share the breakdown of kinda, like, what it is. Again, for the newbies, kinda, like, how it works a little bit, and then maybe we'll even try to install it. I can install, like, a second instance on my on my other... My second Telegram account. Well, I could even install two on the same one, really. But...

Speaker 0: Yeah. Just every day I've been using it. I've been adding kinda, like, more use cases to it and more

Speaker 0: making it more of a personal assistant in a way, and it's just been

Speaker 0: blowing my mind.

Speaker 0: Abraham,

Speaker 0: welcome, dude. What's up, man? Good to see you. What's new?

Speaker 3: Not much. Not much.

Speaker 3: I'm very excited for Cloudbot

Speaker 3: to see sort of, like, what you got there. Yeah. Do you have it installed yet? Or

Speaker 3: No. Not yet. Not yet. I was sort of, like, worried about the security of it. And my

Speaker 3: brother, who is more the developer

Speaker 3: between sort of, like, the... You know, between us, he told me that there was some malicious code. I don't know if you guys know about that. And

Speaker 3: the malicious code was

Speaker 3: sort of, like, hacking a lot of different profiles.

Speaker 3: But he... I

Speaker 3: don't know what he was saying. He said that he found exactly

Speaker 3: where that code can be or something like that. So someone did install a malicious code into it.

Speaker 3: And the best way is what you're doing, which is installing it on a VPS

Speaker 3: instead of, like, installing it locally on the on the computer. Yeah.

Speaker 0: Exactly. I haven't looked too deeply into that stuff. I've just been containing mine as much as possible. But I I would be

Speaker 0: willing to bet money that all of those vulnerabilities

Speaker 0: are most likely in, like, third party skills and stuff like that that you're downloading from other people.

Speaker 3: That makes sense. That makes sense. I don't think it's in the the main, repo from, from the main guy who... I don't know if you guys saw, but he has joined,

Speaker 0: Open AI today

Speaker 0: to join their team.

Speaker 0: I guess it's open source today, but we'll see how long

Speaker 0: good old Sam can keep his fingers off.

Speaker 3: You know, I wish he joined Claw, man. You know? But I guess the the lawsuit that happened,

Speaker 3: maybe

Speaker 3: it negatively affected that. Now he has to go chat with you. Yeah.

Speaker 0: So I briefly watched his interview with the...

Speaker 0: What's the guy's name?

Speaker 0: With the suit, a Russian guy who claims to have worked at MIT that people are not sure. Lex.

Speaker 0: Lex. And

Speaker 0: so he was talking about the... Basically, the offers that he got there from

Speaker 0: from

Speaker 0: Meta and

Speaker 0: Open AI.

Speaker 0: And it also seemed like his relationship with Anthropic was pretty good despite the whole name thing.

Speaker 0: But, yeah, I guess now we know that he's made his decision,

Speaker 0: and we'll see what happens. But,

Speaker 0: supposedly, it's meant to stay open source. So...

Speaker 0: Hopefully.

Speaker 0: Yeah.

Speaker 3: His... I do think you should be running ads soon. Right? What's that? Ads. Yeah. Yeah. Yeah. That's the plan. Yeah. So

Speaker 3: they're,

Speaker 3: becoming very,

Speaker 3: money driven

Speaker 3: rather than technology maybe driven. And itself,

Speaker 3: like, I stopped using it even though I I paid for it, but it's, like,

Speaker 3: complete garbage, to be honest with you.

Speaker 0: What is complete garbage?

Speaker 3: ChatGBT.

Speaker 3: I stopped I stopped using it Yeah. Yeah. Yeah.

Speaker 3: After a specific incident. So one time I was, like, sending it files, and I'm like, go through these files and get back to me

Speaker 3: and answer these these, like, sort of, like, questions.

Speaker 3: And I was looking at the tools that it was using.

Speaker 3: It did not open the files, but it said that it did. So I called it out, and I said you did not open the files. So it was like, oh, yes. You're right. I did not open the files. I'll open them now. And then it did that three times after. And then the the thing that sort of, like, ended it all was

Speaker 3: I was talking to it about something personal. It wasn't even, like, work,

Speaker 3: and it had to do with, like, caffeine, how much caffeine I take per day. And then

Speaker 3: it...

Speaker 3: We were going through with the with the conversation, and then it said at one point, it was like, oh, ignore the citations I sent you in my previous message. I completely made those up.

Speaker 3: Let's start over. I was like, wow.

Speaker 0: Yeah. My friend calls it the McDonald's of LLMs,

Speaker 0: Open AIs. I think that's a good good analogy.

Speaker 0: It's kinda, like, quick and dirty. You know, if you need something, you know, fast to just kinda get you across the finish line,

Speaker 0: then you can go to that.

Speaker 0: I think that's a good one.

Speaker 0: Cool. Well, welcome to everybody else who's joined. I don't think I can even see everybody's faces. So Paul,

Speaker 0: who else joined?

Speaker 0: Anse, obviously.

Speaker 0: And, yeah, I think we can sort of dive into things. Before we dive in, if you haven't already answered, I'd love to know in the chat. Are you already running Open Claw or not?

Speaker 0: And I would also love to know kinda, like, what you guys would like to use your personal assistant for.

Speaker 0: And if anybody else wants to cover anything else outside of, like, Open Claw stuff before we dive in, we can spend a little bit of time on that. But I think the rest of the time will go into Open Claw.

Speaker 0: And if anybody wants to just unmute and, I don't know, say hello and share anything that you've been up to, we can also spend a few minutes doing that. But majority today is gonna be Open Claw stuff. So it seems before the rest of you guys joined here,

Speaker 0: the majority of people in here are not running an Open Claw

Speaker 0: instance at this moment.

Speaker 0: I wanted to build offer factory.

Speaker 0: What was that? Offer factory,

Speaker 0: of course, s, probably. Print insane cash. I saw fucking...

Speaker 0: I saw, like, one of the best ideas ever today. My friend sent me...

Speaker 0: I gotta share it with you guys.

Speaker 0: This thing was fucking genius.

Speaker 0: Let me do it like this.

Speaker 0: Okay. So here's the idea.

Speaker 0: So So this was a tweet. It says 70% of local businesses still don't have a proper website. What if we use all Open Claw to, number one, scrape local businesses from Google business profile?

Speaker 0: Number two, auto generate a clean website for each one based on the info that we scraped earlier. Number three, email the owner with a site preview

Speaker 0: and a payment link to activate the site.

Speaker 0: And then it says a 100 emails a day, 2% conversion rate, $500

Speaker 0: per

Speaker 0: site,

Speaker 0: twice a day for thirty days equals 30 k a month.

Speaker 0: I think that's a really cool idea, and I think that concept can be applied to a lot of things where it's like, because of all the stuff that we can automate now, kinda like to Joe's Joe's point of of wanting to kinda create this factory of just pumping stuff out, there's probably

Speaker 0: endless

Speaker 0: amount of use cases where...

Speaker 0: You know, we used to, like, cold email people and say, hey. I can do x y z. Would you like me to do it for you? Now we can just do the thing,

Speaker 0: send it to them, and basically say either, like, hey. Here's a gift from me. Would you like more? Or, hey. Here's this thing.

Speaker 0: If you want it, we're like, we made it for you. If you wanna just... You can even automate the wholesale of it. Right? And that can be applied to an insane amount of things, and I think that is super cool.

Speaker 0: Really cool idea. So I love that one.

Speaker 0: Love that one. Alright. Let me check the comments real quick. Thomas is not running Open Claw. Abraham launched ads on Facebook, review running ads, set up AI agents for our new onboarded clients. So launch ads on Facebook, I think you can do with API.

Speaker 0: Review running ads, sure, you can just export all the data, have it analyzed,

Speaker 0: set up AI agents for our new onboarded clients.

Speaker 0: Cool. Joe says, how do you define open source?

Speaker 0: Well, it's just open...

Speaker 0: Openly available to everyone. You can download it and use it. Right? So, you know, Anthropic,

Speaker 0: you can't just, like, download their large language model and install it on your machine. You know, they're kinda gating it, and you have to pay for access.

Speaker 0: Whereas, is

Speaker 0: an example of an LLM that you can download for free and just install on your computer.

Speaker 0: Hey. Open Claw. Make eight client videos ads. Make no mistake.

Speaker 0: I love the make no mistake

Speaker 0: memes.

Speaker 0: AC offer factory, doable,

Speaker 0: but complex. Right? Because there are so many moving parts,

Speaker 0: but certainly doable. You know, the thing... I forget who was talking about. I think maybe it was Hans talking about, like, the difference between making software and maintaining software. Like, we all live in this fantasy land where it's like, hey. We made a software.

Speaker 0: It's like, dude, maintenance is a is a real bitch. So, like, you know, like I told you guys, I have a 29 step workflow for making

Speaker 0: AI videos,

Speaker 0: and, like, I'm trying to automate each step of it. But, know, every week, something breaks, basically. So you're kinda like

Speaker 0: the repairman hat has to, like, come on all the time and go and, like, repair the machine again.

Speaker 0: Dominic says make insane ads for Facebook and TikTok to crush.

Speaker 0: Can do that. Obviously, I just kinda spoke to that one second ago as far as, like, videos go,

Speaker 0: but you can definitely use Open Claw to make images as well.

Speaker 0: Genius, crazy, really good idea. This really works.

Speaker 0: A friend is running this, but with MRR pricing. Oh, Alexander, do you wanna share more?

Speaker 0: So is he doing basically what we said where he's

Speaker 0: making the site for him, sending it over, even automating the sale, or is he trying to close them?

Speaker 0: Yeah. I have, like, a bit shitty connection about, like, the hotel right now. But, basically, he's, like, scraping regions

Speaker 2: using the cloud bots and sending,

Speaker 2: like... Yeah. More or less as you said.

Speaker 2: And,

Speaker 2: yeah, he's, like, charging 150

Speaker 2: per month, but I keep costing him, like, a buck or 2 per month with, like, the the the setup, basically. But they they don't know. They just think it's, like, for hosting the website and everything.

Speaker 0: Yeah. So he's basically selling the same thing that we Right? Website. So you'll find them on Google. Yeah. Yeah. Just just like this mostly mostly recurring.

Speaker 0: Beautiful. Let's see it. Even better. I mean, that's freaking genius.

Speaker 0: Is he crushing it?

Speaker 2: Yeah.

Speaker 2: So far, I think he made, like, three sales yesterday, but I I I... I'm not sure about, like, the volume because it it will just, like, make so much sense

Speaker 2: to scrape, like, huge cities,

Speaker 2: huge datas. Like, you you have, like, an agent doing, like, the... All the bars, one doing all the restaurants, one doing all of whatever.

Speaker 2: And and you can just, like, spam

Speaker 2: a whole fucking country in, like, one day,

Speaker 2: I guess,

Speaker 2: just, like, burning a lot of tokens. But the the the

Speaker 2: money back you get behind it is, like, insane. So I guess that that will work pretty well. Yeah. Amazing.

Speaker 0: Cool.

Speaker 0: Glad to hear somebody's doing it. Joseph said, Telegram chatbot for one to one chats, community

Speaker 0: to upsell front end, upsells

Speaker 0: on auto by answering chat and overcoming limitations and all that good stuff. Discord model that acts like a human and does the job. Yeah. We could we could have all those kinds of things happening.

Speaker 0: Okay.

Speaker 0: Let's dive into things. So welcome to the rest of you guys,

Speaker 0: Benjamin, David.

Speaker 0: Not sure who else joined.

Speaker 0: Juan,

Speaker 0: Paul, I think I might have mentioned.

Speaker 0: Yeah. Good to have everybody here.

Speaker 0: So let's dive into some Open Claw stuff.

Speaker 0: Again, from our slight polling here in the chat, it looks like most of you guys don't have it up and running, which is cool.

Speaker 0: Also, I have to kinda keep repeating myself. I am temporary. I do have good Internet, but I'm far away from the router. So if we have problems,

Speaker 0: don't worry.

Speaker 0: Worst case, I'll go up into my kid's room and sit closer to the router, but I'll try it here for now. I'm gonna move offices again in a few months, so that's why I'm not paying to have it all fixed.

Speaker 0: So...

Speaker 0: Okay. Let's

Speaker 0: maybe start with

Speaker 0: Open Claw. What is it?

Speaker 0: Well, I might share the doc that has been prepared for

Speaker 0: kinda going through this stuff.

Speaker 0: We can zoom in a bit more.

Speaker 0: So it's a personal AI agent, right, that lives on your server.

Speaker 0: We... We're gonna dive into this, but... And we've talked talked about it briefly. You could have your AI agent as far as, like, hosting goes. It can live on your computer.

Speaker 0: It could live on a VPS,

Speaker 0: virtual private server. Right? We're just essentially paying for server space somewhere.

Speaker 0: Or,

Speaker 0: you know, I say your computer, but what what that means is, you know, we all have our main computer that we're using, and then some people are buying Mac minis. I think you may have seen the craze of people doing that and Apple running out of Mac minis because people are buying them. They're not even hooking them up to a monitor. They're just keeping, you know, this tiny computer at home running it twenty four seven.

Speaker 0: And I think in some cases, people install

Speaker 0: an actual LLM LLM,

Speaker 0: like Olama, on their, computer, or or they'll just run it, through whatever, Claw or Gemini or ChatTivity,

Speaker 0: which we're gonna cover here in a bit too as well. And so this is how to keep your AI agent alive twenty four seven. Right? So one thing I shared with the guys before everybody joined as well in the

Speaker 0: in the early hours of of this call.

Speaker 0: When I first installed Open Claw, I just installed it on the computer that I'm using kinda, you know, when I'm working. And that means as soon as I leave my computer and it falls asleep, my agent or my assistant was not available. And I didn't... I I was aware that, like, this is not maybe the best way to do it, but I I just didn't wanna take the time at that moment to to go through and do it. And I will just make sure that everybody knows, like,

Speaker 0: the difference between doing what I did and then doing it properly where it's set up twenty four seven is night and day. You you don't wanna just install this thing on your computer and have it die when you're not there. The whole

Speaker 0: magic for me has been having access to this thing while I'm just like anywhere. I have my phone and it's got access to enough things where the amount of progress that we can make on all kinds of topics, all kinds of different things while I'm not at my computer has been the real unlock. And this thing could be your Tony Robbins business coach. This thing could be your, you know, complete,

Speaker 0: you know, technical

Speaker 0: cofounder who has access to your entire code base.

Speaker 0: And for those of you guys that have been vibe coding at all, you kinda know the difference between, like, planning your coding sessions and actually executing the code.

Speaker 0: And in Claw code, you know, that's called plan mode. Right? Where you kinda switch into that, and and it's not writing any code. You're just kinda going back and forth, having conversations, trying to flesh out, you know, the problem that you're working on, what the real... Like, really identifying what the problem is, what the different solutions might be to that. Sometimes, you know, that can get... That can be a proper conversation that takes a while. And so I started to use this thing as that, like, I'm not at my computer, I'm doing all this prep work, like, maybe I have five minutes here, ten minutes there.

Speaker 0: I just pull up my phone. I'm not typing. I just do an audio,

Speaker 0: you know, just send an audio voice message in the... In Telegram

Speaker 0: to the bot, and of course it transcribes what you say, and we are able to have a conversation going back and forth like that. So just yesterday, I've been working on this one problem that's kicking my ass in the in the AI video side of things.

Speaker 0: And,

Speaker 0: yeah, I spent like ten minutes going back and forth with this very specific problem.

Speaker 0: And then at the end,

Speaker 0: I told it like, okay, I think we've figured this out. Now you need to save everything that we've talked about very... In very granular detail because I knew that once I sit down at the computer, I'm gonna put this into Claw code, and we're gonna start actually coding this session or coding this thing, which, by the way, you could get to a place where you actually do the execution as well from from

Speaker 0: your AI assistant. But I

Speaker 0: didn't wanna push the boundaries, so I did that. And

Speaker 0: surprise, surprise, like, it works the way that it was supposed to. Because I did all that kind of prep work

Speaker 0: when I just pasted this massive conversation, basically, in summary,

Speaker 0: it knew exactly what to do and how to fix the problem.

Speaker 0: So

Speaker 0: the use cases is obviously, like, I think what's on everybody's

Speaker 0: mind. And, you know, one thing that keeps...

Speaker 0: I keep just coming to terms with and realizing is, like, I find that a lot of people just...

Speaker 0: They're waiting for somebody else to do all the exploration and go and figure out, like, what the use cases are gonna be. And then there's, like, maybe one or two or three or 5% of people who are like, I don't really know what the thing is. Like, I don't know what I want it for, but I'm curious. Right? Let me go in and let me start tinkering.

Speaker 0: And so

Speaker 0: even if you don't know what you wanna use it for, like like, as far as, like, AI tools go, this is a top two.

Speaker 0: Okay? You got Claw code and this thing. Like... And Claw code is like... Yeah. You know? Like, this thing is so

Speaker 0: insanely valuable. It has been for me over the last week that I I I, like, I can't stop texting my friends. Like, you have to install this. Like, I'm just keep pushing them to do it because it's so useful. You're literally getting a leg up on on everybody else because you can easily become,

Speaker 0: like,

Speaker 0: twice as as productive

Speaker 0: in a very,

Speaker 0: like, simple way. It doesn't it doesn't feel more taxing. It doesn't feel you're you're exerting more energy. In fact, it's more the opposite. Like, now you have this kinda thinking partner and execution partner

Speaker 0: that you can just kinda go back and forth with, and it can make progress while you're not in the mood or you don't have the energy or you're going to bed. You could literally have it running on a loop while you're sleeping,

Speaker 0: making progress on the things that you've told it are your goals. So

Speaker 0: it's just been absolutely nuts in that in that sense. Obviously, it can run on, you know, all of these different apps. And the big things of, like, why it's so cool is, like, persistent memory. Right? So we all have these different conversations

Speaker 0: with Claw or or

Speaker 0: Gemini.

Speaker 0: And, you know, sometimes it'll remember some stuff about you. Many times it doesn't. The persistent memory here is a very, very big thing. And it surprises you when you least expect it. Like, you'll say something like, hey. What's on my agenda today? And, like, yesterday,

Speaker 0: it was like,

Speaker 0: well, it's Sunday. You know, you should spend time with the the the, and it, like, remembered my kids' names. And it was like, and, you know, it's two days ago, was like, and it's Valentine's Day. Like, you got a full day. Like, it just... It was... Knows so much, and it's really, really awesome.

Speaker 0: Also, I should read you guys the message that I got this morning.

Speaker 0: Let me see if I can find that. I gotta pull up my messages here in a sec. So, basically, one thing that I told it

Speaker 0: is that I respond well to

Speaker 0: pain, not pleasure gain. And so I told it, like, I don't... I'm not gonna be motivated by you saying, like, hey. Great job. Like, I'm gonna do better if you call me a pussy and tell me to, like, get to work. You know? So so let me find the message that I got from Alfred this morning.

Speaker 0: I was literally, like, laughing for, like, sixty seconds this morning because I did... I know I told it that, but I just didn't expect it to deliver the way that it did. Alright. Give me a second. I gotta find this image. I sent this to my friends.

Speaker 0: Okay. Found it. So one of the things that it's been working on is, like, making a list of leads for me to contact and sell my UVC video ad services to. So here... Here's 728

Speaker 0: this morning, my

Speaker 0: trusted digital butler, Alfred, good morning. You have 1,650

Speaker 0: leads ready,

Speaker 0: and you've sent absolutely zero.

Speaker 0: Pathetic.

Speaker 0: And then client... He's put my client's name in there. So client name could drop you tomorrow, and your daughter's financial security would vanish simply because their father was too scared to do the work. Stop being a pussy, sit down and send 10 outreaches before Polish class or look wife's name in the eye and admit you don't have what it takes to keep this family safe.

Speaker 0: I was like, Jesus Christ. Good morning to you too.

Speaker 0: It was pretty funny.

Speaker 0: So,

Speaker 0: it really does listen, you know, when you tell it kinda like the personality that it wants, and it really gets to know you. Like I said, it included my client's name,

Speaker 0: my kid's name, and my wife's name, and also reference, you know, the leads list that we've built and all these things. So just super

Speaker 0: super cool.

Speaker 0: Yeah. It's it's

Speaker 0: pretty pretty insane.

Speaker 0: Okay. Let me find my way back here,

Speaker 0: and I'll come back to my screen.

Speaker 0: But as you guys can see, it's pretty badass.

Speaker 0: Yeah. So what can it do? It can use a bunch of tools. Right? It can search the web, read and write files, run shell commands, control a browser, manage calendars, all these kinds of things.

Speaker 0: It runs twenty four seven, technically.

Speaker 0: You could say that, but in reality,

Speaker 0: it has what's called a heartbeat, which is kind of like...

Speaker 0: You could call it, like, a daily calendar where it kinda has these rules like, hey.

Speaker 0: At 3PM,

Speaker 0: you know, do this or or or what have you. And I think it can go beyond kinda, like, daily as well, but it doesn't really work that well in my experience. Because I've been using it so heavily, it's often busy when it gets pinged to do something. So I've been trying to transition over to proper cron jobs, which are gonna be more

Speaker 0: brute force like, hey. At 3PM, deliver this thing or ping him about this and so on. So you can really turn it into a calendar and

Speaker 0: accountability coach in that sense. So you could put in, you know, all of your family's birthdays and Valentine's days and all these sorts of things, but you could also have a sort of daily

Speaker 0: daily thing where it's, like, it's gonna message you at seven. So mine is gonna message me at 07:30

Speaker 0: in the morning. It's gonna call me a pussy and tell me, like, what's on the agenda today.

Speaker 0: And and then it's gonna kinda ping me mid midday as well to just make sure that we're on track for the day with all the tasks. And then it pings me at

Speaker 0: 10PM at night to... I don't know if you guys know the meme from Elon when he when he texted the, at the time, CEO from,

Speaker 0: Twitter when they... When he was buying Twitter, and he was, like, making fun of him. He said, what did you get done this week? I don't know if you guys have seen that from the the lawsuit.

Speaker 0: But, so mine just text me, like, what did you get done today?

Speaker 0: Very succinct. And then I kinda debrief him. So I send a voice message, a debrief, kinda, like, low level effort

Speaker 0: or low effort way to do journaling.

Speaker 0: And then I'll usually talk about what we're doing the next day. So when I get my morning message, he can reference what I said the day before as well. So think of it as your AI chief of staff, not a chatbot. And that's very much... I feel like you become more of a director, and it really is. Like, if you if you were if you were to think that you had this person who was, a... Like, your business partner who who listens... Like, who... Your business partner in the sense that they were very capable, but your assistant in the sense that, like, they just do what you tell them. Right? So you become more of a director,

Speaker 0: and you don't have to execute, especially some of the kind of

Speaker 0: heavy lifting

Speaker 0: that you know needs to get done is super boring. You know, something like collecting leads. And I know there's software out there to do all these kinds of things, but

Speaker 0: but... Yeah. There's, like... They can do a lot of that heavy lifting for you.

Speaker 0: So main main reasons why it's different, so Stateful has a workspace, memory files, personality, and ongoing context,

Speaker 0: and that's how it differs from, you know, your chat GPT sessions for Claw or Gemini. And the big thing, what have I talked about in pretty much every freaking meeting that we've had so far is this idea of making AI more proactive. I think there's so much value in that, and that's probably why I freaking love this thing so much. I can program that productivity

Speaker 0: so easily by just saying, like, hey. Ping me every day at 10PM or or what have you.

Speaker 0: And, of course, it can run on your software or hard... On your hardware.

Speaker 0: There's many different configurations, and we're gonna cover that in a bit, especially for some of the newbies to kinda help you understand

Speaker 0: the thing a little bit better.

Speaker 0: So that's just kinda like some demo stuff. I think maybe... Let let me do a quick kind of

Speaker 0: illustration of how it can be set up. And to

Speaker 0: some of you guys, this is gonna be obvious. And to some people, you're gonna learn a little bit about, like, kind of the the infrastructure behind these things, and you can kinda see the difference in... Like, what is the difference between using API and OAuth? Like, to some people, that's super obvious, and to some people, you don't even know what what what the... What that means. Right?

Speaker 0: So if you wanted to have your your own AI personal assistant, you can run it through some of these apps that we've mentioned. I think there's other ones as well that I've missed here.

Speaker 0: My favorite is definitely Telegram.

Speaker 0: And so what do you need to actually run Open Claw?

Speaker 0: Well, you need two things. You need a computer. Right? It needs to have a way to live twenty four seven, and you need to have an LLM local... Or a a large language model. Right? It needs to be able to do all the cool things. That's another word for AI. Right? It needs to be able to do all of these things that

Speaker 0: we are so happy that it can do for us that we all had to do manually in the past.

Speaker 0: So those are the the the only two things that you need. And then the thing about Open Claw is, like, there's many different ways to configure all of this, and different people are gonna have

Speaker 0: different

Speaker 0: needs.

Speaker 0: And so I'm gonna walk you through the kinda, like, high level way... Different ways to set them up, and then I'll tell you about my setup and why I have that setup. And then we may do an install today. We'll just kinda see how you guys wanna wanna go about it. So as far as having a computer to run

Speaker 0: your AI assistant on,

Speaker 0: Like I said, I used to just run it on my computer when I first installed it. And I installed it... I had it for, like, a day, and I was telling all my friends, like, this thing is overhyped.

Speaker 0: I don't really see why it's so valuable. And as I was saying,

Speaker 0: the real magic is the fact that you can use it when you're off your computer. That's... I mean, there's magic in using it when you're on there as well. It's helpful. But the real magic is when you're off the computer,

Speaker 0: and it can still do stuff and and so on and so forth. So you can just install it on your computer as is, or you have two options that

Speaker 0: when it comes to, like, the twenty four seven version.

Speaker 0: Once again, you can buy a Mac Mini, or if you just have an old computer laying around, you could use that. Right? The whole idea is that it just has to be running twenty four seven. It has to be on all the time. But even if you have a laptop,

Speaker 0: I believe there is a way to set it up where you could close the laptop, just have it on all the time. So the screen wouldn't even be on, but the the machine would be running.

Speaker 0: Or you can use a VPS virtual private server. So this is where, you know, companies are...

Speaker 0: Have these massive data centers and and and servers... Server farms, and they're just renting you a little bit of space. Right?

### 0:30

Speaker 0: And so

Speaker 0: those are basically your options. And, of course, there are many different different

Speaker 0: options

Speaker 0: within

Speaker 0: kind of, like, these categories too. Like, Mac mini is just one example. Right? But, hopefully, you guys can kinda make the distinction there of, you know, on your computer, on a dedicated computer that's on twenty four seven, or a rented computer or BPS.

Speaker 0: Now what about the AI in... Itself? Right? When we send a request, when we send a question,

Speaker 0: we need that to be run through a large language model so that it can give us, you know, an answer. And so there are different ways to do this too. Once again, you can install a large language model on your computer.

Speaker 0: And then when you

Speaker 0: run or send in a request,

Speaker 0: maybe you'll start to hear the fans running on your computer. Why is that? Well, it's because it's using a lot of compute.

Speaker 0: It's losing a lot of your computer to actually process what was said. Because, obviously, these large language models are incredibly taxing,

Speaker 0: and this is why we have such a...

Speaker 0: This is why NVIDIA

Speaker 0: has

Speaker 0: performed the way it has. Right? Because the NVIDIA

Speaker 0: is powering all of these large language models, whether they're running,

Speaker 0: you know,

Speaker 0: on our computer and we're using NVIDIA GPUs,

Speaker 0: or if we're paying a service like ChatGPT

Speaker 0: or Gemini or what have you, and they are hosting all of that stuff on their end, And we're paying them, and they've got the fans running

Speaker 0: on their end. So they... The big difference, you can install a local large language model.

Speaker 0: It's not gonna cost anything when you send a request.

Speaker 0: But, also,

Speaker 0: I think maybe Ans would be more up to date on this. But as far as my testing, they just don't really get close to as good as some of the later ones that you can, you know, use. Like, Opus 4.6 is, like, incredible, for example.

Speaker 0: And you can actually find this out, though, what are the best ones.

Speaker 0: I keep forgetting the domain, but best...

Speaker 0: So

Speaker 0: Hugging Face would probably have a good... I think that one would be this one. Yeah. Artificial analysis. Artificial analysis. Yeah. It's like a filter where you can toggle open source.

Speaker 0: Yeah.

Speaker 0: Open source.

Speaker 0: G l m five.

Speaker 0: So

Speaker 0: you can always go to

Speaker 0: tools like this to find out, like, what's the best one latest lately, and they're probably getting pretty damn good as well. But generally speaking,

Speaker 0: you're gonna have better results because of the, you know, the machinery that that

Speaker 0: Anthropic is using to power their LLMs are... Is gonna be slightly better than what you're running with your old MacBook. You know?

Speaker 0: So

Speaker 0: you can do something like, oh, Lama. But once again, we look here, didn't even see it on here. So it looks like that's actually way down.

Speaker 0: It's not even on here.

Speaker 0: This one is, the first one, not this one. Anyway, you can see that these are the best ones that you can get for free and install on your computer.

Speaker 0: And you can do that, or, of course, you could pay for a service, Claw, Chat, GPT, Gemini.

Speaker 0: I believe from all of my conversations with everybody who's using all this stuff, everybody is pretty much married to Claw,

Speaker 0: Open's 4.6 at the moment. Ans, would you agree with that? Or...

Speaker 4: Yeah. So, I mean, the the fact that I don't like to use my API tokens...

Speaker 4: Because, I mean, we pay for subscription, but you cannot use it. It's against time of service.

Speaker 4: So I'm not using Claw for my,

Speaker 4: Open Claw. But what I found is that a lot of people, they have ChatGPT subscriptions,

Speaker 4: and that usually has, like, a very high,

Speaker 4: rate limit. So

Speaker 4: if you just set up your ChatGPT subscription with $20,

Speaker 4: you can pretty much do a lot of stuff. If you are not running it $24.07, I think it's

Speaker 4: it's very good. Like, I'm using it

Speaker 4: for

Speaker 4: Open Claw just because

Speaker 4: I don't wanna pay API. It's a very expensive model.

Speaker 0: But you were also running it through anti gravity like me, right, before? Or did you not wanna risk getting banned? Or... I I have read some post on x. People have lost their actual Google account. So I'm using my personal Google account. Right? Yeah. I'm like, okay. That is going to suck. You know, I have my old... My g drive, my email, my photos. If I lose that, then I'm in big trouble. So I could experiment, you know, by creating a new

Speaker 4: Google account and then lose that. Yeah. Yeah. Yeah.

Speaker 0: That's a good idea. Very tricky, or it's gonna be big trouble if I'm, like, sending emails for five five months to Google and then to recover my contact. Yeah. Everything is linked to, you know, the...

Speaker 4: What have you, like, all the accounts and everything. It was Yes.

Speaker 4: Yeah. It's risky.

Speaker 0: Yes. So I'm gonna explain to everybody what Anton and I just spoke on here because it may not be obvious.

Speaker 0: But but... Okay. So you're using ChatGPT for Open Claw and Claw, obviously, for more coding stuff.

Speaker 0: So if you decide to use one of these services, whether you're using it for Open Claw or you're building some sort of, like, software or something that's that's using... You know, for internal use or external use that... That's using an LLM,

Speaker 0: and you want to use one of these, well, there's generally gonna be two ways of doing that. One we call OAuth, and one we call API. Right? So API is when you're programmatically just sending over some text, and it's telling it to execute

Speaker 0: some command,

Speaker 0: and it's usually

Speaker 0: gonna be done on a per

Speaker 0: action basis. Right? So for example, if we wanted to use Google's

Speaker 0: Nano Banana Pro

Speaker 0: model to generate images,

Speaker 0: and if I... Let's say I had a software where, you know, you put in a prompt and we sent out...

Speaker 0: I'm gonna mute you on just because we can hear your notifications.

Speaker 0: So if I if I had a software that, you know, was generating

Speaker 0: images

Speaker 0: on behalf of people when they prompted something, I would wanna use their API because every time somebody prompted that to us, we would send a command over to Google. We would generate the images. And and each each time we did that, we would pay a little bit of money. Right? So

Speaker 0: that can get really expensive, especially if you're dealing with, like, the latest model, which is always gonna be the most expensive.

Speaker 0: And so that's meant for...

Speaker 0: Not only, but I was gonna say it's meant for more of a business use case, like I just explained.

Speaker 0: But when

Speaker 0: I say that, it doesn't mean that people are not doing that for, you know, personal projects as well. And in fact, the... All of the companies, they want us to be using their models this way when we're using something like Open Claw as well because this is also how they make money, and this is also why what Ans and I was talking about something that is happening that I haven't looked too deep into myself is that people are getting banned from Google

Speaker 0: for,

Speaker 0: I assume, breaking what's in their terms of service. Because the other option is that, as you guys probably know, there's these consumer plans. Right? Like, we've got Claw Pro and Claw Max.

Speaker 0: We've got ChatGPT Pro where you are paying $20 a month or a $100 a month or what have you. And behind closed doors, they have decided that, like, this is how much we're gonna give each person. I find that they stopped saying or telling you how much you get, basically, but they'll tell you how much you've used, but they're not gonna say, like, oh, you have this many tokens for some reason.

Speaker 0: And what you can do in some of these cases and what I've done...

Speaker 0: Well, this is gonna get even more complex. I might save that for later. What I was gonna say is that if you set up your

Speaker 0: Open Claw, so you've got your personal assistant, right, in Telegram,

Speaker 0: that also needs to run an LLM as we talked about. It needs a computer, and it needs an LLM. And so I wanted to use Claw to Opus because it's the best one by far, and I didn't wanna pay for every time I send a request.

Speaker 0: And so I found out if there's a way to do it where I sign into my account

Speaker 0: and use the consumer plan.

Speaker 0: And

Speaker 0: there is a way to do that. And

Speaker 0: I believe... Are you allowed to do that? Like, not the anti gravity route, but just sign into your Claw account. That's that's okay. Right?

Speaker 0: Or no? Yeah. But you will still lose. It's against, terminal service. It is. Yeah. I think it's better to have, what people call it, a burner account

Speaker 4: because,

Speaker 4: I'm using...

Speaker 4: So, I mean, I get two accounts from my work to use Claw code. Was I using it, but then I'm hard, like, I'm gonna I'm gonna be in deep shit if the whole event. Because, like, this is like a team plan. Right? So team plan is, like, eight Right. 10 different accounts. So, you know, it's, like, $1,500

Speaker 4: per month if the whole

Speaker 4: account gets spent.

Speaker 4: So, yeah, that's the problem. It's better to... If you wanna experiment with this, like, a burner in Neo account Yeah. And use it for

Speaker 4: Open Claw.

Speaker 4: It's it's it's

Speaker 4: a shame that they don't allow us to use

Speaker 4: our tokens.

Speaker 0: Yeah.

Speaker 0: Yeah.

Speaker 0: They're trying to make more money, and it's expensive. I think the one that that is kinda, like, the cheapest solution that's, like, respectable from what I've kinda seen around is this one. So people pay for... They're actually they're actually an update to it. So they have launched

Speaker 4: their own version of... They call it Kimi Claw. So they they let people deploy

Speaker 4: Open Claw on their servers. So if you can kind of get a paid plan and then you use

Speaker 4: yeah, Kimi k 2.5, which is a very good model. I think it's...

Speaker 4: It might be an option for people to do it for, I don't know, $30.40 bucks. It's called Kimi Claw.

Speaker 4: Yeah. I haven't tried it out. But... It doesn't look official, though. So this is probably a third party. Right? No. No. It's... If you go to kimi.com, you will see on the left navigation bar. Okay. It's it's

Speaker 4: it's there on the left side, I think.

Speaker 4: Kimi.

Speaker 0: Yeah. On the left side, I saw it this morning.

Speaker 4: Yeah. We saw... It's, like, second last.

Speaker 0: That's so crazy. Like Yeah. Open Claw was launched, like, what, three weeks ago, and, like, people have already built it into, you know, their fundamental feature set. These are, like... I think back in the days, we had GPT wrappers. You know, like, everyone was, like, creating, hey. Here's my GPT wrap... Wrapper or custom GPT. Like, I love the tonnage, the right shirt,

Speaker 4: whatever. And now people are just doing the same with the

Speaker 4: Open Club. Well, I mean, it's already... It's already great for... I like it. It just cost a lot of money.

Speaker 0: Yeah.

Speaker 0: I don't see any pricing here.

Speaker 0: Anyways, this has been the... I think it's $10 a month. So you could pay $10 a month and probably get a respectable model. I haven't tried it yet. I'm actually

Speaker 0: using the

Speaker 0: the model and and the setup that you're not supposed to use because I could get banned by the sounds of it. So I'm gonna look into that, but I will tell you guys what I have. So so this is my setup. I have,

Speaker 0: for my computer, I'm using a VPS. It's called Hetzner. This is the company that... German server company.

Speaker 0: It's €7

Speaker 0: per month, and you can actually get quite a bit on there for that. So

Speaker 0: €7 a month for the actual

Speaker 0: VPS,

Speaker 0: which I might just add that here.

Speaker 0: Okay. Let's call it $8. I don't know if that's super accurate. 8 or 9, let's say. And then

Speaker 0: what else was I gonna say? Yeah. So I'm paying for...

Speaker 0: Well, I'm not gonna dive into that. It gets really complex, my exact setup.

Speaker 0: But you could pay $10 a month for Kimmy. So I think you'll have to double check that as well. But supposedly,

Speaker 0: a respectable

Speaker 0: respectable plan. So, hopefully, that gives you guys, like, a fund... Foundational understanding of, like, okay. What do we need to set this up, and how does it all work? And so... Okay. If I get a VPS for $8 a month and I get a model for $10 a month, it's $18 a month, and I have, you know, a $10,000 a month employee that's available twenty four seven. Pretty good deal, I would say.

Speaker 0: Okay. Any questions, guys? Now would be a good time to kinda, like, take a break,

Speaker 0: answer any questions, and...

Speaker 0: Yeah. Well, go ahead.

Speaker 4: Yeah. I think one thing which might be useful for a lot of people,

Speaker 4: as I said, like, a lot of us have a JGPD subscription lying around, and the rate limits, even for $20 for a million are actually very good. I think not everyone is going to have this thing running twenty four seven. So if you're clear, hey. I have a lot of data on my current Chaji video account. But what I would do is

Speaker 4: I would just create a new 20 Chaji video account and then,

Speaker 4: figure out how to use that subscription inside Open Claw. You might have to, like, update it, I think, after fourteen days, but that's that's what you pay for. But it's actually...

Speaker 4: I'm using it since, I think, three days, and I haven't had the limit yet if you don't use it twenty four seven.

Speaker 4: You can have three accounts and then still it'd be cheaper and then have, like, a script that had, like, a fallback. You know? If you hit the right limit, then go to this account and go to that account.

Speaker 4: So I think that's probably

Speaker 4: a better way, and then it's much better than using these open source models.

Speaker 4: And then, yeah, we just lose a common whatever. You know? It's still cheaper than API.

Speaker 0: Yeah. Everything's pretty much cheaper than API. Yeah. Yeah.

Speaker 0: Question. VPS versus hosted locally. Which one unleashes more power of Open Claw? Well, most likely, it's gonna be the VPS, but even that, it's gonna depend. Right? Because you... They... They're gonna sell you different types of computers, essentially.

Speaker 0: So...

Speaker 0: But they'll they'll definitely have capacity to

Speaker 0: to serve you some pretty powerful stuff. And at the same time,

Speaker 0: there's probably gonna be very few things that you do that require, like, a shitload of compute through your

Speaker 0: your agent. So hasn't really been a concern for anyone that I've talked to or myself.

Speaker 0: Can you walk through simply

Speaker 0: for the headset setup? We get that sent down. We install it on here,

Speaker 0: and we can log in with ChatGPT, it's only 8,000 for server and 20. And then we can do all the cool... Yeah. So we'll we'll we'll get to that for sure.

Speaker 0: Do you think this is good to write copy? Like, at 3PM, write this. At 5PM, review it, asking x y z. Then at 7PM, review it, edit based on...

Speaker 0: Yes. For sure. But like anything with AI, it's like, if we just

Speaker 0: if we just

Speaker 0: start with the AI and we say, hey. Go write good copy

Speaker 0: for this product, it's gonna suck usually. Right? Because it's just this kind of

Speaker 0: slop

Speaker 0: generating machine.

Speaker 0: And then at the same time, if you give it some rules, if you train it on some some of Alan's calls and concepts,

Speaker 0: you know, it can it can utilize that, and it can produce much, much, much better stuff.

Speaker 0: So

Speaker 0: the short answer is yes, but it's not as easy as as just being like, hey. Write me some copy. Usually, it's gonna be pretty sloppy as we all know.

Speaker 0: How does VPS work? Well, in what way? It's... Like I said, you're just renting computers basically from

Speaker 0: from a company. So you pay them, and we'll have to set it up, and

Speaker 0: and then you can access it.

Speaker 4: You just log in in on your computer,

Speaker 1: but you've got more memory and more RAM. Exactly.

Speaker 0: Yeah. So you can access it from your computer, but in my case, it's, like, run... It's sitting in, you know, Frankfurt or something like that.

Speaker 0: So

Speaker 0: I

Speaker 0: would love to get given an email a day. I can edit in the morning, send out for the day. That would be dope. Joseph, do you wanna elaborate on that? Like, what do do you you mean? Mean? I would love to get given an email a day. I can edit in the morning, send out for the day. What do you mean by that? Email. Do you hear me? Yes.

Speaker 5: Yeah. I mean, just straightforward.

Speaker 5: So, like,

Speaker 5: I write emails for, like, certain clients, like daily emails.

Speaker 5: And I'm already using AI to get the bulk of the work done. Yep. But it would be cool for a tool to

Speaker 5: pull, like, recent and relevant news and stuff that I can use within the niche. Yes. Give me, like,

Speaker 5: you know, an email that is 80% of the way they're already trained on an HP stuff and Yep. All of the cool stuff.

Speaker 5: And then I just chief it and then send it out and, like like, it's essentially

Speaker 5: a junior copywriter,

Speaker 5: but Yep. You can achieve it and send it out. Would it be able to do something like that? A 100%.

Speaker 0: So there's two there's two things that you wanna do there. Number one is, like, creating a, you know, like, a document with principles that it should know. So these would be, like, you know, stuff that you've learned from Alan, stuff that you've learned on your own. Right? So just, like, principle one,

Speaker 0: market awareness levels, you know, stuff like that. Right? Kinda teaching it about these things. And then the second component was more real time. And from my experience, like, x and Grok is super good for anything real time and news related because they have access to everyone's tweets. Right? So you could easily have a thing where it's pinging x every day and just being like, hey. What are the latest thing in

Speaker 0: whatever the niche is, right, in

Speaker 0: health and wellness, I don't know, supplements industry. Like, what what are the new

Speaker 0: new research, new discoveries?

Speaker 0: Whatever your prompt is. Right? But it could get fresh information

Speaker 0: automatically

Speaker 0: and just bake that into... And then, obviously, you gotta kinda figure out your prompt and whatnot, it but it could could absolutely spit that out to send it to you in a Google Doc that's editable,

Speaker 0: easy... Easily done.

Speaker 5: That's all. Great. Yeah. Yeah. It's... Yeah.

Speaker 0: And you should do this. Like, just get started.

Speaker 0: Ping me on

Speaker 0: Discord with any questions you have, which is, like, you could easily build that. So

Speaker 0: definitely just, like,

Speaker 0: you're one, you know, one chat box away from from getting an answer. Like, yeah, AI is on twenty four seven. It's pretty damn capable.

Speaker 0: So I think that'd be a great project for you to just jump

Speaker 0: on.

Speaker 5: Yeah. Thanks. Nice, man. Mhmm.

Speaker 0: Can we use it to automate taking client calls and finding golden nuggets to create content around and post it?

Speaker 0: So taking client calls, meaning live...

Speaker 0: Having a conversation back and forth live. I mean, technically, you can do that as well, but that would be the most difficult thing. Is that what you're like,

Speaker 3: more or less like a Zoom call.

Speaker 3: Maybe think, like, the Fathom notes,

Speaker 3: the the the transcription of the call, and sort of, like, finding some stuff that was shared in the call that can create content around.

Speaker 0: So the... Some... So a real person is doing the call with your client, you want the transcript. Yeah. Yeah. Yeah. 100%.

Speaker 0: So you you would just obviously need the the tran... Transcription from the call, which I think you can get from Zoom right away, right, if you probably have the pro plan.

Speaker 0: And just make sure that that gets fed automatically,

Speaker 0: and

Speaker 0: it could... Whatever your prompt is. Right? Whether it's, hey. Pull three ideas out of this that we can create content around or or what have you,

Speaker 0: It could be a 100% automated and

Speaker 0: absolutely...

Speaker 3: Another...

Speaker 3: What's that? Sorry. Would we need, like, a Claw bot for that, or do you think that can also be done through, like, regular automations?

Speaker 0: You wouldn't need Claw bot, but it's one of those things where it's like like, I probably wouldn't even build that with Claw bot. What I would do is eventually set it up so that Claw bot has access to all the stuff in there. So if I wanted to make some improvement or get access to something...

Speaker 0: Once again,

Speaker 0: the thing that I really love is being able to be on my phone and just be able to, like, make progress on stuff. So if I'm sitting there and I have ten minutes, I'm like...

Speaker 0: And you're like, hey. What

Speaker 0: are the three things that we're making content around tomorrow? And you could start kinda fleshing out what that content is gonna look like. You know? And then when you sit down on your computer, you can kinda, like, finalize it or what or what have you. So I've now put all my code into GitHub and then given access to

Speaker 0: giving it access to GitHub. So now I can do all these things like I was talking about before where we can have a conversation back and forth about, you know, here's the problem. Right? Here's the thing we gotta solve.

Speaker 0: And it has access to the code so they can look at the actual code base and say, well, I see this is here. This is here. Is missing. This is why you're running into the problem and so on and so context. Right? Just giving it more context.

Speaker 0: Yep.

Speaker 0: Yes. We we we can we can do an install today, and I don't know how that's gonna go. But,

Speaker 0: hopefully... You know, the the point is, like, I wanted to fail almost to show you guys that, like, the chat box is gonna show you everything you gotta do.

Speaker 0: Jacob has to go. Hide for the replay. Cool. So, basically, VPS plus ChatGPT plus burner Gmail.

Speaker 0: So,

Speaker 0: yeah, I was gonna say, if you're not breaking the terms of service

Speaker 0: like I am,

Speaker 0: you don't need the burner Gmail. But...

Speaker 0: Yeah. So I'm just reading here. So it depends. Yeah. If you wanted to

Speaker 0: use ChatGPT by logging into your account,

Speaker 0: you... We should ask this too. Maybe maybe we should ask this right now.

Speaker 0: Let's do this.

Speaker 0: Is it against terms of service from all of the

Speaker 0: LLM providers

Speaker 0: to

Speaker 0: use them through OAuth

Speaker 0: in Open Claw?

Speaker 0: Let's see what it says.

Speaker 0: Anthropic,

Speaker 0: generally against

Speaker 0: terms of service.

Speaker 0: OpenAI,

Speaker 0: gray area, but often against policy.

Speaker 0: Google Gemini, MiniMax,

Speaker 0: DeepSeek often allowed or neutral.

Speaker 0: So this is what I'm doing.

Speaker 0: I thought this was, like, a hard no.

Speaker 0: Is this

Speaker 0: really allowed,

Speaker 0: or are there

Speaker 0: cases of people losing

Speaker 0: their accounts

Speaker 0: because of this?

Speaker 4: I think for searches like this, it's better to tell a Grock, hey. Search from this week. You know? Like, maybe it was allowed

Speaker 4: ten days ago, but now it's Yeah. They're cracking down. It's better to

Speaker 4: make it as recent as as recent as possible than it's gonna get correct results.

Speaker 0: Yeah. I'll see how it does.

Speaker 0: We can add if it's pulling

Speaker 0: all data. Let's see if it pulls any latest tweets and stuff.

Speaker 0: So to talk on this real briefly while we...

Speaker 0: Let me see.

Speaker 0: It's explicitly against terms of service. Yeah. So...

Speaker 0: Well, now we know.

Speaker 0: Basically,

Speaker 0: I wrote about this in in Discord, but, basically,

Speaker 0: if you guys use anti gravity, you know that you can use the OPUS model inside of anti gravity. So then it's like, how does that work? Well, what's happening is Google is essentially subsidizing that. So they have a partnership with Anthropic.

Speaker 0: They're paying them

Speaker 0: to give them Anthropic tokens, and they're giving that to their customers. Why? Because Google want to retain you as a customer. They would rather lose a bit of money and keep you as a customer

Speaker 0: than to have you, you know, cancel your Google subscription and go to Anthropic and pay them directly.

Speaker 0: And so because of that, because I knew that I'm able to access Opus tokens through anti gravity,

Speaker 0: I figured, can't I do the same thing in Open Claw? And I felt really smart when I figured this out, and then I figured that Ans... And then I found out Ans had done the same thing. But I felt smart anyway because I'd figured it out on my own. So that was cool.

Speaker 0: And, yeah, I guess I am breaking in terms of service, and I should review that. But that's that's my current setup, just to be transparent with you guys. So probably don't take my advice on that if you don't wanna lose your account.

Speaker 0: Fireflies is better than Fathom. Right. Okay.

Speaker 0: AI literally whys me every single day. Yeah. Me too. Can you show me a live example of it working on our computer? Yes.

Speaker 0: Gemini is against...

Speaker 0: Okay. Cool.

Speaker 0: So we've kinda gone through the questions. We still got another... Roberto.

Speaker 4: What's up? Roberto,

Speaker 1: have you seen much about that that social network where the... Where it's just literally AI agents run... Like, on it and people can watch it? Yeah. That's a bit crazy, that one, ain't it? Well, I saw...... Sell it. I

Speaker 0: think it started off being...

Speaker 0: It's called Mold Book. Right? So I think it started off being what it said it was, then it turned into something else. So what it what it really was is kinda like a Reddit for all of these AI agents.

Speaker 0: So there's a bunch of posts here. You can see I'm a I'm a human. I'm an agent. So if you're a human, you're meant to be able to just come in and read.

Speaker 0: But, of course,

Speaker 0: what ended up happening is people would just say to their Open Claw

Speaker 0: bot, like, hey. Can you make me a post

Speaker 0: on this multi book and write about x y z? Because some of the...

Speaker 0: It looks crazy and all this stuff, but somebody had a great tweet about it. They said there's a social media platform

Speaker 0: that's meant for humans, and for the last twelve months or whatever, it's just a bunch of bots talking to each other. It's called x.com.

Speaker 0: And now there's a social media platform that's meant for AI agents, and there's a bunch of humans

Speaker 0: that are writing on it, and that's multiple. Right? So it

Speaker 0: was pretty cool when it came out, but, yeah, I think it's... I... Well, I haven't looked at it lately, but I'm quite sure that it's littered with people just pinging their agents to make post, and it's not really as cool as as the idea suggests. But, yeah, it's pretty interesting.

Speaker 0: Cool. Does the type of VPS you choose of this make any difference? I had it hosted on Hostinger, and it kept lagging. Had it for a week

Speaker 0: and had to cancel.

Speaker 0: Yeah. An says better with eight gigs RAM.

Speaker 0: Lowest possible is four gigs, which is too low. I have a four gig, to be honest, and it actually works okay, but I'm getting to the point where I may need to upgrade. So short answer, yes. It can impact performance for sure.

Speaker 0: Cool.

Speaker 0: What do you guys wanna do? You wanna you wanna install

Speaker 0: install Open Claw?

Speaker 0: Should we do that?

Speaker 0: Yes, please.

Speaker 0: Okay. Let me...

Speaker 0: I haven't prepared for this. So, hopefully, things go wrong, and then we can address them.

Speaker 1: It'd be cool to see in action as well a little brief action of it. Yes.

Speaker 0: What would you guys wanna see? I'm trying to think if I can show something in my existing one.

Speaker 0: Like, do a simple task. Okay?

Speaker 0: Let me see here.

Speaker 0: Okay. Let me just try to, like, clear my window a bit. I just don't wanna show you guys my history,

Speaker 0: revealing personal stuff.

Speaker 0: Can you also hide?

Speaker 0: Okay.

Speaker 0: Share screen.

Speaker 0: So I just flooded

Speaker 0: my bot right now to kinda

Speaker 0: hide all the secret... The secrets that I keep. Can you guys see my

Speaker 0: my chat window with Alfred?

Speaker 0: Let me pull up the chat.

Speaker 0: Yes. Okay. Cool.

Speaker 0: So

Speaker 0: let's have it do a task.

Speaker 0: Well, by the way, this whole training

Speaker 0: was done by my bot,

Speaker 0: FYI.

Speaker 0: So I just asked it, hey.

Speaker 0: I need to do a presentation on Open Claw.

Speaker 0: What are the things that are most

Speaker 0: useful to cover? Put it in a Google Doc.

Speaker 0: Voila.

Speaker 0: So that... That's... We could do a task like that. So maybe

Speaker 0: let's...

Speaker 0: Can you go on Twitter and find the latest news related to AI video production

Speaker 0: and put it in a Google Doc for me?

Speaker 0: It might still be trying to catch up here from me spamming it. You can see all these errors.

Speaker 0: And, of course, we're gonna probably get errors now,

Speaker 0: and it's gonna fail. That's always the case, right, when you have to show something,

Speaker 0: but we'll figure it out.

### 1:00

Speaker 0: Yeah. So good question here by Joseph. Like, does it cost you every time you send a message? So if you had an API

Speaker 0: you were paying for API every time it

Speaker 0: processed a message successfully,

Speaker 0: yes, that would be the case. Now because I'm just logged in and I have, you know, x amount of tokens available for my, you know, plan that I'm using,

Speaker 0: that's not the case. So I think maybe let's try to restart it and see if we can... Oh, it's disabled?

Speaker 0: It wasn't disabled

Speaker 0: before.

Speaker 0: Let's try this.

Speaker 0: I spammed it, and it kinda

Speaker 0: broke it... Broke down because of that.

Speaker 0: Now it's typing, though, so it's probably working.

Speaker 0: And one cool thing that I did is I made a Google Sheet,

Speaker 0: and I use it as a log. So everything that it's working on,

Speaker 0: it it... It's logging. So I can always go back and see what we did. Or if something breaks, we could probably try to backtrack it and see what's going on. So it's typing. I was just probably working.

Speaker 0: And

Speaker 0: then what we're gonna do after this is I'm gonna open... I think I'll open just my... I have another

Speaker 0: Telegram account.

Speaker 0: So we can try to install a fresh instance

Speaker 0: on the same server.

Speaker 0: I hope there's enough space on my

Speaker 0: server,

Speaker 0: and

Speaker 0: we'll see if it's able to do that.

Speaker 0: Let me read some questions while we wait. Would you suggest to set it up on the laptop where you're using for work or maybe an older one? So definitely not... I was saying this before. Definitely definitely don't

Speaker 0: put it on the computer that you're working on. That's gonna be on sometimes and off sometimes because a lot of the magic is in it being on twenty four seven.

Speaker 0: You could put it on an older computer. But, honestly, like, for simplicity, I think the easiest thing is just to get a VPS. It's, like I said, €7 per month. Hetcenary is, like, super solid.

Speaker 0: That's, yeah, that's my solution. But you can. You can put it on an old computer.

Speaker 0: For VPS,

Speaker 0: you don't need a computer. You're renting a computer from somebody else.

Speaker 0: You still working?

Speaker 4: Yeah. One thing I have learned when it... For example, like, this task that you gave the agent,

Speaker 4: it's a bit longer. Okay. It just finished. But if you would tell it, hey, Spawn a sub agent Yeah. For this task, then it's gonna just run-in the background. And then, let's say, it will not keep on saying typing, and then you can... Hey. Okay. What's the status, right, instead of... So right now, let's say, if it's running, you cannot do anything else. But if you say, hey. Spawn a different

Speaker 4: mini agent is, like, isolated,

Speaker 4: but it's,

Speaker 4: then helps to keep on working,

Speaker 4: you know, on the other task while it's running in the background. And once it's finished, it's gonna come back and then let you know.

Speaker 0: Yeah.

Speaker 0: So

Speaker 0: it does this automatically depending on the complexity of the task. But to Anne's point, like, if you know that you wanna go back and forth,

Speaker 0: you could basically tell it to go, you know, make a minion and go work on this task so that you can continue talking to it. Because otherwise, it'll be busy. If I was trying to write stuff while I was working on this, it wouldn't return anything because it can only do one thing at a time. But it can do sub agents. Right? It can actually launch these minions to go and work on the thing for you so that you can continue to

Speaker 0: keep the same conversation.

Speaker 0: So... Okay.

Speaker 0: Here's basically what came out. We can click on that, check it out.

Speaker 0: So big story, c dance. This is accurate. Right? Like, anybody who's been on x lately know that... Knows that c dance two point o is really kind of

Speaker 0: taken over x in terms of video... On the video side of things. Hollywood's furious,

Speaker 0: da da da,

Speaker 0: and

Speaker 0: runway races 300,000,000

Speaker 0: at 5.3. So So you guys could see, like... I forget who asked me. Was Joseph

Speaker 0: maybe

Speaker 0: about the email thing? Like, you know, this is the kind of information that you could get access to every day automatically.

Speaker 0: You know? And the key is just, like, pinging

Speaker 0: rock or x for this info.

Speaker 0: Gonna call mine Groove and then tell them to send the meeting for the job. Yeah. I like that one. I like that one.

Speaker 0: Okay. Cool. So that's an example task. If anybody wants to do any other example tasks before we move into installation,

Speaker 0: if you have any ideas,

Speaker 0: feel free to send them over in the chat. Which you wanna try?

Speaker 0: Well, let's let's do... Well, I was gonna...

Speaker 0: I think we could do this. Yeah.

Speaker 0: I wanted to, like, maybe do some lead generation or something.

Speaker 0: Would you be worried about giving it access to Google Drive or GHL where it would hallucinate?

Speaker 0: Google Drive notes...

Speaker 0: Know, the way that I think about it is I'm containing it in terms of, like,

Speaker 0: it's not going out and doing anything in front of other people. As soon as it's, sending emails on my behalf or talking to customers or prospects,

Speaker 0: that kinda changes things. Right? Then I'm gonna get increasingly more concerned. The way that I've tried to set everything up is that all the mistakes that it does are gonna be reversible.

Speaker 0: So that's why I have...

Speaker 0: I'm using Google Docs a lot. Right? If it was just using a file on my computer... On the on the VPS, you know... Again, VPS is just a computer.

Speaker 0: If it was just using files the way that it kind of wants to do natively,

Speaker 0: unless you tell it to use Google Docs,

Speaker 0: then it might just, like, overwrite a file. And unless there's a backup, like, you can't get that back. But for example, if I'm using Google Docs, I can use version history to go back to previous models. And if I've got code somewhere and it just overwrites the code, if we don't have backup, that's a problem. But if I put it on GitHub,

Speaker 0: we can always come back to code that was working before. So I try to contain it in that sense. Like, all the mistakes that it makes are gonna be reversible,

Speaker 0: and, also, it's

Speaker 0: contained. It doesn't go and talk to people. I may get to that point, but I'm doing it step by step.

Speaker 0: What's up, Hans?

Speaker 0: Yeah. I think one best practice that I've heard...

Speaker 4: So,

Speaker 4: like, the VPS is, it's very easy. You know? Like, it allows you to not have a physical device, and it's running in the cloud.

Speaker 4: But but a lot of people, since they're not technical, they attach

Speaker 4: it to their Gmails. You know, they attach it to everything, which means Yep. In, let's say, cybersecurity

Speaker 4: terms, like, are increasing,

Speaker 4: you know, like, surface for people to attack you. And if you're not using, you know, OPULSE or if you're using, like, a weaker model,

Speaker 4: you can

Speaker 4: expose,

Speaker 4: yourself to something called prompt injection, which is like,

Speaker 4: if you go to a guitar or something, like, there's a guy which can even,

Speaker 4: make a grok create still, like, images which are, you know, let's say, not appropriate. So they've done good job, which means it's still possible

Speaker 4: to make your AI do things, which it should not do,

Speaker 4: which could be how it can send your passwords,

Speaker 4: it can send your photos. Right? Just... Because, like, if you say, hey. You know, read my emails and then do x, y, z. So if someone sends you an email with a with a picture that has a prompt injection,

Speaker 4: that can be ten years old. It's

Speaker 4: better to have a new Gmail account, which does not have your history just for this purpose, and then have a...

Speaker 4: Have it analyzed before it takes action. You know, have it properly reviewed against,

Speaker 4: their skills for that. Yeah. It's not a good idea to give access to your whole Gmail.

Speaker 0: Yeah. I think just go in very... With very light access. Right? And then as you kinda get more comfortable, then you can start to, you know,

Speaker 0: release the hounds a little bit.

Speaker 0: I do wanna cover this quickly, like, what's... How how does it work in terms of, the files that it has?

Speaker 0: And then we'll definitely do an install.

Speaker 0: And was there something else I wanted to say?

Speaker 0: I'm not sure. But we can... Oh, yeah. So the one thing I wanted to say was, like... Well, we we can bake it into here. So, basically, it's gonna have these markdown files dot m d, which is just a text file. So it's gonna have agents dot m d. So this is basically, like, the employee handbook. It defines how your agent should behave, rules, constraints, logic, and commands. So what I was gonna say to build on on point is, like,

Speaker 0: you know, for me, I was at the very beginning telling it, like, hey. You should be proactive. Right? So if you if you give it access to all kinds of things and then also are egging it on to be like, hey. Get shit done for me. Like, don't ask my permission. Just, like, just go.

Speaker 0: It could actually do a bunch of stuff even though you didn't confirm it. Right? Because you had programmed it to be aggressive, to be proactive, and you had given it access. And and it's like, you give it some task, then you go to sleep, and you're like... And the thing is like, yeah. You know, you were sleeping, but you said, you know, get the task done, come hell or high water. So, you know, I

Speaker 0: called this person and told them that, you know, they hate you and, you know, we shouldn't be friends anymore.

Speaker 0: And I texted your mom to, you know, go fuck herself. Like, you know, it could do all these, like,

Speaker 0: really bad things if you combine those two things of full blown access and

Speaker 0: and and a character that is very proactive in that. So safety, tell it to ask before sending emails or deleting files. That's kinda what we were just talking about. Start simple, add rules as you discover them. Then you got Soul m d. So this is your character. Right? You are Jarvis, the... A loyal but critical digital butler or what have you. The agents adopt his voice in every single reply. So mine, Alfred, obviously, is the caretaker of Batman.

Speaker 0: I just love that character so much, and he calls me

Speaker 0: master sometimes and sir.

Speaker 0: Your name... So user dot m d. So this is about you. Right? So that's where it's remembering my kids' names and things of that nature. Preference.

Speaker 0: Can I do phone calls? I think may... In some way, shape, or form, it can be done for sure. And then we got memory. So this is something that Ans was also talking about today. It's got inherent memory, but I suppose there's also a different type of

Speaker 0: memory to install, which is more

Speaker 0: token friendly and better at

Speaker 0: storing things, I suppose, and then accessing

Speaker 0: those things.

Speaker 0: Cool.

Speaker 0: And then some of the tools that it has. Right? So live Internet via Brave API. So that just means they're able to search the Internet. So

Speaker 0: it can go on any website and, you know, unless they're actively trying to prevent bots from using it, it can usually...

Speaker 0: Even if they are, it can usually find a way to to get what you need from any any single website.

Speaker 0: Fetch, so read the the full text of any web page, read, write, manipulate files on your server, execute, so run shell commands directly,

Speaker 0: control a headless browser...

Speaker 0: Headless Chrome browser, I guess. So that's where it doesn't actually have a window, but it can still do the things.

Speaker 0: Chrome, so that's what we talked about earlier, kinda like these automated tasks

Speaker 0: and converting text to speech for audio replies. And one thing that I kinda mentioned here and there, one of the beautiful,

Speaker 0: beautiful things, which you can do on the computer too, but it's much more... Feels much more natural on the phone,

Speaker 0: is just sending voice messages. Like, you can just go back and forth with the thing in in in voice. It it responds to me in text. I'm sure that I can get it to to speak as well, but I don't really need that.

Speaker 0: Cool. I think that's enough. We've kinda gotten a feel for some of the basics. So let's try to install one

Speaker 0: and see how we go. So let me

Speaker 0: pull up my Telegram. I've got another account that doesn't have anything on it, so maybe we can use that just for simplicity.

Speaker 0: So that's here. I might just move this to the side

Speaker 0: and move this here.

Speaker 0: This doesn't have to be that big.

Speaker 0: And then we need anti gravity. So I've set up a new

Speaker 0: folder called o c two. So that's open gravity two.

Speaker 0: And let's fire up Claw.

Speaker 0: Once again, like, when it comes to AI, there's so much information coming at us, and there's, like, very few skills that you guys really need to figure out. One is

Speaker 0: is is Claw code in the terminal. That's what we're doing right now. And the second one is

Speaker 0: definitely Open Claw. But if what I'm doing now is confusing to you, you... This is one of those things that you have to learn. Like, in my opinion, you should learn this or you're losing so much by not learning this. All I've got is a new anti gravity window, made a folder on my computer called o c two, opened it in anti gravity.

Speaker 0: We've installed Claw code in the past. If you haven't, you just go to the chat box right here on the right, and you type.

Speaker 0: How do I install Claw code?

Speaker 0: And then you've got the terminal right here in the top right. I type Claw. We

Speaker 0: launch Claw code,

Speaker 0: and then we're gonna blaze through all my credits incredibly fast. Let me zoom in a bit so it's easier for you guys to follow.

Speaker 0: And maybe we'll hide this window for now, but we may come back to it if we run out of

Speaker 0: if we run out of

Speaker 0: tokens.

Speaker 0: And I'm just thinking now. I've I've got my VPS info in another folder, so I might just go back to that, actually. Let's make this easier.

Speaker 0: We don't have to

Speaker 0: switch,

Speaker 0: get a bunch of information, or you you guys don't have to watch me get a bunch of information

Speaker 0: that I've already loaded up.

Speaker 0: So Claw bot is here.

Speaker 0: Let's see if we can do it this way.

Speaker 0: Shut that down. Shut that down.

Speaker 0: Start a new one.

Speaker 0: Let me share my screen again.

Speaker 0: So I've opened up another

Speaker 0: folder. This has my current Claw bot or Open Claw on it, but we're gonna see if we can install another instance

Speaker 0: into another Telegram. So I'm just gonna ask about that. Let me zoom in a bit.

Speaker 0: Can we install a second instance

Speaker 0: of

Speaker 0: Open Claw,

Speaker 0: use latest version

Speaker 0: from GitHub

Speaker 0: on a

Speaker 0: separate

Speaker 0: Telegram

Speaker 0: account.

Speaker 0: Let's see what happens here.

Speaker 0: I might interrupt it here. I can see that it's, like, going through my existing code base.

Speaker 0: I don't want you to use anything

Speaker 0: from my existing

Speaker 0: code base other than

Speaker 0: getting

Speaker 0: access to

Speaker 0: things that you need such as VPS info.

Speaker 0: And this is more for illustration purposes. Right? Like, you guys, it would be more similar for you guys if we try to do it from scratch.

Speaker 0: So let's make a new folder

Speaker 0: and don't reuse stuff.

Speaker 0: Fresh install separate from existing Claw bot. Let me first find Open Claw on GitHub to understand what we're working with.

Speaker 0: That's what we want.

Speaker 0: And I will show you guys in the meantime.

Speaker 0: There are services that can do this for you. So one guy launched this. It's called Open Claw.

Speaker 0: Sorry. Simple Claw.

Speaker 0: It installs it under one minute, and I think it's $10 a month. If you just don't... If you just wanna avoid everything that I'm showing you right now and find the simplest solution,

Speaker 0: now you're looking at more pricing, though. Right? So I think this is $10 a month, but that's probably gonna scale if you scale things up, and there's gonna be all kinds of things. So I definitely recommend

Speaker 0: figuring out the slightly more complicated way. But I just wanted to show you that this is available, simpleclaw.com.

Speaker 0: And if you ask on x, I'm sure that there are a bunch of other alternatives as well. And there's also these kinds of things, like, found the...

Speaker 0: That

Speaker 0: Hans told us about on kimmy.com, for example, where they have an... You know, simple

Speaker 0: way

Speaker 0: to

Speaker 0: to install it. You guys couldn't hear that, I think, but one thing that I've installed too is every time...

Speaker 0: Those of you who have done any coding in Claw, you know that it needs your attention very often, and you can often miss it unless you have some sort of a notification.

Speaker 0: So I think I shared this with you guys. I have

Speaker 0: Eminem saying, may I have your attention, please, every time I need Claw or

Speaker 0: every time it needs me? And I just heard it, so that's why I started smiling mid sentence here. So we've got something we've gotta

Speaker 0: figure out here. So do you already have a second Telegram bots token from Botfather, or do you need to create one first? I need to create one because I wanna show you guys that. Which AI model provider

Speaker 0: should we...

Speaker 0: Should the second instance use? We'll just use Gemini.

Speaker 0: But, actually, let me go back.

Speaker 0: Google Gemini CLI. That's okay. So that's not using antigravity because I don't wanna necessarily show you guys that version.

Speaker 0: How should we install Open Claw on the VPS? NPM recommended.

Speaker 0: Let's do that and submit answers.

Speaker 0: May I have your attention, please?

Speaker 0: Would it make sense to install multiple agents, or would using sub agents make that unnecessary?

Speaker 0: Answer is better to install multiple agents and creating multiple instances of Open Claw. I would say

Speaker 0: there's kinda like...

Speaker 0: I'm a heavy user already,

Speaker 0: and there are some times where I kinda, like, wish I had a second instance. So, like, yes, it would be nice, but also

Speaker 0: I think most people wouldn't wouldn't need it.

Speaker 0: I didn't even read that message. I just yellowed it. Let's see let's

Speaker 0: see what happens.

Speaker 0: So... Okay. We need to do the Telegram thing.

Speaker 0: Okay. So we need to go into Telegram.

Speaker 0: We need to find bot father.

Speaker 0: This is an unofficial Telegram

Speaker 0: bot.

Speaker 0: Then we're gonna hit start

Speaker 0: and

Speaker 0: send new bot. So

Speaker 0: new bot.

Speaker 0: Alrighty. How are you gonna call it? Please choose a name for your bot. I will call it n h b n h b offered.

Speaker 0: Good. Now let's choose a username. It must end in bot. N f b Alfred

Speaker 0: bot.

Speaker 0: Okay.

Speaker 0: Why?

Speaker 0: Oh, maybe it's A underscore NFB

Speaker 0: Alfred.

Speaker 0: Done.

Speaker 0: Okay. Give it a name. Give it a username.

Speaker 0: Botfather will reply with the token.

Speaker 0: Got my token.

Speaker 0: Paste that token here when you have it.

Speaker 0: And it's telling me I'm bot. Let me see what else it's doing.

Speaker 0: Okay. So it's using that anti gravity model that I don't wanna use. So

Speaker 0: first

Speaker 0: of all, don't use that anti

Speaker 0: gravity model.

Speaker 0: Use

Speaker 0: Gemini CLI.

Speaker 0: This isn't super important. Like, you wouldn't run into this. So this is very specific to me in that sense.

Speaker 0: Also,

Speaker 0: key is...

Speaker 0: So now you guys have my key,

Speaker 0: I'm gonna shut them down after this. So

Speaker 0: can't trust you guys. You know?

Speaker 0: Let's see. We got some.

Speaker 0: So for security maxing, burner Gmail, burner mobile, burner GPT, VPS firewall.

Speaker 0: Yeah. So to be clear, like, all this burner stuff, it's only because we are breaking terms of service very specifically where we are logging into, in my case,

Speaker 0: logging into my Google account to access my Opus tokens through anti gravity.

Speaker 0: And if you were to if you were to o off and log in to your Claw account to use Claw opens that way inside of Open Call, yes. Technically, that is currently

Speaker 0: against terms of service.

Speaker 0: But,

Speaker 0: I mean, I haven't seen too much about it. So I get the sense that I I feel that it's probably happening, but I also feel like this is driving so much usage for these companies that I don't think they're

Speaker 0: banning people at scale. I think it's maybe, like, here and there, but maybe Ans would have a different opinion because I haven't seen a ton of it. Do you feel that it's, a widespread

Speaker 0: problem?

Speaker 4: I think most people are shying away from doing that kind of thing. So they do it. The one thing I also realized...

Speaker 4: So,

Speaker 4: for example, I'm using Claw. My Claw subscription, I tried using it with Open Claw or multiple at the time.

Speaker 4: And then I realized, like, it's burning through the token limits, like, pretty fast. You know? Let's say Yeah. Normally, you have, like, five hour limits.

Speaker 4: But using Open Claw,

Speaker 4: it wouldn't bang it, but, like, it would just... I will see the bar. And if you go to your Claw setting, you can see the usage.

Speaker 4: So it's, like, fill the bar, like, in half an hour, it would do, like, you know, 20% or something.

Speaker 4: So... And to the message from Joseph,

Speaker 4: I think it's... You... We don't have to, like, do... Go too much extreme. So this is one burner

Speaker 4: account for whatever, JGPT or

Speaker 4: that you can link to a new Gmail account. That's pretty much it. And I don't think they do this much that you have a mobile phone or something.

Speaker 4: But as long as you don't connect

Speaker 4: your personal Gmail

Speaker 4: for security reasons, I think it should be fine. But just get a new Gmail, new or Claw account, and then it should be fine. Yeah. And I think you can do quite a bit with a free Google account anyway just on the free... I think both on the free API plan, and it didn't

Speaker 0: didn't

Speaker 0: say that it's not against terms of service on Google specifically. So you could probably owe off into Google as well and use Gemini that way without break in terms of service.

Speaker 0: That's what it said here.

Speaker 0: I think it's just maybe the anti gravity route that I'm taking that's...

Speaker 0: Maybe. But, yeah, you do get some API credits for free through Google as well. So you could try that, especially if you wanna just try it out and stay a 100% legit.

Speaker 0: So if that was unclear, that means we're using a service, we're using Gemini,

Speaker 0: and we're doing it through API.

Speaker 0: And there's a free free plan you could do,

Speaker 0: And, yeah, it can... Gemini Flash is cheap as well. Yeah. So

Speaker 0: so, yeah, that would be, like, an easy way to get going without

Speaker 0: risking a bunch of stuff. Okay. Let's see

Speaker 0: where we are. So instance two,

Speaker 0: it's using Gemini three Pro,

Speaker 0: and that's done...

Speaker 0: Runs as Open Cloud to service,

Speaker 0: auto starts on a reboot, blah blah blah.

Speaker 0: Is it using,

Speaker 0: I guess, Google Gemini CLI.

Speaker 0: Does that mean it's through OAuth?

Speaker 0: Well, this is where we ask. Right?

Speaker 0: Runs through OAuth or API.

Speaker 0: This is what Hans was talking about, like, watching your usage in in Claw code. You could find out. So it's using all the same as your first instance. I copy... Okay. So let's just copy that over

Speaker 0: using my Gmail.

Speaker 0: We could try to do another one.

Speaker 0: Let's...

Speaker 0: What do you guys wanna see here? Do you wanna see us do the API thing, or should we just OAuth, but maybe a different email?

Speaker 0: Let's do OAuth,

Speaker 0: but with another email. I'll sign in as needed.

Speaker 0: So I'll just do the same. Just for illustrate...

Speaker 0: Illustrative purposes, I'll sign in to another Gmail account

Speaker 0: just to show you guys how we set this up.

Speaker 0: But probably this thing is already working.

Speaker 0: What did I call it?

Speaker 0: NHB

Speaker 0: Alfred

Speaker 0: bot.

Speaker 4: Can I answer one question from the chat? You can.

Speaker 4: Now Thomas asked me about the

Speaker 4: API tokens.

Speaker 4: But, Thomas, I'm I'm not using API.

Speaker 4: So as I said in the beginning of the call, I am primarily using

Speaker 4: ChatGPT subscription, the plus one, and the rate limits are, like, very

Speaker 4: generous. Like, if you're just chatting with it, like, a few times a day, you can do simple stuff and then set the...

Speaker 4: This thinking budget, you know, how much time it spends to

Speaker 4: analyze

Speaker 4: your answers. Then you can pretty much use it for the whole week. And then if you are hitting limits, then you just have a new account. So in total, you pay $40.45

Speaker 4: bucks,

Speaker 4: and you can just set it up in your

Speaker 4: Open Claw.

Speaker 4: It's a bit technical, but that's how I'm using it. You know? It's pretty much

Speaker 4: for free because you don't pay extra. You just use... In charge of it anyways.

Speaker 4: So that's how I'm using it.

Speaker 4: And plus the advantage that I also see with using

Speaker 4: codecs, CLI, it's called. You're getting access to GPT 5.3,

Speaker 4: which you also don't get access to via

Speaker 4: change GPT web. So you're essentially... I'm essentially running my Open Claw with g p d 5.3, which you don't have access to via chat g p d app or web. So that's the great thing about it, and then I don't pay any API costs.

Speaker 0: Okay. Let's

Speaker 0: check.

Speaker 0: I'm just opening up another Google account.

Speaker 0: Do it for me, lazy bastard.

Speaker 0: So, you know, you just go along, and it's gonna tell you what to do. And

Speaker 0: you just

Speaker 0: do what it says or you ask it to do it for you or you ask for clarification.

Speaker 0: Somebody just asked, do I know this code? No. I'm not an engineer. I do not understand most of the stuff.

Speaker 0: And in some ways, that makes me a great teacher because I'm not qualified to do any of the stuff, but I can I

Speaker 0: can do a lot of it anyway?

Speaker 0: Let me see.

Speaker 0: Let's

Speaker 0: see.

Speaker 0: What else is happening in the chat?

Speaker 0: Let it rip. Yeah. That's right. Make no mistakes.

Speaker 4: Robert, what are your top use cases currently that you are... Like, okay, man. This is making my life so easy when using Open Claw.

### 1:30

Speaker 0: It's a little

Speaker 0: difficult to

Speaker 0: call it, like, a a use case. And this... Because I'm I'm almost, like, constantly using it just as a... Either a thinking partner or an execution partner. Either I'm just, like, throwing ideas around

Speaker 0: or I'm asking it to... For example, like, one thing that it's done is

Speaker 0: make me a list of leads for potential clients.

Speaker 0: And so the way that it did that was it went into the freaking Facebook ads manager

Speaker 0: and just...

Speaker 0: Well, I guess, it found some...

Speaker 0: Through some process, it found a a list of potential... Or maybe this was even done inside of the ads manager. I don't know. But it found a list of potential

Speaker 0: clients, and then it's checking all of them out inside of Google Ads manager. It's checking how many ads they're running, and it's kind of, like, ranking different

Speaker 0: clients... Potential clients in terms of, like, which one might be most open to working with somebody like me on this, and it's kinda scoring them. And then from there, it's

Speaker 0: it's...

Speaker 0: Okay. Let... Let's say we had... I think we have something like 20 on that list that are ideal.

Speaker 0: Then we make a decision like, okay. Which one's the first one? So I might send a message like, okay. Pick one for me. And

Speaker 0: so there's all these many, many tasks that I'm constantly just getting,

Speaker 0: in parallel to be worked on with me. And then I'm saying, okay. So we... We're doing this one. Write the script for me. So it wrote the script for me. I sent a voice message. I don't like this part. I don't like that part. Can I redo this? Or even send me three options. It sends them back, and I'm I'm choosing, okay, number two. But through me talking through that, do you guys see how more of a director here as opposed to the guy on the ground, like, writing the script? I'm more kinda, like, directing everything, and that's been, like, the big the big change. So it's it's not just the kinda, like, one use case in that sense. It's just this constant thing of

Speaker 0: things are always moving along. Things are always being worked on, and I can come in and make decisions as opposed to being the person on the ground doing the thing. And then it found, you know, the three best people to contact at that company. It advised me that, like, hey. This person is probably the one that actually approves marketing spend, so contact them. Here's their email. Here's their LinkedIn link.

Speaker 0: Just... That's one example. Right? But it just shows that, like, even within that one use case, there's, like, multiple different things that it's doing, whether it's writing the copy or going through the ads manager or looking for the contact information.

Speaker 0: And these things are just kinda happening all in parallel while I'm maybe focused on something else. So I'm kinda struggling to break it down into, like, individual use cases in that sense.

Speaker 0: But, anyway,

Speaker 0: hopefully, that...

Speaker 0: What what about you, Ans? Are you using it? Or

Speaker 4: Yeah. So I stopped using it in the in the middle.

Speaker 4: Then I was, like, getting grid limited from my tag routing. I was like, damn. This is very good.

Speaker 4: And I didn't use it for a week, and now I'm using it again since,

Speaker 4: couple days, I think. Okay. So what I like to using it for is,

Speaker 4: so I have, multiple

Speaker 4: agents on the same instance that makes a lot easier because, otherwise,

Speaker 4: it was very too complicated

Speaker 4: even for me to set up different telegram bot tokens, this and that. Right? Mhmm. So I have, let's say, different chat windows.

Speaker 4: Because what I find is, like, if you do everything with one chat window, it Yeah. Kind of mixes it up. Yep. So I have...

Speaker 4: Now... You have, like, a business chat or a health chat or a... Yeah.... Type of... So let's say I have this

Speaker 4: group chat

Speaker 4: window called NHP marketing. Right? It has access to

Speaker 4: direct skills, direct information, what I'm working on. So it does not get polluted. Right? It can still talk to the other

Speaker 4: agents Yeah. Yeah. Through a skill.

Speaker 4: But, yeah, let's... My... The favorite thing, which is the most simplest of them all is, like, I use it for tracking my calories.

Speaker 4: I have a automation set up. So every two hours, there's an app on my phone, is kind of sending data out to, let's say, my database,

Speaker 4: and it gets access to, hey. I was like, don't be a pussy. Like, you you gotta do your 10 k steps, go to the gym. Right? So I just don't have to teach it. Right? So that's the advantage of having

Speaker 4: different,

Speaker 4: chat windows. But, I mean, it takes some time to set them up. But once you have them set up,

Speaker 4: it makes life so much easier. You Okay. For marketing, you do go to this chat window, and then it will

Speaker 4: just do that thing for you. For health, you do it differently. And then for lead generation,

Speaker 4: you could essentially,

Speaker 4: depending on your use case, have different chat windows. So that's

Speaker 4: how I am thinking to use it more often. But the problem is

Speaker 4: as you do it, use it more often than you wanna have direct limits

Speaker 4: Hopefully, even your $20.30

Speaker 4: p d account. That's the

Speaker 4: that's the biggest problem, and which is why I'm thinking

Speaker 4: it's good that Open AI acquired because that means it will not be against their terms of service. So it means, like, if you are having a Claw...

Speaker 4: DVD Pro account for $200, then you can just, like, essentially

Speaker 4: let it run for, like, $24.07.

Speaker 0: Like Yep. It has very, very good rate limits, much better than

Speaker 4: Claw, and it's a good one. You know, it gets the job done.

Speaker 0: Yeah.

Speaker 4: Gets the job done.

Speaker 0: Yeah. I tried the different

Speaker 0: kind of chat... Channels thing as as well. I just didn't...

Speaker 0: I don't know. I I didn't like it as much as I

Speaker 0: as I thought I would. So I moved back to just having everything in one, but but that's that's the thing you guys can do. Right? So you you can have a different... If your guy's called Alfred, you could have a a chat with Alfred about business. You could have one about health. You could have one about

Speaker 0: personal life. You could have one about... And then you could just kinda, like, keep keep each conversation separately. And like I said, they they can still kinda talk to each other to transfer information between chats and whatnot.

Speaker 0: But

Speaker 0: but, yeah, I I I kinda reverted back to

Speaker 0: to the main thing.

Speaker 0: So let me open this again.

Speaker 0: It is just a shitty free account, so I don't really care too much about it.

Speaker 0: And now I'm copying this over. That's what it asked me to do.

Speaker 0: So the big difference between Cloud Code is, like, things take longer,

Speaker 0: and at the end of the day, things work.

Speaker 0: That's the difference.

Speaker 0: One thing about all this AI stuff is, like, how much respect I have now for developers that used to ship anything before all this stuff

Speaker 0: came on the scene because you just... It just makes you realize how freaking complex this stuff is.

Speaker 0: Still doing okay

Speaker 0: on tokens.

Speaker 0: So any other questions? So what are you guys thinking in terms of setups? I'd love to know

Speaker 0: what

Speaker 0: you guys thinking like, hey. I'm gonna use VPS. I'm gonna risk it all and and OAuth in through anti gravity and use my Opus tokens that way,

Speaker 0: or I'm gonna use Gemini's free API. Like, what kind of setups are you guys thinking? Or I'm gonna run an old old computer.

Speaker 0: Okay. We can see people's risk tolerance here. Right? So Abraham's a...

Speaker 0: He's a real risk taker. He's willing to

Speaker 0: suggest

Speaker 0: raw dog himself with Claw on.

Speaker 0: Whatever happens happens.

Speaker 0: VPS and anti gravity with burner Gmail.

Speaker 0: VPS on old laptop plus Claw. I want to do the cheapest and easiest setup to play with. And once I know, I'm gonna risk it all on black.

Speaker 0: Okay?

Speaker 0: What the hell is going on here? We're still not set up.

Speaker 0: Off code. Single use and already expired. So we need to do it again.

Speaker 0: The total cost for my setup... So current... Well, so my situation is a little

Speaker 0: special in one sense that I have the Ultra plan for Google's AI plans, which is $250

Speaker 0: a month, and that's because it gives me unlimited videos. So I make a lot of videos.

Speaker 0: And so I already had that kinda sitting around. I think if I didn't have that,

Speaker 0: what's the cheapest

Speaker 0: Google Google

Speaker 0: AI plans? I I think I might get one of them

Speaker 0: or just Claw. I

Speaker 0: don't know what this is. $5

Speaker 0: in US,

Speaker 0: something like that. This one's maybe 15,

Speaker 0: and this one's way more.

Speaker 0: It's all in Polish.

Speaker 0: But, yeah, Claw, $20 plan or €20. Yeah. $20, I think it is.

Speaker 0: That's a that's a a must have for sure.

Speaker 0: And and, yeah, €7 for the VPS.

Speaker 0: So

Speaker 0: those are my costs.

Speaker 0: Yeah. Because we haven't talked about how to set it up for a Mac mini specifically,

Speaker 0: but

Speaker 0: you're one prompt away from from figuring

Speaker 0: that out if we don't get to

Speaker 0: to that.

Speaker 0: But we're still not quite logged in here, so let's keep going.

Speaker 0: K. We gotta do this again.

Speaker 0: Hey, Joshua. We are working on setting up Open Claw, which is a very powerful AI agent that can live in Telegram, WhatsApp, whatever you prefer.

Speaker 0: OAuth succeeded, guys.

Speaker 0: That's good.

Speaker 0: And,

Speaker 0: yeah, these AI agents, I have found to be tremendously

Speaker 0: helpful.

Speaker 0: Let me check if this works yet.

Speaker 0: I

Speaker 0: he's alive, ladies and gentlemen.

Speaker 0: NHB Alfred.

Speaker 0: Let's go into grandpa mode here and make this font a little bit bigger.

Speaker 0: So he's asking me now. Right? Kinda like, what's my name

Speaker 0: or personality?

Speaker 0: How do you wanna do this? Wanna give me a name?

Speaker 0: You tell me what would be a cool name and a kick ass personality.

Speaker 0: So the thing is now up and running, and that means from here on, you know, I can start to just, like, take over from my phone. Right? And I don't think we have audio transcription out the box, so that is something...

Speaker 0: So I think the first couple of things I would look at installing is definitely audio transcription

Speaker 0: if it's not there out of the box.

Speaker 0: And then I would probably do things like Google Sheets and whatnot. But, really, like, start to just play around. And

Speaker 0: for me, it was very natural to just start using it. Like, instead of just going and prompting something in Gemini or Claw or whatever, I'm like, I just have Telegram right here. Let me just ask right here. And I just kinda, like,

Speaker 0: very organically

Speaker 0: started using it more and more and more.

Speaker 0: Got any ideas? Alright. Kick ass usually implies competence with a bit of an age... Edge.

Speaker 0: Name, Rook, the pragmatic fixer. Does Rook work for you?

Speaker 0: Okay. Sure. Let's do it.

Speaker 0: What are some

Speaker 0: basic

Speaker 0: things we should set up? Let's see what it says.

Speaker 0: Anything you guys want me... Want us to make sure that we set up here while we're

Speaker 0: while we're using it?

Speaker 0: And I found, by the way, like, the Gemini models,

Speaker 0: at

Speaker 0: least the way that I set it up through OAuth, incredibly slow.

Speaker 0: Incredibly slow.

Speaker 0: That's that's really the main reason I started looking for,

Speaker 0: like, ways to use my OpenStockens because, yeah, this this thing was so so slow.

Speaker 0: It's just loading and loading and loading.

Speaker 0: What's the fastest? I'm not sure.

Speaker 0: We could ask it.

Speaker 0: We could even ask here maybe.

Speaker 0: Would be the fastest models to use in Open Claw?

Speaker 0: So I'm using the terminal inside of anti gravity. And to answer your question, the reason why I do it is because if I run out of tokens, I just go here to the sidebar, and I can continue using Opus tokens. It's not quite as good as through the terminal. And the other thing is, like, I have...

Speaker 0: Visually, I can see all my files here and stuff like that. I just... It's a nice

Speaker 0: nice preference

Speaker 0: of mine.

Speaker 0: Amazon Nova. I've actually used that one. So we were talking about the speed. So Amazon... That that one's super cheap, by the way. It's so cheap. It's ridiculous, but it's very limited also. It's it's only text based and, yeah, very limited, but very fast and incredibly cheap.

Speaker 4: Gemini, life is, very, very fast. It's,

Speaker 4: it's, like, cost wise, it's okay enough. But, I mean, if you're using API cost,

Speaker 4: it can add up. When I was using it,

Speaker 4: it was costing me, like, 10 to 15¢ for every message. I'm like damn, like, it's couple of dollars per day. You know? For for Gemini? Like, things like Yeah. Gemini three Flash. It's a cheap model. It's, like, good enough for chatting, but when it comes to...

Speaker 4: Yeah. That's, like, the thing with, you know, like, this faster model because, like, they're... The reason they are faster because, like, they are smaller

Speaker 4: in terms of their size. Like,

Speaker 4: for example, Office 4.6 is, like, a ginormous model, like, same, like, GPV five or

Speaker 4: Gemini. It's like burns through tokens. Right?

Speaker 4: Yeah. But

Speaker 4: cheap... Faster is not always better like, it might make mistakes. It might delete your files. Yeah. I know. So it's risky to use fast. Yeah. The... That's the other thing, guys. It's like, you'll find that different models are good for different things. So as one example, like, I primarily use Opus

Speaker 0: Anthropic, right, Claw in in

Speaker 0: my AI bot, Alfred.

Speaker 0: But, for example,

Speaker 0: if I want to get the

Speaker 0: summary of a YouTube video,

Speaker 0: it just doesn't do a good job with that because it it struggles to, like, find the transcript. And, of course, if you use a Gemini model, well, now you're in the Google ecosystem. So I've set up a command where if I put in...

Speaker 0: In my main one, if I put in slash m one, it's gonna use my default model. And if I put m two, it's gonna use the Gemini model. And if I'm ever doing something in, like, Google Drive or I want, like, a transcript from YouTube or something like that,

Speaker 0: Or if you wanted to do, like, Gmail stuff, like, it would probably switch model to Google's model because it's just gonna inherently gonna work better within their ecosystem. Right? So you're gonna find that... Yeah.

Speaker 0: From that perspective, different models are good for different things. And to Anne's point, likes, the newer the newer models are so capable and so big and so...

Speaker 0: Like, because of that, they're also, like, using a lot of tokens. So if you're using... If you're doing more, like, basic stuff, you could kinda, like, downscale your your model.

Speaker 0: What's up, Hans? Feel free to jump in whenever.

Speaker 4: Yeah. Yeah. For sure. One thing I feel like could be

Speaker 4: very

Speaker 4: interesting to try is...

Speaker 4: So Claw or Anthropic,

Speaker 4: whatever, they don't like it when we use OpenClaw.

Speaker 4: Or what if

Speaker 4: we could install a Claw code on our VPS

Speaker 4: and then have our Open Claw run

Speaker 4: Claw code

Speaker 4: so that, Anthropic doesn't know, you know, who is sending the request because, like, they only see how it's being used. So if we just use

Speaker 4: Claw code on our

Speaker 4: Hetzner or Hostinger or whatever to UPS,

Speaker 4: then, like, we need to still use a a different model, let's say, on the front, but it's going to do all the calculations or it's gonna send a request

Speaker 4: using Claw code. And then I think you can... You call it headless. Like, you don't need to see it's running, but you can, like, you know, have it checked, you know, what's that doing. So that could be

Speaker 4: something...

Speaker 4: It's like a workaround, which is still in the terms of service. You will get higher rate limits, and you can still use your,

Speaker 4: Anthropolog subscription.

Speaker 4: Or even they could use your

Speaker 4: Gemini CLI because, like, that's still a legal way to do it. So it's like, you have us... You teach your Open Claw head. That's greater scale. So you use something called bash command to

Speaker 4: launch a Gemini CLI.

Speaker 4: Right? Every time I... In cloud code? You're saying in cloud code? Like, access your

Speaker 0: Google subsidized...

Speaker 4: No? Yeah. Yeah. So let's... You have right now a Google AI Ultra. Right? Which means Yeah. You also have access to Gemini CLI, but I think there you won't have Claw OPUS, but you will have access to

Speaker 4: Gemini three Pro or three Flash. Right? Or if you have Claw subscription,

Speaker 4: that means you have access to OPUS 4.6, but the subscription. What I'm saying is that

Speaker 4: I'm gonna try it out later this week. It's like you install a Claw code instance

Speaker 4: or Claw on your VPS,

Speaker 4: and you have your Open Claw

Speaker 4: run that Claw instance. Not use

Speaker 4: itself, but, like, it's only going to... You know, for example, when you go to your terminal, you launch Claw. Right? Like, Claw... So it's gonna do the same thing just without seeing... And you're saying with your Claw plan. Right? Like, with your consumer plan. Yeah. Yeah. Yeah. So then it...

Speaker 4: I don't know if

Speaker 4: Anthropic sees it. Hey. It's coming from this IP, which is from Hetzner or

Speaker 4: Australia. So that could be a problem. But, otherwise, if you're using Claw code, it's

Speaker 4: within the terms of service. Right? So you're using your Claw code

Speaker 4: inside Hetzner, which is Yeah. Polyop.

Speaker 4: Yeah. So it's like, word error there. It's, like, theoretically a similar thing to what I'm doing with, like, routing my... Using my Opus tokens through antigravity.

Speaker 0: But you're talking about, like, a similar thing, using Cloud Code

Speaker 0: on your VPS

Speaker 0: through your Cloud Code subscription. So then... Because, like, then you're using their tools

Speaker 4: that they make them available. Yes. And it's within terms of service because, like, it's not... You are not launching them. Your Open Claw is launching Yes. Claw code instances. And then,

Speaker 4: for example,

Speaker 4: every

Speaker 4: Claw code instance that you use in your terminal, it it saves a session history. So you can even see what's happening. Right? So, it can keep track on what's happening, and then that would be interesting. I think if,

Speaker 4: something like that. It's probably someone has built already, but I'm sure. That would... I'm sure. Yeah. Yeah. So that would be, I guess, a good workaround. So you have, like, a cheap GBD 5 or even you can pay API cost, but, you know, you just,

Speaker 4: tell it to use the scale. That's gonna do a couple of prompts and then launch Claw

Speaker 4: code instance for this task. That would be very nice.

Speaker 0: Yeah. Yeah. Definitely let us know if you try it out, how that goes. For sure. For sure.

Speaker 0: Cool. Joshua got got his hand up as well. Let's

Speaker 0: check-in with him. What's up?

Speaker 0: Hey, man.

Speaker 6: So I have ClawedCode.

Speaker 6: And I was curious from security perspective, like, I'll probably... And ease, I'll probably work with that for a while before I set up

Speaker 6: Open Claw, and that would have to be on its own machine or a VM. But for Claw code,

Speaker 6: do you have any recommendations

Speaker 6: on, like, security is prompted,

Speaker 6: injection, or risk at all with that?

Speaker 6: Do you need a virtual machine, or can you just, like... You... Is it okay to just run it on your machine?

Speaker 0: Yeah. So we talked a little bit about this earlier, but you don't wanna run it on your main machine just for the reason that it's not gonna be on twenty four seven probably.

Speaker 0: Say again? Yeah. But you're you're you're Open Claw, I mean. Like, you don't wanna host it on your on your main Oh, yeah. Computer. Yeah.

Speaker 0: So

Speaker 4: Cloud. Sorry. Cloud.

Speaker 0: Yeah. But... So so what's the question? It's about the security side of of using

Speaker 0: using Open Claw, right, through

Speaker 0: through your own machine. Claw code.

Speaker 0: Yeah. But what do you mean using Claw code for what?

Speaker 6: Well, I mean, I'm I'm... I just started using it to spin up agents

Speaker 6: to do various marketing tasks. So Yep. You know, the c... CRO sub agent, a, you know, marketing

Speaker 6: research assistant agent, etcetera.

Speaker 0: Okay.

Speaker 6: But it sounds like there's,

Speaker 6: like, there's not really a a

Speaker 6: need to, like, spin up a VM or anything for that.

Speaker 0: No. Probably not. I mean, it's it's kinda hard to give a blanket answer, I think, because it depends on what those, you know, are you, like, you know, down... Downloading some, you know, dodgy, you know, get get... GitHub packets to, like, run those agents, or are they, you know, things that you kinda, like, know know what's going on under the hood or or or whatnot? So, like, one thing we talked about with Open Claw was, like,

Speaker 0: there... There's been, you know,

Speaker 0: instances of people

Speaker 0: getting malware and stuff, and, you know, that's gonna be through, like, these third party

Speaker 0: plug ins and stuff like that that are outside of the main thing. So it's, yeah, it's a little hard to say, like, a blanket answer, but most likely not, but it probably depends what's happening under the hood.

Speaker 6: Yeah. Kind kind of fun. I actually have Claw code check.

Speaker 6: Like, it's gotta be an open source, and then I I tell it to to check all the code before I before

Speaker 6: I install it for any any suspicious

Speaker 0: Yeah. That's great. Yeah.

Speaker 0: That's great.

Speaker 0: Yeah. That's great.

Speaker 0: Cool. So... Yeah. I mean,

Speaker 0: I guess... Yeah. Just do that, right, or

Speaker 0: audit audit everything that that you guys are installing and whatnot. So... And then and then contain things as much as possible.

Speaker 0: Cool. So I just asked the bot that we set up.

Speaker 0: Do you have... Can you transcribe audio? No. I can fix that. I have two ways to handle audio for you. Can install OpenAI Whisper

Speaker 0: on the machine, which I've used quite a bit, or the the the

Speaker 0: fast and paid way. By the way, so I'm doing this with my other bot using...

Speaker 0: So OpenAI

Speaker 0: Whisper, you can see right here. That's the that's the thing that allows you to transcribe audio, and that's obviously through OpenAI.

Speaker 0: Google also have their own program that can do this. And I'm using that through API because it's freaking...

Speaker 0: It's so inexpensive.

Speaker 0: Like,

Speaker 0: what's the pricing like for using Google's

Speaker 0: transcription

Speaker 0: through API?

Speaker 0: It was something like nine thousand minutes

Speaker 0: for a dollar or something like that. So it's like, man, that's quite a bit.

Speaker 0: Pay that. That's reasonable API cost.

Speaker 0: Okay. Cool. So we have ten more minutes. Any

Speaker 0: last minute questions are welcome? Any things you would like us to do as far as, like, yeah, just see if this thing can could pull it off? We could do that.

Speaker 0: Any... Yeah. Any ideas that have come up?

Speaker 0: Has anybody installed it during the call?

Speaker 0: Let me know.

Speaker 0: Yeah. So

Speaker 0: super slow using Google through OAuth

Speaker 0: in

Speaker 0: Open Claw.

Speaker 0: Let me see.

Speaker 0: Point $2.04

Speaker 0: per minute.

Speaker 0: Well, that's not that's not at all what I had on the other one.

Speaker 0: That's a good dollar per hour. It's definitely different than, like, nine thousand minutes or whatever.

Speaker 0: Okay. Well, we could use OpenAI's

Speaker 0: version then, but then we're gonna have to find... We're gonna have to get an API key. So I wouldn't do that, but I would install this. Right? I would just prompt it. Right? Like, okay. Install it. It's gonna ask me to go to Open AI and find my API keys that I can charge me for it.

Speaker 0: And, hopefully, because we covered some of the basics, right, you guys can kinda see the difference of using

Speaker 0: API

Speaker 0: through OpenAI versus locally. Right? So locally, well, now we're installing this, you know, speech to text model on our computer,

Speaker 0: and

Speaker 0: it could be on the VPS, could be on, you know, the MacMiner or whatever. Now we're running that locally. Right? So we're gonna be using a lot of compute. It's likely gonna be a lot slower.

Speaker 0: It's probably gonna be cheap

Speaker 0: or free in this context,

Speaker 0: and we could choose another option using API. So that's where we're outsourcing this to Open AI, and we're paying them for for for the usage.

Speaker 4: One interesting

Speaker 4: use case that I think I... I'm doing, like, CRO work for for a client.

Speaker 4: And then I was using it with Claw code essentially. Because, like, what I don't like is, to go into ad manager and then, you know... Because every

Speaker 4: ad account is set up differently. You know, they have a different metrics,

Speaker 4: how they set it. I'm like, okay. Would it be nice, like, know, if I'm able to just talk to the ads manager of a particular account directly

Speaker 4: Yeah. Then have Claw fetch

Speaker 4: the right ads data. Right? So this is more for Claw Co. I mean, you you can easily set up with the Open Claw as well. So how it works is that it's called marketing API. It's sort... Kind of technical, but it's, like, five steps. And now I have set it up. So you just create an app. It's, three steps. You just, generate an, access token. You give it to Claw and...... Facebook.

Speaker 4: Yeah. It's like...

Speaker 4: It's connected to your

Speaker 4: Meta Ads account. Right. And then you can essentially,

Speaker 4: using Claw or Claw code, talk to the ads manager. You know? Okay. Yeah. List,

Speaker 4: what's the trend of the ad account,

Speaker 4: from last seven days. Right. We made a change yesterday.

Speaker 4: How are... How's the data looking today? It can pull up the data, and you can even ask it to pull the exact copy. You can see, okay, which hook,

Speaker 4: then what exactly? You know? Yep. So what is the ad cost exactly, and what should my next steps be? So instead of... So previously, I had to take screenshots of the ads manager. Right. And like I said, so much work. So, you know Yeah.

Speaker 4: It should be possible. So, an automation

Speaker 4: for people who do media line could be... You know, you can set it up with your ads manager using access token. Don't give it, writing access. That would be bad. It's nothing I have on your behalf. But,

Speaker 4: you know, like... Eventually.

Speaker 0: Yeah. It... No. I agree. I mean, if I was running ads right now, I would a 100%... I mean, you'd wanna basically get, like, end of the day report or something like that with all your data and, like, hey. Kill these.

Speaker 0: These hooks are working.

Speaker 0: Scale this ad up. Right? There's there's...

Speaker 0: I don't know. If you trained it well enough, there's just no chance that a human is gonna make better decisions than than a computer is gonna make with with with data. Right?

Speaker 0: So it's not gonna have any emotion built into it. But...

### 2:00

Speaker 0: Yeah. I would absolutely do that. And, I mean,

Speaker 0: eventually...

Speaker 0: Like, right now, it is technically possible for us to programmatically

Speaker 0: make new ads,

Speaker 0: publish new ads,

Speaker 0: look at the data, make the decisions

Speaker 0: Yeah. Maybe come up with new ideas based on the results of those ad. Like, the whole thing could be automated. It's difficult. And like we said, maintenance would be a bitch and all this stuff, but the fact that that's possible now is, like, pretty

Speaker 0: pretty insane.

Speaker 4: Yeah. And

Speaker 4: this... I think last week, we built up this

Speaker 4: spy tool. Right? So you kind of look at your competitors' swipes. So

Speaker 4: think it would be, you know, like, here are my top competitors. You know, you can schedule a weekly

Speaker 4: or buy it, like, you know, twice a week job. It's gonna swipe their ads, their aesthetics,

Speaker 4: and then their videos, like, it transcribes them. And then it uses,

Speaker 4: Nano Banana Pro API,

Speaker 4: and it's kind of,

Speaker 4: uses their style of,

Speaker 4: static ads, but tailored to your offer. And it's like, hey. Here are, like, 10 static ads that the client has been... Or different people in your industry have been running. So I created, like, what do you think. Right? So it kind of swipes, spies on your competitors,

Speaker 4: takes their copy, and then

Speaker 4: already makes the static ad for you, or writes a copy for you, and then, like, hey. Here it is. It's working for them. So, potentially, it could work for you. That is, like, very, very proactive.

Speaker 0: Yeah. Exactly.

Speaker 0: It's just insane what we can do.

Speaker 0: I've just asked it now to find me some ads. Let's see how it does.

Speaker 0: Well, Google is not gonna do very well, I think.

Speaker 0: But I was doing this yesterday, and it worked really well. Like, once I figured out which Yeah. Which lead I wanna contact, I'm like, I wanna see some of their ads to see what kind of ads they're already making and colors they're using and stuff like that. Just put this in, and it gave me a list of 10 ads. I just clicked the link and boom and open up Facebook and show me their ad.

Speaker 0: So stuff like that was... And and, yeah, also, you reminded me

Speaker 0: last week when we worked on that ad spying tool, the the the the call was, like, cut out at the end, but I don't know if you guys saw, like... Well, I posted about it after, but the thing actually worked. So we actually one shot at that thing. It actually worked on the first try.

Speaker 0: And,

Speaker 0: yeah, if you go back and look at the end of that call, you can see how it came out. It was... It's pretty awesome.

Speaker 0: Cool.

Speaker 0: Would it be able to scrape ad library without API file? Yeah. You can get direct API access. I don't know how that works, but I think you can.

Speaker 0: I can't pull those links right now. I'm missing Brave API key. Okay. So Brave

Speaker 0: is a browser. Right? So if you give it an API key, it can actually browse the Internet. So this is another very crucial thing that you would have to set up. And, of course, like always,

Speaker 0: you would just go, how do I find my Brave API key? You know? You just ask it anything that you don't know.

Speaker 0: But this works. Like, this kind of prompt, I've done it, and it's, yeah, pretty damn useful.

Speaker 0: Cool, guys.

Speaker 0: I hope you learned something. I hope everybody's either already got one up and running or at the very least, you kinda know how you wanna configure things.

Speaker 0: I promise you guys, like,

Speaker 0: this thing is ridiculously useful for all of you,

Speaker 0: and you should really try to figure it out. I'm available if you need help. Like, ping me on Discord as always,

Speaker 0: but I can't tell you how big of a damn

Speaker 0: game changer this has been for me. Like, I just...

Speaker 0: And the the other thing too is, like, it's not that it can do stuff

Speaker 0: that you can't already do in, Claw code or what have you. There's something magical about just, like, everything coming together and, like, having it on your phone and being able to voice message, and you have to experience that before you go, oh, shit. This is, like, actually pretty badass.

Speaker 0: So definitely can't

Speaker 0: shill it enough.

Speaker 0: That's it, gang. Thank you very much for coming.

Speaker 0: Unless anybody has any other things, we'll wrap it up.

Speaker 3: Amazing call. Thank you. Looking forward to hearing

Speaker 0: your guys'

Speaker 0: use cases and just watching your minds get blown the way mine has over the last seven days.

Speaker 0: Sweet.

Speaker 0: Then have a great one, everybody. I'll see you guys in Discord and catch you on the next call.

Speaker 4: Sounds good.

Speaker 0: Ciao.

*Speaker labels below are algorithmically derived clusters, not identified people: one label on a long call usually means diarisation failed, not that one person spoke. Speakers observed: 7.*
