I wanted a research assistant for long-term investing: something that reads a company's official filings, checks the news, and hands me a report I can trust a little more than a web search. Google has a sample called the Financial Advisor agent, free to copy from their Agent Garden. I didn't just run it. I took it apart, learned how it worked, and rebuilt it as a team of two AIs: Google's Gemini does the legwork, and Claude does the thinking and checks Gemini's work. This is the path I took, in order. You won't find code here. Your AI helper will write it with you.

> **This is an educational research tool, not a financial advisor.** It can't see your accounts, can't trade, and it makes confident mistakes. Nothing it produces, and nothing in this guide, is investment advice.

## What you'll build

- A small **team of AI specialists** that researches one US-listed company at a time
- An **SEC analyst** that reads the company's official filings: ten years of financials, the annual and quarterly reports, earnings releases and insider trades
- A **market analyst** that uses Google Search for price, valuation, news and analyst opinion
- Claude, writing the **investment analysis and risk review**, and **fact-checking Gemini** against the original filings
- A finished **Word report** for each company, with a list of what was checked, what was wrong and what's unverified
- All of it started with one sentence, like "research Costco"

## What you need

- A Windows or Mac computer
- A Google account, and a credit card for Google Cloud. New accounts get free-trial credit. I used mine.
- A paid Claude plan with **Claude Code**, Anthropic's AI coding helper. The Claude half of the team runs on that plan.
- A few evenings. Each report takes about half an hour to run.
- No coding experience. If you've followed my [research agent guide](../google-research-agent/), some of the Google setup will feel familiar.

## Accounts and setup you'll do yourself

Same lesson as every project on this show: AI can write and fix the software, but the accounts, billing, logins and security settings need a real person. Your AI helper can tell you where to click. You do the clicking.

Tick things off as you go. Your checkmarks are saved in this browser.

### Google Cloud

- [ ] Sign up for Google Cloud and start the free trial. It asks for a card.
- [ ] Create a **project** for this. Everything Gemini does gets billed to it.
- [ ] Set a **budget alert** under Billing, so you get an email before costs surprise you
- [ ] Turn on the **Vertex AI** API when your AI helper asks. That's how your computer reaches Gemini.

### Your computer

- [ ] Install the **Google Cloud CLI** (Google's command-line tools) and log in with it in your browser. This lets the agent on your computer use Gemini in your project.
- [ ] Install **Claude Code** and log in with your Claude plan
- [ ] Make a folder for the project, and open Claude Code in it

### The SEC

- [ ] Nothing to sign up for. SEC EDGAR, the government's database of company filings, is free. It only asks automated tools to identify themselves with a contact email, so pick an email you don't mind using for that.

### Keeping it safe

- [ ] Never give the agent your brokerage login, account numbers or the ability to trade. It doesn't need them.
- [ ] Don't paste your project ID, login files or keys into chats, screenshots or uploads

## Part one: understand what you downloaded

### 1. Pick the agent

In Google's **Agent Garden**, find the **Financial Advisor** sample. Ask your AI helper to download its code into your project folder. Don't run it yet.

### 2. Read the code before you run anything

Ask your AI helper to read the code with you and tell you what's really in there. My first surprise: a summary on the web said this sample used Anthropic's Claude. The code said Gemini, only Gemini.

> Trust the code, not the description.

Here's what the template actually was:

- A **coordinator** that talks to you
- Four specialists, run in a line: a data analyst, a trading analyst, an execution analyst and a risk analyst
- Google Search as its only source of information
- Built around **short-term trading**

### 3. Ask for a read-me written for you

This was the turning point of the whole project. I told Claude plainly that I didn't understand the agent yet, and asked for a read-me. Here's a prompt to start with:

> I don't really understand this agent yet. Please write me a read-me in plain English, as a Word document: who each team member is and what it does, where each one gets its information, what a session looks like step by step, what it can't do, and a glossary. I'm not a developer.

What came back was a teaching document. The analogy that made it click for me: the coordinator is like a chief resident, handing out work to the specialists and bringing their results back together.

The big idea: **an agent isn't one thing. It's a team with job descriptions.** Each specialist is just an AI model, plus written instructions, plus the tools it's allowed to use. Once you see that, you can change any of them.

My questions after reading it were the kind I couldn't have asked an hour earlier. If it runs on my computer, does it still use Gemini? Who bills me? Ask yours too.

### 4. Run it on your computer, and expect confident mistakes

You don't have to deploy the agent to Google Cloud. It can run on your computer and still use Gemini in your project. For reading reports at your desk, that's all you need.

I ran the original version twice on Microsoft. Every number it pulled from the filings was right. But it also:

- **Invented a $100,000 account** to work out position sizes. Now it uses percentages of your portfolio.
- Flagged a "conflict" between two numbers that were measuring different things
- Rushed two steps into one
- Suggested using an IRA to get around the **wash-sale rule**. That's wrong. The rule covers all your accounts, and buying back inside an IRA can make the tax loss **permanently** lost.

Each one became a written rule in the agent's instructions. Treat it like a smart but overconfident trainee: useful for organizing the thinking, and you verify anything you'd act on.

## Part two: make it yours

### 5. Give it official data

Web search quotes good sources and bad ones with the same confidence. So I asked for a new specialist that reads the SEC filings directly.

> Please add a new specialist to this agent: an SEC analyst that pulls data from SEC EDGAR for one company. It should get up to ten years of financials, the latest earnings release, the business description, risk factors and management's discussion from the annual and quarterly reports, and insider trades. Calculate growth rates and margins in code, not with the AI. Explain each tool you build.

Claude built six data tools for it. One design choice I'd copy: **the math is done by code, not the AI**. Language models are good with words. Arithmetic belongs to a calculator.

For insider trades, ask it to separate routine events (stock awards, shares withheld for tax, pre-scheduled sales) from open-market purchases. Purchases carry more meaning.

### 6. Match it to how you actually invest

I don't trade. I'm a long-term investor. So I asked Claude to remove the short-term trading features and rewrite the specialists around holding for years. They became an **investment strategist**, a **position planner** and a **risk analyst**.

If you invest differently, this is where you say so. The instructions are plain English, so you can change what each specialist cares about.

## Part three: re-staff the team

### 7. Decide who fills each role

If an agent is a team of roles, then **who fills each role is a choice.** You don't have to use one AI for everything. Here's the line-up I ended up with:

**Gemini does the legwork:**

- **SEC analyst:** reading long filings is cheap with Gemini
- **Market analyst:** Google Search inside these agents only works with Gemini

**Claude does the thinking:**

- **Investment analysis:** business quality, the ten-year record, valuation, and the bull and bear cases
- **Risk review:** what could go wrong over five to ten years
- **Fact-check:** re-reads the original filings and checks Gemini's numbers
- **Final report:** writes it up as a Word document

**Shared:** Gemini drafts the strategy and position plan, and Claude reviews them (see step 9).

Use each model for what it's good at.

### 8. Replace the coordinator with a simple script

In this setup, you don't need the original Gemini coordinator. Ask your AI helper for a simple script that runs the Gemini specialists in order and saves each one's output. Claude reads those outputs and does its part. In effect, Claude becomes the coordinator.

> I want to split this agent's work between two AIs. Gemini should run the SEC analyst and market analyst, plus drafts of the strategy and position plan. You, Claude, should then do the investment analysis, the risk review, a fact-check of Gemini's work against the original SEC filings, and write the final report as a Word document. Please replace the Gemini coordinator with a simple script that runs the Gemini steps in order and saves each output, then explain how you'll take over from there.

### 9. Respect the line on advice

Claude drew a line here on its own. It said it would analyze companies and risks, but it wouldn't tell me what to buy, how much, or at what price, because it isn't a licensed advisor. So Gemini still drafts those parts, clearly labelled as an **educational scenario**, and Claude reviews them and flags the errors.

Claude's way of putting it: it will write the case review, but not the prescription. I think that's the right boundary, and I'd keep it in yours.

### 10. Make it one sentence to run

Once it worked, I asked Claude to turn the whole process into a **Claude Code skill**: a saved set of instructions, so that "research Costco" runs every step and saves the finished Word report into its own dated folder. Each report starts with Claude's review notes and ends with the full output of every Gemini specialist, so you can see what was checked.

## Part four: run it, read it, fix it

### 11. Every new company finds a new bug

My first real report was **Costco**. Two things broke:

- The tool couldn't find a whole section of Costco's annual report, because Costco writes its headings with a long dash and the tool expected a short one. A tiny punctuation mark, and the risk factors went missing.
- Gemini quoted an **out-of-date dividend**. So we built a seventh tool that reads dividend announcements straight from the filings, and tested it on seven companies.

My second was **Hims & Hers**, a much messier company. Gemini's summary **missed a federal lawsuit** and reported about **$1 billion of debt as zero**, because our data tool didn't recognize how that company labelled its debt. Claude found both by reading the quarterly report itself.

That's the whole point of the second AI. Not a second opinion on the summary. A second reading of the source.

### 12. Make it sturdy

Real runs also showed us three fixes worth asking for from the start:

- **Automatic retries.** Google's servers threw temporary errors five times in one run.
- **Resume without paying twice.** If a run stops halfway, it should pick up from the last finished step.
- **A fresh start for each step.** Each specialist was carrying all the raw data from the step before it. Giving each one only what it needs cut its input about fourfold.

> Directing is iterative: run it, read the output, decide what to fix, run it again.

## See real reports

Here are the two reports from Part four, exactly as the agent produced them:

- [Costco (COST): long-term investment research (Word document)](../../static/reports/costco-investment-research.docx)
- [Hims & Hers Health (HIMS): long-term investment research (Word document)](../../static/reports/hims-hers-investment-research.docx)

They were tests of the tool, based on public filings as of 30 September 2026. Read them as examples of what the agent produces, **not as investment advice**. Start with Claude's fact-check section near the top of each one. That's where you'll see what Gemini got wrong.

## What it costs

- **Gemini's part:** about **$0.22** for the Costco report and **$0.35–0.40** for Hims & Hers, on my Google Cloud bill. The long filings were most of it.
- **Claude's part:** $0 extra. It runs on the Claude plan I already pay for.
- **SEC data:** free.

Google has said this Gemini model's price doubles in January 2027. Even then, a report would cost well under a dollar.

## The billing lesson

This surprised me the most. With my earlier [research agent](../google-research-agent/), everything lived in Google Cloud. The only way to use Claude in there was through Google's model marketplace, paying per use on my Google bill. My free-trial credit wouldn't cover it, so I shelved the idea.

This time the agent runs on my laptop, and I work with Claude directly. Gemini still does its research in Google Cloud for pennies, and Claude's part runs under my existing plan.

**Where an agent runs decides who bills you for each model.** The trade-offs: it only runs when I'm at my computer working with Claude. It isn't an always-on service, and my plan has its own usage limits.

## What I learned

- **Read the code first.** Descriptions can be wrong.
- **Ask the AI to teach you, in writing.** The read-me turned me from a passenger into a director.
- **Agents are teams of roles,** and you decide who fills each one.
- **Use each model for its strengths.** Gemini for Google Search and cheap reading of long documents. Claude for judgment, fact-checking and writing.
- **Expect confident errors, and have a second AI check the originals.** Claude makes mistakes too. The rule isn't "trust Claude over Gemini". The rule is: go back to the source.
- **Who did what:** I chose the agent, decided what to change and who does each job, and read every report. Claude wrote the code, explained the system, caught the errors and wrote the analysis.

## Mistakes to skip

- Believing a summary of what an agent does without reading its code
- Letting the AI do arithmetic that code should do
- Trusting web search over the company's own filings
- Letting it make up your account size. Use percentages.
- Taking tax advice from it. The wash-sale mistake would have cost real money.
- Assuming the first clean report means it works. The next company will find a new bug.

## Before you walk away

- [ ] Your budget alert is set
- [ ] The agent has no brokerage login, account numbers or ability to trade
- [ ] The wash-sale rule is written correctly into its instructions
- [ ] Every report says it's educational, not advice
- [ ] You check anything you'd act on against the filings yourself, or with a qualified professional
