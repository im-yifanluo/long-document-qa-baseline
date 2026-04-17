# Comparison Report

Run tier: `subset`

## Score Summary

| Task | Metric | vanilla_rag | reorder_only_rag | reorder_only_rag_minus_vanilla_rag |
| --- | --- | --- | --- | --- |
| qmsum | rouge | 16.1329 | 17.1944 | +1.0615 |
| qasper | f1 | 36.6376 | 40.9533 | +4.3157 |
| narrative_qa | f1 | 10.5847 | 10.9790 | +0.3943 |
| quality | exact_match | 48.0000 | 62.0000 | +14.0000 |
| contract_nli | exact_match | 70.0000 | 58.0000 | -12.0000 |

## Runtime Summary

| Method | Total seconds | Total minutes | Seconds / example | Examples / second |
| --- | --- | --- | --- | --- |
| vanilla_rag | 541.81 | 9.03 | 2.1672 | 0.4614 |
| reorder_only_rag | 518.87 | 8.65 | 2.0755 | 0.4818 |

## Example Previews

### qmsum

- examples: 50
- disagreements: 50
- any-positive-score: 50

#### qmsum / va-sq-4

- query: What was the future of data collection?
- references: The group aims to collect over 100 hours of Meeting Recorder data in total. Speaker consent forms are being revised. It was suggested that subjects should sign a new consent form after 10 recording sessions.
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 7.4021
  prediction: The future of data collection involves continuing to gather audio data from meetings, with the goal of collecting significantly more than a hundred hours. Professor E suggested that if they can keep recording meetings for a few months, they could have around a hundred hours of data. They also discussed the possibility of recording meetings at the University of Washington (UW) and other groups on…
  top_chunk: rank=1 score=0.3866 I wanted to ask another a a aspect of the data collection . There 'd be no reason why a person couldn't get together several uh , you know , friends , and come and argue about a topic if they wanted to , right ?
- reorder_only_rag score: 5.8775
  prediction: The future of data collection involved expanding the current setup to collect more data. Professor E mentioned that they were aiming to collect significantly more than a hundred hours of data, with the goal of having at least thirty to fifty hours by the end of the semester and continuing to collect more in the next semester. They also discussed the possibility of recording meetings at other loca…
  top_chunk: rank=1 score=0.3866 I wanted to ask another a a aspect of the data collection . There 'd be no reason why a person couldn't get together several uh , you know , friends , and come and argue about a topic if they wanted to , right ?

#### qmsum / va-sq-47

- query: What demos would the system be involved in?
- references: The final english SmartKom demo will be presented to the whole institute once the system is de-bugged and stabilised.
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 7.9320
  prediction: The system would be involved in demos for the Fall, with requirements taken care of by later that week or so. There's also mention of a larger effort with formalization stuff, and a plan to have a talk in the big room as an institute-wide thing, which could involve showing a demo version of a project. Additionally, there's a belief-net demo level being thought of, and the system needs to fit into…
  top_chunk: rank=1 score=0.3783 Professor C: and , s deliberately . So , the reason I 'd like you to understand uh what 's going on in this demo system is not because it 's important to the research . It 's just for closure . So that if we come up with a question of " co…
- reorder_only_rag score: 6.9783
  prediction: The system would be involved in demos for funding purposes, specifically to show that the project is making progress and to provide the necessary demonstrations as outlined in the contracts. Professor C mentions that the demos for that Fall are "sort of taken care of as of later this week or something," and there won't be another serious demo requirement for about fifteen months. However, the tea…
  top_chunk: rank=1 score=0.3783 Professor C: and , s deliberately . So , the reason I 'd like you to understand uh what 's going on in this demo system is not because it 's important to the research . It 's just for closure . So that if we come up with a question of " co…

#### qmsum / va-sq-1

- query: What was agreed upon on sample transcripts?
- references: To save time, speaker mn005 will only mark the sample of transcribed data for regions of overlapping speech, as opposed to marking all acoustic events. The digits extraction task will be delegated to whomever is working on acoustics for the Meeting Recorder project.
- best_methods: reorder_only_rag
- disagreement: True
- vanilla_rag score: 7.2225
  prediction: Based on the provided context, it was agreed that there is a need to compare the manual transcripts with the IBM-transcribed versions for quality and accuracy. Specifically, Professor E mentioned that there is a forty-five-minute piece that Jane transcribed, which was then sent to IBM for transcription, providing a comparison point. Additionally, a larger piece has been recorded and put on CD-ROM…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- reorder_only_rag score: 7.9643
  prediction: Based on the provided context, there is no explicit agreement mentioned regarding sample transcripts. The discussion revolves around the transcription process, the need for ground truth data, and the challenges of transcribing overlapping speech. However, it is mentioned that there is a forty-five-minute piece of transcription that has been sent to IBM for comparison, and there are ten hours of r…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…

#### qmsum / va-gq-5

- query: What were the main discussion points of the meeting?
- references: The group discussed topics including a potential collaboration with another ICSI member regarding the analysis of inference structures, efforts by speaker mn005 to detect speaker overlap, the current status of recordings and transcriptions, and future efforts to collect meeting data. In addition to weekly meetings by the BMR group, efforts are in progress to record meetings by other ICSI research…
- best_methods: reorder_only_rag
- disagreement: True
- vanilla_rag score: 6.6880
  prediction: The main discussion points of the meeting included: 1. **Recording Meetings**: There was a discussion about recording meetings, particularly those of the Network Services and Applications group, and possibly other meetings at ICSI that have some emotional aspects or conflicts. 2. **Data Collection and Analysis**: The group talked about the data collected so far, including overlaps in speech and t…
  top_chunk: rank=1 score=0.3285 Uh , we {disfmarker} I think the things that we talk about in this meeting uh tend to be a mixture of uh procedural uh mundane things and uh research points and um I was thinking I think it was a meeting a couple of weeks ago that we {disf…
- reorder_only_rag score: 8.0123
  prediction: The main discussion points of the meeting included: 1. **Data Collection and Analysis**: The group discussed the ongoing data collection, particularly focusing on the number of speaker overlaps and the time-consuming nature of transcribing and analyzing the data. They debated whether to focus on marking only speaker overlaps or to include other types of events. 2. **Meeting Recorder and Transcrip…
  top_chunk: rank=1 score=0.3285 Uh , we {disfmarker} I think the things that we talk about in this meeting uh tend to be a mixture of uh procedural uh mundane things and uh research points and um I was thinking I think it was a meeting a couple of weeks ago that we {disf…

#### qmsum / va-sq-46

- query: What were the problems encountered with SmartKom system?
- references: The translation of SmartKom to english is in its final stages. The synthesis module will be the last one to do, after the english syntax trees are completed. The system is still buggy and unstable, but it will soon be ready for a demonstration.
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 8.1051
  prediction: Based on the provided context, some problems encountered with the SmartKom system include: 1. **Language-Specific Issues**: The system uses a German synthesis module for English sentences, which means it has limitations when dealing with English. For example, it struggles with certain constructions and requires additional work to make it function properly for English. 2. **Complexity and Engineer…
  top_chunk: rank=1 score=0.3394 The {disfmarker} we got to the point where we can now speak into the SmartKom system , and it 'll go all the way through and then say something like " Roman numeral one , am Smarticus . " It actually says , " Roemisch einz , am Smarticus ,…
- reorder_only_rag score: 6.8607
  prediction: Based on the provided context, some problems encountered with the SmartKom system include: 1. The system was unstable and required significant manual intervention to make it work. For instance, it needed to be started up and then had to go through 20 changes across 17 modules before it could function properly. 2. The system synthesis was limited to a German synthesis module for English sentences,…
  top_chunk: rank=1 score=0.3394 The {disfmarker} we got to the point where we can now speak into the SmartKom system , and it 'll go all the way through and then say something like " Roman numeral one , am Smarticus . " It actually says , " Roemisch einz , am Smarticus ,…

### qasper

- examples: 50
- disagreements: 41
- any-positive-score: 44

#### qasper / 71e4ba4e87e6596aeca187127c0d088df6570c57

- query: What evaluations methods do they take?
- references: Unanswerable | Unanswerable
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: To get an idea of the kinds of stereotype-driven descriptions that are in the Flickr30K dataset, I made a browser-based annotation tool that shows both the images and their associated descriptions.
  top_chunk: rank=1 score=0.2777 A next step would be to see whether these observations also hold for other age groups, i.e. children and adults. INLINEFORM0 Other methods It may be difficult to spot patterns by just looking at a collection of images. Another method is to…
- reorder_only_rag score: 0.0000
  prediction: In order to get an idea of the kinds of stereotype-driven descriptions that are in the Flickr30K dataset, I made a browser-based annotation tool that shows both the images and their associated descriptions. Another method is to tag all descriptions with part-of-speech information, so that it becomes possible to see e.g. which adjectives are most commonly used for particular nouns. One method read…
  top_chunk: rank=1 score=0.2777 A next step would be to see whether these observations also hold for other age groups, i.e. children and adults. INLINEFORM0 Other methods It may be difficult to spot patterns by just looking at a collection of images. Another method is to…

#### qasper / a313e98994fc039a82aa2447c411dda92c65a470

- query: How do they match words before reordering them?
- references: Unanswerable | CFILT-preorder system
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: They match words before reordering them by applying pre-ordering rules that swap the position of the noun phrase followed by a transitive verb with the transitive verb.
  top_chunk: rank=1 score=0.4351 One of the pre-ordering rule swaps the position of the noun phrase followed by a transitive verb with the transitive verb. The original and the resulting re-ordered parse tree will be as shown in the Table TABREF5 . Applying this reorderin…
- reorder_only_rag score: 0.0000
  prediction: For representing English and other source languages into a common space, we translate each word in the source language into English using a bilingual dictionary (Google Translate word translation in our case).
  top_chunk: rank=1 score=0.4351 One of the pre-ordering rule swaps the position of the noun phrase followed by a transitive verb with the transitive verb. The original and the resulting re-ordered parse tree will be as shown in the Table TABREF5 . Applying this reorderin…

#### qasper / c0bee6539eb6956a7347daa9d2419b367bd02064

- query: Does BERT reach the best performance among all the algorithms compared?
- references: No | No
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: The BERT-based model shows the highest robustness to training-data scarcity, loosing only 7 points of F1-score when trained on 230 instances instead of 21,371. These observation are in line with the results obtained by the NLP community using BERT for other tasks.
  top_chunk: rank=1 score=0.5670 A fact worth highlighting is that, according to these results, BERT achieves a precision lower than the rest of the systems (i.e., it makes more false positive predictions); in exchange, it obtains a remarkably higher recall. Noticeably, i…
- reorder_only_rag score: 0.0000
  prediction: In NUBes-PHI, the BERT-based model outperforms the other systems without requiring any adaptation or domain-specific feature engineering, just by being trained on the provided labelled data.
  top_chunk: rank=1 score=0.5670 A fact worth highlighting is that, according to these results, BERT achieves a precision lower than the rest of the systems (i.e., it makes more false positive predictions); in exchange, it obtains a remarkably higher recall. Noticeably, i…

#### qasper / c0e341c4d2253eb42c8840381b082aae274eddad

- query: What is te core component for KBQA?
- references: answer questions by obtaining information from KB tuples | hierarchical matching between questions and relations with residual learning
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: relation detection
  top_chunk: rank=1 score=0.4426 The KBQA system in the figure performs two key tasks: (1) entity linking, which links $n$ -grams in questions to KB entities, and (2) relation detection, which identifies the KB relation(s) a question refers to. The main focus of this work…
- reorder_only_rag score: 0.0000
  prediction: improved relation detection model
  top_chunk: rank=1 score=0.4426 The KBQA system in the figure performs two key tasks: (1) entity linking, which links $n$ -grams in questions to KB entities, and (2) relation detection, which identifies the KB relation(s) a question refers to. The main focus of this work…

#### qasper / fb2b536dc8e442dffab408db992b971e86548158

- query: What is the interannotator agreement for the human evaluation?
- references: Unanswerable | Unanswerable
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: The context does not provide information about interannotator agreement for the human evaluation.
  top_chunk: rank=1 score=0.3259 The opinons expressed are those of the authors and do not represent the views of the institute or the U.S. Department of Education
- reorder_only_rag score: 0.0000
  prediction: Not provided in the context.
  top_chunk: rank=1 score=0.3259 The opinons expressed are those of the authors and do not represent the views of the institute or the U.S. Department of Education

### narrative_qa

- examples: 50
- disagreements: 42
- any-positive-score: 25

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_0

- query: Which character comes from Bangor, Maine?
- references: Miranda Hope.
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Clara Barnard
  top_chunk: rank=1 score=0.4464 I wonder if she doesn't think me refined--or if she had ever heard anything against Bangor? I can't think it is that. Don't you remember when Clara Barnard went to visit New York, three years ago, how much attention she received? And you k…
- reorder_only_rag score: 0.0000
  prediction: Mamma
  top_chunk: rank=1 score=0.4464 I wonder if she doesn't think me refined--or if she had ever heard anything against Bangor? I can't think it is that. Don't you remember when Clara Barnard went to visit New York, three years ago, how much attention she received? And you k…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_1

- query: Where is the boarding-house located?
- references: Paris
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house.
  top_chunk: rank=1 score=0.3975 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…
- reorder_only_rag score: 0.0000
  prediction: in the Faubourg St. Germain
  top_chunk: rank=1 score=0.3975 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_11

- query: Where is Violet Ray from?
- references: New York
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Paris
  top_chunk: rank=1 score=0.4222 FROM MISS VIOLET RAY, IN PARIS, TO MISS AGNES RICH, IN NEW YORK. September 21st. We had hardly got here when father received a telegram saying he would have to come right back to New York. It was for something about his business--I don't k…
- reorder_only_rag score: 0.0000
  prediction: Bangor
  top_chunk: rank=1 score=0.4222 FROM MISS VIOLET RAY, IN PARIS, TO MISS AGNES RICH, IN NEW YORK. September 21st. We had hardly got here when father received a telegram saying he would have to come right back to New York. It was for something about his business--I don't k…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_17

- query: What name does Herr Professor call Leon?
- references: Simian
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: insatiable little Leon
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…
- reorder_only_rag score: 0.0000
  prediction: exceedingly foreign
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_18

- query: Which traveler finds the other travelers "sub-human"?
- references: Herr Professor
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: She has a way of arriving at her ends which is more efficient than violence.
  top_chunk: rank=1 score=0.3351 But this New England maiden is, in her way, a strange type: she is travelling all over Europe alone--"to see it," she says, "for herself." For herself! What can that stiff slim self of hers do with such sights, such visions!
- reorder_only_rag score: 0.0000
  prediction: He appears to me less human than simian, and whenever I hear him talk I seem to myself to have paused in the street to listen to the shrill clatter of a hand-organ, to which the gambols of a hairy _homunculus_ form an accompaniment.
  top_chunk: rank=1 score=0.3351 But this New England maiden is, in her way, a strange type: she is travelling all over Europe alone--"to see it," she says, "for herself." For herself! What can that stiff slim self of hers do with such sights, such visions!

### quality

- examples: 50
- disagreements: 15
- any-positive-score: 32

#### quality / 30029_F5N22U40_6

- query: Are there indications that the Tr'en would be interested in attacking Earth? Why or why not? (A) Both A and C are correct. (B) No, because Korvin sends a mission back to Earth Central saying that the Tr'en won't come marauding out into space. (C) Yes, because the expert mentions the idea of conquering Earth with Korvin's aid. (D) Yes, because the ruler says the he wants to know about Earth's weap…
- references: Yes, because the ruler says the he wants to know about Earth's weapons, plans, and fortifications.
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: No, because Korvin sends a mission back to Earth Central saying that the Tr'en won't come marauding out into space.
  top_chunk: rank=1 score=0.5556 If you didn't, you never had a second chance to try. But Korvin meant exactly what he'd said. He was going to obey the commands of the Ruler of the Tr'en—and remove the Tr'en threat from the rest of the galaxy forever. That, after all, was…
- reorder_only_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.5556 If you didn't, you never had a second chance to try. But Korvin meant exactly what he'd said. He was going to obey the commands of the Ruler of the Tr'en—and remove the Tr'en threat from the rest of the galaxy forever. That, after all, was…

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

#### quality / 63401_ZCP5ZDGL_4

- query: What was Ann intending to do with Johnathan under the trees before the other women showed up? (A) Sleep with him. (B) Convince him to help her cook dinner. (C) Ask him to be her boyfriend. (D) Talk to him about how he became a pilot.
- references: Sleep with him.
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.4963 He started to rise. Ann Clotilde placed the flat of her hand on his chest and shoved. " Ooof! " he grunted. He sat down rather more forcibly than he had risen. "Don't get up because of me," she informed him. "It's my turn to cook, but I sa…
- reorder_only_rag score: 0.0000
  prediction: C
  top_chunk: rank=1 score=0.4963 He started to rise. Ann Clotilde placed the flat of her hand on his chest and shoved. " Ooof! " he grunted. He sat down rather more forcibly than he had risen. "Don't get up because of me," she informed him. "It's my turn to cook, but I sa…

#### quality / 63401_ZCP5ZDGL_8

- query: What was Johnathan's original mission? (A) To find the missing women and take them to Mars so they could marry the colonists. (B) To deliver tobacco seeds to the colonists on Mars. (C) To deliver tobacco seeds to the colonists on Jupiter. (D) To find the missing women and take them to Jupiter so they could marry the colonists.
- references: To deliver tobacco seeds to the colonists on Jupiter.
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.4600 "They'd kill you," she said. "I can sneak back," he insisted stubbornly. "They might loot the ship. I don't want to lose those cigarettes. I was hauling some good burley tobacco seed too. The colonists were going to experiment with it on G…
- reorder_only_rag score: 0.0000
  prediction: C
  top_chunk: rank=1 score=0.4600 "They'd kill you," she said. "I can sneak back," he insisted stubbornly. "They might loot the ship. I don't want to lose those cigarettes. I was hauling some good burley tobacco seed too. The colonists were going to experiment with it on G…

#### quality / 63523_STSHLFEA_3

- query: What is the Oans' unusual advantage? (A) They have the human's fire weapons. (B) They emit flames. (C) The strength of their arms. (D) Their eyes cut the night.
- references: They have the human's fire weapons.
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: D
  top_chunk: rank=1 score=0.4346 But when I have slain a few Oan, I will set the white ones free. They will help me to make more weapons. Together we will fight the rat men." Na smiled. Ro was angry, but anger did not make him blind. He would make a good mate. The sun was…
- reorder_only_rag score: 0.0000
  prediction: A
  top_chunk: rank=1 score=0.4346 But when I have slain a few Oan, I will set the white ones free. They will help me to make more weapons. Together we will fight the rat men." Na smiled. Ro was angry, but anger did not make him blind. He would make a good mate. The sun was…

### contract_nli

- examples: 50
- disagreements: 11
- any-positive-score: 37

#### contract_nli / 7_nda-2

- query: Confidential Information shall only include technical information.
- references: Entailment
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5743 Confidential Information does not include information: (i) which is or becomes public knowledge and public property in any way without breach of this Agreement by the Recipient; (ii) which the Recipient can show has been known or has been…
- reorder_only_rag score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.5743 Confidential Information does not include information: (i) which is or becomes public knowledge and public property in any way without breach of this Agreement by the Recipient; (ii) which the Recipient can show has been known or has been…

#### contract_nli / 3_nda-1

- query: All Confidential Information shall be expressly identified by the Disclosing Party.
- references: Entailment
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5949 In respect of Confidential Information disclosed in documentary form, model or any other tangible form, this shall be marked by the Disclosing Party as confidential or otherwise designated to show expressly or by necessary implication that…
- reorder_only_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5949 In respect of Confidential Information disclosed in documentary form, model or any other tangible form, this shall be marked by the Disclosing Party as confidential or otherwise designated to show expressly or by necessary implication that…

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
