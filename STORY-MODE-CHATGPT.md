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

## What it is and is not

This is the *experience* of Story Mode: the menu, the number-replies, the chaining. It is not the
full machinery. The full Claude Code version learns which options you actually pick and gets better
at predicting you over time, and it can even run itself. ChatGPT cannot do those parts (they need a
real program running underneath). But the part that makes people fall in love with it, ending every
turn with a menu you steer by number, works exactly the same here.

Full version and the story behind it: [STORY-MODE.md](./STORY-MODE.md).
