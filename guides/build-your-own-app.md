I started this project to show my kids that if Dad can build a real app, they can too. I'm not a developer, and when I started I didn't even know what the app would do. About a week later it was on the Google Play Store for testing, my kids have it on their phones, and the same app runs as the website you're reading. Claude wrote the code. I made the decisions. This is the path I took, in order, so you can build your own.

Download the Word version to keep or print: [Build Your Own App with AI (Word document)](../../static/reports/build-your-own-app-guide.docx)

## What you'll make

- A real **Android app** your friends can install from the **Google Play Store**
- The **same app as a website**, so iPhone friends can use it too
- A **"workshop" design** where every new idea plugs in as its own little build, so the app grows with you
- At least one build that uses **real AI** (mine is a pocket-sized Dungeon Master), running on your own small server with a spending cap
- **Updates that reach phones without a new download** for most changes
- Optional: your own **web address** and an email address on it

Mine is called GBc̄Ai. It has an AI adventure game, a soundboard with a giant airhorn button, a quote-guessing game, a Bitcoin tip jar on the website, and links to the podcast. Yours can be anything.

## What you need

- A **Windows or Mac computer**. I used Windows.
- An **Android phone** for testing. iPhone apps need a $99/year Apple account, so I skipped that and gave iPhone friends the website instead.
- An **AI assistant that can work on files on your computer**. I used **Claude in the desktop app's Code tab** (Claude Code). It writes the code, runs the commands and checks its own work.
- About a week of evenings, plus waiting time for Google
- A budget of about **$25 one-time**, plus about **$10 a year** if you want your own web address, plus a few dollars of AI use

## Accounts and setup you'll do yourself

Same lesson as every project on this show: AI can write the code and run the tools, but accounts, logins, payments, identity checks and anything with a password need a real person. Your AI helper can tell you exactly where to click. You do the clicking.

Tick things off as you go. Your checkmarks are saved in this browser.

### Your computer

- [ ] Install **Node.js** (the free "LTS" version from nodejs.org). The app tools run on it.
- [ ] Make a project folder **outside OneDrive or Dropbox**, for example `C:\Users\you\dev`. Apps come with tens of thousands of small files, and cloud syncing chokes on them.

### Expo (builds your app)

- [ ] Make a free account at **expo.dev**. Expo's servers turn your code into an installable Android app, so you don't need Android Studio.

### GitHub (backup)

- [ ] Make a free account at **github.com** so your code is backed up in a **private** repository
- [ ] If you already have a personal GitHub account, decide which one owns this project before you start. I found out halfway through that I had two.

### Google Play (to publish)

- [ ] Sign up at **play.google.com/console**, choose a **personal** account, and pay the one-time **$25**
- [ ] Verify your identity with a government ID. Mine took about a day.
- [ ] Start collecting **12 or more friends with Android phones** and the Gmail address their Play Store uses. Google requires a 14-day test with at least 12 testers before your first app can go public.

### Your own web address (optional)

- [ ] Buy a domain at **Cloudflare** (about $10 a year at cost). Turn on auto-renew.
- [ ] Optional: turn on Cloudflare's free **Email Routing** to forward an address like `you@yourdomain.com` to your Gmail

### The AI server (for AI builds)

- [ ] Make an account at **platform.claude.com**, add a few dollars of credit, and set a **monthly spending limit**
- [ ] Create an **API key** and keep it to yourself. It's a password that spends your money.
- [ ] Use the same **Cloudflare** account to run the small server that holds that key. The free plan is plenty.

## The golden rule: you're the decider

The AI does the typing. Your job is the part it can't do:

- **Say what you want** in plain words, and say what you *don't* want ("minimal, not cluttered").
- **Make the calls.** It will offer options. Pick one, or ask for its recommendation.
- **Test everything on a real phone.** "It works in the preview" isn't the same as "it works in my hand."
- **Say no.** I built two tools and then deleted them because I wasn't excited about them. That's allowed.

## Part one: get an app on your phone

### 1. Tell it the goal, not the plan

You don't need a technical plan. Here's roughly how I started:

> I want to build an app my friends can download from the Google Play Store. I don't know exactly what it does yet. It should be a collection of small tools and games, some useful and some fun, and it should connect to my podcast's website. I'm not a developer. Recommend the simplest way to build it, explain your choices in plain language, and tell me which steps I need to do myself.

Mine recommended **Expo**, a toolkit where one set of code becomes an Android app, a website and (later, if you want) an iPhone app.

### 2. See it on your phone on day one

Ask it to create the project and start it up. Install the free **Expo Go** app from the Play Store, scan the QR code it shows, and your app opens on your phone. It's rough at first, but it's yours, and that's very motivating.

## Part two: give it a shape

### 3. A name and a look

Decide how it should feel. I wanted the dark, neon "TRON" look of my podcast logo, kept minimal. I named mine after my logo and had Claude turn the logo into the app icon. Give it your style in words:

> Make the design minimal and dark with neon accents, like TRON. Not cluttered. Use one accent color per section.

### 4. Build a "workshop", not a pile of features

This was the most important decision. Instead of hard-wiring each feature, I asked for a shell where every idea is a separate "build" that plugs in:

> Restructure the app so each tool or game is its own self-contained build in its own folder. Adding a new one should mean adding a folder and one line in a list. Group them into sections on a simple list screen. Each build gets a small "Built with AI" card that says what the AI did, what I did, how long it took, and exactly what (if anything) leaves the user's phone.

That card turned out to be my favorite part. It makes the app a portfolio, and it keeps privacy front and center.

### 5. Your first build: something with no server

Start with something that runs entirely on the phone. My first was **AI or Not?**: famous quotes mixed with AI-written fakes. Another easy crowd-pleaser is a **soundboard**: one giant red airhorn button, plus a rimshot, sad trombone and crickets. Ask the AI to **generate sounds from scratch with code** rather than using clips from the internet, which are often copyrighted.

### 6. A front door

My home screen is a short introduction ("Hi, I'm Grant…") with one button into the workshop. Keep it simple. You can always add more later.

## Part three: put it on the web

### 7. The same app as a website

Expo can export the same app as a website. Ask for it, and ask it to make **"Add to Home Screen"** look right on iPhones, so iPhone friends get an icon and a full-screen app feel.

### 8. Your own address (optional)

I bought my domain at Cloudflare and pointed it at my existing GitHub Pages site. If DNS is new to you, ask the AI to walk you through it **one record at a time**. I did, and it was much less confusing. Then I made the workshop the front page of my site and moved the podcast inside it.

## Part four: add real AI

### 9. Keep the key off the phone

Never put an API key inside an app. Anyone can unpack an app and find it. Instead, a tiny server holds the key, and the app talks to the server:

> Set up a small Cloudflare Worker that holds my Claude API key as a secret and does the AI calls for the app. Add daily limits per person and an overall daily cap so my bill can't run away. Use the cheapest Claude model. The server shouldn't store what people type.

You'll sign in to Cloudflare in your browser, and paste the key into a secure prompt yourself. The AI never needs to see it.

### 10. An AI build people want to use

Mine is **Pocket Dungeon Master**: a 20-turn fantasy adventure where you tap one of three actions or type your own. Two tips from testing:

- AI tends to start every story the same way. My first two adventures both began in a tavern with a cursed amulet. Ask it to **mix random ingredients into each opening** (a place, a twist) so every run feels different.
- **Add a "Report" option.** Google Play requires apps with AI-generated content to let users flag offensive content without leaving the app. I almost missed this one.

## Part five: get it on your phone, then your friends' phones

### 11. A test version on your phone

Ask the AI to make an Android **test build** with Expo. You download it and install it directly ("sideloading"). Android will warn you about unknown apps. That's normal for your own test file. Turn the setting back off afterwards.

### 12. Updates without a new download

Expo can push most changes straight to installed apps, without a new download or a store review. Ask the AI to set it up early. One rule: **when you add a new phone feature** (sound, camera, vibration), the app needs a new version number and a new build. Updates sent over the air can't add phone features.

### 13. The store listing

Ask your AI helper to put together a **store kit**: the description, screenshots taken from the real app, a 512×512 icon, a 1024×500 banner, a plain-English privacy page, and written answers for Google's **Data safety** and **content rating** forms. Then you fill in the Play Console yourself, using the kit. The "package name" you enter is permanent, so use your web address backwards (mine is `com.grantbuildswithai.gbcai`).

### 14. Closed testing with friends

Create a **closed test** (not "internal testing", which doesn't count toward Google's requirement), upload the store build, add your testers' Gmail addresses, and send it for review. After Google approves, share the opt-in link. Ask testers to open the app a few times over two weeks. After 14 days with 12 or more testers, you can apply to release it to everyone.

## What it costs (my real numbers)

- **Google Play:** $25, one time
- **Domain:** about $10 a year (optional)
- **Expo, GitHub, Cloudflare:** free plans were plenty
- **AI in the app:** with Claude Haiku, the cheapest model, about **5 to 10 cents per full 20-turn adventure**. With a daily cap, the worst case is a few dollars a day, and real use is pennies.
- **My time:** about a week of evenings, most of it testing and deciding, plus a few days waiting on Google

## What I learned

- You don't need to know how to code anymore. You need to know **what you want**, and to keep deciding.
- **Test on a real phone, early and often.** Some problems only show up there.
- **Cutting things is part of building.** My app got better when I deleted two features.
- **Rules are part of the job.** Payments, privacy and AI content all have app store rules. Ask your AI to check the current rules before you build something sensitive.
- The free plans are slow sometimes. My builds occasionally waited in a queue for an hour. Be patient.

## Mistakes to skip

- Keeping the project inside **OneDrive**, which tries to sync tens of thousands of files
- Uploading **old screenshots** after removing features from the app
- Forgetting the **report button** for AI content
- Trying to send a new phone feature as an **over-the-air update**. It needs a new version and a new build.
- On Windows, `npx` may be blocked in PowerShell. Typing `npx.cmd` instead works without changing security settings.
- Installing from the Play Store **over a sideloaded test copy**. Uninstall the test copy first.
- Verifying your domain with the **wrong GitHub account**
- Downloading wallet software from a search result. **Type the official address yourself**, and ask your AI to check the download's signature.
- Putting your **main** Bitcoin address on a public page. Everything sent to an address is public, so use a fresh one just for tips. I also kept the tip jar on the website only, because Play Store rules on tips are unclear.
- Inviting testers who only have **iPhones**. They can't install an Android app, and Google looks for real testing.

## Security and privacy checklist

- [ ] Your API key, passwords and recovery phrases never go in your code, a screenshot or a chat. If a key leaks, delete it and make a new one.
- [ ] The AI key lives only on your server, never in the app
- [ ] There's a monthly spending limit in the Claude Console, and daily limits on your server
- [ ] Your code is backed up in a **private** repository
- [ ] Your privacy page says, in plain words, what leaves the phone
- [ ] Your app collects as little as possible: no accounts, no tracking, data kept on the phone where you can

## Before you invite testers

- [ ] You've installed your own build and tried every screen on a real phone
- [ ] The store listing uses **current** screenshots and description
- [ ] The Data safety answers match what the app actually sends
- [ ] AI builds have a report option
- [ ] You have **12 or more** Android testers, with the Gmail their Play Store uses
- [ ] You've written a short message telling testers what to try, and that they need to keep the app for 14 days
