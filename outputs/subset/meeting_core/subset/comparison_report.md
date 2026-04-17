# Comparison Report

Run tier: `subset`

## Score Summary

| Task | Metric | vanilla_rag | dos_rag | dos_rag_minus_vanilla_rag |
| --- | --- | --- | --- | --- |
| qmsum | rouge | 16.6505 | 18.2178 | +1.5673 |
| qasper | f1 | 51.4486 | 54.4233 | +2.9747 |
| narrative_qa | f1 | 19.5300 | 21.6398 | +2.1098 |
| quality | exact_match | 70.0000 | 78.0000 | +8.0000 |
| contract_nli | exact_match | 72.0000 | 66.0000 | -6.0000 |

## Example Previews

### qmsum

- examples: 50
- disagreements: 50
- any-positive-score: 49

#### qmsum / va-sq-1

- query: What was agreed upon on sample transcripts?
- references: To save time, speaker mn005 will only mark the sample of transcribed data for regions of overlapping speech, as opposed to marking all acoustic events. The digits extraction task will be delegated to whomever is working on acoustics for the Meeting Recorder project.
- best_methods: vanilla_rag, dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Based on the provided context, it seems that there was a forty-five minute piece that Jane transcribed, which was then sent to IBM for transcription to have a comparison point. Additionally, there was a larger piece recorded and sent to IBM on CD-ROM, but the status of its transcription is uncertain. The team agreed to have some ground truth first from manual marking to ensure accuracy before pro…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- dos_rag score: 0.0000
  prediction: Based on the provided context, the agreed-upon points regarding sample transcripts are: 1. A piece of forty-five minutes was transcribed by Jane and sent to IBM for comparison. 2. There is a larger piece of recorded data (about ten hours) that has been sent to IBM on CD-ROM for transcription. 3. The group aims to record three to four meetings per week, each about an hour long, to gather more data…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…

#### qmsum / va-gq-5

- query: What were the main discussion points of the meeting?
- references: The group discussed topics including a potential collaboration with another ICSI member regarding the analysis of inference structures, efforts by speaker mn005 to detect speaker overlap, the current status of recordings and transcriptions, and future efforts to collect meeting data. In addition to weekly meetings by the BMR group, efforts are in progress to record meetings by other ICSI research…
- best_methods: dos_rag
- disagreement: True
- vanilla_rag score: 6.1729
  prediction: The main discussion points of the meeting included: 1. The need for a Meeting Recorder to document discussions and decisions made in meetings. 2. The challenges of recording meetings, especially those with strong differences of opinion or involving managers. 3. The idea of recording meetings that have more emotional or conflict-driven aspects. 4. The amount of data collected and the progress of t…
  top_chunk: rank=1 score=0.3285 Uh , we {disfmarker} I think the things that we talk about in this meeting uh tend to be a mixture of uh procedural uh mundane things and uh research points and um I was thinking I think it was a meeting a couple of weeks ago that we {disf…
- dos_rag score: 7.0029
  prediction: The main discussion points of the meeting were: 1. The issue of the software crashing when started and stopped repeatedly was identified and resolved by the participant's decision to stop doing that. 2. The process of collecting digit forms and the procedure for reading them out was discussed. 3. The professor suggested an agenda for the meeting, proposing to separate mundane procedural discussio…
  top_chunk: rank=1 score=0.3285 Uh , we {disfmarker} I think the things that we talk about in this meeting uh tend to be a mixture of uh procedural uh mundane things and uh research points and um I was thinking I think it was a meeting a couple of weeks ago that we {disf…

#### qmsum / va-sq-2

- query: What was said on speech overlap?
- references: Efforts by speaker mn005 are in progress to detect overlapping speech. For a single transcribed meeting, speaker mn005 reported approximately 300 cases of overlap. Future work will involve manually deriving time marks from sections of overlapping speech for the same meeting, and then experimenting with different measures, e.g. energy increase, to determine a set of acoustically salient features f…
- best_methods: dos_rag
- disagreement: True
- vanilla_rag score: 5.2958
  prediction: The context discusses several aspects of speech overlap in a research setting: 1. **Definition and Counting Overlaps**: PhD D mentions finding three hundred speaker overlaps in a forty-five-minute session, and later, in twelve minutes, finds one thousand acoustic events, including overlaps. There is a discussion about whether to count each overlap involving multiple speakers as one event or multi…
  top_chunk: rank=1 score=0.4702 Eh almost eh three hundred eh in one session Grad G: Oh , God ! PhD D: in five {disfmarker} eh in forty - five minutes . PhD A: Three hundred overlapping speech {disfmarker} PhD D: Alm - Three hundred overlapping zone . Grad G: Ugh . PhD C…
- dos_rag score: 8.1918
  prediction: The context discusses several aspects of speech overlap in a research project. PhD D was studying overlapping speech zones and had found around three hundred overlapping speech zones in a forty-five-minute session. The team was considering how to define and count speech overlaps, with PhD D considering an entire overlapping zone as one event regardless of the number of speakers involved. The team…
  top_chunk: rank=1 score=0.4653 Eh almost eh three hundred eh in one session Grad G: Oh , God ! PhD D: in five {disfmarker} eh in forty - five minutes . PhD A: Three hundred overlapping speech {disfmarker} PhD D: Alm - Three hundred overlapping zone . Grad G: Ugh . PhD C…

#### qmsum / va-sq-46

- query: What were the problems encountered with SmartKom system?
- references: The translation of SmartKom to english is in its final stages. The synthesis module will be the last one to do, after the english syntax trees are completed. The system is still buggy and unstable, but it will soon be ready for a demonstration.
- best_methods: dos_rag
- disagreement: True
- vanilla_rag score: 7.0147
  prediction: Based on the provided context, the SmartKom system encountered several issues: 1. The system was not functioning properly, as indicated by the statement "the version {disfmarker} that is, the full version that's on the server d does not work." 2. The system required a lot of setup and changes to operate, as mentioned "you need to do a lot of stuff to make it work." 3. The synthesis module was usi…
  top_chunk: rank=1 score=0.3394 The {disfmarker} we got to the point where we can now speak into the SmartKom system , and it 'll go all the way through and then say something like " Roman numeral one , am Smarticus . " It actually says , " Roemisch einz , am Smarticus ,…
- dos_rag score: 8.6833
  prediction: The SmartKom system encountered several issues, including instability and the need for numerous adjustments to function properly. Specifically, it was noted that the full version of the system on the server did not work and required a lot of tweaking to make it operational. Additionally, the system was designed with shortcuts for an October version, indicating that a fully functioning version wit…
  top_chunk: rank=1 score=0.3394 The {disfmarker} we got to the point where we can now speak into the SmartKom system , and it 'll go all the way through and then say something like " Roman numeral one , am Smarticus . " It actually says , " Roemisch einz , am Smarticus ,…

#### qmsum / va-sq-18

- query: Summarize the group's plan of their marketing strategy.
- references: For fear that the exorbitant price of 25 euros of the remote control would shock the potential consumers, Project Manager proposed to trade off some functions for a lower price. Additionally, Project Manager mentioned an American computer electronics store to show that shipping products overseas can also make profits and then added this to the whole plan.
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 9.5690
  prediction: The group's plan for their marketing strategy includes making a universal remote control that is fashionable and stylish, aiming to take ordinary items and make them appealing, similar to the quality found in stores like John Lewis or Debenham's. They aim to balance functionality with a sleek design, possibly incorporating a touch screen or multi-format features. The remote should be user-friendl…
  top_chunk: rank=1 score=0.3665 if you wanna write all five go for it but name one of them that you could um . Oh , we skipped introductions . Nice . I'm a excellent Project Manager . Um . Marketing: {vocalsound} Project Manager: I'm Marty , Industrial Designer: {vocalso…
- dos_rag score: 6.6347
  prediction: The group discussed that their marketing strategy needs to carefully consider the target audience, particularly noting that certain demographics, like older users, might be more accustomed to traditional button-based remotes. They also mentioned the importance of balancing the remote's features and price point to avoid making it too expensive, like a forty Euro remote, which could be seen as too…
  top_chunk: rank=1 score=0.3665 if you wanna write all five go for it but name one of them that you could um . Oh , we skipped introductions . Nice . I'm a excellent Project Manager . Um . Marketing: {vocalsound} Project Manager: I'm Marty , Industrial Designer: {vocalso…

### qasper

- examples: 50
- disagreements: 33
- any-positive-score: 46

#### qasper / 71e4ba4e87e6596aeca187127c0d088df6570c57

- query: What evaluations methods do they take?
- references: Unanswerable | Unanswerable
- best_methods: vanilla_rag, dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: manually detect stereotypes, biases, and odd phrases Leverage the structure of Flickr30K Entities Use Louvain clustering on the coreference graph Tag all descriptions with part-of-speech information
  top_chunk: rank=1 score=0.2777 A next step would be to see whether these observations also hold for other age groups, i.e. children and adults. INLINEFORM0 Other methods It may be difficult to spot patterns by just looking at a collection of images. Another method is to…
- dos_rag score: 0.0000
  prediction: manual detection, part-of-speech tagging, coreference graph analysis
  top_chunk: rank=1 score=0.2593 I will build on earlier work on linguistic bias in general BIBREF3 , providing examples from the Flickr30K data, and present a taxonomy of unwarranted inferences. Finally, I will discuss several methods to analyze the data in order to dete…

#### qasper / a313e98994fc039a82aa2447c411dda92c65a470

- query: How do they match words before reordering them?
- references: Unanswerable | CFILT-preorder system
- best_methods: vanilla_rag, dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: using a bilingual dictionary (Google Translate word translation in our case)
  top_chunk: rank=1 score=0.4351 One of the pre-ordering rule swaps the position of the noun phrase followed by a transitive verb with the transitive verb. The original and the resulting re-ordered parse tree will be as shown in the Table TABREF5 . Applying this reorderin…
- dos_rag score: 0.0000
  prediction: They translate each word in the source language into English using a bilingual dictionary (Google Translate word translation in their case).
  top_chunk: rank=1 score=0.4591 We also found that these embeddings were not useful for transfer learning. We use the CFILT-preorder system for reordering English sentences to match the Indian language word order. It contains two re-ordering systems: (1) generic rules th…

#### qasper / 2df4a045a9cd7b44874340b6fdf9308d3c55327a

- query: What crowdsourcing platform is used?
- references: Unanswerable | They did not use any platform, instead they hired undergraduate students to do the annotation.
- best_methods: dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Amazon Mechanical Turk
  top_chunk: rank=1 score=0.4819 Our work is similar to these work but is applies on crowdsourcing learning, aiming to find invariant features among different crowdsourcing workers. Crowdsourcing. Most NLP tasks require a massive amount of labeled training data which are…
- dos_rag score: 25.0000
  prediction: undergraduate students
  top_chunk: rank=1 score=0.4819 Our work is similar to these work but is applies on crowdsourcing learning, aiming to find invariant features among different crowdsourcing workers. Crowdsourcing. Most NLP tasks require a massive amount of labeled training data which are…

#### qasper / d9b6c61fc6d29ad399d27b931b6cb7b1117b314a

- query: Where is a question generation model used?
- references: The question generation model provides each candidate answer with a score by measuring semantic relevance between the question and the generated question based on the semantics of the candidate answer. | framework consisting of both a question answering model and a question generation model
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 91.6667
  prediction: in our framework consisting of both a question answering model and a question generation model
  top_chunk: rank=1 score=0.5894 16) The Question Generation Model In this section, we present the generation model which generates a question based on the semantics of a candidate answer. Afterward, we introduce how our paraphrasing model, which measures the semantic rel…
- dos_rag score: 0.0000
  prediction: In the generative models approach
  top_chunk: rank=1 score=0.5894 16) The Question Generation Model In this section, we present the generation model which generates a question based on the semantics of a candidate answer. Afterward, we introduce how our paraphrasing model, which measures the semantic rel…

#### qasper / c0bee6539eb6956a7347daa9d2419b367bd02064

- query: Does BERT reach the best performance among all the algorithms compared?
- references: No | No
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 100.0000
  prediction: No
  top_chunk: rank=1 score=0.5670 A fact worth highlighting is that, according to these results, BERT achieves a precision lower than the rest of the systems (i.e., it makes more false positive predictions); in exchange, it obtains a remarkably higher recall. Noticeably, i…
- dos_rag score: 0.0000
  prediction: Yes
  top_chunk: rank=1 score=0.5765 To finish with this experiment set, Table also shows the strict classification precision, recall and F1-score for the compared systems. Despite the fact that, in general, the systems obtain high values, BERT outperforms them again. BERT's…

### narrative_qa

- examples: 50
- disagreements: 34
- any-positive-score: 24

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
  prediction: German
  top_chunk: rank=1 score=0.2748 he bursts out laughing so loud that all the plates clatter on the table. But at such a time as this there is always one person who seems interested in what I say--a German gentleman, a professor, who sits next to me at dinner, and whom I m…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_16

- query: What is William Platt's relationship to Miranda Hope?
- references: Platt is a Miranda's suitor | a previous suitor
- best_methods: vanilla_rag, dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: unclear from the context provided
  top_chunk: rank=1 score=0.3804 I try to talk with Madame de Maisonrouge all I can (she is the lady of the house, and the _real_ family consists only of herself and her two daughters). They are all most elegant, interesting women, and I am sure we shall become intimate f…
- dos_rag score: 0.0000
  prediction: not specified in the text
  top_chunk: rank=1 score=0.3806 I try to talk with Madame de Maisonrouge all I can (she is the lady of the house, and the _real_ family consists only of herself and her two daughters). They are all most elegant, interesting women, and I am sure we shall become intimate f…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_17

- query: What name does Herr Professor call Leon?
- references: Simian
- best_methods: vanilla_rag, dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: insatiable little Leon
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…
- dos_rag score: 0.0000
  prediction: intellectual broom
  top_chunk: rank=1 score=0.2915 he bursts out laughing so loud that all the plates clatter on the table. But at such a time as this there is always one person who seems interested in what I say--a German gentleman, a professor, who sits next to me at dinner, and whom I m…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_2

- query: Which character does Herr Professor refer to as "simian"?
- references: The frenchman Leon Verdier. | Leon
- best_methods: vanilla_rag, dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: the remaining figure is apparently that of a man, but I hesitate to classify him so superficially. He appears to me less human than simian
  top_chunk: rank=1 score=0.3908 The remaining figure is apparently that of a man, but I hesitate to classify him so superficially. He appears to me less human than simian, and whenever I hear him talk I seem to myself to have paused in the street to listen to the shrill…
- dos_rag score: 0.0000
  prediction: He appears to me less human than simian, and whenever I hear him talk I seem to myself to have paused in the street to listen to the shrill clatter of a hand-organ, to which the gambols of a hairy homunculus form an accompaniment. The character referred to as "simian" is not explicitly named but is described as a French-speaking individual in the context provided.
  top_chunk: rank=1 score=0.3824 He appears to me less human than simian, and whenever I hear him talk I seem to myself to have paused in the street to listen to the shrill clatter of a hand-organ, to which the gambols of a hairy _homunculus_ form an accompaniment. I ment…

### quality

- examples: 50
- disagreements: 12
- any-positive-score: 41

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
  top_chunk: rank=1 score=0.5583 But, then, it was lack of that insight that had called for this particular plan. That, and the political structure of the Tr'en. The same lack of insight let the Tr'en subconscious work on his escape without any annoying distractions in th…

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
  top_chunk: rank=1 score=0.6603 But these, and other, similar, cases, had to do with mal-adjusted people, and moreover, the super-image in each instance had been an image that the person involved had wanted to create. Therefore, even assuming that Blake was less well-adj…

#### quality / 62476_Z8GFDCIZ_2

- query: Did Duane actually kill Stevens? How do you know? (A) No, because even though he was attempting to kill Stevens, he blacked out before he had the chance. (B) No, because the nurse said that Stevens died of a head injury an hour before Duane woke up. (C) Yes, because once Duane woke up with amnesia, Andrias told him that he had killed Stevens. (D) Yes, because he shot Stevens with his dis-gun just…
- references: No, because even though he was attempting to kill Stevens, he blacked out before he had the chance.
- best_methods: vanilla_rag, dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: No, because the nurse said that Stevens died of a head injury an hour before Duane woke up.
  top_chunk: rank=1 score=0.6365 Duane got up, retrieving the two heat guns, and stared at him. " They tell me I killed Stevens the same way ," he thought. " I'm getting in a rut! " But Andrias was not dead, though he was out as cold as the void beyond Pluto. The thick ca…
- dos_rag score: 0.0000
  prediction: Yes, because he shot Stevens with his dis-gun just before he blacked out.
  top_chunk: rank=1 score=0.6423 But Andrias, unconscious already, tumbled back with Duane on top of him. His head made an audible, spine-chilling thud as it hit the carpeted floor. Duane got up, retrieving the two heat guns, and stared at him. " They tell me I killed Ste…

#### quality / 63401_ZCP5ZDGL_4

- query: What was Ann intending to do with Johnathan under the trees before the other women showed up? (A) Sleep with him. (B) Convince him to help her cook dinner. (C) Ask him to be her boyfriend. (D) Talk to him about how he became a pilot.
- references: Sleep with him.
- best_methods: vanilla_rag, dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Convince him to help her cook dinner.
  top_chunk: rank=1 score=0.4963 He started to rise. Ann Clotilde placed the flat of her hand on his chest and shoved. " Ooof! " he grunted. He sat down rather more forcibly than he had risen. "Don't get up because of me," she informed him. "It's my turn to cook, but I sa…
- dos_rag score: 0.0000
  prediction: C
  top_chunk: rank=1 score=0.4381 "It's my turn to cook, but I saw you out here beneath the trees. Dinner can wait. Jonathan do you know that you are irresistible?" She seized his shoulders, stared into his eyes. He couldn't have felt any more uncomfortable had a hungry bo…

#### quality / 30029_F5N22U40_3

- query: How was Korvin able to avoid disclosing the true intent of his mission under the lie detector questioning? (A) While he was strapped down in the lie-detector, Korvin subtly switched the wire that indicated a truth with the one that indicated a lie. (B) Korvin said truths that literally answered the Tr'en's questions but evaded the intent behind their questions. . (C) The Tr'en hadn't tested the l…
- references: Korvin said truths that literally answered the Tr'en's questions but evaded the intent behind their questions. .
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 100.0000
  prediction: Korvin said truths that literally answered the Tr'en's questions but evaded the intent behind their questions.
  top_chunk: rank=1 score=0.5941 True, every night the guards came in and gave him a concentrated lesson in the local language, but Korvin failed to get much pleasure out of that, being unconscious at the time. But now he was equipped to discuss almost anything from philo…
- dos_rag score: 0.0000
  prediction: B Korvin said truths that literally answered the Tr'en's questions but evaded the intent behind their questions.
  top_chunk: rank=1 score=0.6747 The Ruler flashed a look at the technicians handling the lie-detector. Korvin turned to see their expression. They needed no words; the lie-detector was telling them, perfectly obviously, that he was speaking the truth. But the truth wasn'…

### contract_nli

- examples: 50
- disagreements: 8
- any-positive-score: 38

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
  top_chunk: rank=1 score=0.5750 2. Nondisclosure. Nothing in this Agreement may be construed to allow any Party to maintain, use, disclose, or share Confidential Information in a manner not allowed under federal or state law or regulation, or outside the scope of this ag…

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
  top_chunk: rank=1 score=0.5338 or becomes public knowledge after such disclosure, through no action or omission by or on behalf of the Receiving Party; c) is lawfully disclosed or made available to the Receiving Party by a third party having no obligation to the Disclos…

#### contract_nli / 3_nda-13

- query: Receiving Party may acquire information similar to Confidential Information from a third party.
- references: Entailment
- best_methods: dos_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5225 The Receiving Party undertakes to permit access to the Confidential Information only to its Representatives or employees who require access to such Information solely for the fulfilment of the Permitted Purpose, and furnished on a need-to-…
- dos_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5308 or becomes public knowledge after such disclosure, through no action or omission by or on behalf of the Receiving Party; c) is lawfully disclosed or made available to the Receiving Party by a third party having no obligation to the Disclos…

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
