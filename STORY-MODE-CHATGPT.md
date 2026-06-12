# Story Mode for ChatGPT

Story Mode is a way of using an AI where every reply ends with a short numbered menu of what you
might want next, and you just type a number to keep going. It started as a Claude Code tool, but the
core of it is pure instruction, so it runs on ChatGPT too, with no setup beyond a copy-paste.

This page is written so you can hand it to someone who only uses ChatGPT and have them up and
running in a minute.

## The instruction (this is the whole thing)

```
You are running "Story Mode." Follow these rules in every single reply, no exceptions:

1. First, do what I asked.
2. Then, at the very end of EVERY reply, add a menu titled exactly:
   Story Mode — reply with a number, or pick a few in order (like 3 or 5,4,1):
3. Under that title, list 10 short options for what I might want to do next, your best
   guess first. Each option is one short line I can choose just by typing its number.
4. If I reply with only a number, do that option. If I reply with several numbers like
   5,4,1, do them in that order. Do not ask me to confirm. Just do it.
5. Keep showing the menu at the end of every reply, even after I pick. The menu never stops.
```

## Three ways to turn it on, easiest first

**1. Build a "Story Mode" GPT (best for someone else to use).**
You need ChatGPT Plus. Go to *Explore GPTs > Create*, paste the instruction above into the
*Instructions* box, name it "Story Mode," save, and share the link. Whoever you send it to just
clicks the link and starts chatting. Zero setup on their end. This is the one to use for your dad:
he clicks once and it is always on.

**2. Custom Instructions (set it once for all your own chats).**
In ChatGPT: *Settings > Personalization > Custom Instructions*. Paste the instruction into the box
labeled "How would you like ChatGPT to respond?" and save. Now every new chat is Story Mode.

**3. Paste it at the start of a chat (no setup, one chat at a time).**
Open a new chat and paste the instruction as your first message. That chat will run Story Mode until
you close it.

## How far ChatGPT can actually take it

The copy-paste above is the simplest version: the menu, the number-replies, the chaining, by
instruction alone. But it would be wrong to stop there and treat ChatGPT like a dumb terminal. It has
real machinery that can carry Story Mode most of the way to the full thing:

- **Persistent memory.** ChatGPT remembers facts and preferences across your chats. That alone gives
  a soft version of learning your hand: it can notice the kinds of moves you tend to pick and lean the
  menu toward them, with no code at all.
- **Code Interpreter (Advanced Data Analysis).** It runs real Python in a sandbox. Within a session it
  can keep a log of every pick and compute the actual catch-rate, the same metric the hook version
  tracks. That is a program running underneath, not a chatbot guessing.
- **Custom GPT + Actions.** A Custom GPT can call an external API. Point it at a small backend and you
  have the full persistent, self-tuning corpus, the same as the local hook version, just hosted instead
  of sitting on your disk.

The one thing the consumer ChatGPT chat genuinely cannot do is drive itself turn after turn while you
are away. There is no equivalent of the Stop-hook that re-prompts it. And even that has a platform
answer: the Assistants / Agents API can run autonomous multi-step loops.

So the honest summary: ChatGPT can do nearly all of Story Mode. It just assembles it from different
parts, memory plus Code Interpreter plus Actions, instead of local hooks. The copy-paste is the front
door; the machinery is there if you want to go deeper.

## Building the fuller version (a sketch)

If you want the near-complete Story Mode on ChatGPT, the same self-tuning loop the hook version runs,
here is the architecture using only ChatGPT-native parts:

- **Custom GPT instructions** carry the rules above: end every turn with the ranked menu, interpret
  number replies, allow chaining. This is the deterministic-enough surface.
- **Code Interpreter** is the program running underneath. Have the GPT keep a small log of every pick
  in the sandbox during the session, then compute the real catch-rate (how often your move was in the
  ten) and the rank it landed at. That is the exact metric the hook computes, in real Python.
- **An Action to a tiny backend** is what makes it persist and learn across sessions. The sandbox
  resets between chats, so on each turn the GPT calls an Action: read the user's pick history, rank
  the menu using it, and after the user picks, write the new pick back. That backend is the corpus.
  A dozen lines of serverless code plus a key-value store is enough.
- **Persistent memory** is the zero-effort fallback: even with no backend, ChatGPT memory will softly
  remember the kinds of moves you pick and lean the menu that way.

The only piece that stays out of reach on the consumer chat surface is unattended self-driving, the
agent re-prompting itself turn after turn while you are away. That lives at the platform layer
(the Assistants / Agents API), not in a chat window. Everything else, the menu, the chaining, the
real catch-rate, the cross-session learning, is buildable today with a Custom GPT, Code Interpreter,
and one Action.

Full version and the story behind it: [STORY-MODE.md](./STORY-MODE.md).
