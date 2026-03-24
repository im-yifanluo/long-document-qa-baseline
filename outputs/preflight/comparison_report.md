# Comparison Report

Run tier: `preflight`

## Score Summary

| Task | Metric | vanilla_rag | dos_rag | dos_rag_minus_vanilla_rag |
| --- | --- | --- | --- | --- |
| gov_report | rouge | 15.0500 | 16.4236 | +1.3737 |
| summ_screen_fd | rouge | 14.8470 | 16.0474 | +1.2005 |
| qmsum | rouge | 0.0006 | 0.0007 | +0.0001 |
| qasper | f1 | 22.2222 | 13.3333 | -8.8889 |
| narrative_qa | f1 | 44.4444 | 33.3333 | -11.1111 |
| quality | exact_match | 0.0000 | 100.0000 | +100.0000 |
| contract_nli | exact_match | 0.0000 | 0.0000 | +0.0000 |

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
- vanilla_rag score: 15.0500
  prediction: The document outlines two congressionally mandated reviews of the United States Special Operations Command (USSOCOM) and its Special Operations Forces (SOF). The first review, to be conducted by the Assistant Secretary of Defense for Special Operations and Low Intensity Conflict (ASD SOLIC), must be completed within 270 days of the Act's enactment and focuses on the adequacy of SOF capabilities t…
  top_chunk: rank=1 score=0.3173 (c) DEADLINES.— (1) COMPLETION OF REVIEW.—The review required by subsection (a) shall be completed by not later than 270 days after the date of the enactment of this Act. (2) REPORT.—Not later than 30 days after completion of the review, t…
- dos_rag score: 16.4236
  prediction: The document provides an overview of the U.S. Special Operations Command (USSOCOM) and its components, detailing their roles, structures, and responsibilities within the U.S. military. Special operations, as defined, are unique military operations that require specialized training, equipment, and expertise, often conducted in hostile or politically sensitive environments. USSOCOM, established in…
  top_chunk: rank=1 score=0.3173 (c) DEADLINES.— (1) COMPLETION OF REVIEW.—The review required by subsection (a) shall be completed by not later than 270 days after the date of the enactment of this Act. (2) REPORT.—Not later than 30 days after completion of the review, t…

### summ_screen_fd

- examples: 1
- disagreements: 1
- any-positive-score: 1

#### summ_screen_fd / fd_FRIENDS_05x03

- query: Summarize the episode.
- references: Feeling guilty over Phoebe missing out on London, the gang plan a weekend trip to Atlantic City, but just as they are about to leave, Phoebe's water breaks and they head to the hospital. In an attempt to get over Ross, Rachel asks out two male nurses for her and Monica. This causes friction between Monica and Chandler, with Chandler reacting as if he does not care. In the delivery room, Phoebe fr…
- best_methods: dos_rag
- disagreement: True
- vanilla_rag score: 14.8470
  prediction: The document is a script excerpt from an episode of the TV show Friends, focusing on Phoebe's childbirth and Joey's kidney stone ordeal. The episode intertwines several storylines: 1. **Phoebe's Childbirth:** - Phoebe is in labor and is coached by her husband Frank and her sister Alice, who is delayed due to a phone call. - Phoebe's doctor, Dr. Harad, is a big fan of the TV show "Happy Days" and…
  top_chunk: rank=1 score=0.3240 Up, up is not an option--what's a urethra? (Monica whispers what it is in his ear.) Are you crazy?! [Scene: The delivery room, Rachel and Frank are there.] Phoebe: (To Rachel) So did you ask him? Rachel: No, I haven't had a chance to be al…
- dos_rag score: 16.0474
  prediction: The document is a script excerpt from an episode of the TV show "Friends," focusing on Phoebe's experience of giving birth to triplets for her brother Frank and his wife Alice. The episode opens with Phoebe arriving at the hospital with her friends Ross, Joey, and Rachel, where she meets a nurse and expresses her nervousness about the pain of labor. The nurse informs her that she hasn't started h…
  top_chunk: rank=1 score=0.3240 Up, up is not an option--what's a urethra? (Monica whispers what it is in his ear.) Are you crazy?! [Scene: The delivery room, Rachel and Frank are there.] Phoebe: (To Rachel) So did you ask him? Rachel: No, I haven't had a chance to be al…

### qmsum

- examples: 1
- disagreements: 1
- any-positive-score: 1

#### qmsum / va-sq-1

- query: What was agreed upon on sample transcripts?
- references: To save time, speaker mn005 will only mark the sample of transcribed data for regions of overlapping speech, as opposed to marking all acoustic events. The digits extraction task will be delegated to whomever is working on acoustics for the Meeting Recorder project.
- best_methods: dos_rag
- disagreement: True
- vanilla_rag score: 0.0006
  prediction: Based on the provided context, it seems that the team agreed to have some ground truth first by manually marking transcripts to ensure accuracy. Specifically, Professor E mentioned that the idea of the manual marking was to confirm the accuracy of the transcriptions, saying "it's really here." Additionally, there was a forty-five minute piece transcribed by Jane that was sent to IBM for compariso…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- dos_rag score: 0.0007
  prediction: Based on the provided context, it seems that a forty-five minute piece of recorded data was transcribed by Jane and then sent to IBM for comparison. Additionally, a larger piece of recorded data, approximately ten hours, was also sent to IBM. The context does not specify any other agreements on sample transcripts beyond these points.
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…

### qasper

- examples: 1
- disagreements: 1
- any-positive-score: 1

#### qasper / b6f15fb6279b82e34a5bf4828b7b5ddabfdf1d54

- query: which multilingual approaches do they compare with?
- references: BIBREF19, BIBREF20
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 22.2222
  prediction: They compare with multilingual NMT (MNMT) BIBREF19.
  top_chunk: rank=1 score=0.4322 The results show that our approaches consistently outperform other approaches across languages and datasets, especially surpass pivoting, which is a strong baseline in the zero-shot scenario that multilingual NMT systems often fail to beat…
- dos_rag score: 13.3333
  prediction: They compare with multilingual NMT (MNMT) BIBREF19 and cross-lingual transfer without pretraining BIBREF16.
  top_chunk: rank=1 score=0.4322 The results show that our approaches consistently outperform other approaches across languages and datasets, especially surpass pivoting, which is a strong baseline in the zero-shot scenario that multilingual NMT systems often fail to beat…

### narrative_qa

- examples: 1
- disagreements: 1
- any-positive-score: 1

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_0

- query: Which character comes from Bangor, Maine?
- references: Miranda Hope.
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 44.4444
  prediction: Miss Miranda Hope comes from Bangor, Maine.
  top_chunk: rank=1 score=0.4464 I wonder if she doesn't think me refined--or if she had ever heard anything against Bangor? I can't think it is that. Don't you remember when Clara Barnard went to visit New York, three years ago, how much attention she received? And you k…
- dos_rag score: 33.3333
  prediction: Miss Miranda Mope (or Miranda Hope) comes from Bangor, Maine.
  top_chunk: rank=1 score=0.4464 I wonder if she doesn't think me refined--or if she had ever heard anything against Bangor? I can't think it is that. Don't you remember when Clara Barnard went to visit New York, three years ago, how much attention she received? And you k…

### quality

- examples: 1
- disagreements: 1
- any-positive-score: 1

#### quality / 52845_75VB1ISR_1

- query: How much time has passed between Blake's night with Eldoria and his search for Sabrina York in his mind-world? (A) 7 years (B) 10 hours (C) 12 years (D) 1 hour
- references: 10 hours
- best_methods: dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: 12 years
  top_chunk: rank=1 score=0.4728 It was a remarkably detailed materialization, and his quarry's footprints stood out clearly in the duplicated sand. Sabrina York did not even know the rudiments of the art of throwing off a mind-tracker. It would have done her but little g…
- dos_rag score: 100.0000
  prediction: 10 hours
  top_chunk: rank=1 score=0.4728 It was a remarkably detailed materialization, and his quarry's footprints stood out clearly in the duplicated sand. Sabrina York did not even know the rudiments of the art of throwing off a mind-tracker. It would have done her but little g…

### contract_nli

- examples: 1
- disagreements: 1
- any-positive-score: 0

#### contract_nli / 3_nda-11

- query: Receiving Party shall not reverse engineer any objects which embody Disclosing Party's Confidential Information.
- references: Entailment
- best_methods: vanilla_rag, dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Entailment The context explicitly states that the Receiving Party "shall not alter, modify, disassemble, reverse engineer or decompile any Confidential Information," which entails that the Receiving Party shall not reverse engineer any objects which embody the Disclosing Party's Confidential Information.
  top_chunk: rank=1 score=0.5490 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
- dos_rag score: 0.0000
  prediction: Entailment The hypothesis "Receiving Party shall not reverse engineer any objects which embody Disclosing Party's Confidential Information" is supported by the context provided. Specifically, the context states under Obligations of confidentiality and non-use (point c) that the Receiving Party "Not to use, in whole or in part, the Confidential Information for anything other than the Permitted Pur…
  top_chunk: rank=1 score=0.5490 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
