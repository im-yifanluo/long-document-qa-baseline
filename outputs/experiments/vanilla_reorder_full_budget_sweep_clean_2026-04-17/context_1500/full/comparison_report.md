# Comparison Report

Run tier: `full`

## Score Summary

| Task | Metric | vanilla_rag | reorder_only_rag | reorder_only_rag_minus_vanilla_rag |
| --- | --- | --- | --- | --- |
| qmsum | rouge | 16.4250 | 17.0937 | +0.6687 |
| qasper | f1 | 36.1983 | 38.1578 | +1.9595 |
| narrative_qa | f1 | 19.5002 | 20.6444 | +1.1442 |
| quality | exact_match | 51.0067 | 53.2119 | +2.2052 |
| contract_nli | exact_match | 60.6557 | 55.4484 | -5.2073 |

## Runtime Summary

| Method | Total seconds | Total minutes | Seconds / example | Examples / second |
| --- | --- | --- | --- | --- |
| vanilla_rag | 12271.97 | 204.53 | 1.5725 | 0.6359 |
| reorder_only_rag | 12185.51 | 203.09 | 1.5614 | 0.6404 |

## Example Previews

### qmsum

- examples: 272
- disagreements: 272
- any-positive-score: 269

#### qmsum / va-gq-233

- query: What was the meeting about?
- references: The revised semantic specification and construction formalism are more stable than the previous versions. Semantic constraints also come into play. The semantic specification, on the other hand, is split into three levels: "scenario" is a list of schemas and bindings between them, which describes the current event in terms of Source-Path-Goal, Container, etc.; "referent" is about the entities in…
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: The meeting was about discussing a graduate student's (Grad A) research progress, specifically focusing on a sheet of thoughts and justifications for comments, and planning future meetings to provide feedback on a thesis proposal draft. The discussion also touched on structuring a model of a hypothetical past France universe and the concept of focus and scope in language. Additionally, the group…
  top_chunk: rank=1 score=0.2806 Grad A: Yes . Um . Professor C: Oh , you have something . Grad A: In the process thereof , or whatever . Professor C: OK . So , what 's {disfmarker} what {disfmarker} when are we gonna meet again ? Grad F: When are you leaving ? Grad A: Fr…
- reorder_only_rag score: 0.0000
  prediction: The meeting appears to be about a research project, likely in linguistics or a related field, where participants are discussing their work, including thoughts and justifications for comments, a model of a hypothetical past France universe, and the structure of composite events. They are also planning future meetings and considering feedback sessions for thesis proposals.
  top_chunk: rank=1 score=0.2806 Grad A: Yes . Um . Professor C: Oh , you have something . Grad A: In the process thereof , or whatever . Professor C: OK . So , what 's {disfmarker} what {disfmarker} when are we gonna meet again ? Grad F: When are you leaving ? Grad A: Fr…

#### qmsum / va-sq-35

- query: Summarize the discussion about user requirements.
- references: According to a market survey, there were several things that users didn't like in current remote controls. First of all, users find them very ugly. Second, the current remote controls were not so easy to use and the facilities that they offered did not match what people really wanted. Third, people were very frustrated with their remote controls because sometimes they just couldn't find them. The…
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: The discussion centered around user requirements for a new remote control, particularly focusing on the preferences and behaviors of the target users. Marketing emphasized that young people are the early adopters and primary users of new devices, suggesting that the remote control should cater to their needs. Key points included: 1. **Power Button Usage**: The power button is used infrequently, w…
  top_chunk: rank=1 score=0.3915 Marketing: this is of course , depends on that . And um I don't have any conclusion , I didn't have time the meeting was very tight , so that's basically my findings . And uh , if you have any question ? Project Manager: Mm I think it's go…
- reorder_only_rag score: 0.0000
  prediction: The discussion about user requirements centered around understanding the needs of the target users for the new remote control project. Marketing presented insights based on user preferences and behaviors, highlighting that the power button is used infrequently, while channel selection and volume control are used more often. The team agreed that the target audience should be young people, as they…
  top_chunk: rank=1 score=0.3915 Marketing: this is of course , depends on that . And um I don't have any conclusion , I didn't have time the meeting was very tight , so that's basically my findings . And uh , if you have any question ? Project Manager: Mm I think it's go…

#### qmsum / va-sq-83

- query: Why the intensity of demands for the services in the early implementer areas would not be spread across Wales?
- references: Huw Irranca-Davies mentioned there were some economic issues and cultural issues to deal with, rather than the capacity problems.
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: The intensity of demand for the services in the early implementer areas is not spread evenly across Wales because the early adopter areas were specifically chosen for deep dives into regions that vary from very rural areas in mid Wales, areas in north Wales, and areas around Welsh language provision, as well as areas in deep valleys. These areas were selected to understand the cultural and econom…
  top_chunk: rank=1 score=0.5453 So, we have the confidence now that, with that learning going on from different pilot areas, we'll have the full roll-out by 2020. Hefin David AM: Is it true to say that, in the early adopter areas, the intensity of demand for the services…
- reorder_only_rag score: 0.0000
  prediction: The intensity of demand for the services in the early implementer areas is not spread evenly across Wales because, as mentioned in the context, "in the early adopter areas, the intensity of demand for the services is not spread evenly across." This uneven distribution is due to various factors, including regional variations in the scale and type of childcare offers, cultural and economic impacts,…
  top_chunk: rank=1 score=0.5453 So, we have the confidence now that, with that learning going on from different pilot areas, we'll have the full roll-out by 2020. Hefin David AM: Is it true to say that, in the early adopter areas, the intensity of demand for the services…

#### qmsum / va-sq-84

- query: Summarize the discussion about the childcare offer.
- references: Huw Irranca-Davies first talked about the registration of grandparents. Next, Huw Irranca-Davies denied the statement that Wales has the most fragile childcare sector in Britain, pointing out that childcare offers can make the section more resilient and robust. To continue, Huw Irranca-Davies mentioned that there would be capacity growth in the next several years to deliver the product.
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 4.4154
  prediction: The discussion centers around the Welsh Government's childcare offer and its alignment with early years development. Key points include: 1. **Purpose and Scope**: The offer aims to provide both childcare and educational support, with 10 hours of foundation education included in the 30-hour childcare provision. This is designed to support working parents and enhance school readiness. 2. **Affordab…
  top_chunk: rank=1 score=0.5670 Now, we're doing some fascinating work that I think I've referred to on this committee before about aligning the early years development entirely. Now, this is an evolving piece of work, but I think the childcare offer should ultimately fi…
- reorder_only_rag score: 0.0000
  prediction: The discussion centers around the Welsh Government's childcare offer, which includes 30 hours of childcare and 10 hours of early education per week. Key points include: 1. **Phased Implementation**: The offer is being piloted and phased in to learn from experiences in other regions, such as England, where a different approach was taken. 2. **Affordability and National Roll-Out**: There is a focus…
  top_chunk: rank=1 score=0.5670 Now, we're doing some fascinating work that I think I've referred to on this committee before about aligning the early years development entirely. Now, this is an evolving piece of work, but I think the childcare offer should ultimately fi…

#### qmsum / va-sq-18

- query: Summarize the group's plan of their marketing strategy.
- references: For fear that the exorbitant price of 25 euros of the remote control would shock the potential consumers, Project Manager proposed to trade off some functions for a lower price. Additionally, Project Manager mentioned an American computer electronics store to show that shipping products overseas can also make profits and then added this to the whole plan.
- best_methods: reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: The group plans to develop a marketing strategy that focuses on making ordinary products fashionable and appealing, aligning with the corporate strategy of enhancing everyday items to match the quality of brands like John Lewis or Debenhams. They aim to tap into their collective knowledge to identify user needs and preferences, and to negotiate between what users want and what they can realistica…
  top_chunk: rank=1 score=0.3665 if you wanna write all five go for it but name one of them that you could um . Oh , we skipped introductions . Nice . I'm a excellent Project Manager . Um . Marketing: {vocalsound} Project Manager: I'm Marty , Industrial Designer: {vocalso…
- reorder_only_rag score: 7.2262
  prediction: The group plans to develop a marketing strategy that focuses on making ordinary products fashionable and appealing, aligning with the corporate strategy of enhancing the perceived niceness of everyday items. They aim to consider user needs and preferences in their product development, and will discuss trade-offs and specific instructions in their next meeting. The team will also explore innovativ…
  top_chunk: rank=1 score=0.3665 if you wanna write all five go for it but name one of them that you could um . Oh , we skipped introductions . Nice . I'm a excellent Project Manager . Um . Marketing: {vocalsound} Project Manager: I'm Marty , Industrial Designer: {vocalso…

### qasper

- examples: 984
- disagreements: 630
- any-positive-score: 799

#### qasper / 00050f7365e317dc0487e282a4c33804b58b1fb3

- query: Is SemCor3.0 reflective of English language data in general?
- references: Yes | Unanswerable
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: SemCor3.0 is the largest corpus manually annotated with WordNet sense for WSD.
  top_chunk: rank=1 score=0.4463 Experiments ::: Datasets ::: Training Dataset Following previous work BIBREF13, BIBREF12, BIBREF10, BIBREF17, BIBREF9, BIBREF7, we choose SemCor3.0 as training corpus, which is the largest corpus manually annotated with WordNet sense for W…
- reorder_only_rag score: 0.0000
  prediction: Following previous work BIBREF13, BIBREF12, BIBREF10, BIBREF17, BIBREF9, BIBREF7, we choose SemCor3.0 as training corpus, which is the largest corpus manually annotated with WordNet sense for WSD.
  top_chunk: rank=1 score=0.4463 Experiments ::: Datasets ::: Training Dataset Following previous work BIBREF13, BIBREF12, BIBREF10, BIBREF17, BIBREF9, BIBREF7, we choose SemCor3.0 as training corpus, which is the largest corpus manually annotated with WordNet sense for W…

#### qasper / 007b13f05d234d37966d1aa7d85b5fd78564ff45

- query: Do the errors of the model reflect linguistic similarity between different L1s?
- references: Unanswerable
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: An important limitation of this experiment is that it does not account for topic bias, an important issue in NLI BIBREF22 . This is due to the fact that NLI-PT is not balanced by topic and the model could be learning topic associations instead.
  top_chunk: rank=1 score=0.4805 An experiment with the texts written by the speakers of five L1s: Chinese, English, German, Italian, and Spanish using a bag of words model achieved 70% accuracy. We are currently experimenting with different features taking advantage of t…
- reorder_only_rag score: 0.0000
  prediction: An important limitation of this experiment is that it does not account for topic bias, an important issue in NLI BIBREF22 .
  top_chunk: rank=1 score=0.4805 An experiment with the texts written by the speakers of five L1s: Chinese, English, German, Italian, and Spanish using a bag of words model achieved 70% accuracy. We are currently experimenting with different features taking advantage of t…

#### qasper / 00c57e45ac6afbdfa67350a57e81b4fad0ed2885

- query: Do they evaluate only on English datasets?
- references: Yes | Yes
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: No, the context does not explicitly state that they evaluate only on English datasets. The provided context does not mention the language of the datasets used for evaluation.
  top_chunk: rank=1 score=0.3615 However, more research is needed to better understand the predictive power of supervised machine learning classifiers and the influence of feature groups and feature sets for efficiently classifying depression-related tweets to support men…
- reorder_only_rag score: 0.0000
  prediction: No
  top_chunk: rank=1 score=0.3615 However, more research is needed to better understand the predictive power of supervised machine learning classifiers and the influence of feature groups and feature sets for efficiently classifying depression-related tweets to support men…

#### qasper / 0101ebfbaba75fd47868ad0c796ac44ebc19c566

- query: How do they split text to obtain sentence levels?
- references: Unanswerable
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: For one-stage QACNN, we didn't split an entire passage into sentences.
  top_chunk: rank=1 score=0.4306 For one-stage QACNN, we didn't split an entire passage into sentences. That is, the shape of passage-query similarity map INLINEFORM0 and passage-choice similarity map INLINEFORM1 are 2D rather than 3D. We convolved them directly on word-l…
- reorder_only_rag score: 0.0000
  prediction: They split an entire passage into sentences in the second stage of the CNN architecture.
  top_chunk: rank=1 score=0.4306 For one-stage QACNN, we didn't split an entire passage into sentences. That is, the shape of passage-query similarity map INLINEFORM0 and passage-choice similarity map INLINEFORM1 are 2D rather than 3D. We convolved them directly on word-l…

#### qasper / 01a41c0a4a7365cd37d28690735114f2ff5229f2

- query: What social media platform did they look at?
- references: http://www.blogger.com | http://www.blogger.com
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Sina Weibo
  top_chunk: rank=1 score=0.3878 At the same time, a number of researchers sought to predict the social media users' age and/or gender BIBREF14 , BIBREF15 , BIBREF16 , while others targeted and analyzed the ethnicity, nationality, and race of the users BIBREF17 , BIBREF18…
- reorder_only_rag score: 0.0000
  prediction: Blogger
  top_chunk: rank=1 score=0.3878 At the same time, a number of researchers sought to predict the social media users' age and/or gender BIBREF14 , BIBREF15 , BIBREF16 , while others targeted and analyzed the ethnicity, nationality, and race of the users BIBREF17 , BIBREF18…

### narrative_qa

- examples: 3425
- disagreements: 2291
- any-positive-score: 2048

#### narrative_qa / 00fb61fa7bee266ad995e52190ebb73606b60b70_0

- query: WHO NORMALLY DELIVERS THE OPENING PROLOGUE IN THE PLAY?
- references: THE ACTOR WEARING THE BLACK CLOAK | The actor in the black cloak
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: since I speak not his prologue, I'll go tell all the argument of his play afore-hand, and so stale his invention to the auditory, before it come forth.
  top_chunk: rank=1 score=0.3583 Stay Jack: 'slid I'll do somewhat now afore I go in, though it be nothing but to revenge myself on the author; since I speak not his prologue, I'll go tell all the argument of his play afore-hand, and so stale his invention to the auditory…
- reorder_only_rag score: 0.0000
  prediction: "that he may have the justice, before he encounter his respected adversary, to see some light stroke of his play, commenced with some other."
  top_chunk: rank=1 score=0.3583 Stay Jack: 'slid I'll do somewhat now afore I go in, though it be nothing but to revenge myself on the author; since I speak not his prologue, I'll go tell all the argument of his play afore-hand, and so stale his invention to the auditory…

#### narrative_qa / 00fb61fa7bee266ad995e52190ebb73606b60b70_1

- query: WHAT NAME WAS CYNTHIA MORE FAMOUSLY KNOWN BY?
- references: THE GODDESS DIANA
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Cynthia's Revels
  top_chunk: rank=1 score=0.4410 Cynthia, by my bright soul, is a right exquisite and spendidious lady; yet Amorphus, I think, hath seen more fashions, I am sure more countries; but whether I have or not, what need we gaze on Cynthia, that have ourself to admire? PHA.
- reorder_only_rag score: 0.0000
  prediction: Cynthia, and her court.
  top_chunk: rank=1 score=0.4410 Cynthia, by my bright soul, is a right exquisite and spendidious lady; yet Amorphus, I think, hath seen more fashions, I am sure more countries; but whether I have or not, what need we gaze on Cynthia, that have ourself to admire? PHA.

#### narrative_qa / 00fb61fa7bee266ad995e52190ebb73606b60b70_13

- query: Where is Narcissus's spring?
- references: Gargaphie Valley Greece. | Gargaphie
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: "Would I had never look'd / In such a flattering mirror!"
  top_chunk: rank=1 score=0.4261 See, see, the mourning fount, whose springs weep yet Th' untimely fate of that too beauteous boy, That trophy of self-love, and spoil of nature, Who, now transform'd into this drooping flower, Hangs the repentant head, back from the stream…
- reorder_only_rag score: 0.0000
  prediction: See, see, the mourning fount, whose springs weep yet Th' untimely fate of that too beauteous boy, That trophy of self-love, and spoil of nature, Who, now transform'd into this drooping flower, Hangs the repentant head, back from the stream, As if it wish'd, "Would I had never look'd In such a flattering mirror!"
  top_chunk: rank=1 score=0.4261 See, see, the mourning fount, whose springs weep yet Th' untimely fate of that too beauteous boy, That trophy of self-love, and spoil of nature, Who, now transform'd into this drooping flower, Hangs the repentant head, back from the stream…

#### narrative_qa / 00fb61fa7bee266ad995e52190ebb73606b60b70_14

- query: Which two societies are aligned in this play?
- references: Greek mythology and Queen Elizabeth's Court | Greece and England
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: the more judicious part of it
  top_chunk: rank=1 score=0.3522 This play as a fabric of plot is a very slight affair; but as a satirical picture of the manners of the time, proceeding by means of vivid caricature, couched in witty and brilliant dialogue and sustained by that righteous indignation whic…
- reorder_only_rag score: 0.0000
  prediction: "the divided heads"
  top_chunk: rank=1 score=0.3522 This play as a fabric of plot is a very slight affair; but as a satirical picture of the manners of the time, proceeding by means of vivid caricature, couched in witty and brilliant dialogue and sustained by that righteous indignation whic…

#### narrative_qa / 00fb61fa7bee266ad995e52190ebb73606b60b70_16

- query: Which page performs the dialogue?
- references: Anaides
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Crites
  top_chunk: rank=1 score=0.3508 ANA. And my cockatrice here. AMO. She is welcome. THE CITIZEN, AND HIS WIFE, PAGES, ETC., APPEAR AT THE DOOR. MORP. Knock those same pages there; and, goodman coxcomb the citizen, who would you speak withal? WIFE. My brother. AMO. With who…
- reorder_only_rag score: 0.0000
  prediction: ANA.
  top_chunk: rank=1 score=0.3508 ANA. And my cockatrice here. AMO. She is welcome. THE CITIZEN, AND HIS WIFE, PAGES, ETC., APPEAR AT THE DOOR. MORP. Knock those same pages there; and, goodman coxcomb the citizen, who would you speak withal? WIFE. My brother. AMO. With who…

### quality

- examples: 2086
- disagreements: 616
- any-positive-score: 1265

#### quality / 20006_RQF3XP3W_7

- query: According to Slate's ratings, which of the orderings below correctly goes from most reprehensible to least reprehensible? (A) Bob Barr, James Carville, Lanny Davis, Erskine Bowles (B) James Carville, Lanny Davis, Bob Barr, Erskine Bowles (C) Lanny Davis, Bob Barr, James Carville, Erskine Bowles (D) Bob Barr, Erskine Bowles, James Carville, Lanny Davis
- references: James Carville, Lanny Davis, Bob Barr, Erskine Bowles
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: James Carville
  top_chunk: rank=1 score=0.4228 Slate rating: +3 Erskine Bowles (The public's rating: Doesn't care ) Minuses: a) Refused to involve himself in the critical issue of the presidency. b) Stood aside while White House was shanghaied by lawyers.
- reorder_only_rag score: 0.0000
  prediction: Lanny Davis
  top_chunk: rank=1 score=0.4228 Slate rating: +3 Erskine Bowles (The public's rating: Doesn't care ) Minuses: a) Refused to involve himself in the critical issue of the presidency. b) Stood aside while White House was shanghaied by lawyers.

#### quality / 20006_VZW02G1T_8

- query: What is one of Jessie Jackson's "minuses" in relation to this issue? (A) He did not rebuke Clinton for his actions. (B) He used his time as pastoral counsel for Clinton to gain media attention. (C) He does not meet with Monica. (D) He was not really there for Clinton in his time of spiritual need.
- references: He used his time as pastoral counsel for Clinton to gain media attention.
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: B) Parlayed pastoral visit into a week of self-promotion.
  top_chunk: rank=1 score=0.5852 Jesse Jackson (The public's rating: +2 ) Minuses: a) Revealed Clinton family troubles immediately after his pastoral visit. b) Parlayed pastoral visit into a week of self-promotion. Pluses: a) Graciously counseled a political rival in time…
- reorder_only_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.5852 Jesse Jackson (The public's rating: +2 ) Minuses: a) Revealed Clinton family troubles immediately after his pastoral visit. b) Parlayed pastoral visit into a week of self-promotion. Pluses: a) Graciously counseled a political rival in time…

#### quality / 20007_RZDMZJYW_2

- query: What made it easier for previous presidents to get away with adultery? (A) Their staff did not know (B) They always tried to hide it well (C) The secret service budget was small (D) The reporters never found out
- references: The secret service budget was small
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: They always tried to hide it well
  top_chunk: rank=1 score=0.5717 Not only are newspapers and magazines willing to publish an adultery story about him, but many are pursuing it. For the same reason, Clinton would find it difficult to hire a mistress. A lovely young secretary would set off alarm bells in…
- reorder_only_rag score: 0.0000
  prediction: D
  top_chunk: rank=1 score=0.5717 Not only are newspapers and magazines willing to publish an adultery story about him, but many are pursuing it. For the same reason, Clinton would find it difficult to hire a mistress. A lovely young secretary would set off alarm bells in…

#### quality / 20020_L7G74WXN_1

- query: Why does the author say Monica was hired? (A) Clinton insisted his staff remain (B) She was a secretary (C) Due to the government shutdown (D) It was in the budget
- references: Due to the government shutdown
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.4923 [As the relationship between Clinton and Monica continues, some members of the White House staff become worried about the prudence of continuing the relationship with so much potential for scandal.
- reorder_only_rag score: 0.0000
  prediction: It was in the budget
  top_chunk: rank=1 score=0.4923 [As the relationship between Clinton and Monica continues, some members of the White House staff become worried about the prudence of continuing the relationship with so much potential for scandal.

#### quality / 20020_TRPTAKN4_5

- query: What is the musical’s relationship like between Monica and Linda? (A) Monica and Linda conspired together to hatch the plan (B) Monica keeps reiterating the story over and over in different ways to Linda (C) Linda does not believe what Monica is telling here and discredits it (D) Linda presses for details and Monica obliges
- references: Linda presses for details and Monica obliges
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: D Linda presses for details and Monica obliges
  top_chunk: rank=1 score=0.4751 CURRIE: He comes back From Easter services, Soon she's bopping in the door. LIEBERMAN: "Hallelujah, He Is Risen" Shouldn't inspire thoughts so sizzlin'. Yes, it's really time for Monica to go. [Times passes. Monica moves to the Pentagon, b…
- reorder_only_rag score: 0.0000
  prediction: Linda does not believe what Monica is telling here and discredits it
  top_chunk: rank=1 score=0.4751 CURRIE: He comes back From Easter services, Soon she's bopping in the door. LIEBERMAN: "Hallelujah, He Is Risen" Shouldn't inspire thoughts so sizzlin'. Yes, it's really time for Monica to go. [Times passes. Monica moves to the Pentagon, b…

### contract_nli

- examples: 1037
- disagreements: 175
- any-positive-score: 680

#### contract_nli / 10_nda-4

- query: Receiving Party shall not use any Confidential Information for any purpose other than the purposes stated in Agreement.
- references: Entailment
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.6151 2.04 No Benefit, Restricted Use The Receiving Party shall not, in any manner, derive any benefit, directly or indirectly, from the Confidential Information or the use of such Confidential Information, for any purpose. The Receiving Party a…
- reorder_only_rag score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.6151 2.04 No Benefit, Restricted Use The Receiving Party shall not, in any manner, derive any benefit, directly or indirectly, from the Confidential Information or the use of such Confidential Information, for any purpose. The Receiving Party a…

#### contract_nli / 13_nda-7

- query: Receiving Party may share some Confidential Information with some third-parties (including consultants, agents and professional advisors).
- references: Entailment
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5244 Confidential Information excludes any information that: (i) the Disclosing Party has not specifically notified the Party is confidential; (ii) becomes available to the Party or the Reviewing Representative on a non-confidential basis from…
- reorder_only_rag score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.5244 Confidential Information excludes any information that: (i) the Disclosing Party has not specifically notified the Party is confidential; (ii) becomes available to the Party or the Reviewing Representative on a non-confidential basis from…

#### contract_nli / 16_nda-7

- query: Receiving Party may share some Confidential Information with some third-parties (including consultants, agents and professional advisors).
- references: Entailment
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.4970 This information received from a party (including of any of the Corporations), either orally or in writing, during the course of the Project shall be deemed to be confidential information (Confidential Information) for purposes of this Con…
- reorder_only_rag score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.4970 This information received from a party (including of any of the Corporations), either orally or in writing, during the course of the Project shall be deemed to be confidential information (Confidential Information) for purposes of this Con…

#### contract_nli / 19_nda-5

- query: Receiving Party may share some Confidential Information with some of Receiving Party's employees.
- references: Entailment
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.4990 and c) Confidant shall cause all of its applicable employees to observe the terms of this Agreement, and shall be responsible for any breach of the terms of this Agreement by it or any such employee. 4. Return of Confidential Information:…
- reorder_only_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.4990 and c) Confidant shall cause all of its applicable employees to observe the terms of this Agreement, and shall be responsible for any breach of the terms of this Agreement by it or any such employee. 4. Return of Confidential Information:…

#### contract_nli / 20_nda-17

- query: Receiving Party may create a copy of some Confidential Information in some circumstances.
- references: Entailment
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.5795 Return of Confidential Information 3.1 All Confidential Information disclosed by the Disclosing Party to the Receiving Party shall remain the property of the Disclosing Party. The Receiving Party shall not be entitled to copy any Confident…
- reorder_only_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5795 Return of Confidential Information 3.1 All Confidential Information disclosed by the Disclosing Party to the Receiving Party shall remain the property of the Disclosing Party. The Receiving Party shall not be entitled to copy any Confident…
