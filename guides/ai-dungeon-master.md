I'm not a programmer. A few weeks ago I had never written a line of code. Now an AI Dungeon Master runs a D&D campaign for me, my brother, and my cousin in Discord, all day, every day. This is the path I took, in order, so you can follow it without hitting all the same walls. You won't find code here. Your AI tutor will write it with you, one step at a time.

## What you'll build

- A Discord bot that acts as the Dungeon Master for a D&D 5e game
- It narrates, plays every character you meet, and rolls real dice
- It remembers the story and keeps a character sheet for each player
- It runs 24/7 on a small cloud server, so friends can play when your laptop is off

## What you need

- A Windows or Mac computer
- About 1 to 2 hours a week. I did this over a few weeks.
- A credit card for the AI and server accounts. My real costs are near the end.
- No coding experience

## Accounts and setup you'll do yourself

This was the biggest surprise of the project. AI can write, test and fix the software for you, but it can't do the infrastructure: the accounts, the payments, the logins and the security settings. Those need a real person to sign up, pay, and say yes. You'll do these by hand, with your AI tutor telling you where to click. Budget an evening or two.

Tick things off as you go. Your checkmarks are saved in this browser.

### Discord

- [ ] A Discord account and a server you own. A private test server is perfect.
- [ ] Register an application in the Discord Developer Portal and add a bot to it
- [ ] Copy the bot's **token** and store it safely. It's a password.
- [ ] Turn on **Message Content Intent**, or the bot can't read what players type
- [ ] Invite the bot to your server

### Claude API (Anthropic)

- [ ] An account at console.anthropic.com. This is separate from a regular Claude chat subscription.
- [ ] Add a payment method and buy some credit. A few dollars is plenty to start.
- [ ] Create an **API key** and store it safely. It's a password.
- [ ] Set a monthly spending limit so there are no surprises

### A server to run it 24/7 (for step 8)

- [ ] An AWS account. It asks for a credit card and verifies your identity. Easier hosts like Railway exist if you'd rather skip AWS.
- [ ] Launch a small Ubuntu server
- [ ] Download the server's **key file** and store it safely. It's the key to your server.
- [ ] Expect some clicking around the AWS console for storage size, security settings and backups. Your AI can tell you exactly what to click, but you have to click it.

### GitHub (for step 10)

- [ ] A GitHub account and a **private** repository for your code
- [ ] Approve logins from your laptop and your server. GitHub shows a one-time code that you enter in your browser.

### Claude Code (for step 10)

- [ ] A Claude subscription or API account that includes Claude Code
- [ ] Log in to Claude Code yourself on each machine you use it on

### Keeping your keys safe

- [ ] Keep your bot token, API key and server key file in a password manager or another safe place
- [ ] Never paste them into chats, screenshots, or anything you upload

## The golden rule: use AI as a tutor, not a vending machine

The most important decision I made was to learn the basics before letting AI do everything for me. Using AI to write code you don't understand is like using a calculator before you've learned arithmetic: it works until something breaks, and then you're stuck. I did every step below with Claude as a patient tutor. Here's a prompt to start with:

> I'm a complete beginner with no coding experience. I want to build a D&D Dungeon Master bot for Discord using Python and the Claude API. I have 1-2 hours a week. Please teach me step by step, one small piece at a time. Explain what each thing does and why, and wait for me to confirm each step works before moving on.

## The roadmap

### 1. Set up your computer

Install Python and VS Code, learn what a terminal is, and run your first tiny program. It feels small, but everything else builds on it.

### 2. Talk to Claude from your own code

Using your API key, write a small program that sends Claude a question and prints the answer. Then give it memory. The AI doesn't remember anything on its own; your code keeps a list of the conversation and sends the whole thing every time. Understanding that one idea explains a lot about how these bots work and what they cost.

### 3. Connect your Discord bot

Using the bot you set up in the checklist, get your code talking to Discord. Your first milestone is small: type "hello" and get "Hello, adventurer!" back.

### 4. Give it a Dungeon Master's brain

Connect Discord to Claude and write a **system prompt**: the DM's personality and rules. This is the most fun part to experiment with. Label each message with the player's name so the DM knows who's talking, and keep a separate conversation for each channel. My first working DM was about 30 lines of code.

### 5. The big idea: dice rolls make it an agent

Claude doesn't roll dice itself. You give it a **tool**, and when it needs a roll, it *asks your code* to roll. Your code generates a real random number and hands it back, and Claude writes the result into the story. Have your code print each request so you can watch it happen.

That's the line between a chatbot and an **agent**: an agent can ask your code to do real things. Everything after this works the same way. Saving a character sheet, looking up lore and tracking where everyone is are all just more tools.

### 6. Make memory survive restarts

Save the conversation to a file after every message so the story survives a restart. Keep in mind that the whole conversation is sent every time, so long campaigns cost more. Eventually you'll cap the history and keep the important facts somewhere else (see step 9).

### 7. Character sheets

Add a tool the DM uses to save each character's stats, gear and gold to a file. Two lessons from my campaign:

- **Merge, don't replace.** My first version wiped the whole sheet every time it saved one field.
- **Save by character name, not "whoever typed last."** My DM once wrote my brother's character's name onto my sheet because I happened to be the last person who typed. Then it couldn't tell us apart and had to retcon the story.

### 8. Run it 24/7

So friends can play when your laptop is off, move the bot to the server from your checklist. Set it up as a service that starts on boot and restarts itself if it crashes.

### 9. Build your world in files, not in the AI's memory

This is the single most important design idea in the project. Conversation memory scrolls away, but **files don't**. My campaign's world lives in text files on the server: places, characters, factions, a running session log, and each character's sheet and location. The DM has tools to look things up and to record new facts, and the bot re-reads the files on every message.

- Write your lore as simple text files, one per place or character, plus an index listing what exists
- Give the DM a way to record facts it invents, so the story stays consistent
- Real-world ties make it feel alive. My campaign, "A Patient River," is set in a real valley in the early 1900s, with real towns and landmarks worked into the story.
- Fun option: have an AI write the lore and don't read it yourself, so you can play without spoilers. That's what I did.

### 10. Back it up, then level up with Claude Code

Put your code in your private GitHub repository so it's backed up and easy to update on the server. Back up your character sheets and world files too; they can't be regenerated. Then, once you understand the basics, switch to **Claude Code**. Instead of copying code out of a chat window, it works right inside your project: it reads your files, fixes bugs, tests changes and deploys them while explaining what it's doing. That's where my project took off. I went from weeks of copy and paste to more progress in twelve days than in all the time before, and it worked well because I understood the structure of what we'd built.

## What it costs (my real numbers)

- **AI:** about **8 cents per message** with Claude Sonnet 5 and a big, detailed world. That came to $14 for 159 messages over five days of active play. A simple bot with little lore costs much less.
- **Biggest savings:** prompt caching and capping the conversation history. Ask Claude Code to help with both once your world grows.
- Cheaper models exist, but the storytelling gets noticeably flatter. I chose the better story.
- **Server:** a small AWS server is cheap or covered by the free tier. Check current pricing.

## Mistakes I made so you don't have to

- Keeping API keys and the server key in the same folder as my code, one careless upload away from leaking
- A settings file in the wrong format, so the bot couldn't find its keys
- A copy-paste slip that left a setting name blank
- Saving Claude's replies without converting them first, which crashed the bot
- Letting the bot freeze while it waited for the AI, which dropped players' messages
- Saving character sheets to whoever typed last, which swapped two characters
- Not backing up the character sheets
- A DM that rolled the dice but never told us what happened. The players can't see what the DM's tools see, so tell it to always describe the result.

## Security checklist

- [ ] Your API key, Discord token and server key are passwords. Never share, screenshot or upload them.
- [ ] Keep your GitHub repo private, and make sure your keys are excluded before your first upload.
- [ ] If a key ever leaks, delete it and create a new one right away.
- [ ] Set a monthly spending limit in the Anthropic console.
