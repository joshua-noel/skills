---
name: ste-writing
description: Rewrite or write text at about 80% of ASD-STE100 Simplified Technical English. Use when the user asks for "STE", "ASD-STE100", "simplified technical English", "plain technical English", or asks to make an explanation, doc, README, runbook, or procedure clearer and easier to read. Also used by the visualize-diagram and visualize-webpage skills for their labels and prose.
---

# STE writing (80%)

ASD-STE100 is a controlled language for aerospace maintenance documents. The full specification is strict. Use about 80% of it: keep the rules that make text clear, and relax the rules that make technical text unnatural.

## Rules to keep

### Words
1. Use one word for one thing. Do not change the word to get variety.
2. Use the simple word. Examples:

   | Do not use | Use |
   |---|---|
   | utilize | use |
   | commence, initiate | start |
   | terminate | stop |
   | prior to | before |
   | subsequent to | after |
   | ensure | make sure |
   | in order to | to |
   | approximately | about |
   | replenish | fill |
   | facilitate | help, let |
   | leverage | use |
   | sufficient | enough |

3. Do not leave out the words "the", "a", "an" and "this".
4. Keep noun clusters to 3 words or fewer. Write "the cache for user sessions", not "user session cache invalidation handler".

### Sentences
5. Procedural sentences: 20 words or fewer.
6. Descriptive sentences: 25 words or fewer.
7. Give one instruction in each sentence. Two actions at the same time are the only exception.
8. Use the active voice in procedures. Write "Run the migration", not "The migration should be run".
9. Use the command form for instructions.
10. Use simple tenses: present, past and future.

### Paragraphs and structure
11. Write one topic in each paragraph.
12. Use 6 sentences or fewer in each paragraph.
13. Use vertical lists for steps, options and complex conditions.
14. Number steps in a procedure. Put the condition before the action: "If the build fails, read the log."

### Safety notes
15. Use `WARNING` for a risk of injury, data loss or security exposure. Use `CAUTION` for a risk of damage to a system.
16. Start the note with a clear command. Then give the risk.

    `WARNING: Do not run this command on production. It deletes all rows.`

## Rules to relax (the other 20%)

- No closed dictionary. Any common English word is allowed when it is the clearest word.
- Technical names are allowed freely: code identifiers, file paths, product names and domain terms.
- The passive voice is allowed in descriptive text when the agent is unknown or not important.
- The "-ing" form is allowed when it reads naturally.
- Code, commands, logs and quoted output are not changed.

## Procedure

1. Find the purpose of the text: instruction, description or warning.
2. Split long sentences. Put one idea in each sentence.
3. Replace complex words with the words in the table above.
4. Change passive procedures to commands.
5. Change dense paragraphs to lists where there are steps or options.
6. Keep all facts. Do not remove meaning to make the text shorter.
7. Read the result again. Make sure each technical term has one name in all of the text.

## Example

Before:
> It is imperative that the operator ensures the hydraulic reservoir is replenished prior to commencing operation.

After:
> Make sure that the hydraulic reservoir is full before you start the operation.
