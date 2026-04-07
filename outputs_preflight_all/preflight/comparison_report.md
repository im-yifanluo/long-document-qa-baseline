# Comparison Report

Run tier: `preflight`

## Score Summary

| Task | Metric | vanilla_rag | dos_rag | raptor | dos_rag_minus_vanilla_rag |
| --- | --- | --- | --- | --- | --- |
| gov_report | rouge | 14.3736 | 23.1876 | 22.6258 | +8.8140 |
| summ_screen_fd | rouge | 14.8470 | 16.3796 | 19.3173 | +1.5326 |
| qmsum | rouge | 0.0000 | 5.6369 | 0.0000 | +5.6369 |
| qasper | f1 | 100.0000 | 100.0000 | 46.1538 | +0.0000 |
| narrative_qa | f1 | 80.0000 | 40.0000 | 0.0000 | -40.0000 |
| quality | exact_match | 0.0000 | 100.0000 | 100.0000 | +100.0000 |
| contract_nli | exact_match | 100.0000 | 100.0000 | 100.0000 | +0.0000 |

## Example Previews

### gov_report

- examples: 1
- disagreements: 1
- any-positive-score: 1

#### gov_report / crs_RS21048

- query: Summarize the report.
- references: Special Operations Forces (SOF) play a significant role in U.S. military operations and, in recent years, have been given greater responsibility for planning and conducting worldwide counterterrorism operations. U.S. Special Operations Command (USSOCOM) has about 70,000 Active Duty, National Guard, and reserve personnel from all four services and Department of Defense (DOD) civilians assigned to…
- best_methods: dos_rag
- disagreement: True
- vanilla_rag score: 14.3736
  prediction: The document outlines two congressionally mandated reviews of the United States Special Operations Command (USSOCOM) and its Special Operations Forces (SOF). The first review, to be conducted by the Assistant Secretary of Defense for Special Operations and Low Intensity Conflict (ASD SOLIC), must be completed within 270 days of the Act's enactment and focuses on the adequacy of SOF capabilities t…
  top_chunk: rank=1 score=0.3173 (c) DEADLINES.— (1) COMPLETION OF REVIEW.—The review required by subsection (a) shall be completed by not later than 270 days after the date of the enactment of this Act. (2) REPORT.—Not later than 30 days after completion of the review, t…
- dos_rag score: 23.1876
  prediction: The document provides an overview of the U.S. Special Operations Command (USSOCOM) and its components, detailing their roles, structures, and responsibilities. Special operations are defined as military operations requiring unique modes of employment, often conducted in hostile or politically sensitive environments. USSOCOM, established in 1986, is responsible for training, doctrine, and equippin…
  top_chunk: rank=1 score=0.3142 (c) DEADLINES.— (1) COMPLETION OF REVIEW.—The review required by subsection (a) shall be completed by not later than 270 days after the date of the enactment of this Act. (2) REPORT.—Not later than 30 days after completion of the review, t…
- raptor score: 22.6258
  prediction: The document discusses the structure, roles, and future of U.S. Special Operations Forces (SOF) and the U.S. Special Operations Command (USSOCOM). Key points include: 1. **Structure and Components**: USSOCOM oversees four main components: Army Special Operations Command (USASOC), Naval Special Warfare Command (NSWC), Air Force Special Operations Command (AFSOC), and Marine Corps Forces Special Op…
  top_chunk: rank=1 score=n/a SOF will be undertaken, potentially resulting in a number of changes for ASD SOLIC, USSOCOM, and U S SOF

### summ_screen_fd

- examples: 1
- disagreements: 1
- any-positive-score: 1

#### summ_screen_fd / fd_FRIENDS_05x03

- query: Summarize the episode.
- references: Feeling guilty over Phoebe missing out on London, the gang plan a weekend trip to Atlantic City, but just as they are about to leave, Phoebe's water breaks and they head to the hospital. In an attempt to get over Ross, Rachel asks out two male nurses for her and Monica. This causes friction between Monica and Chandler, with Chandler reacting as if he does not care. In the delivery room, Phoebe fr…
- best_methods: raptor
- disagreement: True
- vanilla_rag score: 14.8470
  prediction: The document is a script excerpt from an episode of the TV show Friends, focusing on Phoebe's childbirth and Joey's kidney stone ordeal. The episode intertwines several storylines: 1. **Phoebe's Childbirth:** - Phoebe is in labor and is coached by her husband Frank and her sister Alice, who is delayed due to a phone call. - Phoebe's doctor, Dr. Harad, is a big fan of the TV show "Happy Days" and…
  top_chunk: rank=1 score=0.3240 Up, up is not an option--what's a urethra? (Monica whispers what it is in his ear.) Are you crazy?! [Scene: The delivery room, Rachel and Frank are there.] Phoebe: (To Rachel) So did you ask him? Rachel: No, I haven't had a chance to be al…
- dos_rag score: 16.3796
  prediction: The document is a script excerpt from an episode of the TV show "Friends," focusing on Phoebe's experience of giving birth to triplets for her brother Frank and his wife Alice. The episode begins with Phoebe arriving at the hospital with her friends Ross, Joey, and Rachel, where she meets a nurse and expresses her nervousness about the pain of labor. The nurse informs her that her doctor is unava…
  top_chunk: rank=1 score=0.3453 Phoebe: You're right. (There's an awkward silence then suddenly Phoebe gets an idea.) Phoebe: Tell him it's for you. [Scene: Joey's room, his doctor, Chandler, and Monica are there.] Monica: Feeling a little better sweetie? Joey: Well, may…
- raptor score: 19.3173
  prediction: The document describes a series of events taking place in a hospital where Phoebe is about to give birth to triplets for her friends Frank and Alice. The main characters, including Phoebe, Ross, Rachel, Monica, Chandler, and Joey, are present in the delivery room and waiting room. Phoebe's doctor, Dr. Harad, refers to himself as "Fonzie," which causes confusion and amusement among the characters.…
  top_chunk: rank=1 score=n/a I'll be back in a minute to do your internal, in the meantime, just relax because everything here looks great And also, I love Fonzie (Exits) Chandler: Did he just say, he loves Fonzie Monica: That's what it sounded like Chandler: All righ…

### qmsum

- examples: 1
- disagreements: 1
- any-positive-score: 1

#### qmsum / va-sq-1

- query: What was agreed upon on sample transcripts?
- references: To save time, speaker mn005 will only mark the sample of transcribed data for regions of overlapping speech, as opposed to marking all acoustic events. The digits extraction task will be delegated to whomever is working on acoustics for the Meeting Recorder project.
- best_methods: dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Based on the provided context, it seems that the team agreed to have some ground truth first by manually marking transcripts to ensure accuracy. Specifically, Professor E mentioned that the idea of the manual marking was to confirm the accuracy of the transcriptions, saying "it's really here." Additionally, there was a forty-five minute piece transcribed by Jane that was sent to IBM for compariso…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- dos_rag score: 5.6369
  prediction: Based on the provided context, the agreed points regarding sample transcripts are: 1. A piece of forty-five minutes was transcribed by Jane and sent to IBM for comparison. 2. There is a larger piece of recorded data (about ten hours) that has been sent to IBM on CD-ROM for transcription. 3. The group aims to record three to four meetings per week, each about an hour long, to gather more data. 4.…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- raptor score: 0.0000
  prediction: Based on the provided context, the discussion around sample transcripts involved several points: 1. A forty-five minute piece transcribed by Jane was sent to IBM for comparison. 2. A larger piece was recorded and sent to IBM on CD-ROM. 3. There was a suggestion to restart recording after participants identified their channels and devices, but it was decided to continue recording. 4. There was a d…
  top_chunk: rank=1 score=n/a and in the distant mike you could

### qasper

- examples: 1
- disagreements: 1
- any-positive-score: 1

#### qasper / b6f15fb6279b82e34a5bf4828b7b5ddabfdf1d54

- query: which multilingual approaches do they compare with?
- references: BIBREF19, BIBREF20 | multilingual NMT (MNMT) BIBREF19
- best_methods: vanilla_rag, dos_rag
- disagreement: True
- vanilla_rag score: 100.0000
  prediction: multilingual NMT (MNMT) BIBREF19
  top_chunk: rank=1 score=0.4322 The results show that our approaches consistently outperform other approaches across languages and datasets, especially surpass pivoting, which is a strong baseline in the zero-shot scenario that multilingual NMT systems often fail to beat…
- dos_rag score: 100.0000
  prediction: multilingual NMT (MNMT) BIBREF19
  top_chunk: rank=1 score=0.4322 MLM+BRLM-SA performs the best, and is better than MLM+BRLM-HA indicating that soft alignment is helpful than hard alignment for the cross-lingual pretraining. Experiments ::: Main Results ::: Results on MultiUN Dataset. Like experimental r…
- raptor score: 46.1538
  prediction: pivoting, multilingual NMT (MNMT), and cross-lingual transfer without pretraining
  top_chunk: rank=1 score=n/a , Arabic (source) sentence is translated to English (pivot) first which is later translated to Spanish (target) BIBREF4, BIBREF5 However, the pivot-based method requires doubled decoding time and suffers from the propagation of translation…

### narrative_qa

- examples: 1
- disagreements: 1
- any-positive-score: 1

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_0

- query: Which character comes from Bangor, Maine?
- references: Miranda Hope.
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 80.0000
  prediction: Miss Miranda Hope
  top_chunk: rank=1 score=0.4464 I wonder if she doesn't think me refined--or if she had ever heard anything against Bangor? I can't think it is that. Don't you remember when Clara Barnard went to visit New York, three years ago, how much attention she received? And you k…
- dos_rag score: 40.0000
  prediction: Miss Miranda Mope
  top_chunk: rank=1 score=0.4903 I tell Miss Vane that at Bangor we think such ideas vulgar; but then she looks as though she had never heard of Bangor. I often want to shake her, though she _is_ so sweet. If she isn't angry with the people who make her feel that way, I a…
- raptor score: 0.0000
  prediction: a young woman from the State of Maine, in the province of New England
  top_chunk: rank=1 score=n/a I never supposed, when I left Bangor, that I was coming to Europe to learn _English_ If I do learn it, I don't think you will understand me when I get back, and I don't think you'll like it much I should be a good deal criticised if I spok…

### quality

- examples: 1
- disagreements: 1
- any-positive-score: 1

#### quality / 52845_75VB1ISR_1

- query: How much time has passed between Blake's night with Eldoria and his search for Sabrina York in his mind-world? (A) 7 years (B) 10 hours (C) 12 years (D) 1 hour
- references: 10 hours
- best_methods: dos_rag, raptor
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: 12 years
  top_chunk: rank=1 score=0.4728 It was a remarkably detailed materialization, and his quarry's footprints stood out clearly in the duplicated sand. Sabrina York did not even know the rudiments of the art of throwing off a mind-tracker. It would have done her but little g…
- dos_rag score: 100.0000
  prediction: 10 hours
  top_chunk: rank=1 score=0.4728 It was a remarkably detailed materialization, and his quarry's footprints stood out clearly in the duplicated sand. Sabrina York did not even know the rudiments of the art of throwing off a mind-tracker. It would have done her but little g…
- raptor score: 100.0000
  prediction: 10 hours
  top_chunk: rank=1 score=n/a Sabrina York did not even know the rudiments of the art of throwing off a mind-tracker It would have done her but little good if she had, for twelve years as a psycheye had taught Blake all the tricks Probably she had taken it for granted…

### contract_nli

- examples: 1
- disagreements: 0
- any-positive-score: 1

#### contract_nli / 3_nda-11

- query: Receiving Party shall not reverse engineer any objects which embody Disclosing Party's Confidential Information.
- references: Entailment
- best_methods: vanilla_rag, dos_rag, raptor
- disagreement: False
- vanilla_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5490 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
- dos_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5557 d) Not to use the Confidential Information for their own commercial use or for that of any other person or party, without prior written consent by the Disclosing Party; e) Not to make copies of the Confidential Information in any format wi…
- raptor score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=n/a d) Not to use the Confidential Information for their own commercial use or for that of any other person or party, without prior written consent by the Disclosing Party; e) Not to make copies of the Confidential Information in any format wi…
