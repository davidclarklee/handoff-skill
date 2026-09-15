# /handoff

A Claude skill that packs up everything you and Claude figured out in a session, so
the next session can pick it up and keep working. The next session can be a fresh
Claude Code window, a chat on claude.ai, or a completely different assistant like
ChatGPT or Gemini.

After creating this skill, research was done to find other similar handoff skills.
The two most popular, by Matt Pocock and ToolMonsters, plus a third by Ruben Hassid,
were each compared against this skill, and any positive attributes from them were
added to this already robust handoff skill.

More information can be found at the [end of this readme](#Attribution) regarding what positive 
attributes were selected from each skill and then added to this build.

Full disclosure: Claude wrote quite a bit of this Readme, and a lot has been removed,
and some human adjustments have been made when the language was too robotic.

The skill itself has been checked for any security issues, but feel free to upload it 
to Claude and have it check out the skill for you before you install it. It's a best 
practice procedure to follow with any skill with a low GitHub star count like mine.

## The problem

You work with Claude for two hours. You make decisions. You hit dead ends. You find
solutions that you'll forget ten minutes later. Then the chat gets too long, or it's 
late, or you found a good stopping point and want to save on tokens. 

Because you know that every question you ask, Claude rereads everything in that same 
chat, eating your tokens, so you start a new chat. But, the new session knows nothing 
of the previous chat. Ten minutes in, it suggests the exact approach you already 
threw out, and rediscovers that setting the hard way.

The obvious fix is to ask for a summary. But a simple summary can get really messy,
really fast. There are miles of nuance in your chat. Things that you tried and found 
were the wrong approach, and random solutions Claude stumbled across and you have no 
idea how to put into words.
What the new session needs is a picture of **what's true right now**, plus, and most importantly, 
**the reasoning that isn't saved anywhere else**.

That's what this skill writes... and more. 

It's a way to start a fresh session with all of your progress intact. Every u-turn,
every discovery, every file needed to continue as if you just hit the reset button
on your token pool, and with the /handoff skill you're ready to keep going!

## The idea behind it

Everything that went *right* is already saved in your files. The code is there. The
document is there. You don't need to write it down again.

Everything that went *wrong* only exists in the conversation, and the conversation
is what you're about to lose. The failed attempts. The moment you realized why
something wasn't working. The thing you nearly "fixed" that turned out not to be
broken.

That's the expensive knowledge, and it's the first thing an ordinary summary throws
away, because it looks like clutter. This skill goes looking for it on purpose.

## What it does

- **It checks the files before it trusts its memory.**

- **It reads the chat a second time before delivering.** After drafting, it goes back
for the things a first read misses: a correction you made once in passing, a limit
you mentioned once and never repeated, and whether a file reference points at the
current version. If two parts of the chat contradict each other and it was never
settled, it lists that as an open question instead of picking a side.

- **It asks where the handoff is going, and never assumes.**

- **It includes your actual work when the next session can't reach your files.** More
on this below, because it's the rule people ask about most.

- **It says how sure it is about each thing.**

- **It won't make things up to look thorough.**

- **It copies names and numbers exactly.**

- **It removes passwords and personal details.** It scrubs out "dangerous" information
such as a password, an access key, or a real person’s email address. If it isn't sure
whether something counts, it asks you instead of guessing. The next session learns how
the thing works without inheriting your credentials.

- **It separates facts that expire from facts that don't.** When a session produces
enough permanent knowledge (like setup quirks that cost you time, or a rejected idea
likely to come up again), the skill writes a **second, short file** just for that.
If there isn't enough, it says so in one line and skips the file. It also tells you
where that file should live so it gets read automatically: as `CLAUDE.md` in your
project folder for Claude Code, in Project knowledge on claude.ai, or in another AI's
saved-instructions setting.

- **It tells you which files to bring.** A handoff that mentions `screenshot-3.png`
is useless if the screenshot stays behind. So the list of files to bring goes in two
places: inside the document, and as a plain checklist at the end of the chat reply,
so you don't have to open the document to find out what to move. If the next session
is a terminal tool other than Claude Code, the fingerprint script is on that list too.

- **It won't overwrite your files without asking.** If a file it wants to write already
exists, like an older handoff or a `CLAUDE.md`, it checks with you first. For an existing
`CLAUDE.md`, it shows you what it would add instead of replacing what's there.

- **It keeps things short.** Most handoffs land between 150 and 300 lines. Past about 500, it assumes it started 
telling the story of the session instead of describing where things stand and reevaluates
what is going into the markdown document. However, pasted work is not counted in those 
numbers and is never shortened to fit them.

- **It suggests you test the handoff.** It recommends opening a fresh chat with
nothing but the handoff, and watching whether the new session asks sensible
questions or charges ahead on assumptions.

- **It names other skills that would help.** Taken from the comparison with Matt Pocock's
handoff skill, because of his multiple skills he's created, it lists them *and* explains 
in one line what each one does, so the note still makes sense if the next session doesn't 
have that skill installed. It skips this entirely when you're heading somewhere that
can't use Claude skills at all.

- **It only runs when you ask.** In Claude Code it won't offer itself, and it won't 
trigger because your conversation sounds like it's wrapping up. On claude.ai it may 
still start on its own, but nothing else changes, because the skill asks its questions 
out loud rather than relying on what you typed after the command. But to date, the skill
has never fired for me without typing "/handoff" (without quotes) into the prompt field.

## What's in the document

A single markdown file. It starts at its own heading and ends at the last section.
No "here's the handoff you asked for," no sign-off.

- **Start here:** where things stand in two or three lines, then the first action
- **Paths and inventory:** where everything lives, plus the companion files to bring
- **Work in progress (verbatim):** your actual draft or code, when the destination needs it
- **What this thing is:** just enough to get oriented, plus what must not be changed
- **Environment notes:** the settings, flags and quirks that cost you time to find
- **Known broken:** including anything written but never actually run, flagged clearly
- **Decisions and rejected alternatives:** what was chosen, and what was ruled out and why
- **Open items**, **open questions**, and **how to verify a change**
- **Working preferences:** how you like to be worked with, and corrections you've made
- **Suggested skills:** when the destination can use them
- **Suggested opening prompt:** a ready-to-paste first message for the new chat, when
  heading to claude.ai or another AI. Left out for Claude Code, which opens the file
  directly.

Empty sections get dropped rather than padded. Depending on the session you may
also get `project-notes-<topic>.md`, the permanent-knowledge file described above.
The main document is saved as `handoff-<topic>-<YYYY-MM-DD>.md` in your working
folder, not a temporary folder, so you can actually find it.

## The verbatim rule, and how this skill handles it

"Verbatim" means word for word. Copying the real thing instead of describing it.

It matters because of how AI models behave. Hand one a *description* of your draft
and it will helpfully write a new draft. The new one will look fine. It will also
have quietly lost every deliberate choice you made, and neither of you will notice.

Some handoff tools solve this by always pasting everything, every time. This skill
does something slightly different: it asks where the document is going first, then
picks.

- **Going to a new Claude Code session on the same computer?** The document points
  at your files instead of copying them. The next session can just open them, and a
  copy would start going out of date the moment it was made.
- **Going to claude.ai, or to ChatGPT, Gemini, or anything else?** Your work gets
  pasted in whole. Those places can't reach your computer, so a file path is a dead
  end there.
- **Don't know yet?** It asks one simpler question: should your work be pasted in
  full, or just referenced by its file path? If you can't answer that either, it
  pastes everything. A document that's longer than it needed to be just wastes a
  little space. A document pointing at a file nobody can open
  has lost the one thing it was carrying.

Three more things protect that rule:

1. **Nothing gets trimmed to hit a length limit.** As mentioned, the pasted work 
   sits outside the 150-to-300-line target. If a file is big enough that pasting it 
   whole seems unwise, the skill stops and asks you rather than deciding alone. 
   **If you don't answer, it pastes the whole thing.**
2. **Scrubbing passwords takes priority over completeness.** Before pasting, it 
   scans your work for keys and personal details. If it finds any it stops and 
   tells you what it found and where, without printing the secret back at you. 
   If you don't answer, it removes them rather than sending them.
3. **"Nothing to paste?"** If the file was discussed but never actually shown, 
   it says so and offers you the choice: attach it, accept a description, or drop 
   the section with a note explaining why.

## The bundled script (why this skill is handoff.skill and not SKILL.md)

Most public skills are a single instruction file. This one ships with a small
helper: `scripts/inventory.py`.

It produces a table of every file that matters, with each file's size and a short
fingerprint (a 12-character hash) of its contents. That table goes in the *Paths
and inventory* section.

The point is to catch changes. When the next session can run commands on your files
(a new Claude Code session, or a terminal tool like Codex CLI with the files checked
out), the handoff tells it to offer to re-run the script and compare before editing
anything, and to run nothing without a yes. If a fingerprint doesn't match, somebody
edited that file after the handoff was written, and it should be sorted out before
anyone starts editing further. Without this, the next session trusts a description
of a file that has since moved on. For a plain chat like claude.ai or ChatGPT on the
web, this step is left out, since there's nothing to run it on.

One detail worth knowing: for zipped file types, including `.zip`, `.skill`,
`.docx`, `.xlsx` and `.pptx`, it fingerprints the contents rather than the
container. Rezipping a file changes the outside bytes even when nothing inside
changed, so fingerprinting the container would report changes that never happened.
The script is also strict on purpose: if you point it at a file that doesn't exist,
it still prints the table for the files it found, but it also names the missing file
and ends with an error, so the gap can't go unnoticed. An incomplete
inventory is worse than none, because the next session believes it.

Run it directly if you ever want to:

```
python scripts/inventory.py <path> [<path> ...]
```

When installing, the script must stay in `scripts/` next to `SKILL.md`. Copying
`SKILL.md` on its own gives you a skill that refers to a tool that isn't there.
When a handoff is headed to a terminal tool other than Claude Code, the skill copies
the script next to the handoff file so it can travel with it, since that tool won't
have the skill installed.

## Install

**Installing in Claude Code or the CLI.** If you're flush with tokens, you can always 
just ask Claude to install it for you (and if updating, uninstall the prior version first). Otherwise, put the whole folder at `~/.claude/skills/handoff` for personal use, or at `.claude/skills/handoff` inside a project for that project only.  
Keep the structure intact:

```
handoff/
├── SKILL.md
└── scripts/
    └── inventory.py
```

**To install in Claude apps (claude.ai and desktop).** Upload the packaged `handoff.skill` file
under **Settings → Capabilities → Skills**. You have the option to toggle it on or off there.

## Use
```
/handoff
```

In the Claude CLI you may also see
```
/anthropic-skills:handoff
```
as a possible selection. **They are the same skill.** Just choose the /handoff option,
but either will work.

On its own, it always asks where the next session is going. It only asks what the
next session is for if your chat covered more than one topic. Answer both up front
and it skips those questions:

```
/handoff finishing the grant draft in ChatGPT
/handoff continuing this session later, same repo
```

Those two facts are checked separately. Give it the topic but not the destination
and it will still ask about the destination. It may also check a few details along
the way: whether the next tool can run a terminal, what to do if it finds a password
or personal detail in your work, or how to handle a very large file.

## Not what it's for

Meeting minutes. Release notes. A summary for your manager. A recap of what you and
Claude talked about.

Those are documents for people, where the story of what happened is the whole
point. This one is written for a machine that's about to start working, and it
deliberately throws away the material those documents are made of.

## License

MIT

## <a id="Attribution"></a>Attribution for upgrades: What changed, and who inspired it

The changes were not a result of forking any of the handoff skills that inspired
them. Each one's SKILL.md was uploaded into Claude and compared, one at a time,
against my previously existing handoff.skill. The positive traits were added to a prompt, and
then Claude made the changes to my handoff.skill package where possible.

## Credits (short version)

This update borrowed ideas from three other handoff skills found online:
- **Matt Pocock's** handoff skill https://github.com/mattpocock
- **ToolMonsters'** handoff skill https://github.com/ToolMonsters
- **Ruben Hassid's** handoff skill https://ruben.substack.com/

Everything below is grouped by which one inspired it, plus what was already part
of the skill before any were reviewed. Documentation compiled by Claude Code.

---

## Changes inspired by Matt Pocock's skill

1. **Manual-only triggering.** The skill no longer offers itself unprompted or
   triggers from natural phrases like "hand this off" — it now only runs when you
   type `/handoff` directly.  
   (Mainly true for Claude Code, though there's been no record of it firing without manual initiation in Claude.ai.) 
2. **A focus argument.** You can now type something after the command, like
   `/handoff continue the login bug fix`, and the document will lean toward that
   topic.
3. **A "suggested skills" section** in the output, listing which other skills you
   have that might help continue the work, and what each one does. (This one was
   refined further — see "Where the two ideas had to be reconciled" below.)
4. **Naming concrete examples** in the existing "don't repeat content that lives
   elsewhere" rule — specs, plans, tickets, commits, and similar, spelled out
   up front instead of left implied.
5. **Widening the existing redaction rule to cover personal information** (names,
   emails), not just passwords and API keys. The redaction itself already
   existed — see "What was already part of the handoff.skill before any review" below — Matt's example is
   what prompted broadening what it catches.

## Changes inspired by ToolMonsters' skill

1. **Pasting work-in-progress content word-for-word** (a draft, code, a plan)
   instead of just pointing at the file, for situations where the next
   session won't be able to open that file itself.
2. **"Zero invention"** — reinforcing that if there isn't enough to go on, the
   document should say "unclear" rather than filling the gap with a guess. This
   sits alongside the skill's existing [observed] / [verified] / [inferred]
   labeling — it didn't replace it, just tightened the one edge case where there's
   nothing to reason from at all.
3. **Cleaner output** — no "here's your document!" before it, no closing remarks
   after it. Just the document itself.
4. **Precision rules** — numbers, file names, links, and dates get copied exactly
   as they appeared, instead of being casually restated.
5. **The general push toward supporting handoff to other AI tools**, not just
   another Claude session — ToolMonsters' version was explicitly built for
   ChatGPT, Gemini, or any LLM, and that's what prompted adding real support for
   that case rather than assuming the next stop is always Claude.

## Changes inspired by Ruben Hassid's skill

Ruben's skill is a short, single-purpose summary tool (about 150 lines). Most of what it
does was already covered here, so only two ideas were taken.

1. **A suggested opening prompt.** A ready-to-paste first message for the new chat,
   added as its own section at the end of the document. It only appears when the
   handoff is going to claude.ai or another AI, since a Claude Code session opens the
   file directly. It doesn't repeat the handoff; it points the new session at the first
   action in "Start here."
2. **A second pass before delivering.** After drafting, the skill re-reads the
   conversation for three things that are easy to miss: a correction made once in a
   throwaway line, a constraint stated once and never repeated, and a file reference
   that points at an old version instead of the current one. Unresolved contradictions
   get listed as open questions rather than quietly decided. The first two checks were
   folded into the existing "what did the user ask for or rule out" step, and the
   version check into the existing precision rules, so each rule lives in one place.
   Only the second pass itself was added as a new step.

Not taken: Ruben's option to write handoffs for a human colleague or your future self.
This skill is written for a model that will act on the handoff, not a person catching
up, so adding those would contradict its purpose.

## Where the two ideas had to be reconciled (not from any of the source skills directly)

Matt's "suggested skills" idea and ToolMonsters' "hand off to any AI" idea don't
naturally fit together — a list of Claude skills is useless if the next stop is
ChatGPT. So the skill now explicitly asks (or picks up from your typed focus, if
you mentioned it) where the conversation is actually headed next, and reuses that
one answer for several decisions at once:
- whether to paste content in full vs. just reference the file,
- whether the "suggested skills" section gets included at all,
- whether the document ends with a suggested opening prompt, and
- whether the file-fingerprint check is offered, and whether the script travels
  with the handoff.

This piece was original glue work needed to make the two borrowed ideas coexist
without contradicting each other — worth a mention in credits, but it's not
something to attribute to any source skill specifically.

## What was already part of the handoff.skill before any review

None of this came from Matt, ToolMonsters, or Ruben — it's what the skill already did
before any of them were reviewed. Some of it was later improved, as described above:
- Digging into what actually happened (checking file changes, error messages,
  things that failed) instead of relying on memory of the conversation.
- Separating "worth remembering forever" from "will be stale in a week," with an
  offer to save the forever-stuff to its own file.
- A checklist of companion files (screenshots, data, etc.) that need to travel
  alongside the handoff document.
- Trimming ruthlessly so the document doesn't balloon in length.
- Suggesting a test run in a brand-new chat before trusting the handoff.
- **Redacting secrets before they reach the document** — live API keys, passwords,
  tokens, database connection strings, that kind of thing pulled out of error text
  or logs before anything gets written down.
  
  (This list may be incomplete, as it wasn't the primary objective of the session
  that produced this output &#58;)

## The clarification flagged during the build process: redaction still applies to the verbatim content

The earlier summary described the "paste it word-for-word" change without saying
whether that content still gets scrubbed for secrets first — a fair thing to
notice missing, since pasting something in full is exactly where a stray API key
or credential is most likely to slip through if it isn't. It does still get
scrubbed: redaction was never scoped to one section of the document, it applies to
everything going into it, and that rule was explicitly protected — not weakened or
bypassed — while this update was made. So a code snippet or draft that happens to
contain a live credential still gets that value redacted before it's pasted in,
whether it's being included in full or just referenced.