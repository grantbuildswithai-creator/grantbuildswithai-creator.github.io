I wanted a research assistant that digs through the web for ten minutes and hands me a report with citations. Google already has one. It's called Deep Search, and it's free to copy from their Agent Garden. In one day I had it running in my own Google Cloud account, plus a small tool on my laptop that sends it questions and saves its reports as Word documents. This is the path I took, in order. You won't find code here. Your AI helper will write it with you.

## What you'll build

- Your own copy of Google's **Deep Search** research agent, running in Google Cloud
- It proposes a research plan and **waits for your approval** before it starts
- It searches Google over and over, grades its own findings and fills the gaps
- It writes a long report with citations
- A small tool on your computer that sends it questions and saves each report as a **Word document**

## What you need

- A Windows or Mac computer
- A Google account, and a credit card for Google Cloud. New accounts get free-trial credit. I used mine.
- An afternoon to deploy it, and another to build the tool
- An AI coding helper for part two. I used Claude Code.
- No coding experience

## Accounts and setup you'll do yourself

Same lesson as my Discord bot: AI can write and fix the software, but the accounts, billing, logins and security settings need a real person. Your AI helper can tell you where to click. You do the clicking.

Tick things off as you go. Your checkmarks are saved in this browser.

### Google Cloud

- [ ] Sign up for Google Cloud and start the free trial. It asks for a card.
- [ ] Create a **project** for this. Everything you build lives inside it.
- [ ] Set a **budget alert** under Billing, so you get an email before costs surprise you
- [ ] Turn on the APIs the setup asks for when it asks. You'll click "Enable" a few times.

### Your computer (for part two)

- [ ] Install the **Google Cloud CLI** (Google's command-line tools)
- [ ] Log in with it in your browser. This lets tools on your computer act as you in your project.
- [ ] Windows: if PowerShell refuses to run the Google tools, ask your AI helper. The fix is small.
- [ ] Install your AI coding helper and log in to it

### Keeping it safe

- [ ] Leave your agent **private**. Only your account should be able to call it.
- [ ] Don't share your project ID, login files or keys in chats, screenshots or uploads

## Part one: get the agent running in the cloud

### 1. Pick the agent

In the Google Cloud console, open **Agent Garden** and find **Deep Search**. It's built on Google's Agent Development Kit (ADK). Read its description, so you know what it's supposed to do before you deploy it.

### 2. Deploy it from Cloud Shell

**Cloud Shell** is a terminal that runs in your browser, already logged in to your account. Agent Garden gives you setup commands to paste into it, and they deploy the agent to **Agent Runtime**, Google's service for hosting agents.

### 3. Expect it to break (mine broke twice)

- Google's one-click setup command failed for me, and I had to adjust it. Paste the exact error into your AI helper and ask what to change.
- Then the agent crashed on startup, because nobody told it which AI model to use. That setting has to be passed in when you deploy.

Every error message is a clue. Copy the whole thing, not a summary.

### 4. Test it in the Playground

Once it's deployed, the console has a test chat window called the **Playground**. Ask it a real question you care about. My first was about reselling Formula 1 tickets, and I got back a surprisingly thorough, cited report. The catch is that you have to copy and paste everything out of the chat box, which gets old fast.

## Part two: talk to it from your own computer

### 5. Check the settings for idle costs, first

This step saved me the most money. Before building anything, ask your AI helper to read your agent's settings and look for anything that runs all the time. Mine was set to keep one copy **running 24/7**. That makes sense for a business that needs instant answers, but it meant I paid even when nobody used it. By Claude's rough estimate, that would have burned through my $300 trial credit in about three months. One setting change, and now it only runs when asked.

> Cloud defaults are built for businesses. Read them before you leave anything running.

### 6. Understand how the agent talks

Your agent isn't a program on your computer. It's a **service** in the cloud, and anything with permission can talk to it: the Playground, a script or another agent. Deep Search publishes an **agent card**, a description of itself, and speaks **A2A**, a standard protocol for agents talking to agents. That's how your own tool can reach it.

### 7. Build your tool with your AI helper

Here's a prompt to start with:

> I have Google's Deep Search agent deployed to Agent Runtime in my Google Cloud project, and I'm logged in with the Google Cloud CLI. I'm a beginner. Please help me build a small command-line tool that sends it a research question over A2A, shows me its research plan so I can approve or change it, and saves the final report as a Word document with clickable citations, plus a log of every step. Explain each piece as you go.

Mine came out to about 150 lines, and Claude wrote all of them. I didn't write the code, but I understand what each piece does and why.

### 8. Steer the plan like an expert

When the plan comes back, read it before you say go. This is where your knowledge counts. My test was a clinical question: how tirzepatide and retatrutide compare on muscle loss during weight loss. I added two things only a clinician would think to ask for: muscle *function*, not just lean mass on a DEXA scan, and a comparison with bariatric surgery. The agent rewrote its plan, and about ten minutes later I had a 10-page report with a comparison table and citations.

Your most valuable contribution isn't code. It's knowing what to ask for.

## See a real report

Here's the report from step 8, exactly as the agent wrote it: [Tirzepatide vs. retatrutide: muscle loss during weight loss (Word document)](../../static/reports/tirzepatide-vs-retatrutide-muscle-loss.docx)

Read it as an example of what the agent produces, **not as medical advice**. It has real problems:

- It mixes PubMed studies with Reddit posts and websites that sell peptides
- It compares trials in different patient groups without saying so
- Its citation links go through Google redirect links, which may stop working after a while

AI research is a first draft, not a final answer. Check the sources before you trust a claim.

## What I learned

- **Most of an agent's "intelligence" is written instructions.** The planning, the self-grading and the report style all come from prompts in the agent's code, not from the AI model itself.
- **You steer an agent in plain English.** The plan-approval step is where you add the most value.
- **Check the output.** Look at what kind of sources it cites, not just how many.
- **Read the cloud settings.** One setting was the difference between pennies and burning through my trial credit.
- **Who did what:** I chose the agent, deployed it, made the decisions and brought the medical judgment. Claude wrote the code, diagnosed the errors, found the cost problem and critiqued the sources.

## Mistakes to skip

- Trusting the one-click setup command to just work
- Deploying without telling the agent which model to use
- Leaving the default "always running" setting on for a hobby project
- Taking a well-formatted report at face value because it has lots of citations

## Before you walk away

- [ ] Your agent only runs when called, not 24/7
- [ ] Your budget alert is set
- [ ] Your agent is private to your account
- [ ] When you're done experimenting, delete the agent in the console so it can't cost you anything
