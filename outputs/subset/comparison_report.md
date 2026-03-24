# Comparison Report

Run tier: `subset`

## Score Summary

| Task | Metric | vanilla_rag | dos_rag | dos_rag_minus_vanilla_rag |
| --- | --- | --- | --- | --- |
| qmsum | rouge | 16.6505 | 18.0397 | +1.3892 |
| qasper | f1 | 43.0575 | 47.0508 | +3.9932 |
| narrative_qa | f1 | 11.3727 | 11.7651 | +0.3924 |
| quality | exact_match | 70.0000 | 76.0000 | +6.0000 |
| contract_nli | exact_match | 72.0000 | 64.0000 | -8.0000 |

## Example Previews

### qmsum

- examples: 50
- disagreements: 50
- any-positive-score: 50

#### qmsum / va-sq-1

- query: What was agreed upon on sample transcripts?
- references: To save time, speaker mn005 will only mark the sample of transcribed data for regions of overlapping speech, as opposed to marking all acoustic events. The digits extraction task will be delegated to whomever is working on acoustics for the Meeting Recorder project.
- best_methods: dos_rag
- disagreement: True
- vanilla_rag score: 0.0006
  prediction: Based on the provided context, it seems that there was a forty-five minute piece that Jane transcribed, which was then sent to IBM for transcription to have a comparison point. Additionally, there was a larger piece recorded and sent to IBM on CD-ROM, but the status of its transcription is uncertain. The team agreed to have some ground truth first from manual marking to ensure accuracy before pro…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- dos_rag score: 0.0007
  prediction: Based on the provided context, it seems that a forty-five minute piece of recorded data was transcribed by Jane and then sent to IBM for comparison. Additionally, a larger piece of recorded data, approximately ten hours, was also sent to IBM. The context does not specify any other agreements on sample transcripts beyond these points.
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…

#### qmsum / va-sq-2

- query: What was said on speech overlap?
- references: Efforts by speaker mn005 are in progress to detect overlapping speech. For a single transcribed meeting, speaker mn005 reported approximately 300 cases of overlap. Future work will involve manually deriving time marks from sections of overlapping speech for the same meeting, and then experimenting with different measures, e.g. energy increase, to determine a set of acoustically salient features f…
- best_methods: dos_rag
- disagreement: True
- vanilla_rag score: 5.2958
  prediction: The context discusses several aspects of speech overlap in a research setting: 1. **Definition and Counting Overlaps**: PhD D mentions finding three hundred speaker overlaps in a forty-five-minute session, and later, in twelve minutes, finds one thousand acoustic events, including overlaps. There is a discussion about whether to count each overlap involving multiple speakers as one event or multi…
  top_chunk: rank=1 score=0.4702 Eh almost eh three hundred eh in one session Grad G: Oh , God ! PhD D: in five {disfmarker} eh in forty - five minutes . PhD A: Three hundred overlapping speech {disfmarker} PhD D: Alm - Three hundred overlapping zone . Grad G: Ugh . PhD C…
- dos_rag score: 6.3409
  prediction: The context discusses several aspects of speech overlap in a research project. Key points include: 1. PhD D is studying overlapping speech zones and has found around three hundred overlapping speech zones in a forty-five-minute session. 2. The team is interested in how to define and count speech overlaps. For example, if two people are talking and a third person starts talking, it is considered o…
  top_chunk: rank=1 score=0.4702 Eh almost eh three hundred eh in one session Grad G: Oh , God ! PhD D: in five {disfmarker} eh in forty - five minutes . PhD A: Three hundred overlapping speech {disfmarker} PhD D: Alm - Three hundred overlapping zone . Grad G: Ugh . PhD C…

#### qmsum / va-gq-5

- query: What were the main discussion points of the meeting?
- references: The group discussed topics including a potential collaboration with another ICSI member regarding the analysis of inference structures, efforts by speaker mn005 to detect speaker overlap, the current status of recordings and transcriptions, and future efforts to collect meeting data. In addition to weekly meetings by the BMR group, efforts are in progress to record meetings by other ICSI research…
- best_methods: dos_rag
- disagreement: True
- vanilla_rag score: 6.1729
  prediction: The main discussion points of the meeting included: 1. The need for a Meeting Recorder to document discussions and decisions made in meetings. 2. The challenges of recording meetings, especially those with strong differences of opinion or involving managers. 3. The idea of recording meetings that have more emotional or conflict-driven aspects. 4. The amount of data collected and the progress of t…
  top_chunk: rank=1 score=0.3285 Uh , we {disfmarker} I think the things that we talk about in this meeting uh tend to be a mixture of uh procedural uh mundane things and uh research points and um I was thinking I think it was a meeting a couple of weeks ago that we {disf…
- dos_rag score: 7.7658
  prediction: The main discussion points of the meeting were: 1. The issue of the software crashing when started and stopped repeatedly was identified and resolved by the participant's promise to stop doing that. 2. The team discussed the definition and counting of overlapping speech and non-speech acoustic events, with a suggestion to simplify the marking process to focus only on speaker overlaps. 3. There wa…
  top_chunk: rank=1 score=0.3285 Uh , we {disfmarker} I think the things that we talk about in this meeting uh tend to be a mixture of uh procedural uh mundane things and uh research points and um I was thinking I think it was a meeting a couple of weeks ago that we {disf…

#### qmsum / va-sq-38

- query: Summarize the discussion about technical function design.
- references: The user interface designer stressed that they should design nothing but a remote control because their principle was to make users' simple desires into simple actions. Therefore, the proposed concept for the design included just a few buttons, a screen with a back light which can change colours and titanium, which was accepted by the group.
- best_methods: dos_rag
- disagreement: True
- vanilla_rag score: 6.8700
  prediction: The discussion about technical function design centered around creating a user-friendly and efficient TV remote control. Key points included: 1. Limiting the number of functions to make the remote control more user-friendly and less cluttered. 2. Considering the integration of speech recognition technology to allow users to control the TV with voice commands. 3. Implementing an automatic on/off f…
  top_chunk: rank=1 score=0.4660 Industrial Designer: I have to do working design so uh Project Manager: So you're {disfmarker} User Interface: That's {disfmarker} but this but number three , yes . Mm-hmm . So , my name is Mark Dwight , and um I am responsible for User In…
- dos_rag score: 8.6630
  prediction: The discussion about technical function design centered around creating a user-friendly, possibly universal remote control with a focus on a TV remote initially. Key points included: - The remote would have a digital signal processing chip, an infrared LED source, and a battery as its main components. - Speech recognition was proposed as an additional feature, with the idea of training the device…
  top_chunk: rank=1 score=0.4660 Industrial Designer: I have to do working design so uh Project Manager: So you're {disfmarker} User Interface: That's {disfmarker} but this but number three , yes . Mm-hmm . So , my name is Mark Dwight , and um I am responsible for User In…

#### qmsum / va-sq-47

- query: What demos would the system be involved in?
- references: The final english SmartKom demo will be presented to the whole institute once the system is de-bugged and stabilised.
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 8.9674
  prediction: The context mentions that there are demo requirements for the Fall, and there was a mention of a demo level they were thinking of. However, specific details about which demos the system would be involved in beyond these vague references are not provided in the given text. The focus seems to be more on the development and understanding of the system rather than specific demo events.
  top_chunk: rank=1 score=0.3783 Professor C: and , s deliberately . So , the reason I 'd like you to understand uh what 's going on in this demo system is not because it 's important to the research . It 's just for closure . So that if we come up with a question of " co…
- dos_rag score: 7.2458
  prediction: The context mentions that the system would be involved in demos required for funding. Specifically, it is noted that the team is committed to providing demos that meet the funding requirements, and there are demo requirements for the fall that are expected to be taken care of soon, with another serious demo requirement expected around fifteen months later. The team is focused on getting the demos…
  top_chunk: rank=1 score=0.3783 Professor C: and , s deliberately . So , the reason I 'd like you to understand uh what 's going on in this demo system is not because it 's important to the research . It 's just for closure . So that if we come up with a question of " co…

### qasper

- examples: 25
- disagreements: 17
- any-positive-score: 20

#### qasper / a313e98994fc039a82aa2447c411dda92c65a470

- query: How do they match words before reordering them?
- references: CFILT-preorder system
- best_methods: vanilla_rag, dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: using a bilingual dictionary (Google Translate word translation in our case)
  top_chunk: rank=1 score=0.4351 One of the pre-ordering rule swaps the position of the noun phrase followed by a transitive verb with the transitive verb. The original and the resulting re-ordered parse tree will be as shown in the Table TABREF5 . Applying this reorderin…
- dos_rag score: 0.0000
  prediction: They translate each word in the source language into English using a bilingual dictionary (Google Translate word translation in their case).
  top_chunk: rank=1 score=0.4351 One of the pre-ordering rule swaps the position of the noun phrase followed by a transitive verb with the transitive verb. The original and the resulting re-ordered parse tree will be as shown in the Table TABREF5 . Applying this reorderin…

#### qasper / b5e4866f0685299f1d7af267bbcc4afe2aab806f

- query: what is the source of the news sentences?
- references: links between Wikipedia articles to generate sequences of named-entity annotated tokens
- best_methods: vanilla_rag, dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: ilur.am
  top_chunk: rank=1 score=0.3977 Included sentences are from political, sports, local and world news (Figures FIGREF8 , FIGREF9 ), covering the period between August 2012 and July 2018. The dataset provides annotations for 3 popular named entity classes: people (PER), org…
- dos_rag score: 0.0000
  prediction: over 250 news texts from ilur.am
  top_chunk: rank=1 score=0.3977 Included sentences are from political, sports, local and world news (Figures FIGREF8 , FIGREF9 ), covering the period between August 2012 and July 2018. The dataset provides annotations for 3 popular named entity classes: people (PER), org…

#### qasper / c0e341c4d2253eb42c8840381b082aae274eddad

- query: What is te core component for KBQA?
- references: hierarchical matching between questions and relations with residual learning
- best_methods: vanilla_rag, dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: relation detection
  top_chunk: rank=1 score=0.4426 The KBQA system in the figure performs two key tasks: (1) entity linking, which links $n$ -grams in questions to KB entities, and (2) relation detection, which identifies the KB relation(s) a question refers to. The main focus of this work…
- dos_rag score: 0.0000
  prediction: relation detection model
  top_chunk: rank=1 score=0.4426 The KBQA system in the figure performs two key tasks: (1) entity linking, which links $n$ -grams in questions to KB entities, and (2) relation detection, which identifies the KB relation(s) a question refers to. The main focus of this work…

#### qasper / f5e6f43454332e0521a778db0b769481e23e7682

- query: what are the pivot-based baselines?
- references: firstly translates a source language into the pivot language which is later translated to the target language
- best_methods: vanilla_rag, dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: pivoting
  top_chunk: rank=1 score=0.4193 Our approaches use one encoder-decoder model to translate between any zero-shot directions, which is more efficient than pivoting. Regarding the comparison between transfer approaches, our cross-lingual pretraining based transfer outperfor…
- dos_rag score: 0.0000
  prediction: pivoting, pivoting$_{\rm m}$_
  top_chunk: rank=1 score=0.4193 Our approaches use one encoder-decoder model to translate between any zero-shot directions, which is more efficient than pivoting. Regarding the comparison between transfer approaches, our cross-lingual pretraining based transfer outperfor…

#### qasper / 2df4a045a9cd7b44874340b6fdf9308d3c55327a

- query: What crowdsourcing platform is used?
- references: They did not use any platform, instead they hired undergraduate students to do the annotation.
- best_methods: dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Amazon Mechanical Turk
  top_chunk: rank=1 score=0.4819 Our work is similar to these work but is applies on crowdsourcing learning, aiming to find invariant features among different crowdsourcing workers. Crowdsourcing. Most NLP tasks require a massive amount of labeled training data which are…
- dos_rag score: 25.0000
  prediction: undergraduate students
  top_chunk: rank=1 score=0.4819 Our work is similar to these work but is applies on crowdsourcing learning, aiming to find invariant features among different crowdsourcing workers. Crowdsourcing. Most NLP tasks require a massive amount of labeled training data which are…

### narrative_qa

- examples: 32
- disagreements: 26
- any-positive-score: 13

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_1

- query: Where is the boarding-house located?
- references: Paris
- best_methods: vanilla_rag, dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: in the Faubourg St. Germain
  top_chunk: rank=1 score=0.3975 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…
- dos_rag score: 0.0000
  prediction: Boulevard Haussman
  top_chunk: rank=1 score=0.3975 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_12

- query: Where is Herr professor from?
- references: Germany
- best_methods: vanilla_rag, dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Göttingen
  top_chunk: rank=1 score=0.2680 But at such a time as this there is always one person who seems interested in what I say--a German gentleman, a professor, who sits next to me at dinner, and whom I must tell you more about another time. He is very learned, and has a great…
- dos_rag score: 0.0000
  prediction: Gotttingen
  top_chunk: rank=1 score=0.2680 But at such a time as this there is always one person who seems interested in what I say--a German gentleman, a professor, who sits next to me at dinner, and whom I must tell you more about another time. He is very learned, and has a great…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_16

- query: What is William Platt's relationship to Miranda Hope?
- references: a previous suitor
- best_methods: vanilla_rag, dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: unclear from the context provided
  top_chunk: rank=1 score=0.3804 I try to talk with Madame de Maisonrouge all I can (she is the lady of the house, and the _real_ family consists only of herself and her two daughters). They are all most elegant, interesting women, and I am sure we shall become intimate f…
- dos_rag score: 0.0000
  prediction: not specified in the text
  top_chunk: rank=1 score=0.3804 I try to talk with Madame de Maisonrouge all I can (she is the lady of the house, and the _real_ family consists only of herself and her two daughters). They are all most elegant, interesting women, and I am sure we shall become intimate f…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_17

- query: What name does Herr Professor call Leon?
- references: Simian
- best_methods: vanilla_rag, dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: insatiable little Leon
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…
- dos_rag score: 0.0000
  prediction: little Leon
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_2

- query: Which character does Herr Professor refer to as "simian"?
- references: Leon
- best_methods: vanilla_rag, dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: the remaining figure is apparently that of a man, but I hesitate to classify him so superficially. He appears to me less human than simian
  top_chunk: rank=1 score=0.3908 The remaining figure is apparently that of a man, but I hesitate to classify him so superficially. He appears to me less human than simian, and whenever I hear him talk I seem to myself to have paused in the street to listen to the shrill…
- dos_rag score: 0.0000
  prediction: the remaining figure is apparently that of a man, but I hesitate to classify him so superficially. He appears to me less human than simian, and whenever I hear him talk I seem to myself to have paused in the street to listen to the shrill clatter of a hand-organ, to which the gambols of a hairy homunculus form an accompaniment.
  top_chunk: rank=1 score=0.3908 The remaining figure is apparently that of a man, but I hesitate to classify him so superficially. He appears to me less human than simian, and whenever I hear him talk I seem to myself to have paused in the street to listen to the shrill…

### quality

- examples: 50
- disagreements: 7
- any-positive-score: 39

#### quality / 30029_F5N22U40_6

- query: Are there indications that the Tr'en would be interested in attacking Earth? Why or why not? (A) Both A and C are correct. (B) No, because Korvin sends a mission back to Earth Central saying that the Tr'en won't come marauding out into space. (C) Yes, because the expert mentions the idea of conquering Earth with Korvin's aid. (D) Yes, because the ruler says the he wants to know about Earth's weap…
- references: Yes, because the ruler says the he wants to know about Earth's weapons, plans, and fortifications.
- best_methods: vanilla_rag, dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: No, because Korvin sends a mission back to Earth Central saying that the Tr'en won't come marauding out into space.
  top_chunk: rank=1 score=0.5556 If you didn't, you never had a second chance to try. But Korvin meant exactly what he'd said. He was going to obey the commands of the Ruler of the Tr'en—and remove the Tr'en threat from the rest of the galaxy forever. That, after all, was…
- dos_rag score: 0.0000
  prediction: Both A and C are correct.
  top_chunk: rank=1 score=0.5556 If you didn't, you never had a second chance to try. But Korvin meant exactly what he'd said. He was going to obey the commands of the Ruler of the Tr'en—and remove the Tr'en threat from the rest of the galaxy forever. That, after all, was…

#### quality / 52845_75VB1ISR_4

- query: Why did Blake create the three female super-images of Miss Stoddart, Officer Finch, and Vera Velvetskin? (A) He feels guilty about having slept with Eldoria which perpetuated the demand for female prostitution. (B) Even though he is a psycheye, he feels guilty about hunting down Sabrina York. (C) He is still grieving his mother's death and regrets not being a more loving son. (D) He feels guilty…
- references: He feels guilty about hurting Deirdre's feelings after her graduation when he ignored their romantic connection, and instead, played the part of a parent.
- best_methods: vanilla_rag, dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Even though he is a psycheye, he feels guilty about hunting down Sabrina York.
  top_chunk: rank=1 score=0.6204 Therefore, even assuming that Blake was less well-adjusted than he considered himself to be, why had he created three such malevolent super-images as Miss Stoddart, Officer Finch, and Vera Velvetskin? They followed him off the campus into…
- dos_rag score: 0.0000
  prediction: He feels guilty about having slept with Eldoria which perpetuated the demand for female prostitution.
  top_chunk: rank=1 score=0.6204 Therefore, even assuming that Blake was less well-adjusted than he considered himself to be, why had he created three such malevolent super-images as Miss Stoddart, Officer Finch, and Vera Velvetskin? They followed him off the campus into…

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

#### quality / 52845_75VB1ISR_3

- query: Why does shame flame in Blake's cheeks when Deirdre goes to prepare Eldoria's dias? (A) He is embarrassed at the thought that Deirdre might enter the room while he is sleeping with Eldoria. (B) He feels that prostitution is morally reprehensible. (C) He feels guilty about sleeping with Eldoria when there's a child in the hut, Deirdre, who knows exactly what's going on. (D) He feels guilty about w…
- references: He feels guilty about sleeping with Eldoria when there's a child in the hut, Deirdre, who knows exactly what's going on.
- best_methods: dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: He feels that prostitution is morally reprehensible.
  top_chunk: rank=1 score=0.5885 Shame flamed in Blake's cheeks, and for a moment he considered leaving; then he remembered Eldoria's dance, and he went right on sitting where he was. Presently the girl returned, and not long afterward the cloying scent of native incense…
- dos_rag score: 100.0000
  prediction: He feels guilty about sleeping with Eldoria when there's a child in the hut, Deirdre, who knows exactly what's going on.
  top_chunk: rank=1 score=0.5885 Shame flamed in Blake's cheeks, and for a moment he considered leaving; then he remembered Eldoria's dance, and he went right on sitting where he was. Presently the girl returned, and not long afterward the cloying scent of native incense…

#### quality / 62476_Z8GFDCIZ_4

- query: Why didn't Duane and Stevens go to the pressure bunks when they announced the course change? (A) They didn't hear the announcement because they were fighting. (B) They each thought they had time to kill the other before the course change started. (C) They thought they were skilled enough to weather the course change outside the bunks. (D) They didn't think the heavy-set man in blue knew what he w…
- references: They didn't hear the announcement because they were fighting.
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 100.0000
  prediction: They didn't hear the announcement because they were fighting.
  top_chunk: rank=1 score=0.5617 will you listen to reason?" Duane panted. But he halted, and the muzzle of his weapon wavered. The floor swooped and surged beneath him as the thrust of the mighty jets was cut off. Suddenly there was no gravity. The two men, locked togeth…
- dos_rag score: 0.0000
  prediction: They each thought they had time to kill the other before the course change started.
  top_chunk: rank=1 score=0.5617 will you listen to reason?" Duane panted. But he halted, and the muzzle of his weapon wavered. The floor swooped and surged beneath him as the thrust of the mighty jets was cut off. Suddenly there was no gravity. The two men, locked togeth…

### contract_nli

- examples: 50
- disagreements: 8
- any-positive-score: 37

#### contract_nli / 7_nda-7

- query: Receiving Party may share some Confidential Information with some third-parties (including consultants, agents and professional advisors).
- references: Entailment
- best_methods: vanilla_rag, dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.5166 independent contractors and professional advisors who need to know the same for the Purpose and that: (i) such directors, employees, servants, agents, officers, representatives, consultants, independent contractors and professional advisor…
- dos_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5166 independent contractors and professional advisors who need to know the same for the Purpose and that: (i) such directors, employees, servants, agents, officers, representatives, consultants, independent contractors and professional advisor…

#### contract_nli / 9_nda-15

- query: Agreement shall not grant Receiving Party any right to Confidential Information.
- references: Not mentioned
- best_methods: vanilla_rag, dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5636 Nothing in this Agreement may be construed to allow any Party to maintain, use, disclose, or share Confidential Information in a manner not allowed under federal or state law or regulation, or outside the scope of this agreement. Authorize…
- dos_rag score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.5636 Nothing in this Agreement may be construed to allow any Party to maintain, use, disclose, or share Confidential Information in a manner not allowed under federal or state law or regulation, or outside the scope of this agreement. Authorize…

#### contract_nli / 3_nda-1

- query: All Confidential Information shall be expressly identified by the Disclosing Party.
- references: Entailment
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5949 In respect of Confidential Information disclosed in documentary form, model or any other tangible form, this shall be marked by the Disclosing Party as confidential or otherwise designated to show expressly or by necessary implication that…
- dos_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5949 In respect of Confidential Information disclosed in documentary form, model or any other tangible form, this shall be marked by the Disclosing Party as confidential or otherwise designated to show expressly or by necessary implication that…

#### contract_nli / 3_nda-12

- query: Receiving Party may independently develop information similar to Confidential Information.
- references: Entailment
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5296 c) is lawfully disclosed or made available to the Receiving Party by a third party having no obligation to the Disclosing Party to maintain the confidentiality of such information; d) was independently developed or derived by the Receiving…
- dos_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5296 c) is lawfully disclosed or made available to the Receiving Party by a third party having no obligation to the Disclosing Party to maintain the confidentiality of such information; d) was independently developed or derived by the Receiving…

#### contract_nli / 3_nda-17

- query: Receiving Party may create a copy of some Confidential Information in some circumstances.
- references: Entailment
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5584 The Receiving Party may retain one (1) copy of any such Confidential Information to be stored securely with its legal representative only if required for regulatory or insurance purposes, but in this event the confidentiality and non-use p…
- dos_rag score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.5584 The Receiving Party may retain one (1) copy of any such Confidential Information to be stored securely with its legal representative only if required for regulatory or insurance purposes, but in this event the confidentiality and non-use p…
