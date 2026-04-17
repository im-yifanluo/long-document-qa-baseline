# Comparison Report

Run tier: `subset`

## Score Summary

| Task | Metric | vanilla_rag | reorder_only_rag | reorder_only_rag_minus_vanilla_rag |
| --- | --- | --- | --- | --- |
| qmsum | rouge | 16.8977 | 17.3904 | +0.4927 |
| qasper | f1 | 38.0419 | 37.3698 | -0.6721 |
| narrative_qa | f1 | 12.5530 | 10.4185 | -2.1345 |
| quality | exact_match | 44.0000 | 52.0000 | +8.0000 |
| contract_nli | exact_match | 66.0000 | 58.0000 | -8.0000 |

## Runtime Summary

| Method | Total seconds | Total minutes | Seconds / example | Examples / second |
| --- | --- | --- | --- | --- |
| vanilla_rag | 421.14 | 7.02 | 1.6846 | 0.5936 |
| reorder_only_rag | 447.69 | 7.46 | 1.7908 | 0.5584 |

## Example Previews

### qmsum

- examples: 50
- disagreements: 50
- any-positive-score: 50

#### qmsum / va-gq-5

- query: What were the main discussion points of the meeting?
- references: The group discussed topics including a potential collaboration with another ICSI member regarding the analysis of inference structures, efforts by speaker mn005 to detect speaker overlap, the current status of recordings and transcriptions, and future efforts to collect meeting data. In addition to weekly meetings by the BMR group, efforts are in progress to record meetings by other ICSI research…
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 7.6235
  prediction: The main discussion points of the meeting included the recording of meetings, particularly those of the network services and applications group, which would start the following week. There was also a discussion about data collection, specifically the number of overlaps between speakers and the potential for recording meetings with more emotional or conflicting aspects. Additionally, the group tal…
  top_chunk: rank=1 score=0.3285 Uh , we {disfmarker} I think the things that we talk about in this meeting uh tend to be a mixture of uh procedural uh mundane things and uh research points and um I was thinking I think it was a meeting a couple of weeks ago that we {disf…
- reorder_only_rag score: 0.0000
  prediction: The main discussion points of the meeting included the nature of overlaps and interruptions during meetings, the recording of meetings for research purposes, and the collection of data on meeting interactions. Participants also discussed the frequency of their meetings, the types of meetings that could be recorded (such as those with conflicts or strong opinions), and the potential for recording…
  top_chunk: rank=1 score=0.3285 Uh , we {disfmarker} I think the things that we talk about in this meeting uh tend to be a mixture of uh procedural uh mundane things and uh research points and um I was thinking I think it was a meeting a couple of weeks ago that we {disf…

#### qmsum / va-sq-35

- query: Summarize the discussion about user requirements.
- references: According to a market survey, there were several things that users didn't like in current remote controls. First of all, users find them very ugly. Second, the current remote controls were not so easy to use and the facilities that they offered did not match what people really wanted. Third, people were very frustrated with their remote controls because sometimes they just couldn't find them. The…
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 7.7266
  prediction: The discussion centered around user requirements for a new remote control design, particularly focusing on the preferences and behaviors of the target users. Key points included: 1. **Target Audience**: The primary target is young people, as they are early adopters of new devices and less likely to use features like teletext, which they can access through other means. 2. **Functionality**: - The…
  top_chunk: rank=1 score=0.3915 Marketing: this is of course , depends on that . And um I don't have any conclusion , I didn't have time the meeting was very tight , so that's basically my findings . And uh , if you have any question ? Project Manager: Mm I think it's go…
- reorder_only_rag score: 0.0000
  prediction: The discussion about user requirements centered around understanding the needs of the target users for the new remote control project. Marketing presented insights based on user preferences and behaviors, highlighting that the power button is used infrequently, while channel selection and volume control are more commonly used. The team agreed that the remote control should be designed with a focu…
  top_chunk: rank=1 score=0.3915 Marketing: this is of course , depends on that . And um I don't have any conclusion , I didn't have time the meeting was very tight , so that's basically my findings . And uh , if you have any question ? Project Manager: Mm I think it's go…

#### qmsum / va-sq-2

- query: What was said on speech overlap?
- references: Efforts by speaker mn005 are in progress to detect overlapping speech. For a single transcribed meeting, speaker mn005 reported approximately 300 cases of overlap. Future work will involve manually deriving time marks from sections of overlapping speech for the same meeting, and then experimenting with different measures, e.g. energy increase, to determine a set of acoustically salient features f…
- best_methods: reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: The discussion centered around the challenge of marking speech overlaps manually, which was found to be time-consuming. PhD D mentioned finding one thousand acoustic events, including overlaps, in just twelve minutes of recording. The group debated whether to mark all acoustic events or just the overlaps. PhD D defined an acoustic event as the overlapping zone where three or more speakers are tal…
  top_chunk: rank=1 score=0.4702 Eh almost eh three hundred eh in one session Grad G: Oh , God ! PhD D: in five {disfmarker} eh in forty - five minutes . PhD A: Three hundred overlapping speech {disfmarker} PhD D: Alm - Three hundred overlapping zone . Grad G: Ugh . PhD C…
- reorder_only_rag score: 8.3437
  prediction: PhD D mentioned that they found almost three hundred overlapping speech zones in one session lasting forty-five minutes. This amounts to about three hundred overlapping speech events in twelve minutes of recorded speech. PhD D considers an acoustic event to be the overlapping zone where three or more speakers are talking together, without distinguishing between the number of speakers involved. Th…
  top_chunk: rank=1 score=0.4702 Eh almost eh three hundred eh in one session Grad G: Oh , God ! PhD D: in five {disfmarker} eh in forty - five minutes . PhD A: Three hundred overlapping speech {disfmarker} PhD D: Alm - Three hundred overlapping zone . Grad G: Ugh . PhD C…

#### qmsum / va-sq-18

- query: Summarize the group's plan of their marketing strategy.
- references: For fear that the exorbitant price of 25 euros of the remote control would shock the potential consumers, Project Manager proposed to trade off some functions for a lower price. Additionally, Project Manager mentioned an American computer electronics store to show that shipping products overseas can also make profits and then added this to the whole plan.
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 7.3356
  prediction: The group plans to develop a marketing strategy that focuses on making ordinary products fashionable and appealing, aligning with the corporate strategy. They aim to tap into their collective knowledge to identify user needs and preferences, and to negotiate between what users want and what they can realistically offer. The team will document their ideas and trade-offs in project documents for fu…
  top_chunk: rank=1 score=0.3665 if you wanna write all five go for it but name one of them that you could um . Oh , we skipped introductions . Nice . I'm a excellent Project Manager . Um . Marketing: {vocalsound} Project Manager: I'm Marty , Industrial Designer: {vocalso…
- reorder_only_rag score: 7.2262
  prediction: The group plans to develop a marketing strategy that focuses on making ordinary products fashionable and appealing, aligning with the corporate strategy of enhancing the perceived niceness of everyday items. They aim to consider user needs and preferences in their product development, and will discuss trade-offs and specific instructions in their next meeting. The team will also explore innovativ…
  top_chunk: rank=1 score=0.3665 if you wanna write all five go for it but name one of them that you could um . Oh , we skipped introductions . Nice . I'm a excellent Project Manager . Um . Marketing: {vocalsound} Project Manager: I'm Marty , Industrial Designer: {vocalso…

#### qmsum / va-sq-4

- query: What was the future of data collection?
- references: The group aims to collect over 100 hours of Meeting Recorder data in total. Speaker consent forms are being revised. It was suggested that subjects should sign a new consent form after 10 recording sessions.
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 8.2940
  prediction: The future of data collection involves expanding the current data set, which is predominantly composed of meeting recordings. There is a suggestion to record additional meetings, possibly two or three more per week, even if they are not transcribed, to accumulate more audio data. The goal is to collect significantly more than a hundred hours of data, with the possibility of collecting more at the…
  top_chunk: rank=1 score=0.3866 I wanted to ask another a a aspect of the data collection . There 'd be no reason why a person couldn't get together several uh , you know , friends , and come and argue about a topic if they wanted to , right ?
- reorder_only_rag score: 6.1694
  prediction: Based on the provided context, the future of data collection involves expanding the current dataset, particularly focusing on meeting recordings. The goal is to collect significantly more data, aiming for over a hundred hours, to support various projects and analyses. The team is considering recording additional meetings, both at their location and at the University of Washington, to increase the…
  top_chunk: rank=1 score=0.3866 I wanted to ask another a a aspect of the data collection . There 'd be no reason why a person couldn't get together several uh , you know , friends , and come and argue about a topic if they wanted to , right ?

### qasper

- examples: 50
- disagreements: 34
- any-positive-score: 44

#### qasper / 71e4ba4e87e6596aeca187127c0d088df6570c57

- query: What evaluations methods do they take?
- references: Unanswerable | Unanswerable
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Another method is to tag all descriptions with part-of-speech information, so that it becomes possible to see e.g. which adjectives are most commonly used for particular nouns.
  top_chunk: rank=1 score=0.2777 A next step would be to see whether these observations also hold for other age groups, i.e. children and adults. INLINEFORM0 Other methods It may be difficult to spot patterns by just looking at a collection of images. Another method is to…
- reorder_only_rag score: 0.0000
  prediction: They take several evaluations methods including: - Manually inspecting a subset of the Flickr30K data to group inferences into categories - Counting the proportion of descriptions that contain markers for ethnicity - Tagging all descriptions with part-of-speech information - Applying Louvain clustering to the coreference graph to analyze referring expressions
  top_chunk: rank=1 score=0.2777 A next step would be to see whether these observations also hold for other age groups, i.e. children and adults. INLINEFORM0 Other methods It may be difficult to spot patterns by just looking at a collection of images. Another method is to…

#### qasper / a313e98994fc039a82aa2447c411dda92c65a470

- query: How do they match words before reordering them?
- references: Unanswerable | CFILT-preorder system
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Pre-ordering the source language sentences to match the target language word order.
  top_chunk: rank=1 score=0.4351 One of the pre-ordering rule swaps the position of the noun phrase followed by a transitive verb with the transitive verb. The original and the resulting re-ordered parse tree will be as shown in the Table TABREF5 . Applying this reorderin…
- reorder_only_rag score: 0.0000
  prediction: One of the pre-ordering rule swaps the position of the noun phrase followed by a transitive verb with the transitive verb.
  top_chunk: rank=1 score=0.4351 One of the pre-ordering rule swaps the position of the noun phrase followed by a transitive verb with the transitive verb. The original and the resulting re-ordered parse tree will be as shown in the Table TABREF5 . Applying this reorderin…

#### qasper / fb2b536dc8e442dffab408db992b971e86548158

- query: What is the interannotator agreement for the human evaluation?
- references: Unanswerable | Unanswerable
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: The context does not provide the interannotator agreement for the human evaluation.
  top_chunk: rank=1 score=0.3259 The opinons expressed are those of the authors and do not represent the views of the institute or the U.S. Department of Education
- reorder_only_rag score: 0.0000
  prediction: Not provided
  top_chunk: rank=1 score=0.3259 The opinons expressed are those of the authors and do not represent the views of the institute or the U.S. Department of Education

#### qasper / 3de0487276bb5961586acc6e9f82934ef8cb668c

- query: What are the clinical datasets used in the paper?
- references: MEDDOCAN, NUBes-PHI | MEDDOCAN, NUBes
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 8.0000
  prediction: Two datasets are exploited in this article. Both datasets consist of plain text containing clinical narrative written in Spanish, and their respective manual annotations of sensitive information in BRAT standoff format. The first set of experiments uses the NUBes-PHI corpus, and the second set uses the MEDDOCAN 2019 shared task competition dataset.
  top_chunk: rank=1 score=0.4802 This section describes the data involved in the experiments and the systems evaluated. Finally, we introduce the experimental setup. Materials and Methods ::: Data Two datasets are exploited in this article. Both datasets consist of plain…
- reorder_only_rag score: 0.0000
  prediction: Two datasets are exploited in this article. Both datasets consist of plain text containing clinical narrative written in Spanish, and their respective manual annotations of sensitive information in BRAT standoff format.
  top_chunk: rank=1 score=0.4802 This section describes the data involved in the experiments and the systems evaluated. Finally, we introduce the experimental setup. Materials and Methods ::: Data Two datasets are exploited in this article. Both datasets consist of plain…

#### qasper / 10d450960907091f13e0be55f40bcb96f44dd074

- query: Is the template-based model realistic?
- references: Yes | Yes
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 14.2857
  prediction: Yes, the template-based model is realistic given the context of limited resources and small datasets.
  top_chunk: rank=1 score=0.4674 While the proposed template-based model was intended for data synthesis, with minor modification it can be adapted for summarization itself. Because the modifications introduce few parameters, the model is suitable for small datasets. Reca…
- reorder_only_rag score: 0.0000
  prediction: While the proposed template-based model was intended for data synthesis, with minor modification it can be adapted for summarization itself. Because the modifications introduce few parameters, the model is suitable for small datasets.
  top_chunk: rank=1 score=0.4674 While the proposed template-based model was intended for data synthesis, with minor modification it can be adapted for summarization itself. Because the modifications introduce few parameters, the model is suitable for small datasets. Reca…

### narrative_qa

- examples: 50
- disagreements: 36
- any-positive-score: 19

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_12

- query: Where is Herr professor from?
- references: Germany
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: German
  top_chunk: rank=1 score=0.2680 But at such a time as this there is always one person who seems interested in what I say--a German gentleman, a professor, who sits next to me at dinner, and whom I must tell you more about another time. He is very learned, and has a great…
- reorder_only_rag score: 0.0000
  prediction: He is a German gentleman.
  top_chunk: rank=1 score=0.2680 But at such a time as this there is always one person who seems interested in what I say--a German gentleman, a professor, who sits next to me at dinner, and whom I must tell you more about another time. He is very learned, and has a great…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_13

- query: Where is Leon Verdier from?
- references: France
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: French
  top_chunk: rank=1 score=0.3490 I am afraid you will never ask me again. CHAPTER VII FROM LEON VERDIER, IN PARIS, TO PROSPER GOBAIN, AT LILLE. September 28th. My Dear Prosper--It is a long time since I have given you of my news, and I don't know what puts it into my head…
- reorder_only_rag score: 0.0000
  prediction: New York
  top_chunk: rank=1 score=0.3490 I am afraid you will never ask me again. CHAPTER VII FROM LEON VERDIER, IN PARIS, TO PROSPER GOBAIN, AT LILLE. September 28th. My Dear Prosper--It is a long time since I have given you of my news, and I don't know what puts it into my head…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_17

- query: What name does Herr Professor call Leon?
- references: Simian
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: insatiable little Leon
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…
- reorder_only_rag score: 0.0000
  prediction: _dis donc, mon gras Prosper_
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_18

- query: Which traveler finds the other travelers "sub-human"?
- references: Herr Professor
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: He appears to me less human than simian, and whenever I hear him talk I seem to myself to have paused in the street to listen to the shrill clatter of a hand-organ, to which the gambols of a hairy _homunculus_ form an accompaniment.
  top_chunk: rank=1 score=0.3351 But this New England maiden is, in her way, a strange type: she is travelling all over Europe alone--"to see it," she says, "for herself." For herself! What can that stiff slim self of hers do with such sights, such visions!
- reorder_only_rag score: 0.0000
  prediction: This, I confess, has been something of a surprise to me, and I have not yet made up my mind as to the fundamental cause of the anomaly.
  top_chunk: rank=1 score=0.3351 But this New England maiden is, in her way, a strange type: she is travelling all over Europe alone--"to see it," she says, "for herself." For herself! What can that stiff slim self of hers do with such sights, such visions!

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_19

- query: What does Evelyn Vane claim Leverett is always talking about?
- references: The color of the sky
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: its being "a real Corot day," etc.
  top_chunk: rank=1 score=0.3699 You know I told you, in writing some time ago, that I had tried to get some insight into the position of woman in England, and, being here with Miss Vane, it has seemed to me to be a good opportunity to get a little more. I have asked her…
- reorder_only_rag score: 0.0000
  prediction: "a real Corot day" etc.
  top_chunk: rank=1 score=0.3699 You know I told you, in writing some time ago, that I had tried to get some insight into the position of woman in England, and, being here with Miss Vane, it has seemed to me to be a good opportunity to get a little more. I have asked her…

### quality

- examples: 50
- disagreements: 16
- any-positive-score: 28

#### quality / 30029_F5N22U40_4

- query: What is the most likely reason for Korvin's solitude in jail? (A) Solitary confinement was part of Korvin's punishment. (B) There weren't any other prisoners in the jail because virtually all of the Tr'en obey the Ruler. Those who don't obey are executed. (C) The Tr'en didn't want Korvin to interact with the other Tr'en prisoners because there was a chance that together they might incite an upris…
- references: There weren't any other prisoners in the jail because virtually all of the Tr'en obey the Ruler. Those who don't obey are executed.
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.5857 The Wonders of Tr'en, according to all the advance reports, were likely to be pretty boring, but they'd have been better than nothing. In any decently-run jail, he told himself with indignation, there would at least have been other prisone…
- reorder_only_rag score: 0.0000
  prediction: The Tr'en are so logical and mathematic that they don't see the need for social interaction
  top_chunk: rank=1 score=0.5857 The Wonders of Tr'en, according to all the advance reports, were likely to be pretty boring, but they'd have been better than nothing. In any decently-run jail, he told himself with indignation, there would at least have been other prisone…

#### quality / 52845_75VB1ISR_4

- query: Why did Blake create the three female super-images of Miss Stoddart, Officer Finch, and Vera Velvetskin? (A) He feels guilty about having slept with Eldoria which perpetuated the demand for female prostitution. (B) Even though he is a psycheye, he feels guilty about hunting down Sabrina York. (C) He is still grieving his mother's death and regrets not being a more loving son. (D) He feels guilty…
- references: He feels guilty about hurting Deirdre's feelings after her graduation when he ignored their romantic connection, and instead, played the part of a parent.
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Even though he is a psycheye, he feels guilty about hunting down Sabrina York.
  top_chunk: rank=1 score=0.6204 Therefore, even assuming that Blake was less well-adjusted than he considered himself to be, why had he created three such malevolent super-images as Miss Stoddart, Officer Finch, and Vera Velvetskin? They followed him off the campus into…
- reorder_only_rag score: 0.0000
  prediction: D
  top_chunk: rank=1 score=0.6204 Therefore, even assuming that Blake was less well-adjusted than he considered himself to be, why had he created three such malevolent super-images as Miss Stoddart, Officer Finch, and Vera Velvetskin? They followed him off the campus into…

#### quality / 62139_J05FWZR6_9

- query: What would've happened if the new cook had told the Skipper about the ekalastron deposits earlier? (A) The text doesn't indicate how the Skipper would've acted in a different scenario. (B) The Skipper still would've ignored the new cook's advice. (C) The Skipper would have mulled over the information for a few days before deciding to switch their course from Vesta to Iris. (D) The Skipper's would…
- references: The Skipper's would have set course for Iris from the beginning.
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: The text doesn't indicate how the Skipper would've acted in a different scenario.
  top_chunk: rank=1 score=0.5666 Why should there be?" "Well, for one thing," wrangled our pint-sized cook, "because rich ekalastron deposits were recently discovered on Vesta. For another, because Vesta's orbit is now going into aphelion stage, which will favor a concent…
- reorder_only_rag score: 0.0000
  prediction: The Skipper still would've ignored the new cook's advice.
  top_chunk: rank=1 score=0.5666 Why should there be?" "Well, for one thing," wrangled our pint-sized cook, "because rich ekalastron deposits were recently discovered on Vesta. For another, because Vesta's orbit is now going into aphelion stage, which will favor a concent…

#### quality / 62476_Z8GFDCIZ_2

- query: Did Duane actually kill Stevens? How do you know? (A) No, because even though he was attempting to kill Stevens, he blacked out before he had the chance. (B) No, because the nurse said that Stevens died of a head injury an hour before Duane woke up. (C) Yes, because once Duane woke up with amnesia, Andrias told him that he had killed Stevens. (D) Yes, because he shot Stevens with his dis-gun just…
- references: No, because even though he was attempting to kill Stevens, he blacked out before he had the chance.
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.6365 Duane got up, retrieving the two heat guns, and stared at him. " They tell me I killed Stevens the same way ," he thought. " I'm getting in a rut! " But Andrias was not dead, though he was out as cold as the void beyond Pluto. The thick ca…
- reorder_only_rag score: 0.0000
  prediction: No, because the nurse said that Stevens died of a head injury an hour before Duane woke up.
  top_chunk: rank=1 score=0.6365 Duane got up, retrieving the two heat guns, and stared at him. " They tell me I killed Stevens the same way ," he thought. " I'm getting in a rut! " But Andrias was not dead, though he was out as cold as the void beyond Pluto. The thick ca…

#### quality / 63401_ZCP5ZDGL_10

- query: What is the most likely reason that Johnathan decides to stay on the asteroid? (A) He realizes that his life as a pilot was unfulfilling, and he doesn't want to go back. (B) He realizes that he'd rather stay with wild women than travel back with the posh Doctor Boynton. (C) He realizes that he wants to stay and enjoy sexual relations with the twenty-seven beautiful women. (D) He realizes that if…
- references: He realizes that he wants to stay and enjoy sexual relations with the twenty-seven beautiful women.
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.5326 "I only came back here after the cigarettes." "But it will be three years before the asteroid's orbit brings it back in the space lanes," said Doctor Boynton. "You don't possibly expect to be picked up before then!" Jonathan shook his head…
- reorder_only_rag score: 0.0000
  prediction: D
  top_chunk: rank=1 score=0.5326 "I only came back here after the cigarettes." "But it will be three years before the asteroid's orbit brings it back in the space lanes," said Doctor Boynton. "You don't possibly expect to be picked up before then!" Jonathan shook his head…

### contract_nli

- examples: 50
- disagreements: 10
- any-positive-score: 36

#### contract_nli / 3_nda-11

- query: Receiving Party shall not reverse engineer any objects which embody Disclosing Party's Confidential Information.
- references: Entailment
- best_methods: reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5490 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
- reorder_only_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5490 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…

#### contract_nli / 3_nda-12

- query: Receiving Party may independently develop information similar to Confidential Information.
- references: Entailment
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5296 c) is lawfully disclosed or made available to the Receiving Party by a third party having no obligation to the Disclosing Party to maintain the confidentiality of such information; d) was independently developed or derived by the Receiving…
- reorder_only_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5296 c) is lawfully disclosed or made available to the Receiving Party by a third party having no obligation to the Disclosing Party to maintain the confidentiality of such information; d) was independently developed or derived by the Receiving…

#### contract_nli / 3_nda-13

- query: Receiving Party may acquire information similar to Confidential Information from a third party.
- references: Entailment
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5225 The Receiving Party undertakes to permit access to the Confidential Information only to its Representatives or employees who require access to such Information solely for the fulfilment of the Permitted Purpose, and furnished on a need-to-…
- reorder_only_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5225 The Receiving Party undertakes to permit access to the Confidential Information only to its Representatives or employees who require access to such Information solely for the fulfilment of the Permitted Purpose, and furnished on a need-to-…

#### contract_nli / 3_nda-15

- query: Agreement shall not grant Receiving Party any right to Confidential Information.
- references: Entailment
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.6255 The Receiving Party undertakes to permit access to the Confidential Information only to its Representatives or employees who require access to such Information solely for the fulfilment of the Permitted Purpose, and furnished on a need-to-…
- reorder_only_rag score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.6255 The Receiving Party undertakes to permit access to the Confidential Information only to its Representatives or employees who require access to such Information solely for the fulfilment of the Permitted Purpose, and furnished on a need-to-…

#### contract_nli / 3_nda-17

- query: Receiving Party may create a copy of some Confidential Information in some circumstances.
- references: Entailment
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5584 The Receiving Party may retain one (1) copy of any such Confidential Information to be stored securely with its legal representative only if required for regulatory or insurance purposes, but in this event the confidentiality and non-use p…
- reorder_only_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5584 The Receiving Party may retain one (1) copy of any such Confidential Information to be stored securely with its legal representative only if required for regulatory or insurance purposes, but in this event the confidentiality and non-use p…
