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
➡️ Next Phase — Phase 2: Write structured JSON files
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
- discovered clues,
- dialogue history,
- current game state,
- consistency rules.

The larger product idea is a prototype for future RPGs where NPCs can hold more natural conversations with players while the story remains coherent and controlled.

---

# 2. Plot Source Decision

We considered whether to use existing online mystery stories, public-domain detective fiction, or an API/source of mystery plots.

## Decision

For the MVP, the playable case will be **original**, created by us.

Public-domain mystery stories may be used only as inspiration or later as a possible corpus for analysis, but the actual game case will use original characters, clues, locations, and solution.

## Reason

This avoids copyright problems and gives full control over the mystery structure, NPC knowledge boundaries, clues, and final accusation logic.

---

# 3. Case Premise

## Case Title

**Murder at Blackwood Manor**

## Setting

A 1930s English country house during a stormy evening.

## Victim

**Edward Blackwood**

A wealthy publisher and family patriarch. He is intelligent, controlling, cruel, and surrounded by people who have reasons to hate or fear him.

## Crime

Edward Blackwood is found murdered in his private library after dinner.

At first, the murder appears connected to inheritance, family resentment, or a romantic scandal. The true motive is deeper: Edward had discovered a hidden medical crime committed years earlier by Dr. Henry Ashford and intended to expose him.

---

# 4. Motive Web

A central design decision is that the mystery should not have a single obvious motive. Several suspects should have plausible reasons to kill Edward.

The final accusation should be cumulative, not just “who did it.”

The player must understand:

- who killed Edward,
- why they killed him,
- how they did it,
- what evidence proves it,
- which motives were misleading.

## Motive Matrix

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

Edward had discovered that Henry falsified medical records years earlier connected to the death of Edward’s wife. Henry’s negligence, or possibly intentional overmedication, contributed to her death, and he covered it up.

Edward planned to expose him.

Henry killed Edward to protect himself.

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

### What Clara Reveals if Confronted

If the player finds evidence about the will or forged letter, Clara admits she tried to secure her inheritance dishonestly, but insists she did not kill Edward.

Possible line:

> “Yes, I was afraid he would cut me out. Yes, I did something foolish with the letter. But Edward was alive when I last saw him.”

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

This makes him look dangerous, but not necessarily calculating enough for the murder.

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

### What Julian Reveals if Confronted

If the player confronts him with evidence of the argument, Julian admits he threatened Edward but denies killing him.

Possible line:

> “I said I wished him dead. I won’t deny it. But wishing is not doing. When I left that room, he was alive.”

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

Her letters make her look unstable enough to commit the crime.

### Real Secret

Beatrice was Edward’s lover, and she was devastated when he ended the affair.

However, she did not kill him. She lies because she wants to hide the affair and protect her reputation.

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

### What Beatrice Reveals if Confronted

If the player finds her letters, she admits the affair and the breakup, but insists her anger was emotional, not murderous.

Possible line:

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

Edward planned to expose him.

Henry killed Edward to protect himself.

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

### What Henry Reveals if Confronted

Henry should never confess easily.

If confronted with weak evidence, he deflects:

> “You are mistaking melodrama for proof. This house is full of motives. That does not make any of them evidence.”

If confronted with stronger evidence, such as the medical vial and altered death certificate, he becomes colder:

> “Edward always had a talent for opening graves that should have remained closed.”

Only near the end, if the accusation is correct, he can admit the truth indirectly or after the ending is triggered.

---

# 6. Clues

The clue system should contain both red herrings and solution clues.

## 6.1 Torn Will Note

```text
id: torn_will_note
name: Torn Will Note
location: Edward’s Study
related_suspect: Clara Vale
type: Red herring / inheritance motive
```

### Description

A torn handwritten note is found in Edward’s study. It appears to mention a planned change to the will and includes Clara’s name.

### What it Suggests

Clara may have killed Edward to prevent him from cutting her out of the inheritance.

### What it Actually Means

Clara was desperate about the inheritance and may have tried to manipulate Edward, but this does not prove murder.

### Dialogue Use

If the player confronts Clara with this clue, she becomes defensive and may admit she was afraid of losing her inheritance.

---

## 6.2 Beatrice’s Furious Letters

```text
id: beatrice_letters
name: Beatrice’s Furious Letters
location: Beatrice’s Room
related_suspect: Beatrice Ashford
type: Red herring / romantic motive
```

### Description

A bundle of unsent or returned letters from Beatrice to Edward. They are emotional, bitter, and desperate. She refuses to accept that Edward ended their affair.

### What it Suggests

Beatrice may have killed Edward because he rejected her.

### What it Actually Means

Beatrice was emotionally devastated and lied about the affair, but she did not kill Edward.

### Dialogue Use

If confronted, Beatrice admits the affair and reveals that Henry knew about it but seemed strangely indifferent.

This clue should unlock an important Henry-related insight:

```text
Henry was not truly jealous.
```

---

## 6.3 Julian’s Broken Watch

```text
id: broken_watch
name: Julian’s Broken Watch
location: Garden Path
related_suspect: Julian Blackwood
type: Red herring / timeline clue
```

### Description

Julian’s pocket watch is found near the garden path, cracked and stopped at 9:20.

### What it Suggests

Julian was outside around the time of the murder and may be lying about his movements.

### What it Actually Means

Julian did go outside after arguing with Edward. The broken watch supports that part of his story rather than disproving it.

### Dialogue Use

If confronted, Julian admits he stormed out after the argument. He says he threw the watch against the stone path in anger.

---

## 6.4 Small Medical Vial

```text
id: medical_vial
name: Small Medical Vial
location: Henry’s Medical Bag
related_suspect: Dr. Henry Ashford
type: Solution clue
```

### Description

A small vial is found in Henry’s medical bag. Its label is partially scratched off. It contains a sedative or cardiac medication that could weaken a person quickly if mixed into a drink.

### What it Suggests

Henry had access to a substance that could incapacitate Edward.

### What it Actually Means

This is one of the key clues pointing toward Henry’s method.

### Dialogue Use

If confronted weakly, Henry dismisses it as ordinary medicine. If confronted together with the brandy glass residue, it becomes much more incriminating.

---

## 6.5 Brandy Glass Residue

```text
id: brandy_glass_residue
name: Residue on the Brandy Glass
location: Library
related_suspect: Dr. Henry Ashford
type: Solution clue / method clue
```

### Description

A faint bitter-smelling residue is found at the bottom of Edward’s brandy glass. The glass appears to have been wiped, but not thoroughly.

### What it Suggests

Edward may have been drugged before he was killed.

### What it Actually Means

Henry weakened Edward with medication before staging the murder.

### Dialogue Use

This clue supports the method. It becomes especially powerful when combined with the medical vial.

---

## 6.6 Silver Letter Opener

```text
id: letter_opener
name: Silver Letter Opener
location: Library
related_suspect: Clara Vale / staged evidence
type: Misleading weapon clue
```

### Description

A silver letter opener is found near Edward’s desk. It appears to be the murder weapon. It belongs to Clara, or at least was recently used by her.

### What it Suggests

Clara may have killed Edward with an object connected to her.

### What it Actually Means

Henry used or planted the letter opener to redirect suspicion toward Clara and the inheritance dispute.

### Dialogue Use

Clara panics when confronted because the letter opener is connected to her, but she insists she did not bring it to the library that night.

This clue becomes solution-relevant if the player realizes it was planted.

---

## 6.7 Altered Death Certificate

```text
id: altered_death_certificate
name: Altered Death Certificate
location: Locked Drawer in Henry’s Study
related_suspect: Dr. Henry Ashford
type: Deep solution clue / true motive
```

### Description

An old death certificate related to Edward’s late wife shows signs of alteration. The handwriting resembles Henry’s medical hand, and dates or dosages appear inconsistent.

### What it Suggests

Henry was involved in falsifying records related to a death years earlier.

### What it Actually Means

This is the deepest clue. Edward had discovered Henry’s old medical cover-up and intended to expose him.

### Dialogue Use

Henry should not casually explain this away. If confronted, he becomes colder and more evasive.

This clue supports the true motive:

```text
Edward knew about Henry’s old crime.
```

---

## 6.8 Edward’s Final Appointment Note

```text
id: final_appointment_note
name: Edward’s Final Appointment Note
location: Edward’s Desk
related_suspect: Dr. Henry Ashford
type: Solution clue / confrontation clue
```

### Description

A note in Edward’s handwriting reads:

> “H. after dinner. No more delays.”

At first, “H.” could refer to Henry, but it is not immediately obvious.

### What it Suggests

Edward planned to confront someone after dinner.

### What it Actually Means

Edward had arranged to confront Henry about the old medical records.

### Dialogue Use

This clue becomes meaningful once the player has found the altered death certificate or questioned Henry about the old medical documents.

---

## Clue Summary Table

| Clue | Points Toward | Function |
|---|---|---|
| Torn Will Note | Clara | Inheritance red herring |
| Beatrice’s Furious Letters | Beatrice | Romantic red herring |
| Julian’s Broken Watch | Julian | Old grudge/timeline clue |
| Medical Vial | Henry | Method clue |
| Brandy Glass Residue | Henry | Poison/drugging clue |
| Silver Letter Opener | Clara / Henry | Staged weapon clue |
| Altered Death Certificate | Henry | True motive clue |
| Final Appointment Note | Henry | Confrontation clue |

---

# 7. Locations

For the MVP, all locations are visible from the start, and all inspectable areas can be clicked from the start.

Locked/unlocked clue progression may be added later as a stretch goal.

## 7.1 Library

```text
id: library
name: The Library
```

### Description

Edward Blackwood’s private library is the murder scene. It is a dark, wood-paneled room lined with bookshelves, legal documents, and locked cabinets. A large desk sits near the fireplace. The storm outside rattles the windows, and the room still smells faintly of brandy and smoke.

### Function in the Mystery

The library is the central crime scene. It contains clues about the method and the staging of the murder.

### Clues Found Here

- brandy_glass_residue
- letter_opener

### Inspectable Areas

| Area | Clue | Result |
|---|---|---|
| Brandy glass | brandy_glass_residue | A faint bitter residue remains at the bottom of the glass. |
| Silver letter opener | letter_opener | A silver letter opener lies near the desk. It appears recently handled. |
| Edward’s desk | None | Papers are scattered across the desk, but nothing here seems decisive. |
| Fireplace | None | The fire is low. The ashes show signs of burned paper, but nothing readable remains. |
| Library window | None | Rain lashes the glass. The window is closed from the inside. |

---

## 7.2 Edward’s Study

```text
id: edward_study
name: Edward’s Study
```

### Description

Edward’s study is smaller and more private than the library. This is where he kept business papers, personal correspondence, and drafts of legal documents. Unlike the grand library, this room feels cramped, secretive, and practical.

### Function in the Mystery

This location reveals Edward’s private plans before his death: the will, the confrontation note, and possibly his investigation into Henry.

### Clues Found Here

- torn_will_note
- final_appointment_note

### Inspectable Areas

| Area | Clue | Result |
|---|---|---|
| Wastebasket | torn_will_note | A torn note mentions a planned change to the will and Clara’s name. |
| Writing desk | final_appointment_note | A short note reads: “H. after dinner. No more delays.” |
| Correspondence box | None | The box contains business letters and old publishing contracts. |
| Bookshelf | None | Several legal volumes have been recently disturbed. |
| Locked drawer | None | The drawer is locked. It may require a key or later clue. |

---

## 7.3 Beatrice’s Room

```text
id: beatrice_room
name: Beatrice’s Room
```

### Description

Beatrice’s room is elegant but disordered. A perfume bottle lies open on the dressing table, gloves are tossed onto a chair, and several torn pieces of stationery are hidden beneath a folded shawl. The room suggests someone trying to preserve dignity while quietly falling apart.

### Function in the Mystery

This location reveals the affair between Beatrice and Edward, and makes Beatrice look emotionally capable of murder.

### Clues Found Here

- beatrice_letters

### Inspectable Areas

| Area | Clue | Result |
|---|---|---|
| Writing box | beatrice_letters | Several furious letters to Edward reveal Beatrice’s rejected affair. |
| Dressing table | None | Perfume, gloves, and jewelry are arranged hastily. |
| Fireplace | None | Some paper ash remains, but nothing readable. |
| Wardrobe | None | A dark shawl is missing from its hook. |
| Bedside table | None | A handkerchief is damp, as if someone had been crying. |

---

## 7.4 Garden Path

```text
id: garden_path
name: Garden Path
```

### Description

The garden path runs along the side of the manor, beneath the library windows. Rain has softened the gravel and mud. A stone bench sits near the rose bushes, half-hidden in the dark.

### Function in the Mystery

This location supports Julian’s story and complicates the timeline. It makes him look suspicious, but also gives evidence that he may have left the library before the murder.

### Clues Found Here

- broken_watch

### Inspectable Areas

| Area | Clue | Result |
|---|---|---|
| Stone path | broken_watch | Julian’s broken pocket watch lies near the path, stopped around 9:20. |
| Library window exterior | None | The mud beneath the window is disturbed, but the window itself appears closed. |
| Stone bench | None | Rainwater gathers on the bench. Someone may have stood here recently. |
| Rose bushes | None | The branches are wet and torn by the storm. |
| Side door | None | The side door leads back into the corridor near the library. |

---

## 7.5 Henry’s Study

```text
id: henry_study
name: Henry’s Study
```

### Description

Henry’s study is tidy, cold, and almost unnervingly precise. Medical books are stacked in perfect order. A locked drawer sits beneath the writing desk, and Henry’s black medical bag rests near the chair.

### Function in the Mystery

This is the deepest solution location. It connects Henry to both the method and the true motive.

### Clues Found Here

- medical_vial
- altered_death_certificate

### Inspectable Areas

| Area | Clue | Result |
|---|---|---|
| Medical bag | medical_vial | A small vial with a scratched label contains a strong sedative/cardiac medicine. |
| Locked drawer | altered_death_certificate | An old death certificate shows signs of alteration in Henry’s handwriting. |
| Medical books | None | The books are carefully arranged, with a volume on cardiac failure recently moved. |
| Writing desk | None | Henry’s notes are precise and difficult to read. |
| Wastepaper basket | None | Torn scraps mention dosage calculations, but not enough to prove anything alone. |

---

# 8. Murder-Night Timeline

The murder happens around **9:28 PM**.

The body is discovered around **9:50 PM**.

## Official Timeline

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

Claimed location:

- Drawing room / writing letters.

Truth:

- She later passed near the library and panicked.

Suspicious because:

- Inheritance motive,
- letter opener,
- proximity to body.

Innocent because:

- She arrived after Henry had already killed Edward.

---

### Julian Blackwood

Claimed location:

- Garden path after argument.

Truth:

- Mostly true. He stormed out and broke his watch.

Suspicious because:

- He fought with Edward and threatened him.

Innocent because:

- Edward was alive when Julian left; Julian’s anger is real but not the murder method.

---

### Beatrice Ashford

Claimed location:

- Her room, feeling unwell.

Truth:

- She came downstairs and approached the library but did not enter.

Suspicious because:

- Furious rejected lover.

Innocent because:

- She lost courage and retreated; she may have seen or heard something useful.

---

### Dr. Henry Ashford

Claimed location:

- His study.

Truth:

- He entered the library around 9:22 and killed Edward.

Suspicious because:

- Medical vial,
- glass residue,
- old death certificate,
- appointment note.

Guilty because:

- Only he has motive, method, opportunity, and reason to stage the scene.

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

- medical_vial
- brandy_glass_residue
- altered_death_certificate

Supporting/bonus evidence:

- final_appointment_note
- letter_opener

## Correct Solution Explanation

Dr. Henry Ashford killed Edward Blackwood.

Henry’s true motive was not jealousy over Beatrice’s affair. He already knew about the affair and was mostly indifferent to it. His real motive was self-preservation: Edward had discovered that Henry falsified medical records years earlier connected to the death of Edward’s wife, and Edward intended to expose him.

Henry met Edward in the library after dinner, under the pretext of their private appointment. He used medical drops or a sedative in Edward’s brandy to weaken him. Then he used the letter opener to stage the murder as a sudden act of passion, hoping suspicion would fall on Clara, Julian, or Beatrice.

The key evidence is the medical vial, the residue on the brandy glass, and the altered death certificate. The appointment note confirms Edward planned to confront “H.” after dinner.

## Partial Feedback Examples

### Correct Culprit, Wrong Motive

Example:

```text
Henry + jealousy
```

Feedback:

> You identified Henry, but for the wrong reason. The affair was a distraction. Henry knew about Beatrice and Edward, but his real fear was exposure of the old medical cover-up.

### Correct Culprit, Weak Method

Example:

```text
Henry + letter opener only
```

Feedback:

> You identified Henry, but missed the medical method. The letter opener was part of the staging; the brandy residue and medical vial reveal that Edward was weakened first.

### Clara Red Herring

Example:

```text
Clara + inheritance + letter opener
```

Feedback:

> Clara had motive and the letter opener points toward her, but the medical evidence does not fit her. The letter opener was used to mislead you.

### Beatrice Red Herring

Example:

```text
Beatrice + romantic rejection + letters
```

Feedback:

> Beatrice had emotional motive and lied about the affair, but the letters show desperation, not the method. She had no connection to the medical evidence.

### Julian Red Herring

Example:

```text
Julian + old grudge + argument
```

Feedback:

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

# 10. Clue Discovery Mechanics

The player should not receive clues automatically. They discover them by exploring locations and inspecting objects.

## MVP Version

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
    update game state
Else:
    show descriptive text
        ↓
Discovered clues become available in:
- suspect interviews
- final accusation
- case notes
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

# 11. Visual Assets

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

# 12. Phase 1 Summary

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
- timeline,
- final accusation logic,
- MVP and stretch goals.

The next phase is to translate this design into structured JSON files.

---

# 13. Next Phase

## Phase 2 — Write Structured JSON Files

Planned files:

```text
data/mystery_case.json
data/characters.json
data/clues.json
data/locations.json
data/solution.json
```

Recommended order:

```text
Step 2.1 — Fill mystery_case.json
Step 2.2 — Fill characters.json
Step 2.3 — Fill clues.json
Step 2.4 — Fill locations.json
Step 2.5 — Fill solution.json
```
