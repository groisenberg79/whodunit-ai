# Whodunit AI — Phase 1 Planning Document

## Current Project Status

```text
✅ Phase 0 — Project setup completed
✅ Phase 1, Step 1.1 — Decide plot source / original case direction
✅ Phase 1, Step 1.2 — Define motive web and true solution
✅ Phase 1, Step 1.3 — Define the four suspects
✅ Phase 1, Step 1.4 — Define the clues
✅ Phase 1, Step 1.5 — Define locations and assign clues
✅ Phase 1, Step 1.6 — Define the murder-night timeline
✅ Phase 1, Step 1.7 — Define final accusation logic
✅ Phase 1, Step 1.8 — Define clue discovery mechanics and inspectable areas
✅ Phase 1, Step 1.9 — Define discovered clues vs. confronted evidence
✅ Phase 1, Step 1.10 — Define FAISS/RAG as core MVP component
✅ Phase 1, Step 1.11 — Define LangGraph interview orchestration as core MVP component
➡️ Current Development Phase — Phase 4: Prompt Builder and NPC Dialogue Layer
```

---

# 1. Project Concept

## Project Title

**Whodunit AI: An LLM-Powered Mystery Game Prototype**

## Core Idea

Whodunit AI is an interactive detective/mystery game prototype where the player investigates a fictional murder case by interviewing suspects, examining clues, and making a final accusation.

The main GenAI idea is to explore how large language models can power dynamic NPC dialogue in a narrative game. Instead of selecting from fixed dialogue trees, the player can ask free-form questions. Each NPC responds through an LLM, but their answers are constrained by:

- structured character profiles,
- personality,
- private secrets,
- individual knowledge,
- clues discovered by the player,
- evidence explicitly revealed to each suspect,
- dialogue history,
- current game state,
- FAISS/RAG retrieved context,
- LangGraph-managed interview workflow,
- consistency rules.

The larger product idea is a prototype for future RPGs where NPCs can hold more natural conversations with players while the story remains coherent and controlled.

The technical architecture also demonstrates bootcamp GenAI tools. FAISS/RAG will be used to retrieve relevant case context, while LangGraph will orchestrate the multi-step NPC interview pipeline: evidence validation, context construction, retrieval, prompt building, response generation, consistency checking, and dialogue recording.

---

# 2. Plot Source Decision

For the MVP, the playable case will be **original**, created by us. Public-domain mystery stories may be used only as inspiration or later as a possible corpus for analysis.

This avoids copyright problems and gives full control over the mystery structure, NPC knowledge boundaries, clues, and final accusation logic.

---

# 3. Case Premise

## Case Title

**Murder at Blackwood Manor**

## Setting

A 1930s English country house during a stormy evening.

## Victim

**Edward Blackwood** — a wealthy publisher and family patriarch. He is intelligent, controlling, cruel, and surrounded by people who have reasons to hate or fear him.

## Crime

Edward Blackwood is found murdered in his private library after dinner.

At first, the murder appears connected to inheritance, family resentment, or a romantic scandal. The true motive is deeper: Edward had discovered a hidden medical crime committed years earlier by Dr. Henry Ashford and intended to expose him.

---

# 4. Motive Web

A central design decision is that the mystery should not have a single obvious motive. Several suspects should have plausible reasons to kill Edward.

The final accusation should be cumulative, not just “who did it.” The player must understand:

- who killed Edward,
- why they killed him,
- how they did it,
- what evidence proves it,
- which motives were misleading.

| Motive | Suspect It Points Toward | Role in Mystery |
|---|---|---|
| Inheritance | Clara Vale | Obvious financial red herring |
| Romantic rejection | Beatrice Ashford | Emotional/scandal red herring |
| Jealousy over affair | Dr. Henry Ashford | False interpretation of Henry |
| Old family grudge / abuse | Julian Blackwood | Violent/emotional red herring |
| Hidden old medical crime | Dr. Henry Ashford | True motive |

## True Culprit

**Dr. Henry Ashford**

## True Motive

Edward had discovered that Henry falsified medical records years earlier connected to the death of Edward’s wife. Henry’s negligence, or possibly intentional overmedication, contributed to her death, and he covered it up. Edward planned to expose him. Henry killed Edward to protect himself.

## Core Twist

Henry knew about Beatrice and Edward’s affair, but he was not truly jealous. His marriage to Beatrice was already emotionally dead, and Henry himself was involved in another affair.

The affair is therefore a red herring. It makes both Beatrice and Henry look suspicious, but it is not the true motive.

---

# 5. Suspects

## 5.1 Clara Vale

```text
id: clara_vale
name: Clara Vale
role: The victim’s niece
relationship_to_victim: Edward Blackwood’s niece and expected heir
```

### Public Description

Clara Vale is Edward Blackwood’s elegant but financially dependent niece. She has lived under Edward’s protection for years and was widely believed to be one of the main beneficiaries of his will.

Recently, Edward had become displeased with her lifestyle and hinted that he intended to reduce or remove her inheritance.

### Personality

- controlled,
- proud,
- intelligent,
- socially polished,
- defensive when pressured,
- more frightened than she wants to appear.

### Apparent Motive

**Inheritance**

Clara had a clear financial motive. If Edward changed his will, she could lose her expected fortune.

### Real Secret

Clara secretly tried to influence Edward’s will. She may have forged or altered a private letter suggesting that Edward had promised her a larger inheritance.

This makes her look guilty, but her crime is fraud, not murder.

### Alibi

Clara claims she was in the drawing room after dinner, writing letters. However, nobody can fully confirm this for the entire period around the murder.

### What Clara Knows

- Edward had recently threatened to change the will.
- Edward argued with Julian earlier that evening.
- Beatrice was emotionally distressed and had tried to speak privately with Edward.
- Henry seemed unusually calm after the body was discovered.

### What Clara Lies About

- She lies about how desperate her financial situation is.
- She lies about the forged or altered inheritance letter.
- She minimizes her argument with Edward about the will.

### Evidence Reactions

#### Torn Will Note

If the player confronts Clara with the torn will note, Clara becomes defensive and may admit she was afraid of losing her inheritance.

> “Yes, I was afraid he would cut me out. Yes, I did something foolish with the letter. But Edward was alive when I last saw him.”

#### Silver Letter Opener

If the player confronts Clara with the letter opener, she panics because it is connected to her, but insists she did not bring it to the library that night.

> “It was mine once, yes. But I did not use it. I had not seen it on Edward’s desk until after he was dead.”

---

## 5.2 Julian Blackwood

```text
id: julian_blackwood
name: Julian Blackwood
role: The victim’s estranged son
relationship_to_victim: Edward Blackwood’s son
```

### Public Description

Julian Blackwood is Edward’s estranged son. He left Blackwood Manor years ago after a bitter break with his father. His return on the night of the murder shocked the household.

Everyone knows Julian and Edward had a painful relationship, but few know the full extent of it.

### Personality

- bitter,
- impulsive,
- wounded,
- direct,
- emotionally volatile,
- still seeking recognition from his father.

### Apparent Motive

**Old family grudge**

Julian resented Edward for years of emotional neglect and possible violence during childhood. On the night of the murder, several people heard them arguing.

### Real Secret

Julian did come back because he needed money, but also because he wanted Edward to acknowledge what he had done to him. He had no intention of killing him, but he did threaten Edward during their argument.

### Alibi

Julian claims he left the library after arguing with Edward and went outside to the garden path to cool down. His alibi is weak because he was alone for several minutes.

### What Julian Knows

- Edward was alive when Julian left the library.
- Edward seemed nervous about something unrelated to the will.
- Julian saw Henry near the study later that night.
- Julian noticed Beatrice crying before dinner.

### What Julian Lies About

- He lies about the intensity of his argument with Edward.
- He hides that he threatened Edward.
- He hides that he desperately needed money.

### Evidence Reactions

#### Broken Watch

If the player confronts Julian with the broken watch, he admits he stormed outside after the argument and broke it in anger.

> “I said I wished him dead. I won’t deny it. But wishing is not doing. When I left that room, he was alive.”

The watch supports Julian’s emotional state, but it also supports the fact that he left the library before the murder.

---

## 5.3 Beatrice Ashford

```text
id: beatrice_ashford
name: Beatrice Ashford
role: Dr. Henry Ashford’s wife
relationship_to_victim: Edward Blackwood’s lover
```

### Public Description

Beatrice Ashford is the wife of Dr. Henry Ashford. She is socially graceful, emotional, and deeply concerned with appearances.

Unknown to most of the household, Beatrice had been having an affair with Edward Blackwood. Edward had recently ended the relationship, saying that his feelings for her had faded.

Beatrice did not accept the breakup. She wrote Edward several furious, desperate letters.

### Personality

- romantic,
- proud,
- wounded,
- impulsive,
- dramatic under pressure,
- terrified of public humiliation.

### Apparent Motive

**Romantic rejection**

Beatrice appears to have a strong emotional motive. She was humiliated, abandoned, and desperate.

### Real Secret

Beatrice was Edward’s lover, and she was devastated when he ended the affair. However, she did not kill him. She lies because she wants to hide the affair and protect her reputation.

### Alibi

Beatrice claims she went to her room after dinner because she felt unwell. A maid saw her near the staircase, but there is a gap in the timeline.

### What Beatrice Knows

- Edward had ended their affair.
- Henry knew about the affair and did not seem jealous.
- Edward was frightened by something Henry-related, though Beatrice does not know exactly what.
- Edward received or handled some old medical document before dinner.

### What Beatrice Lies About

- She denies the affair at first.
- She denies writing the furious letters.
- She lies about trying to see Edward privately on the night of the murder.

### Evidence Reactions

#### Beatrice’s Furious Letters

If the player confronts Beatrice with the letters, she admits the affair and the breakup, but insists her anger was emotional, not murderous.

> “I loved him. Or I thought I did. He made a fool of me, and yes, I wrote those letters. But I did not kill him.”

She may also reveal:

> “Henry knew. That is the strangest part. He knew, and he barely cared.”

This helps move suspicion away from jealousy and toward Henry’s deeper secret.

---

## 5.4 Dr. Henry Ashford

```text
id: henry_ashford
name: Dr. Henry Ashford
role: Family physician and Beatrice’s husband
relationship_to_victim: Edward Blackwood’s old friend and doctor
```

### Public Description

Dr. Henry Ashford is the Blackwood family physician and an old acquaintance of Edward’s. Calm, precise, and respectable, Henry appears to be the most rational person in the household after the murder.

He is married to Beatrice Ashford, though their marriage has long been emotionally dead.

### Personality

- calm,
- intellectual,
- detached,
- dryly ironic,
- controlled,
- contemptuous when challenged,
- very careful with words.

### Apparent Motive

**Jealous husband**

Once the player discovers Beatrice’s affair with Edward, Henry appears to have a possible motive: jealousy.

But this is misleading.

### True Motive

**Exposure of hidden medical crime**

Edward had discovered that years earlier Henry falsified medical records related to the death of Edward’s wife. Henry’s negligence, or possibly intentional overmedication, contributed to her death, and he covered it up.

### Real Secret

Henry knows Beatrice was having an affair with Edward, but he does not care much. He is himself involved in another affair and considers his marriage to Beatrice practically finished.

His real fear is not romantic humiliation. It is professional ruin, prison, and exposure.

### Alibi

Henry claims he was in the study reviewing medical correspondence. His alibi appears respectable but depends almost entirely on his own testimony.

### What Henry Knows

- Edward had discovered the old medical cover-up.
- Edward intended to confront or expose him.
- Beatrice had been Edward’s lover.
- Clara was worried about the will.
- Julian argued with Edward that evening.

### What Henry Lies About

- He lies about the old medical records.
- He lies about the contents of his final conversation with Edward.
- He pretends to be more shocked by the affair than he really is.
- He may subtly encourage suspicion toward Beatrice, Clara, or Julian.

### Evidence Reactions

Henry should never confess easily.

#### Medical Vial

If the player confronts Henry with the medical vial alone, Henry should dismiss it as ordinary medicine.

> “You have discovered that a doctor carries medicine. I congratulate you on the triumph.”

#### Brandy Glass Residue

If the player confronts Henry with the brandy residue, he should remain controlled and suggest contamination or amateur speculation.

> “Residue in a glass proves very little unless one already knows what one wishes it to prove.”

#### Medical Vial + Brandy Glass Residue

If the player has discovered both the vial and residue and confronts Henry with either, Henry should become more guarded, but still not confess.

> “You are assembling fragments into a drama. It is an entertaining habit, but not a scientific one.”

#### Altered Death Certificate

If the player confronts Henry with the altered death certificate, he becomes colder and more evasive.

> “Edward always had a talent for opening graves that should have remained closed.”

Only near the end, if the accusation is correct, Henry can admit the truth indirectly or after the ending is triggered.

---

## 5.5 Single-Clue and Combo Evidence Reactions

NPCs can react in two ways during interviews:

1. **Single-clue reactions**  
   The suspect reacts to one specific clue presented by the player.

2. **Combo evidence reactions**  
   The suspect reacts differently when the player has discovered a meaningful combination of clues and confronts them with one of those clues.

Combo reactions do not necessarily reveal guilt. They can trigger panic, defensiveness, fear, realization, shame, or stronger evasiveness.

Examples:

- Clara reacts more strongly if the player has both the torn will note and the letter opener.
- Julian reacts differently if the player has both the broken watch and Edward’s final appointment note.
- Beatrice becomes more afraid if the player connects her letters with Henry’s medical access.
- Henry becomes more guarded if the player connects the medical vial with the brandy glass residue.
- Henry also becomes colder if the player connects the altered death certificate with Edward’s final appointment note.

This makes evidence feel cumulative rather than isolated.

---

# 6. Clues

The clue system should contain both red herrings and solution clues.

Each clue has two important states:

1. **Discovered by the player** — the player has found the clue while exploring locations.
2. **Revealed to a suspect / used in confrontation** — the player explicitly brings up the clue during an interview.

A suspect should not automatically react to every discovered clue. They react directly only when the player confronts them with that clue.

## Clue List

| ID | Name | Location | Points Toward | Function | Confrontation Targets |
|---|---|---|---|---|---|
| `torn_will_note` | Torn Will Note | Edward’s Study | Clara | Inheritance red herring | Clara |
| `beatrice_letters` | Beatrice’s Furious Letters | Beatrice’s Room | Beatrice / Henry | Romantic red herring; weakens jealousy motive | Beatrice, Henry |
| `broken_watch` | Julian’s Broken Watch | Garden Path | Julian | Old grudge/timeline clue | Julian |
| `medical_vial` | Small Medical Vial | Henry’s Medical Bag | Henry | Method clue | Henry |
| `brandy_glass_residue` | Residue on the Brandy Glass | Library | Henry | Poison/drugging clue | Henry |
| `letter_opener` | Silver Letter Opener | Library | Clara / Henry | Staged weapon clue | Clara, Henry |
| `altered_death_certificate` | Altered Death Certificate | Henry’s Study | Henry | True motive clue | Henry |
| `final_appointment_note` | Edward’s Final Appointment Note | Edward’s Study | Henry | Confrontation clue | Henry |

## Clue Details

### Torn Will Note

A torn handwritten note is found in Edward’s study. It appears to mention a planned change to the will and includes Clara’s name.

It suggests Clara may have killed Edward to prevent him from cutting her out of the inheritance. Actually, Clara was desperate and may have tried to manipulate Edward, but this does not prove murder.

### Beatrice’s Furious Letters

A bundle of letters from Beatrice to Edward. They are emotional, bitter, and desperate. She refuses to accept that Edward ended their affair.

They suggest Beatrice may have killed Edward because he rejected her. Actually, Beatrice was emotionally devastated and lied about the affair, but she did not kill Edward.

If confronted, Beatrice admits the affair and reveals that Henry knew about it but seemed strangely indifferent.

### Julian’s Broken Watch

Julian’s pocket watch is found near the garden path, cracked and stopped at 9:20.

It suggests Julian was outside around the time of the murder and may be lying about his movements. Actually, the broken watch supports that he left the library after arguing with Edward.

### Small Medical Vial

A small vial is found in Henry’s medical bag. Its label is partially scratched off. It contains a sedative or cardiac medication that could weaken a person quickly if mixed into a drink.

It is one of the key clues pointing toward Henry’s method.

### Brandy Glass Residue

A faint bitter-smelling residue is found at the bottom of Edward’s brandy glass. The glass appears to have been wiped, but not thoroughly.

It suggests Edward may have been drugged before he was killed.

### Silver Letter Opener

A silver letter opener is found near Edward’s desk. It appears to be the murder weapon. It belongs to Clara, or at least was recently used by her.

It suggests Clara may have killed Edward. Actually, Henry used or planted the letter opener to redirect suspicion toward Clara and the inheritance dispute.

### Altered Death Certificate

An old death certificate related to Edward’s late wife shows signs of alteration. The handwriting resembles Henry’s medical hand, and dates or dosages appear inconsistent.

This is the deepest clue. Edward had discovered Henry’s old medical cover-up and intended to expose him.

### Edward’s Final Appointment Note

A note in Edward’s handwriting reads:

> “H. after dinner. No more delays.”

At first, “H.” could refer to Henry, but it is not immediately obvious. It becomes meaningful once the player has found the altered death certificate or questioned Henry about the old medical documents.

---

# 7. Locations

For the MVP, all locations are visible from the start, and all inspectable areas can be clicked from the start. Locked/unlocked clue progression may be added later as a stretch goal.

## 7.1 Library

```text
id: library
name: The Library
```

Edward Blackwood’s private library is the murder scene. It is a dark, wood-paneled room lined with bookshelves, legal documents, and locked cabinets. A large desk sits near the fireplace. The storm outside rattles the windows, and the room still smells faintly of brandy and smoke.

### Function

Crime scene, method clues, staged weapon.

### Inspectable Areas

| Area | Clue | Result |
|---|---|---|
| Brandy glass | `brandy_glass_residue` | A faint bitter residue remains at the bottom of the glass. |
| Silver letter opener | `letter_opener` | A silver letter opener lies near the desk. It appears recently handled. |
| Edward’s desk | None | Papers are scattered across the desk, but nothing here seems decisive. |
| Fireplace | None | The fire is low. The ashes show signs of burned paper, but nothing readable remains. |
| Library window | None | Rain lashes the glass. The window is closed from the inside. |

## 7.2 Edward’s Study

```text
id: edward_study
name: Edward’s Study
```

Edward’s study is smaller and more private than the library. This is where he kept business papers, personal correspondence, and drafts of legal documents.

### Function

Will clue and appointment clue.

### Inspectable Areas

| Area | Clue | Result |
|---|---|---|
| Wastebasket | `torn_will_note` | A torn note mentions a planned change to the will and Clara’s name. |
| Writing desk | `final_appointment_note` | A short note reads: “H. after dinner. No more delays.” |
| Correspondence box | None | The box contains business letters and old publishing contracts. |
| Bookshelf | None | Several legal volumes have been recently disturbed. |
| Locked drawer | None | The drawer is locked. It may require a key or later clue. |

## 7.3 Beatrice’s Room

```text
id: beatrice_room
name: Beatrice’s Room
```

Beatrice’s room is elegant but disordered. A perfume bottle lies open on the dressing table, gloves are tossed onto a chair, and several torn pieces of stationery are hidden beneath a folded shawl.

### Function

Reveals the affair and creates Beatrice’s red herring motive.

### Inspectable Areas

| Area | Clue | Result |
|---|---|---|
| Writing box | `beatrice_letters` | Several furious letters to Edward reveal Beatrice’s rejected affair. |
| Dressing table | None | Perfume, gloves, and jewelry are arranged hastily. |
| Fireplace | None | Some paper ash remains, but nothing readable. |
| Wardrobe | None | A dark shawl is missing from its hook. |
| Bedside table | None | A handkerchief is damp, as if someone had been crying. |

## 7.4 Garden Path

```text
id: garden_path
name: Garden Path
```

The garden path runs along the side of the manor, beneath the library windows. Rain has softened the gravel and mud.

### Function

Julian timeline clue.

### Inspectable Areas

| Area | Clue | Result |
|---|---|---|
| Stone path | `broken_watch` | Julian’s broken pocket watch lies near the path, stopped around 9:20. |
| Library window exterior | None | The mud beneath the window is disturbed, but the window itself appears closed. |
| Stone bench | None | Rainwater gathers on the bench. Someone may have stood here recently. |
| Rose bushes | None | The branches are wet and torn by the storm. |
| Side door | None | The side door leads back into the corridor near the library. |

## 7.5 Henry’s Study

```text
id: henry_study
name: Henry’s Study
```

Henry’s study is tidy, cold, and almost unnervingly precise. Medical books are stacked in perfect order. A locked drawer sits beneath the writing desk, and Henry’s black medical bag rests near the chair.

### Function

True method and true motive.

### Inspectable Areas

| Area | Clue | Result |
|---|---|---|
| Medical bag | `medical_vial` | A small vial with a scratched label contains a strong sedative/cardiac medicine. |
| Locked drawer | `altered_death_certificate` | An old death certificate shows signs of alteration in Henry’s handwriting. |
| Medical books | None | The books are carefully arranged, with a volume on cardiac failure recently moved. |
| Writing desk | None | Henry’s notes are precise and difficult to read. |
| Wastepaper basket | None | Torn scraps mention dosage calculations, but not enough to prove anything alone. |

---

# 8. Murder-Night Timeline

The murder happens around **9:28 PM**. The body is discovered around **9:50 PM**.

| Time | Location | Event |
|---|---|---|
| 7:30 PM | Dining Room | Dinner begins; tensions are visible. |
| 8:05 PM | Dining Room / Corridor | Clara argues with Edward about the will. |
| 8:20 PM | Conservatory / Corridor | Edward rejects Beatrice again. |
| 8:40 PM | Edward’s Study | Edward hints that he will confront Henry. |
| 9:00 PM | Dining Room | Dinner ends; Edward goes to the library. |
| 9:05 PM | Library | Julian argues with Edward. |
| 9:15 PM | Garden Path | Julian goes outside and breaks his watch. |
| 9:18 PM | Corridor near Library | Beatrice approaches the library, then retreats. |
| 9:22 PM | Library | Henry enters and drugs Edward’s brandy. |
| 9:28 PM | Library | Henry kills Edward and stages the scene. |
| 9:35 PM | Henry’s Study | Henry hides or guards old medical documents. |
| 9:45 PM | Library Corridor | Clara approaches the library and panics. |
| 9:50 PM | Library | Body is discovered. |

## Suspect Alibi Summary

### Clara Vale

Claimed location: drawing room / writing letters.

Truth: she later passed near the library and panicked.

Suspicious because of inheritance motive, letter opener, and proximity to body.

Innocent because she arrived after Henry had already killed Edward.

### Julian Blackwood

Claimed location: garden path after argument.

Truth: mostly true. He stormed out and broke his watch.

Suspicious because he fought with Edward and threatened him.

Innocent because Edward was alive when Julian left; his anger is real but not the murder method.

### Beatrice Ashford

Claimed location: her room, feeling unwell.

Truth: she came downstairs and approached the library but did not enter.

Suspicious because she was a furious rejected lover.

Innocent because she lost courage and retreated; she may have seen or heard something useful.

### Dr. Henry Ashford

Claimed location: his study.

Truth: he entered the library around 9:22 and killed Edward.

Suspicious because of the medical vial, glass residue, old death certificate, and appointment note.

Guilty because only he has motive, method, opportunity, and reason to stage the scene.

---

# 9. Final Accusation Logic

The final accusation should test whether the player has understood the whole chain of explanation.

The player should identify:

1. the culprit,
2. the motive,
3. the method,
4. the supporting evidence.

## MVP Version

The MVP accusation screen will use dropdowns and multiselect options.

### Culprit Options

- Clara Vale
- Julian Blackwood
- Beatrice Ashford
- Dr. Henry Ashford

Correct answer:

- Dr. Henry Ashford

### Motive Options

- Inheritance
- Romantic rejection
- Jealousy over affair
- Old family grudge
- Exposure of hidden medical crime

Correct answer:

- Exposure of hidden medical crime

### Method Options

- Stabbed in sudden anger with the letter opener
- Poisoned/drugged through the brandy, then staged with the letter opener
- Shot with a hidden revolver
- Pushed from the library window
- Killed during a physical fight

Correct answer:

- Poisoned/drugged through the brandy, then staged with the letter opener

### Required Evidence

For the full correct ending, the player must select:

- `medical_vial`
- `brandy_glass_residue`
- `altered_death_certificate`

Supporting/bonus evidence:

- `final_appointment_note`
- `letter_opener`

## Correct Solution Explanation

Dr. Henry Ashford killed Edward Blackwood.

Henry’s true motive was not jealousy over Beatrice’s affair. He already knew about the affair and was mostly indifferent to it. His real motive was self-preservation: Edward had discovered that Henry falsified medical records years earlier connected to the death of Edward’s wife, and Edward intended to expose him.

Henry met Edward in the library after dinner, under the pretext of their private appointment. He used medical drops or a sedative in Edward’s brandy to weaken him. Then he used the letter opener to stage the murder as a sudden act of passion, hoping suspicion would fall on Clara, Julian, or Beatrice.

The key evidence is the medical vial, the residue on the brandy glass, and the altered death certificate. The appointment note confirms Edward planned to confront “H.” after dinner.

## Partial Feedback Examples

### Correct Culprit, Wrong Motive

Example: `Henry + jealousy`

> You identified Henry, but for the wrong reason. The affair was a distraction. Henry knew about Beatrice and Edward, but his real fear was exposure of the old medical cover-up.

### Correct Culprit, Weak Method

Example: `Henry + letter opener only`

> You identified Henry, but missed the medical method. The letter opener was part of the staging; the brandy residue and medical vial reveal that Edward was weakened first.

### Clara Red Herring

Example: `Clara + inheritance + letter opener`

> Clara had motive and the letter opener points toward her, but the medical evidence does not fit her. The letter opener was used to mislead you.

### Beatrice Red Herring

Example: `Beatrice + romantic rejection + letters`

> Beatrice had emotional motive and lied about the affair, but the letters show desperation, not the method. She had no connection to the medical evidence.

### Julian Red Herring

Example: `Julian + old grudge + argument`

> Julian’s anger was real, but his broken watch supports that he left the library after the argument. His motive was emotional, but the method points elsewhere.

## Stretch Goal: Free-Form Accusation

In a more advanced version, the player writes the accusation in free text.

Example:

```text
I accuse Dr. Henry Ashford. He killed Edward because Edward had discovered his old medical cover-up and was going to expose him. Henry used medicine in Edward’s brandy to weaken him, then used the letter opener to stage the scene and point suspicion toward Clara.
```

Then an LLM evaluates whether the explanation contains the required components:

- correct culprit,
- correct motive,
- correct method,
- correct evidence,
- explanation of red herrings.

The LLM would return structured JSON:

```json
{
  "culprit_correct": true,
  "motive_correct": true,
  "method_correct": true,
  "evidence_correct": true,
  "red_herring_understanding": true,
  "score": 5,
  "feedback": "Correct. You identified Henry’s true motive and explained how he staged the crime."
}
```

This is a stretch goal, not required for the MVP.

---

# 10. Clue Discovery and Evidence Confrontation Mechanics

The player should not receive clues automatically. They discover them by exploring locations and inspecting objects.

The game distinguishes between two different clue states:

1. **Discovered by the player**  
   The player has found the clue while inspecting a location. The clue appears in the player’s case notes and can be used in the final accusation.

2. **Revealed to a suspect / used in confrontation**  
   The player explicitly brings up the clue during an interview with a suspect. Only then should the suspect react directly to that evidence.

This distinction is important because a suspect should not automatically know which clues the player has found. For example, if the player discovers Beatrice’s letters, Beatrice should not react to them unless the player confronts her with the letters.

## MVP Clue Discovery Version

The MVP will use generated location images plus clickable inspection buttons.

Example:

```text
Location: Library

[Generated image of library]

What do you want to inspect?

[Brandy glass]
[Silver letter opener]
[Fireplace]
[Edward’s desk]
[Library window]
```

If the player clicks **Brandy glass**, the app reveals:

```text
You found a clue: Residue on the Brandy Glass
```

If the player clicks **Fireplace**, the app may say:

```text
The ashes are cold. Nothing useful remains here.
```

## Discovery Loop

```text
Player chooses "Examine Location"
        ↓
Player selects location
        ↓
App displays generated location image
        ↓
App shows inspectable areas / objects
        ↓
Player clicks an object
        ↓
If object contains a clue:
    reveal clue
    mark clue as discovered
    add clue to case notes
Else:
    show descriptive text
```

## Evidence Confrontation Loop

During an interview, the player may ask a free-form question and optionally select a discovered clue to confront the suspect with.

Example:

```text
Suspect: Beatrice Ashford
Selected evidence: Beatrice’s Furious Letters

Player question:
“I found your letters to Edward. You seemed furious that he ended the affair. Did you kill him?”
```

The game then records that `beatrice_letters` were revealed to `beatrice_ashford`.

The NPC response should depend on:

- the suspect’s personality,
- the suspect’s private knowledge,
- the suspect’s lies and secrets,
- the player’s question,
- the clue explicitly used in confrontation,
- whether a single-clue or combo evidence reaction applies,
- previous dialogue,
- relevant retrieved FAISS/RAG context,
- consistency rules.

## Updated Combined Loop

```text
Player chooses "Examine Location"
        ↓
Player discovers clue
        ↓
Clue is added to case notes
        ↓
Player later interviews suspect
        ↓
Player asks free-form question
        ↓
Player optionally selects discovered clue as confronted evidence
        ↓
Game engine validates whether this clue can confront this suspect
        ↓
Game checks whether a single-clue or combo evidence reaction applies
        ↓
LangGraph interview workflow begins
        ↓
LangGraph nodes handle:
- evidence validation
- interview context construction
- FAISS/RAG retrieval
- prompt building
- NPC response generation
- consistency checking
- dialogue recording
        ↓
Dialogue history and game state are updated
```

## Case Notes

Whenever a clue is discovered, it appears in the player’s case notes.

Example:

```text
Discovered Evidence:

- Residue on the Brandy Glass
- Silver Letter Opener
- Beatrice’s Furious Letters
```

The final accusation evidence selection should only show discovered clues.

## Game State Implication

The game state should track both discovered clues and confronted clues.

Example:

```json
{
  "discovered_clues": [
    "beatrice_letters"
  ],
  "revealed_clues": {
    "clara_vale": [],
    "julian_blackwood": [],
    "beatrice_ashford": [
      "beatrice_letters"
    ],
    "henry_ashford": []
  }
}
```

This allows the game to know:

- the player has found Beatrice’s letters,
- Beatrice has been confronted with the letters,
- Henry has not yet been confronted with the letters.

## Stretch Goal: Point-and-Click Hotspots

A more advanced version would allow the player to click directly on objects inside the generated image.

Example:

```text
Player clicks the brandy glass in the room image
        ↓
Hotspot detects selected area
        ↓
Clue is revealed
```

This would require one of:

- image coordinate tracking,
- custom Streamlit component,
- HTML/JavaScript image map,
- a separate frontend.

This is a stretch goal because it would make the game feel more like a classic point-and-click adventure, but it is not required for the MVP.

---

# 11. FAISS / RAG Design

FAISS-based retrieval is part of the MVP, not a stretch goal.

The retrieval system will help ground NPC responses by retrieving relevant context from:

- clue descriptions,
- character memories,
- timeline facts,
- previous dialogue,
- suspect-specific knowledge.

However, retrieved context must be filtered by game state. The LLM should not automatically receive every clue or the full solution.

During an interview, the prompt should distinguish between:

```text
NPC private knowledge
Player-discovered clues
Clues explicitly used to confront this NPC
Relevant retrieved context
```

This prevents the LLM from spoiling the mystery while still allowing richer, context-aware NPC dialogue.

## RAG Flow During Interviews

```text
Player asks question
        ↓
Optional confronted evidence selected
        ↓
LangGraph workflow receives interview input
        ↓
Evidence validation node checks:
- selected suspect
- player question
- confronted clue
- whether clue was discovered
- whether clue can confront this suspect
        ↓
Game State Manager provides:
- discovered clues
- clues revealed to this suspect
- previous dialogue
- current game status
        ↓
FAISS retriever searches relevant context:
- clue descriptions
- suspect knowledge
- timeline facts
- location details
- previous dialogue
        ↓
Retrieved context is filtered by:
- current suspect
- discovered clues
- confronted evidence
- game state
        ↓
Prompt Builder combines:
- suspect profile
- suspect private knowledge
- allowed retrieved context
- player question
- confronted evidence
- evidence reaction guidance
        ↓
LLM generates NPC response
        ↓
Consistency checker validates response
        ↓
Dialogue is recorded in GameState
```

---

# 12. LangGraph Interview Orchestration

LangGraph is part of the MVP.

The project will use LangGraph to orchestrate the suspect interview workflow. This is appropriate because each interview is not a single isolated LLM call. It is a multi-step stateful process involving validation, game state, retrieval, prompting, response generation, consistency checking, and dialogue recording.

## Why LangGraph Fits This Project

The interview system requires several steps:

```text
Player interview input
        ↓
Validate evidence
        ↓
Build interview context
        ↓
Retrieve FAISS/RAG context
        ↓
Build NPC prompt
        ↓
Generate NPC response
        ↓
Check consistency
        ↓
Record dialogue in GameState
        ↓
Return response to Streamlit
```

LangGraph gives this process a clear structure. Each step can be represented as a node, and the interview state can be passed through the graph.

## Planned LangGraph Nodes

```text
validate_evidence_node
build_context_node
retrieve_context_node
build_prompt_node
generate_response_node
consistency_check_node
record_dialogue_node
```

## LangGraph State

The LangGraph interview state should contain:

```text
game_state
game_data
suspect_id
player_question
confronted_clue_id
interview_context
retrieved_context
messages
npc_response
consistency_result
error
```

## Relationship to the Core Game Engine

LangGraph will not replace the core game engine.

Instead, LangGraph will orchestrate calls to existing Python functions such as:

```text
can_confront_suspect_with_clue()
build_interview_context()
build_npc_messages()
record_interview_exchange()
```

The deterministic game rules remain in Python. LangGraph coordinates the flow of the interview pipeline.

## MVP Role

LangGraph is required for the MVP interview system because it demonstrates agentic workflow orchestration, one of the central tools learned during the bootcamp.

---

# 13. Visual Assets

The project should eventually include generated images for:

## Location Images

- Library
- Edward’s Study
- Beatrice’s Room
- Garden Path
- Henry’s Study

Optional:

- Dining Room

## Suspect Portraits

- Clara Vale
- Julian Blackwood
- Beatrice Ashford
- Dr. Henry Ashford

## Optional Evidence Images

- Torn Will Note
- Beatrice’s Furious Letters
- Julian’s Broken Watch
- Small Medical Vial
- Brandy Glass
- Silver Letter Opener
- Altered Death Certificate
- Final Appointment Note

For the MVP, location and suspect images are enough. Evidence images are optional polish.

---

# 14. Phase 1 Summary

Phase 1 produced the complete mystery design.

We now have:

- original case premise,
- central motive web,
- true culprit and motive,
- four suspects,
- eight clues,
- five locations,
- inspectable areas,
- clue discovery mechanic,
- distinction between discovered clues and confronted evidence,
- single-clue and combo evidence reaction design,
- FAISS/RAG as a core MVP component,
- LangGraph interview orchestration as a core MVP component,
- timeline,
- final accusation logic,
- MVP and stretch goals.

The next phase is to translate this design into structured JSON files.

---

# 15. Updated Development Roadmap

## Phase 2 — Write Structured JSON Files

Planned files:

```text
data/mystery_case.json
data/characters.json
data/clues.json
data/locations.json
data/solution.json
```

Status:

```text
✅ Completed
```

## Phase 3 — Core Game Engine

Purpose:

Build the deterministic game logic before adding LLM behavior.

Includes:

```text
data loading utilities
GameState structure
location inspection logic
clue discovery logic
evidence confrontation logic
combo evidence reaction logic
final accusation checking
terminal smoke test
```

Status:

```text
✅ Completed
```

## Phase 4 — Prompt Builder and NPC Dialogue Layer

Purpose:

Prepare structured prompts for NPC interviews.

Includes:

```text
format suspect profile
format evidence reaction guidance
format confronted clue
format dialogue history
build system and user messages
test prompt construction from terminal
```

Status:

```text
➡️ Current / Next
```

## Phase 5 — FAISS / RAG Retrieval

Purpose:

Build a vector retrieval layer for case context.

Includes:

```text
create retrievable documents from JSON data
embed clue, character, location, and timeline facts
build FAISS index
retrieve relevant context during interviews
filter retrieved context by game state
```

## Phase 6 — LangGraph Interview Workflow

Purpose:

Use LangGraph to orchestrate the NPC interview pipeline.

Includes:

```text
define LangGraph interview state
create validation node
create context-building node
create RAG retrieval node
create prompt-building node
create NPC response node
create consistency-check node
create dialogue-recording node
test graph from terminal
```

## Phase 7 — LLM Integration

Purpose:

Connect the prompt and graph workflow to an actual LLM.

Includes:

```text
model selection
LLM call wrapper
mock/fallback response mode
NPC response generation
error handling
```

## Phase 8 — Streamlit Interface

Purpose:

Create the playable app interface.

Includes:

```text
case introduction
location exploration
clue discovery
case notes
suspect interviews
evidence confrontation selector
final accusation screen
ending / feedback screen
```

## Phase 9 — Logging, Pandas Analysis, and Visualizations

Purpose:

Demonstrate data analysis and reflection on player interactions.

Includes:

```text
log inspections, interviews, clue discoveries, and accusations
load logs into Pandas
analyze clue discovery patterns
analyze suspect interview frequency
visualize evidence usage
visualize accusation attempts
```

## Phase 10 — README, Ethics, and Demo Polish

Purpose:

Prepare the project for submission.

Includes:

```text
README
setup instructions
architecture explanation
tooling explanation
ethical reflection
limitations
future directions
demo screenshots
```

Future directions should mention MCP as a possible extension, not as part of the MVP.
