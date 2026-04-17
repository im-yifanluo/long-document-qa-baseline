# Comparison Report

Run tier: `subset`

## Score Summary

| Task | Metric | vanilla_rag | reorder_only_rag | reorder_only_rag_minus_vanilla_rag |
| --- | --- | --- | --- | --- |
| qmsum | rouge | 15.4723 | 17.7533 | +2.2810 |
| qasper | f1 | 35.6440 | 41.4484 | +5.8044 |
| narrative_qa | f1 | 16.4705 | 16.3083 | -0.1622 |
| quality | exact_match | 48.0000 | 64.0000 | +16.0000 |
| contract_nli | exact_match | 68.0000 | 56.0000 | -12.0000 |

## Runtime Summary

| Method | Total seconds | Total minutes | Seconds / example | Examples / second |
| --- | --- | --- | --- | --- |
| vanilla_rag | 666.16 | 11.10 | 2.6646 | 0.3753 |
| reorder_only_rag | 529.38 | 8.82 | 2.1175 | 0.4723 |

## Example Previews

### qmsum

- examples: 50
- disagreements: 50
- any-positive-score: 50

#### qmsum / va-sq-1

- query: What was agreed upon on sample transcripts?
- references: To save time, speaker mn005 will only mark the sample of transcribed data for regions of overlapping speech, as opposed to marking all acoustic events. The digits extraction task will be delegated to whomever is working on acoustics for the Meeting Recorder project.
- best_methods: reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Based on the provided context, it seems that the group agreed to use the manually marked transcripts as a form of ground truth. Specifically, Professor E mentioned, "The idea of the manual marking was to say 'OK this, i you know, it's really here.'" This suggests that the manually marked transcripts were used to identify and mark specific instances for comparison and validation purposes.
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- reorder_only_rag score: 9.7507
  prediction: Based on the provided context, it was agreed that there was a forty-five-minute piece of transcription that was sent to IBM for comparison, and a larger piece of recorded data that was put on CD-ROM and sent to IBM for transcription. Additionally, it was mentioned that there were about ten hours of meetings that had been recorded and sent to IBM for transcription, though the exact amount of trans…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…

#### qmsum / va-sq-4

- query: What was the future of data collection?
- references: The group aims to collect over 100 hours of Meeting Recorder data in total. Speaker consent forms are being revised. It was suggested that subjects should sign a new consent form after 10 recording sessions.
- best_methods: reorder_only_rag
- disagreement: True
- vanilla_rag score: 4.9059
  prediction: The future of data collection involves continuing to record meetings, with the goal of collecting significantly more than the current amount. Professor E suggests aiming for more than a hundred hours of data, with the idea that if they can keep collecting data for a few months, they could have around a hundred hours. They also discuss the possibility of recording meetings from other groups on cam…
  top_chunk: rank=1 score=0.3866 I wanted to ask another a a aspect of the data collection . There 'd be no reason why a person couldn't get together several uh , you know , friends , and come and argue about a topic if they wanted to , right ?
- reorder_only_rag score: 6.7558
  prediction: The future of data collection involves continuing to collect data beyond the end of the semester. The goal is to collect significantly more than a hundred hours of data, with the hope of having around thirty to fifty hours by the end of the current semester. In the near future, the team aims to collect data for at least three months, which would provide enough data to start more detailed projects…
  top_chunk: rank=1 score=0.3866 I wanted to ask another a a aspect of the data collection . There 'd be no reason why a person couldn't get together several uh , you know , friends , and come and argue about a topic if they wanted to , right ?

#### qmsum / va-gq-5

- query: What were the main discussion points of the meeting?
- references: The group discussed topics including a potential collaboration with another ICSI member regarding the analysis of inference structures, efforts by speaker mn005 to detect speaker overlap, the current status of recordings and transcriptions, and future efforts to collect meeting data. In addition to weekly meetings by the BMR group, efforts are in progress to record meetings by other ICSI research…
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 8.3574
  prediction: The main discussion points of the meeting included: 1. **Recording Meetings**: The group discussed recording meetings, particularly those of the Network Services and Applications group, and the potential for recording other meetings at ICSI that might have more emotional or conflict aspects. 2. **Data Collection and Analysis**: There was a discussion about the amount of data collected so far, the…
  top_chunk: rank=1 score=0.3285 Uh , we {disfmarker} I think the things that we talk about in this meeting uh tend to be a mixture of uh procedural uh mundane things and uh research points and um I was thinking I think it was a meeting a couple of weeks ago that we {disf…
- reorder_only_rag score: 7.1647
  prediction: The main discussion points of the meeting included: 1. **Data Collection and Transcription**: The group discussed the amount of data collected so far, including meetings from different groups and the possibility of recording more meetings. They also talked about the transcription process and the time it takes to transcribe the data. 2. **Acoustic Event Detection**: PhD D discussed their work on d…
  top_chunk: rank=1 score=0.3285 Uh , we {disfmarker} I think the things that we talk about in this meeting uh tend to be a mixture of uh procedural uh mundane things and uh research points and um I was thinking I think it was a meeting a couple of weeks ago that we {disf…

#### qmsum / va-sq-3

- query: What’s the current status of recordings and transcriptions?
- references: Approximately 12-13 hours of Meeting Recorder data have been collected, roughly 45 minutes of which have been transcribed. Additional meetings by other ICSI research groups will be recorded. A suggestion was made that multi-channel data also be collected in cooperation with local media broadcasters, and that such events might be recorded live from ICSI.
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 8.7210
  prediction: Currently, the group has recorded approximately twelve to thirteen hours of meetings, but only about one hour of this has been transcribed. They plan to start recording meetings of the Network Services and Applications group, which meet on Tuesdays, starting the following week. The group is also considering recording meetings with the State of California, though there are doubts about the feasibi…
  top_chunk: rank=1 score=0.3967 See I was wondering cuz we st we have these ten hours of other stuff that is not yet transcribed . PhD D: Yeah . Yeah .
- reorder_only_rag score: 8.1580
  prediction: The current status of recordings and transcriptions, as discussed in the meeting, is as follows: - There is a forty-five-minute piece that has been transcribed and sent to IBM for comparison. - About twelve hours of meetings have been recorded but not transcribed yet. - By the end of the semester, they expect to have around forty to fifty hours of recordings, assuming they continue at the current…
  top_chunk: rank=1 score=0.3967 See I was wondering cuz we st we have these ten hours of other stuff that is not yet transcribed . PhD D: Yeah . Yeah .

#### qmsum / va-sq-47

- query: What demos would the system be involved in?
- references: The final english SmartKom demo will be presented to the whole institute once the system is de-bugged and stabilised.
- best_methods: reorder_only_rag
- disagreement: True
- vanilla_rag score: 8.4734
  prediction: The system would be involved in demos for the Fall, with the requirements for these demos being taken care of by later that week. Additionally, there is a plan to set up a demo as an institute-wide thing, where they could give a talk in the big room so that people know what is going on. The context also mentions that there are demo requirements every fifteen months, but they can't think about the…
  top_chunk: rank=1 score=0.3783 Professor C: and , s deliberately . So , the reason I 'd like you to understand uh what 's going on in this demo system is not because it 's important to the research . It 's just for closure . So that if we come up with a question of " co…
- reorder_only_rag score: 8.8329
  prediction: The system would be involved in demos for funding purposes, specifically to provide the demos that are required by their funding. Additionally, there is a suggestion to set up an internal demo that could be shown to anyone interested, and potentially an institute-wide demo where people can see what SmartKom is about. There are also plans to give a talk in the big room to inform people about the p…
  top_chunk: rank=1 score=0.3783 Professor C: and , s deliberately . So , the reason I 'd like you to understand uh what 's going on in this demo system is not because it 's important to the research . It 's just for closure . So that if we come up with a question of " co…

### qasper

- examples: 50
- disagreements: 41
- any-positive-score: 45

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

#### qasper / 26c2e1eb12143d985e4fb50543cf0d1eb4395e67

- query: What biases are found in the dataset?
- references: Ethnic bias | adjectives are used to create “more narrow labels [or subtypes] for individuals who do not fit with general social category expectations”
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 7.2727
  prediction: Ethnicity marking biases, where babies are only mentioned by ethnicity unless they are black or Asian, and there is a marked difference in how often white, Asian, and black babies are described by their ethnicity.
  top_chunk: rank=1 score=0.4560 I will build on earlier work on linguistic bias in general BIBREF3 , providing examples from the Flickr30K data, and present a taxonomy of unwarranted inferences. Finally, I will discuss several methods to analyze the data in order to dete…
- reorder_only_rag score: 0.0000
  prediction: Stereotype-driven descriptions
  top_chunk: rank=1 score=0.4560 I will build on earlier work on linguistic bias in general BIBREF3 , providing examples from the Flickr30K data, and present a taxonomy of unwarranted inferences. Finally, I will discuss several methods to analyze the data in order to dete…

### narrative_qa

- examples: 50
- disagreements: 45
- any-positive-score: 27

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_1

- query: Where is the boarding-house located?
- references: Paris
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house.
  top_chunk: rank=1 score=0.3975 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…
- reorder_only_rag score: 0.0000
  prediction: in the Boulevard Haussman
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

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_12

- query: Where is Herr professor from?
- references: Germany
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: German
  top_chunk: rank=1 score=0.2680 But at such a time as this there is always one person who seems interested in what I say--a German gentleman, a professor, who sits next to me at dinner, and whom I must tell you more about another time. He is very learned, and has a great…
- reorder_only_rag score: 0.0000
  prediction: He is a German gentleman, a professor, or doctor.
  top_chunk: rank=1 score=0.2680 But at such a time as this there is always one person who seems interested in what I say--a German gentleman, a professor, who sits next to me at dinner, and whom I must tell you more about another time. He is very learned, and has a great…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_13

- query: Where is Leon Verdier from?
- references: France
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: New York
  top_chunk: rank=1 score=0.3490 I am afraid you will never ask me again. CHAPTER VII FROM LEON VERDIER, IN PARIS, TO PROSPER GOBAIN, AT LILLE. September 28th. My Dear Prosper--It is a long time since I have given you of my news, and I don't know what puts it into my head…
- reorder_only_rag score: 0.0000
  prediction: Poitou
  top_chunk: rank=1 score=0.3490 I am afraid you will never ask me again. CHAPTER VII FROM LEON VERDIER, IN PARIS, TO PROSPER GOBAIN, AT LILLE. September 28th. My Dear Prosper--It is a long time since I have given you of my news, and I don't know what puts it into my head…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_17

- query: What name does Herr Professor call Leon?
- references: Simian
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too.
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…
- reorder_only_rag score: 0.0000
  prediction: Herr Professor calls Leon "le petit Leon" or "my little Leon".
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…

### quality

- examples: 50
- disagreements: 12
- any-positive-score: 32

#### quality / 30029_F5N22U40_6

- query: Are there indications that the Tr'en would be interested in attacking Earth? Why or why not? (A) Both A and C are correct. (B) No, because Korvin sends a mission back to Earth Central saying that the Tr'en won't come marauding out into space. (C) Yes, because the expert mentions the idea of conquering Earth with Korvin's aid. (D) Yes, because the ruler says the he wants to know about Earth's weap…
- references: Yes, because the ruler says the he wants to know about Earth's weapons, plans, and fortifications.
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.5556 If you didn't, you never had a second chance to try. But Korvin meant exactly what he'd said. He was going to obey the commands of the Ruler of the Tr'en—and remove the Tr'en threat from the rest of the galaxy forever. That, after all, was…
- reorder_only_rag score: 0.0000
  prediction: D
  top_chunk: rank=1 score=0.5556 If you didn't, you never had a second chance to try. But Korvin meant exactly what he'd said. He was going to obey the commands of the Ruler of the Tr'en—and remove the Tr'en threat from the rest of the galaxy forever. That, after all, was…

#### quality / 52845_75VB1ISR_2

- query: Why does Deirdre get so upset when Blake Past suggests she go to prom with the young man? (A) Because Blake is trying to guilt Deirdre into going with the young man by telling her that it'll ease her conscience. (B) Because Deirdre has fallen in love with Blake, despite his age, and wants him to take her to the prom. (C) Because Blake is acting like he's her father, which is a sensitive topic for…
- references: Because Deirdre has fallen in love with Blake, despite his age, and wants him to take her to the prom.
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Because Blake is acting like he's her father, which is a sensitive topic for Deirdre because she lost her real parents.
  top_chunk: rank=1 score=0.6406 Lord, he must have been feeling old to have pictured himself like that! Deirdre was speaking. "Yes," she was saying, "at nine o'clock. And I should very much like for you to come." Blake Past shook his head. "Proms aren't for parents. You…
- reorder_only_rag score: 0.0000
  prediction: Because Blake is trying to guilt Deirdre into going with the young man by telling her that it'll ease his conscience.
  top_chunk: rank=1 score=0.6406 Lord, he must have been feeling old to have pictured himself like that! Deirdre was speaking. "Yes," she was saying, "at nine o'clock. And I should very much like for you to come." Blake Past shook his head. "Proms aren't for parents. You…

#### quality / 63401_ZCP5ZDGL_4

- query: What was Ann intending to do with Johnathan under the trees before the other women showed up? (A) Sleep with him. (B) Convince him to help her cook dinner. (C) Ask him to be her boyfriend. (D) Talk to him about how he became a pilot.
- references: Sleep with him.
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.4963 He started to rise. Ann Clotilde placed the flat of her hand on his chest and shoved. " Ooof! " he grunted. He sat down rather more forcibly than he had risen. "Don't get up because of me," she informed him. "It's my turn to cook, but I sa…
- reorder_only_rag score: 0.0000
  prediction: She said in an angry voice: "He's mine. I found him. Leave him alone."
  top_chunk: rank=1 score=0.4963 He started to rise. Ann Clotilde placed the flat of her hand on his chest and shoved. " Ooof! " he grunted. He sat down rather more forcibly than he had risen. "Don't get up because of me," she informed him. "It's my turn to cook, but I sa…

#### quality / 63523_STSHLFEA_7

- query: Why did Ro change his mind about the people on Mars being backwards? (A) Because he realized that despite human's technological advancements, they have over-complicated marriage. (B) Because he realized that while the humans are physically vulnerable without their weapons, the red people have formidable strength in their arms. (C) Because he realized that human males suppress public affection whe…
- references: Because he realized that despite human's technological advancements, they have over-complicated marriage.
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Because he realized that while the humans are physically vulnerable without their weapons, the red people have formidable strength in their arms.
  top_chunk: rank=1 score=0.5245 We want the other to walk, we think of the other walking. A picture is transmitted and understood. It is a message in a Universal language." Ro sighed. "I am afraid we are very backward here on Mars," he said wearily. "I would like to lear…
- reorder_only_rag score: 0.0000
  prediction: Because he realized that human males suppress public affection when they are intimidated by other males, whereas male Martians don't hide their affection.
  top_chunk: rank=1 score=0.5245 We want the other to walk, we think of the other walking. A picture is transmitted and understood. It is a message in a Universal language." Ro sighed. "I am afraid we are very backward here on Mars," he said wearily. "I would like to lear…

#### quality / 52845_75VB1ISR_1

- query: How much time has passed between Blake's night with Eldoria and his search for Sabrina York in his mind-world? (A) 7 years (B) 10 hours (C) 12 years (D) 1 hour
- references: 10 hours
- best_methods: reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: 12 years
  top_chunk: rank=1 score=0.4728 It was a remarkably detailed materialization, and his quarry's footprints stood out clearly in the duplicated sand. Sabrina York did not even know the rudiments of the art of throwing off a mind-tracker. It would have done her but little g…
- reorder_only_rag score: 100.0000
  prediction: 10 hours
  top_chunk: rank=1 score=0.4728 It was a remarkably detailed materialization, and his quarry's footprints stood out clearly in the duplicated sand. Sabrina York did not even know the rudiments of the art of throwing off a mind-tracker. It would have done her but little g…

### contract_nli

- examples: 50
- disagreements: 11
- any-positive-score: 36

#### contract_nli / 7_nda-2

- query: Confidential Information shall only include technical information.
- references: Entailment
- best_methods: vanilla_rag, reorder_only_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.5743 Confidential Information does not include information: (i) which is or becomes public knowledge and public property in any way without breach of this Agreement by the Recipient; (ii) which the Recipient can show has been known or has been…
- reorder_only_rag score: 0.0000
  prediction: Not mentioned
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
