# Comparison Report

Run tier: `subset`

## Score Summary

| Task | Metric | vanilla_rag | reorder_only_rag | reverse_order_rag | random_order_rag | anchor1_doc_order_rag | anchor2_doc_order_rag | reorder_only_rag_minus_vanilla_rag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| qmsum | rouge | 16.1329 | 17.1944 | 14.5383 | 15.6044 | 16.7214 | 16.6045 | +1.0615 |
| qasper | f1 | 36.6376 | 40.9533 | 35.2614 | 31.8040 | 36.5850 | 38.4786 | +4.3157 |
| narrative_qa | f1 | 10.5847 | 10.9790 | 15.5252 | 14.8018 | 13.2098 | 15.0063 | +0.3943 |
| quality | exact_match | 48.0000 | 62.0000 | 50.0000 | 56.0000 | 60.0000 | 60.0000 | +14.0000 |
| contract_nli | exact_match | 70.0000 | 58.0000 | 56.0000 | 62.0000 | 64.0000 | 64.0000 | -12.0000 |

## Runtime Summary

| Method | Total seconds | Total minutes | Seconds / example | Examples / second |
| --- | --- | --- | --- | --- |
| vanilla_rag | 538.67 | 8.98 | 2.1547 | 0.4641 |
| reorder_only_rag | 516.70 | 8.61 | 2.0668 | 0.4838 |
| reverse_order_rag | 542.95 | 9.05 | 2.1718 | 0.4604 |
| random_order_rag | 542.76 | 9.05 | 2.1710 | 0.4606 |
| anchor1_doc_order_rag | 541.18 | 9.02 | 2.1647 | 0.4620 |
| anchor2_doc_order_rag | 541.51 | 9.03 | 2.1660 | 0.4617 |

## Example Previews

### qmsum

- examples: 50
- disagreements: 50
- any-positive-score: 50

#### qmsum / va-sq-1

- query: What was agreed upon on sample transcripts?
- references: To save time, speaker mn005 will only mark the sample of transcribed data for regions of overlapping speech, as opposed to marking all acoustic events. The digits extraction task will be delegated to whomever is working on acoustics for the Meeting Recorder project.
- best_methods: reverse_order_rag
- disagreement: True
- vanilla_rag score: 7.2225
  prediction: Based on the provided context, it was agreed that there is a need to compare the manual transcripts with the IBM-transcribed versions for quality and accuracy. Specifically, Professor E mentioned that there is a forty-five-minute piece that Jane transcribed, which was then sent to IBM for transcription, providing a comparison point. Additionally, a larger piece has been recorded and put on CD-ROM…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- reorder_only_rag score: 7.9643
  prediction: Based on the provided context, there is no explicit agreement mentioned regarding sample transcripts. The discussion revolves around the transcription process, the need for ground truth data, and the challenges of transcribing overlapping speech. However, it is mentioned that there is a forty-five-minute piece of transcription that has been sent to IBM for comparison, and there are ten hours of r…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- reverse_order_rag score: 9.4298
  prediction: Based on the provided context, it appears that a sample of transcript data was sent to IBM for transcription as a comparison point. Specifically, a forty-five minute piece of recorded data was transcribed and sent to IBM, and a larger piece of recorded data was also sent to IBM and put on CD-ROM for transcription. This was done to have some ground truth to compare against when the manual marking…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- random_order_rag score: 0.0000
  prediction: Based on the provided context, it was agreed that some ground truth would be useful for comparing against when the transcription system is developed. Specifically, Professor E mentioned that the idea of manual marking was to have "OK this, i you know, it's really here" as a way to ensure accurate transcription. Additionally, it was noted that transcriptions are not a significant bottleneck in the…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- anchor1_doc_order_rag score: 7.9643
  prediction: Based on the provided context, there is no explicit agreement mentioned regarding sample transcripts. The discussion revolves around the transcription process, the need for ground truth data, and the challenges of transcribing overlapping speech. However, it is mentioned that there is a forty-five-minute piece of transcription that has been sent to IBM for comparison, and there are ten hours of r…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- anchor2_doc_order_rag score: 7.6951
  prediction: Based on the provided context, there is no explicit agreement mentioned regarding sample transcripts. The discussion revolves around the transcription process, the need for ground truth data, and the challenges of transcribing overlapping speech. However, it is mentioned that there is a forty-five-minute piece of transcription that has been sent to IBM for comparison, and there are ten hours of r…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…

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
- reverse_order_rag score: 6.1770
  prediction: Based on the provided context, some of the problems encountered with the SmartKom system include: 1. **Instability**: The system is described as unstable, with the version on the server not working properly and requiring a lot of work to make it functional. 2. **Brittleness**: The system is described as brittle, requiring significant changes (twenty changes on seventeen modules) before it can be…
  top_chunk: rank=1 score=0.3394 The {disfmarker} we got to the point where we can now speak into the SmartKom system , and it 'll go all the way through and then say something like " Roman numeral one , am Smarticus . " It actually says , " Roemisch einz , am Smarticus ,…
- random_order_rag score: 6.1847
  prediction: Based on the provided context, several problems and issues with the SmartKom system were mentioned: 1. **Inconsistency Across Versions**: The full version of the system on the server did not work, and there was a need to do a lot of work to make it functional. This suggests that there were issues with the system's consistency and reliability. 2. **Brittleness and Complexity**: The system was desc…
  top_chunk: rank=1 score=0.3394 The {disfmarker} we got to the point where we can now speak into the SmartKom system , and it 'll go all the way through and then say something like " Roman numeral one , am Smarticus . " It actually says , " Roemisch einz , am Smarticus ,…
- anchor1_doc_order_rag score: 6.4773
  prediction: Based on the provided context, several problems were encountered with the SmartKom system: 1. **Language-Specific Issues**: The system uses a German synthesis module for English sentences, indicating that it has language-specific limitations. This suggests that the system may not be fully language-independent. 2. **Brittleness and Complexity**: The system is described as brittle, requiring signif…
  top_chunk: rank=1 score=0.3394 The {disfmarker} we got to the point where we can now speak into the SmartKom system , and it 'll go all the way through and then say something like " Roman numeral one , am Smarticus . " It actually says , " Roemisch einz , am Smarticus ,…
- anchor2_doc_order_rag score: 7.5938
  prediction: Based on the provided context, some of the problems encountered with the SmartKom system include: 1. **Language-Specific Components**: The system uses a German synthesis module for English sentences, indicating that it is not fully language-independent. This means that while the system can generate some English sentences, it relies on specific components for different languages. 2. **Brittleness…
  top_chunk: rank=1 score=0.3394 The {disfmarker} we got to the point where we can now speak into the SmartKom system , and it 'll go all the way through and then say something like " Roman numeral one , am Smarticus . " It actually says , " Roemisch einz , am Smarticus ,…

#### qmsum / va-sq-47

- query: What demos would the system be involved in?
- references: The final english SmartKom demo will be presented to the whole institute once the system is de-bugged and stabilised.
- best_methods: random_order_rag
- disagreement: True
- vanilla_rag score: 7.9320
  prediction: The system would be involved in demos for the Fall, with requirements taken care of by later that week or so. There's also mention of a larger effort with formalization stuff, and a plan to have a talk in the big room as an institute-wide thing, which could involve showing a demo version of a project. Additionally, there's a belief-net demo level being thought of, and the system needs to fit into…
  top_chunk: rank=1 score=0.3783 Professor C: and , s deliberately . So , the reason I 'd like you to understand uh what 's going on in this demo system is not because it 's important to the research . It 's just for closure . So that if we come up with a question of " co…
- reorder_only_rag score: 6.9783
  prediction: The system would be involved in demos for funding purposes, specifically to show that the project is making progress and to provide the necessary demonstrations as outlined in the contracts. Professor C mentions that the demos for that Fall are "sort of taken care of as of later this week or something," and there won't be another serious demo requirement for about fifteen months. However, the tea…
  top_chunk: rank=1 score=0.3783 Professor C: and , s deliberately . So , the reason I 'd like you to understand uh what 's going on in this demo system is not because it 's important to the research . It 's just for closure . So that if we come up with a question of " co…
- reverse_order_rag score: 6.3327
  prediction: Based on the provided context, the system would be involved in demos for the following purposes: 1. To give a talk institute-wide in a big room to inform people about the project and its current demo version. 2. To demonstrate the current state of the belief-net and related work. 3. To show the running system and its capabilities, especially to new members or interested parties who might ask abou…
  top_chunk: rank=1 score=0.3783 Professor C: and , s deliberately . So , the reason I 'd like you to understand uh what 's going on in this demo system is not because it 's important to the research . It 's just for closure . So that if we come up with a question of " co…
- random_order_rag score: 9.0233
  prediction: The system would be involved in demos for the Fall, with the requirements for these demos being taken care of as of later that week. Additionally, there is a suggestion to set up a demo as an institute-wide event, where the project can be showcased, and people can be informed about the work being done. The belief-net system is also mentioned as needing to be completed in the next few weeks for a…
  top_chunk: rank=1 score=0.3783 Professor C: and , s deliberately . So , the reason I 'd like you to understand uh what 's going on in this demo system is not because it 's important to the research . It 's just for closure . So that if we come up with a question of " co…
- anchor1_doc_order_rag score: 7.7670
  prediction: The system would be involved in demos for funding requirements. Specifically, Professor C mentions, "So uh we are committed for our funding . . . to get the demos they need." He also notes, "The demo the demo requirements for this Fall are sort of taken care of as of later this week or something." Additionally, there is a mention of demos being required in fifteen months, after which the group wi…
  top_chunk: rank=1 score=0.3783 Professor C: and , s deliberately . So , the reason I 'd like you to understand uh what 's going on in this demo system is not because it 's important to the research . It 's just for closure . So that if we come up with a question of " co…
- anchor2_doc_order_rag score: 7.7017
  prediction: The system would be involved in demos for the Fall, with the requirements for these demos being taken care of as of later that week. There is a commitment to get the necessary demos done for funding purposes. The next serious demo requirement is not expected for about fifteen months, after which the team can think about it again but not for six months. In the meantime, the focus is on stepping ba…
  top_chunk: rank=1 score=0.3783 Professor C: and , s deliberately . So , the reason I 'd like you to understand uh what 's going on in this demo system is not because it 's important to the research . It 's just for closure . So that if we come up with a question of " co…

#### qmsum / va-sq-3

- query: What’s the current status of recordings and transcriptions?
- references: Approximately 12-13 hours of Meeting Recorder data have been collected, roughly 45 minutes of which have been transcribed. Additional meetings by other ICSI research groups will be recorded. A suggestion was made that multi-channel data also be collected in cooperation with local media broadcasters, and that such events might be recorded live from ICSI.
- best_methods: reorder_only_rag
- disagreement: True
- vanilla_rag score: 5.9926
  prediction: Based on the provided context, here is the current status of recordings and transcriptions: - **Recordings:** - They have recorded about 12 hours of meetings so far. - They plan to start recording meetings of the Network Services and Applications group, which meet on Tuesdays, starting next week. - They are considering recording additional meetings, such as those at ICSI, to increase the amount o…
  top_chunk: rank=1 score=0.3967 See I was wondering cuz we st we have these ten hours of other stuff that is not yet transcribed . PhD D: Yeah . Yeah .
- reorder_only_rag score: 9.1900
  prediction: Based on the provided context, the current status of recordings and transcriptions is as follows: - About twelve hours of meetings have been recorded, though not all have been transcribed. - There is a forty-five-minute segment that has been transcribed and sent to IBM for comparison. - A larger segment, which is twelve hours, has been recorded but not transcribed. - IBM has not yet provided tran…
  top_chunk: rank=1 score=0.3967 See I was wondering cuz we st we have these ten hours of other stuff that is not yet transcribed . PhD D: Yeah . Yeah .
- reverse_order_rag score: 7.8211
  prediction: Based on the provided context, the current status of recordings and transcriptions is as follows: - They have recorded about twelve hours of audio data so far. - They have sent one forty-five minute piece to IBM for transcription, which has been transcribed and compared. - They have also sent a larger piece that has been recorded, put on CD-ROM, and sent to IBM for transcription. - They have star…
  top_chunk: rank=1 score=0.3967 See I was wondering cuz we st we have these ten hours of other stuff that is not yet transcribed . PhD D: Yeah . Yeah .
- random_order_rag score: 7.8968
  prediction: Based on the provided context, the current status of recordings and transcriptions is as follows: - They have approximately twelve hours of recorded meetings, with some of this data not yet transcribed. - There are ten hours of other recorded meetings that are not yet transcribed. - About three hundred speaker overlaps were identified in a forty-five-minute piece that has been transcribed and sen…
  top_chunk: rank=1 score=0.3967 See I was wondering cuz we st we have these ten hours of other stuff that is not yet transcribed . PhD D: Yeah . Yeah .
- anchor1_doc_order_rag score: 7.9618
  prediction: Based on the provided context, the current status of recordings and transcriptions is as follows: - About twelve hours of meetings have been recorded. - There is a forty-five-minute segment that has been transcribed and sent to IBM for comparison. - A larger segment, spanning about twelve hours, has been recorded but not yet transcribed. - IBM has not yet provided transcriptions for the recording…
  top_chunk: rank=1 score=0.3967 See I was wondering cuz we st we have these ten hours of other stuff that is not yet transcribed . PhD D: Yeah . Yeah .
- anchor2_doc_order_rag score: 9.1071
  prediction: Based on the provided context, the current status of recordings and transcriptions is as follows: 1. **Recordings:** - About twelve hours of recordings have been made, primarily from meetings. - Some meetings have been recorded and transcribed, while others have been recorded but not yet transcribed. - Plans are in place to continue recording meetings, including starting to record additional meet…
  top_chunk: rank=1 score=0.3967 See I was wondering cuz we st we have these ten hours of other stuff that is not yet transcribed . PhD D: Yeah . Yeah .

#### qmsum / va-sq-14

- query: What did the group discuss about the functions of the remote control?
- references: The User Interface proposed to build a stand-alone one, which can be different from any other devices. The Project Manager then added that it might be better with more useful functions like changing the faces. Marketing came up with the idea of making it be functional for other devices as well, just including everything in this remote control.
- best_methods: anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 9.9792
  prediction: The group discussed several functions and features for the remote control, including: 1. It should be a universal remote control capable of controlling various devices. 2. It should have a touch screen interface with multi-format features. 3. It could include a locator device with a simple button to help find the remote. 4. It might have additional useful functions, such as a clapper or a small p…
  top_chunk: rank=1 score=0.3972 But I think that that is more or less a good place to start for now um and as more things come up we'll have meetings and you'll get emails and so forth . Um any questions , before we get started ? User Interface: I assume that we're build…
- reorder_only_rag score: 8.9061
  prediction: The group discussed several functions and features for the remote control, including: 1. It should be a universal remote control capable of handling different formats such as N_T_S_C_, PAL, and various other formats to control devices like D_V_D_s. 2. The remote should be affordable, aiming to sell it for 25 Euros, but potentially for as low as 125 Euros. 3. It should have multi-format features a…
  top_chunk: rank=1 score=0.3972 But I think that that is more or less a good place to start for now um and as more things come up we'll have meetings and you'll get emails and so forth . Um any questions , before we get started ? User Interface: I assume that we're build…
- reverse_order_rag score: 6.3414
  prediction: The group discussed several potential functions and features for the remote control, including: 1. **Selling overseas**: The remote could be sold in one country and shipped to another, potentially for around 20-30 pounds. 2. **Targeting specific users**: They considered the needs of users like "grandmas" who might prefer a simpler design with familiar buttons. 3. **Price and features trade-off**:…
  top_chunk: rank=1 score=0.3972 But I think that that is more or less a good place to start for now um and as more things come up we'll have meetings and you'll get emails and so forth . Um any questions , before we get started ? User Interface: I assume that we're build…
- random_order_rag score: 8.3755
  prediction: The group discussed several potential functions and features for the remote control, including: 1. **Universal Control**: The remote should be able to control various devices such as DVD players, televisions, and other electronic gadgets. 2. **Multi-Format Compatibility**: It should support different video formats like N_T_S_C_ and PAL. 3. **Touch Screen Interface**: The idea of a touch screen re…
  top_chunk: rank=1 score=0.3972 But I think that that is more or less a good place to start for now um and as more things come up we'll have meetings and you'll get emails and so forth . Um any questions , before we get started ? User Interface: I assume that we're build…
- anchor1_doc_order_rag score: 8.7430
  prediction: The group discussed several functions and features for the remote control, including: 1. It should be a universal remote control capable of handling different formats like N_T_S_C_, PAL, and various other formats to control devices like D_V_D_s. 2. The remote should be affordable, aiming to sell it for 25 Euros, though they considered a lower price point of 125 Euros. 3. It should have multi-form…
  top_chunk: rank=1 score=0.3972 But I think that that is more or less a good place to start for now um and as more things come up we'll have meetings and you'll get emails and so forth . Um any questions , before we get started ? User Interface: I assume that we're build…
- anchor2_doc_order_rag score: 10.2556
  prediction: The group discussed several functions and features for the remote control, including: 1. It should be a universal remote control capable of handling different formats such as N_T_S_C_, PAL, and various other formats to control D_V_D_s. 2. The remote should be touch screen-based for a more user-friendly interface. 3. It should have multi-format features to cater to different devices. 4. The remote…
  top_chunk: rank=1 score=0.3972 But I think that that is more or less a good place to start for now um and as more things come up we'll have meetings and you'll get emails and so forth . Um any questions , before we get started ? User Interface: I assume that we're build…

### qasper

- examples: 50
- disagreements: 46
- any-positive-score: 45

#### qasper / 71e4ba4e87e6596aeca187127c0d088df6570c57

- query: What evaluations methods do they take?
- references: Unanswerable | Unanswerable
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: To get an idea of the kinds of stereotype-driven descriptions that are in the Flickr30K dataset, I made a browser-based annotation tool that shows both the images and their associated descriptions.
  top_chunk: rank=1 score=0.2777 A next step would be to see whether these observations also hold for other age groups, i.e. children and adults. INLINEFORM0 Other methods It may be difficult to spot patterns by just looking at a collection of images. Another method is to…
- reorder_only_rag score: 0.0000
  prediction: In order to get an idea of the kinds of stereotype-driven descriptions that are in the Flickr30K dataset, I made a browser-based annotation tool that shows both the images and their associated descriptions. Another method is to tag all descriptions with part-of-speech information, so that it becomes possible to see e.g. which adjectives are most commonly used for particular nouns. One method read…
  top_chunk: rank=1 score=0.2777 A next step would be to see whether these observations also hold for other age groups, i.e. children and adults. INLINEFORM0 Other methods It may be difficult to spot patterns by just looking at a collection of images. Another method is to…
- reverse_order_rag score: 0.0000
  prediction: To evaluate the dataset, they apply part-of-speech tagging, use Louvain clustering on the coreference graph, and manually categorize the descriptions. They also inspect a subset of the data to group unwarranted inferences into categories and use methods to detect stereotype-driven descriptions.
  top_chunk: rank=1 score=0.2777 A next step would be to see whether these observations also hold for other age groups, i.e. children and adults. INLINEFORM0 Other methods It may be difficult to spot patterns by just looking at a collection of images. Another method is to…
- random_order_rag score: 0.0000
  prediction: To get an idea of the kinds of stereotype-driven descriptions that are in the Flickr30K dataset, I made a browser-based annotation tool that shows both the images and their associated descriptions. You can simply leaf through the images by clicking `Next' or `Random' until you find an interesting pattern.
  top_chunk: rank=1 score=0.2777 A next step would be to see whether these observations also hold for other age groups, i.e. children and adults. INLINEFORM0 Other methods It may be difficult to spot patterns by just looking at a collection of images. Another method is to…
- anchor1_doc_order_rag score: 0.0000
  prediction: In order to get an idea of the kinds of stereotype-driven descriptions that are in the Flickr30K dataset, I made a browser-based annotation tool that shows both the images and their associated descriptions. You can simply leaf through the images by clicking `Next' or `Random' until you find an interesting pattern.
  top_chunk: rank=1 score=0.2777 A next step would be to see whether these observations also hold for other age groups, i.e. children and adults. INLINEFORM0 Other methods It may be difficult to spot patterns by just looking at a collection of images. Another method is to…
- anchor2_doc_order_rag score: 0.0000
  prediction: In order to get an idea of the kinds of stereotype-driven descriptions that are in the Flickr30K dataset, I made a browser-based annotation tool that shows both the images and their associated descriptions. You can simply leaf through the images by clicking `Next' or `Random' until you find an interesting pattern.
  top_chunk: rank=1 score=0.2777 A next step would be to see whether these observations also hold for other age groups, i.e. children and adults. INLINEFORM0 Other methods It may be difficult to spot patterns by just looking at a collection of images. Another method is to…

#### qasper / a313e98994fc039a82aa2447c411dda92c65a470

- query: How do they match words before reordering them?
- references: Unanswerable | CFILT-preorder system
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: They match words before reordering them by applying pre-ordering rules that swap the position of the noun phrase followed by a transitive verb with the transitive verb.
  top_chunk: rank=1 score=0.4351 One of the pre-ordering rule swaps the position of the noun phrase followed by a transitive verb with the transitive verb. The original and the resulting re-ordered parse tree will be as shown in the Table TABREF5 . Applying this reorderin…
- reorder_only_rag score: 0.0000
  prediction: For representing English and other source languages into a common space, we translate each word in the source language into English using a bilingual dictionary (Google Translate word translation in our case).
  top_chunk: rank=1 score=0.4351 One of the pre-ordering rule swaps the position of the noun phrase followed by a transitive verb with the transitive verb. The original and the resulting re-ordered parse tree will be as shown in the Table TABREF5 . Applying this reorderin…
- reverse_order_rag score: 0.0000
  prediction: They do not provide explicit details on how words are matched before reordering them.
  top_chunk: rank=1 score=0.4351 One of the pre-ordering rule swaps the position of the noun phrase followed by a transitive verb with the transitive verb. The original and the resulting re-ordered parse tree will be as shown in the Table TABREF5 . Applying this reorderin…
- random_order_rag score: 0.0000
  prediction: They translate each word in the source language into English using a bilingual dictionary (Google Translate word translation in our case).
  top_chunk: rank=1 score=0.4351 One of the pre-ordering rule swaps the position of the noun phrase followed by a transitive verb with the transitive verb. The original and the resulting re-ordered parse tree will be as shown in the Table TABREF5 . Applying this reorderin…
- anchor1_doc_order_rag score: 0.0000
  prediction: For representing English and other source languages into a common space, we translate each word in the source language into English using a bilingual dictionary (Google Translate word translation in our case).
  top_chunk: rank=1 score=0.4351 One of the pre-ordering rule swaps the position of the noun phrase followed by a transitive verb with the transitive verb. The original and the resulting re-ordered parse tree will be as shown in the Table TABREF5 . Applying this reorderin…
- anchor2_doc_order_rag score: 0.0000
  prediction: We translate each word in the source language into English using a bilingual dictionary (Google Translate word translation in our case).
  top_chunk: rank=1 score=0.4351 One of the pre-ordering rule swaps the position of the noun phrase followed by a transitive verb with the transitive verb. The original and the resulting re-ordered parse tree will be as shown in the Table TABREF5 . Applying this reorderin…

#### qasper / c0bee6539eb6956a7347daa9d2419b367bd02064

- query: Does BERT reach the best performance among all the algorithms compared?
- references: No | No
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: The BERT-based model shows the highest robustness to training-data scarcity, loosing only 7 points of F1-score when trained on 230 instances instead of 21,371. These observation are in line with the results obtained by the NLP community using BERT for other tasks.
  top_chunk: rank=1 score=0.5670 A fact worth highlighting is that, according to these results, BERT achieves a precision lower than the rest of the systems (i.e., it makes more false positive predictions); in exchange, it obtains a remarkably higher recall. Noticeably, i…
- reorder_only_rag score: 0.0000
  prediction: In NUBes-PHI, the BERT-based model outperforms the other systems without requiring any adaptation or domain-specific feature engineering, just by being trained on the provided labelled data.
  top_chunk: rank=1 score=0.5670 A fact worth highlighting is that, according to these results, BERT achieves a precision lower than the rest of the systems (i.e., it makes more false positive predictions); in exchange, it obtains a remarkably higher recall. Noticeably, i…
- reverse_order_rag score: 0.0000
  prediction: BERT outperforms other systems in terms of recall and achieves a remarkably higher recall than the other systems.
  top_chunk: rank=1 score=0.5670 A fact worth highlighting is that, according to these results, BERT achieves a precision lower than the rest of the systems (i.e., it makes more false positive predictions); in exchange, it obtains a remarkably higher recall. Noticeably, i…
- random_order_rag score: 0.0000
  prediction: BERT outperforms its competitors in both NUBes-PHI and MEDDOCAN experiments.
  top_chunk: rank=1 score=0.5670 A fact worth highlighting is that, according to these results, BERT achieves a precision lower than the rest of the systems (i.e., it makes more false positive predictions); in exchange, it obtains a remarkably higher recall. Noticeably, i…
- anchor1_doc_order_rag score: 0.0000
  prediction: In NUBes-PHI, the BERT-based model outperforms the other systems without requiring any adaptation or domain-specific feature engineering, just by being trained on the provided labelled data.
  top_chunk: rank=1 score=0.5670 A fact worth highlighting is that, according to these results, BERT achieves a precision lower than the rest of the systems (i.e., it makes more false positive predictions); in exchange, it obtains a remarkably higher recall. Noticeably, i…
- anchor2_doc_order_rag score: 0.0000
  prediction: In NUBes-PHI, the BERT-based model outperforms the other systems without requiring any adaptation or domain-specific feature engineering, just by being trained on the provided labelled data.
  top_chunk: rank=1 score=0.5670 A fact worth highlighting is that, according to these results, BERT achieves a precision lower than the rest of the systems (i.e., it makes more false positive predictions); in exchange, it obtains a remarkably higher recall. Noticeably, i…

#### qasper / fb2b536dc8e442dffab408db992b971e86548158

- query: What is the interannotator agreement for the human evaluation?
- references: Unanswerable | Unanswerable
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: The context does not provide information about interannotator agreement for the human evaluation.
  top_chunk: rank=1 score=0.3259 The opinons expressed are those of the authors and do not represent the views of the institute or the U.S. Department of Education
- reorder_only_rag score: 0.0000
  prediction: Not provided in the context.
  top_chunk: rank=1 score=0.3259 The opinons expressed are those of the authors and do not represent the views of the institute or the U.S. Department of Education
- reverse_order_rag score: 0.0000
  prediction: Not explicitly stated in the provided context.
  top_chunk: rank=1 score=0.3259 The opinons expressed are those of the authors and do not represent the views of the institute or the U.S. Department of Education
- random_order_rag score: 0.0000
  prediction: 20 evaluators were recruited from our institution and asked to each perform 20 annotations.
  top_chunk: rank=1 score=0.3259 The opinons expressed are those of the authors and do not represent the views of the institute or the U.S. Department of Education
- anchor1_doc_order_rag score: 0.0000
  prediction: Not provided in the context.
  top_chunk: rank=1 score=0.3259 The opinons expressed are those of the authors and do not represent the views of the institute or the U.S. Department of Education
- anchor2_doc_order_rag score: 0.0000
  prediction: Not provided in the context.
  top_chunk: rank=1 score=0.3259 The opinons expressed are those of the authors and do not represent the views of the institute or the U.S. Department of Education

#### qasper / 99e78c390932594bd833be0f5c890af5c605d808

- query: What is the baseline?
- references: QA PGNet, Multi-decoder QA PGNet with lookup table embedding | QA PGNet and Multi-decoder QA PGNet
- best_methods: anchor1_doc_order_rag
- disagreement: True
- vanilla_rag score: 11.7647
  prediction: `Nearest Number' for Dosage extraction and `Random Top-3' for Frequency extraction.
  top_chunk: rank=1 score=0.4107 Apart from learning-based baselines, we also create two naive baselines, one each for the Dosage and Frequency extraction tasks. For Dosage extraction, the baseline we consider is `Nearest Number', where we take the number nearest to the M…
- reorder_only_rag score: 11.7647
  prediction: Nearest Number for Dosage extraction and Random Top-3 for Frequency extraction.
  top_chunk: rank=1 score=0.4107 Apart from learning-based baselines, we also create two naive baselines, one each for the Dosage and Frequency extraction tasks. For Dosage extraction, the baseline we consider is `Nearest Number', where we take the number nearest to the M…
- reverse_order_rag score: 2.9412
  prediction: For Dosage extraction, the baseline we consider is `Nearest Number', where we take the number nearest to the Medication Name as the prediction, and `none' if no number is mentioned or if the Medication Name is not detected in the input. For Frequency extraction, the baseline we consider is `Random Top-3' where we predict a random Frequency tag, from top-3 most frequent ones from our dataset - {`n…
  top_chunk: rank=1 score=0.4107 Apart from learning-based baselines, we also create two naive baselines, one each for the Dosage and Frequency extraction tasks. For Dosage extraction, the baseline we consider is `Nearest Number', where we take the number nearest to the M…
- random_order_rag score: 0.0000
  prediction: Nearest Number
  top_chunk: rank=1 score=0.4107 Apart from learning-based baselines, we also create two naive baselines, one each for the Dosage and Frequency extraction tasks. For Dosage extraction, the baseline we consider is `Nearest Number', where we take the number nearest to the M…
- anchor1_doc_order_rag score: 20.0000
  prediction: `Nearest Number' and `none'
  top_chunk: rank=1 score=0.4107 Apart from learning-based baselines, we also create two naive baselines, one each for the Dosage and Frequency extraction tasks. For Dosage extraction, the baseline we consider is `Nearest Number', where we take the number nearest to the M…
- anchor2_doc_order_rag score: 11.7647
  prediction: `Nearest Number' for Dosage extraction, and `Random Top-3' for Frequency extraction.
  top_chunk: rank=1 score=0.4107 Apart from learning-based baselines, we also create two naive baselines, one each for the Dosage and Frequency extraction tasks. For Dosage extraction, the baseline we consider is `Nearest Number', where we take the number nearest to the M…

### narrative_qa

- examples: 50
- disagreements: 48
- any-positive-score: 30

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_1

- query: Where is the boarding-house located?
- references: Paris
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house.
  top_chunk: rank=1 score=0.3975 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…
- reorder_only_rag score: 0.0000
  prediction: in the Faubourg St. Germain
  top_chunk: rank=1 score=0.3975 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…
- reverse_order_rag score: 0.0000
  prediction: in the Boulevard Haussman
  top_chunk: rank=1 score=0.3975 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…
- random_order_rag score: 0.0000
  prediction: Faubourg St. Germain
  top_chunk: rank=1 score=0.3975 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…
- anchor1_doc_order_rag score: 0.0000
  prediction: from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house.
  top_chunk: rank=1 score=0.3975 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…
- anchor2_doc_order_rag score: 0.0000
  prediction: from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house.
  top_chunk: rank=1 score=0.3975 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_17

- query: What name does Herr Professor call Leon?
- references: Simian
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: insatiable little Leon
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…
- reorder_only_rag score: 0.0000
  prediction: exceedingly foreign
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…
- reverse_order_rag score: 0.0000
  prediction: "insatiable little Leon"
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…
- random_order_rag score: 0.0000
  prediction: "insatiable little Leon"
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…
- anchor1_doc_order_rag score: 0.0000
  prediction: my good Prosper
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…
- anchor2_doc_order_rag score: 0.0000
  prediction: My good Prosper
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_18

- query: Which traveler finds the other travelers "sub-human"?
- references: Herr Professor
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: She has a way of arriving at her ends which is more efficient than violence.
  top_chunk: rank=1 score=0.3351 But this New England maiden is, in her way, a strange type: she is travelling all over Europe alone--"to see it," she says, "for herself." For herself! What can that stiff slim self of hers do with such sights, such visions!
- reorder_only_rag score: 0.0000
  prediction: He appears to me less human than simian, and whenever I hear him talk I seem to myself to have paused in the street to listen to the shrill clatter of a hand-organ, to which the gambols of a hairy _homunculus_ form an accompaniment.
  top_chunk: rank=1 score=0.3351 But this New England maiden is, in her way, a strange type: she is travelling all over Europe alone--"to see it," she says, "for herself." For herself! What can that stiff slim self of hers do with such sights, such visions!
- reverse_order_rag score: 0.0000
  prediction: He accordingly engaged a room in the house of a lady of pure French extraction and education, who supplements the shortcomings of an income insufficient to the ever-growing demands of the Parisian system of sense-gratification, by providing food and lodging for a limited number of distinguished strangers. My dear brother in Science--I resume my hasty notes, of which I sent you the first instalmen…
  top_chunk: rank=1 score=0.3351 But this New England maiden is, in her way, a strange type: she is travelling all over Europe alone--"to see it," she says, "for herself." For herself! What can that stiff slim self of hers do with such sights, such visions!
- random_order_rag score: 0.0000
  prediction: He appears to me less human than simian, and whenever I hear him talk I seem to myself to have paused in the street to listen to the shrill clatter of a hand-organ, to which the gambols of a hairy _homunculus_ form an accompaniment.
  top_chunk: rank=1 score=0.3351 But this New England maiden is, in her way, a strange type: she is travelling all over Europe alone--"to see it," she says, "for herself." For herself! What can that stiff slim self of hers do with such sights, such visions!
- anchor1_doc_order_rag score: 0.0000
  prediction: He appears to me less human than simian, and whenever I hear him talk I seem to myself to have paused in the street to listen to the shrill clatter of a hand-organ, to which the gambols of a hairy _homunculus_ form an accompaniment.
  top_chunk: rank=1 score=0.3351 But this New England maiden is, in her way, a strange type: she is travelling all over Europe alone--"to see it," she says, "for herself." For herself! What can that stiff slim self of hers do with such sights, such visions!
- anchor2_doc_order_rag score: 0.0000
  prediction: He appears to me less human than simian, and whenever I hear him talk I seem to myself to have paused in the street to listen to the shrill clatter of a hand-organ, to which the gambols of a hairy _homunculus_ form an accompaniment.
  top_chunk: rank=1 score=0.3351 But this New England maiden is, in her way, a strange type: she is travelling all over Europe alone--"to see it," she says, "for herself." For herself! What can that stiff slim self of hers do with such sights, such visions!

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_19

- query: What does Evelyn Vane claim Leverett is always talking about?
- references: The color of the sky
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: "its being 'a real Corot day,' etc."
  top_chunk: rank=1 score=0.3699 You know I told you, in writing some time ago, that I had tried to get some insight into the position of woman in England, and, being here with Miss Vane, it has seemed to me to be a good opportunity to get a little more. I have asked her…
- reorder_only_rag score: 0.0000
  prediction: Boston
  top_chunk: rank=1 score=0.3699 You know I told you, in writing some time ago, that I had tried to get some insight into the position of woman in England, and, being here with Miss Vane, it has seemed to me to be a good opportunity to get a little more. I have asked her…
- reverse_order_rag score: 0.0000
  prediction: "its being 'a real Corot day,' etc."
  top_chunk: rank=1 score=0.3699 You know I told you, in writing some time ago, that I had tried to get some insight into the position of woman in England, and, being here with Miss Vane, it has seemed to me to be a good opportunity to get a little more. I have asked her…
- random_order_rag score: 0.0000
  prediction: "its being 'a real Corot day,' etc."
  top_chunk: rank=1 score=0.3699 You know I told you, in writing some time ago, that I had tried to get some insight into the position of woman in England, and, being here with Miss Vane, it has seemed to me to be a good opportunity to get a little more. I have asked her…
- anchor1_doc_order_rag score: 0.0000
  prediction: Boston
  top_chunk: rank=1 score=0.3699 You know I told you, in writing some time ago, that I had tried to get some insight into the position of woman in England, and, being here with Miss Vane, it has seemed to me to be a good opportunity to get a little more. I have asked her…
- anchor2_doc_order_rag score: 0.0000
  prediction: Boston
  top_chunk: rank=1 score=0.3699 You know I told you, in writing some time ago, that I had tried to get some insight into the position of woman in England, and, being here with Miss Vane, it has seemed to me to be a good opportunity to get a little more. I have asked her…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_20

- query: Where is the boarding house located?
- references: Paris
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: from the depths of a second-rate boarding-house.
  top_chunk: rank=1 score=0.3925 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…
- reorder_only_rag score: 0.0000
  prediction: in the Boulevard Haussman
  top_chunk: rank=1 score=0.3925 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…
- reverse_order_rag score: 0.0000
  prediction: in the Boulevard Haussman
  top_chunk: rank=1 score=0.3925 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…
- random_order_rag score: 0.0000
  prediction: in the Faubourg St. Germain
  top_chunk: rank=1 score=0.3925 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…
- anchor1_doc_order_rag score: 0.0000
  prediction: from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house.
  top_chunk: rank=1 score=0.3925 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…
- anchor2_doc_order_rag score: 0.0000
  prediction: from the depths of a second-rate boarding-house.
  top_chunk: rank=1 score=0.3925 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…

### quality

- examples: 50
- disagreements: 26
- any-positive-score: 37

#### quality / 30029_F5N22U40_4

- query: What is the most likely reason for Korvin's solitude in jail? (A) Solitary confinement was part of Korvin's punishment. (B) There weren't any other prisoners in the jail because virtually all of the Tr'en obey the Ruler. Those who don't obey are executed. (C) The Tr'en didn't want Korvin to interact with the other Tr'en prisoners because there was a chance that together they might incite an upris…
- references: There weren't any other prisoners in the jail because virtually all of the Tr'en obey the Ruler. Those who don't obey are executed.
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: The Tr'en are so logical and mathematic that they don't see the need for social interaction.
  top_chunk: rank=1 score=0.5857 The Wonders of Tr'en, according to all the advance reports, were likely to be pretty boring, but they'd have been better than nothing. In any decently-run jail, he told himself with indignation, there would at least have been other prisone…
- reorder_only_rag score: 0.0000
  prediction: The Tr'en are so logical and mathematic that they don't see the need for social interaction.
  top_chunk: rank=1 score=0.5857 The Wonders of Tr'en, according to all the advance reports, were likely to be pretty boring, but they'd have been better than nothing. In any decently-run jail, he told himself with indignation, there would at least have been other prisone…
- reverse_order_rag score: 0.0000
  prediction: D
  top_chunk: rank=1 score=0.5857 The Wonders of Tr'en, according to all the advance reports, were likely to be pretty boring, but they'd have been better than nothing. In any decently-run jail, he told himself with indignation, there would at least have been other prisone…
- random_order_rag score: 0.0000
  prediction: The Tr'en are so logical and mathematic that they don't see the need for social interaction.
  top_chunk: rank=1 score=0.5857 The Wonders of Tr'en, according to all the advance reports, were likely to be pretty boring, but they'd have been better than nothing. In any decently-run jail, he told himself with indignation, there would at least have been other prisone…
- anchor1_doc_order_rag score: 0.0000
  prediction: The Tr'en are so logical and mathematic that they don't see the need for social interaction.
  top_chunk: rank=1 score=0.5857 The Wonders of Tr'en, according to all the advance reports, were likely to be pretty boring, but they'd have been better than nothing. In any decently-run jail, he told himself with indignation, there would at least have been other prisone…
- anchor2_doc_order_rag score: 0.0000
  prediction: The Tr'en are so logical and mathematic that they don't see the need for social interaction.
  top_chunk: rank=1 score=0.5857 The Wonders of Tr'en, according to all the advance reports, were likely to be pretty boring, but they'd have been better than nothing. In any decently-run jail, he told himself with indignation, there would at least have been other prisone…

#### quality / 30029_F5N22U40_6

- query: Are there indications that the Tr'en would be interested in attacking Earth? Why or why not? (A) Both A and C are correct. (B) No, because Korvin sends a mission back to Earth Central saying that the Tr'en won't come marauding out into space. (C) Yes, because the expert mentions the idea of conquering Earth with Korvin's aid. (D) Yes, because the ruler says the he wants to know about Earth's weap…
- references: Yes, because the ruler says the he wants to know about Earth's weapons, plans, and fortifications.
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: No, because Korvin sends a mission back to Earth Central saying that the Tr'en won't come marauding out into space.
  top_chunk: rank=1 score=0.5556 If you didn't, you never had a second chance to try. But Korvin meant exactly what he'd said. He was going to obey the commands of the Ruler of the Tr'en—and remove the Tr'en threat from the rest of the galaxy forever. That, after all, was…
- reorder_only_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.5556 If you didn't, you never had a second chance to try. But Korvin meant exactly what he'd said. He was going to obey the commands of the Ruler of the Tr'en—and remove the Tr'en threat from the rest of the galaxy forever. That, after all, was…
- reverse_order_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.5556 If you didn't, you never had a second chance to try. But Korvin meant exactly what he'd said. He was going to obey the commands of the Ruler of the Tr'en—and remove the Tr'en threat from the rest of the galaxy forever. That, after all, was…
- random_order_rag score: 0.0000
  prediction: No, because Korvin sends a mission back to Earth Central saying that the Tr'en won't come marauding out into space.
  top_chunk: rank=1 score=0.5556 If you didn't, you never had a second chance to try. But Korvin meant exactly what he'd said. He was going to obey the commands of the Ruler of the Tr'en—and remove the Tr'en threat from the rest of the galaxy forever. That, after all, was…
- anchor1_doc_order_rag score: 0.0000
  prediction: No, because Korvin sends a mission back to Earth Central saying that the Tr'en won't come marauding out into space.
  top_chunk: rank=1 score=0.5556 If you didn't, you never had a second chance to try. But Korvin meant exactly what he'd said. He was going to obey the commands of the Ruler of the Tr'en—and remove the Tr'en threat from the rest of the galaxy forever. That, after all, was…
- anchor2_doc_order_rag score: 0.0000
  prediction: No, because Korvin sends a mission back to Earth Central saying that the Tr'en won't come marauding out into space.
  top_chunk: rank=1 score=0.5556 If you didn't, you never had a second chance to try. But Korvin meant exactly what he'd said. He was going to obey the commands of the Ruler of the Tr'en—and remove the Tr'en threat from the rest of the galaxy forever. That, after all, was…

#### quality / 62476_Z8GFDCIZ_2

- query: Did Duane actually kill Stevens? How do you know? (A) No, because even though he was attempting to kill Stevens, he blacked out before he had the chance. (B) No, because the nurse said that Stevens died of a head injury an hour before Duane woke up. (C) Yes, because once Duane woke up with amnesia, Andrias told him that he had killed Stevens. (D) Yes, because he shot Stevens with his dis-gun just…
- references: No, because even though he was attempting to kill Stevens, he blacked out before he had the chance.
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.6365 Duane got up, retrieving the two heat guns, and stared at him. " They tell me I killed Stevens the same way ," he thought. " I'm getting in a rut! " But Andrias was not dead, though he was out as cold as the void beyond Pluto. The thick ca…
- reorder_only_rag score: 0.0000
  prediction: No, because the nurse said that Stevens died of a head injury an hour before Duane woke up.
  top_chunk: rank=1 score=0.6365 Duane got up, retrieving the two heat guns, and stared at him. " They tell me I killed Stevens the same way ," he thought. " I'm getting in a rut! " But Andrias was not dead, though he was out as cold as the void beyond Pluto. The thick ca…
- reverse_order_rag score: 0.0000
  prediction: No, because the nurse said that Stevens died of a head injury an hour before Duane woke up.
  top_chunk: rank=1 score=0.6365 Duane got up, retrieving the two heat guns, and stared at him. " They tell me I killed Stevens the same way ," he thought. " I'm getting in a rut! " But Andrias was not dead, though he was out as cold as the void beyond Pluto. The thick ca…
- random_order_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.6365 Duane got up, retrieving the two heat guns, and stared at him. " They tell me I killed Stevens the same way ," he thought. " I'm getting in a rut! " But Andrias was not dead, though he was out as cold as the void beyond Pluto. The thick ca…
- anchor1_doc_order_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.6365 Duane got up, retrieving the two heat guns, and stared at him. " They tell me I killed Stevens the same way ," he thought. " I'm getting in a rut! " But Andrias was not dead, though he was out as cold as the void beyond Pluto. The thick ca…
- anchor2_doc_order_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.6365 Duane got up, retrieving the two heat guns, and stared at him. " They tell me I killed Stevens the same way ," he thought. " I'm getting in a rut! " But Andrias was not dead, though he was out as cold as the void beyond Pluto. The thick ca…

#### quality / 63401_ZCP5ZDGL_10

- query: What is the most likely reason that Johnathan decides to stay on the asteroid? (A) He realizes that his life as a pilot was unfulfilling, and he doesn't want to go back. (B) He realizes that he'd rather stay with wild women than travel back with the posh Doctor Boynton. (C) He realizes that he wants to stay and enjoy sexual relations with the twenty-seven beautiful women. (D) He realizes that if…
- references: He realizes that he wants to stay and enjoy sexual relations with the twenty-seven beautiful women.
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: He realizes that if he stays on the asteroid, he won't have to give up the tobacco seeds for experimentation and can grow and enjoy it himself.
  top_chunk: rank=1 score=0.5326 "I only came back here after the cigarettes." "But it will be three years before the asteroid's orbit brings it back in the space lanes," said Doctor Boynton. "You don't possibly expect to be picked up before then!" Jonathan shook his head…
- reorder_only_rag score: 0.0000
  prediction: He realizes that if he stays on the asteroid, he won't have to give up the tobacco seeds for experimentation and can grow and enjoy it himself.
  top_chunk: rank=1 score=0.5326 "I only came back here after the cigarettes." "But it will be three years before the asteroid's orbit brings it back in the space lanes," said Doctor Boynton. "You don't possibly expect to be picked up before then!" Jonathan shook his head…
- reverse_order_rag score: 0.0000
  prediction: He realizes that if he stays on the asteroid, he won't have to give up the tobacco seeds for experimentation and can grow and enjoy it himself.
  top_chunk: rank=1 score=0.5326 "I only came back here after the cigarettes." "But it will be three years before the asteroid's orbit brings it back in the space lanes," said Doctor Boynton. "You don't possibly expect to be picked up before then!" Jonathan shook his head…
- random_order_rag score: 0.0000
  prediction: D
  top_chunk: rank=1 score=0.5326 "I only came back here after the cigarettes." "But it will be three years before the asteroid's orbit brings it back in the space lanes," said Doctor Boynton. "You don't possibly expect to be picked up before then!" Jonathan shook his head…
- anchor1_doc_order_rag score: 0.0000
  prediction: He realizes that if he stays on the asteroid, he won't have to give up the tobacco seeds for experimentation and can grow and enjoy it himself.
  top_chunk: rank=1 score=0.5326 "I only came back here after the cigarettes." "But it will be three years before the asteroid's orbit brings it back in the space lanes," said Doctor Boynton. "You don't possibly expect to be picked up before then!" Jonathan shook his head…
- anchor2_doc_order_rag score: 0.0000
  prediction: He realizes that if he stays on the asteroid, he won't have to give up the tobacco seeds for experimentation and can grow and enjoy it himself.
  top_chunk: rank=1 score=0.5326 "I only came back here after the cigarettes." "But it will be three years before the asteroid's orbit brings it back in the space lanes," said Doctor Boynton. "You don't possibly expect to be picked up before then!" Jonathan shook his head…

#### quality / 63401_ZCP5ZDGL_4

- query: What was Ann intending to do with Johnathan under the trees before the other women showed up? (A) Sleep with him. (B) Convince him to help her cook dinner. (C) Ask him to be her boyfriend. (D) Talk to him about how he became a pilot.
- references: Sleep with him.
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.4963 He started to rise. Ann Clotilde placed the flat of her hand on his chest and shoved. " Ooof! " he grunted. He sat down rather more forcibly than he had risen. "Don't get up because of me," she informed him. "It's my turn to cook, but I sa…
- reorder_only_rag score: 0.0000
  prediction: C
  top_chunk: rank=1 score=0.4963 He started to rise. Ann Clotilde placed the flat of her hand on his chest and shoved. " Ooof! " he grunted. He sat down rather more forcibly than he had risen. "Don't get up because of me," she informed him. "It's my turn to cook, but I sa…
- reverse_order_rag score: 0.0000
  prediction: Talk to him about how he became a pilot.
  top_chunk: rank=1 score=0.4963 He started to rise. Ann Clotilde placed the flat of her hand on his chest and shoved. " Ooof! " he grunted. He sat down rather more forcibly than he had risen. "Don't get up because of me," she informed him. "It's my turn to cook, but I sa…
- random_order_rag score: 0.0000
  prediction: Talk to him about how he became a pilot.
  top_chunk: rank=1 score=0.4963 He started to rise. Ann Clotilde placed the flat of her hand on his chest and shoved. " Ooof! " he grunted. He sat down rather more forcibly than he had risen. "Don't get up because of me," she informed him. "It's my turn to cook, but I sa…
- anchor1_doc_order_rag score: 0.0000
  prediction: Talk to him about how he became a pilot.
  top_chunk: rank=1 score=0.4963 He started to rise. Ann Clotilde placed the flat of her hand on his chest and shoved. " Ooof! " he grunted. He sat down rather more forcibly than he had risen. "Don't get up because of me," she informed him. "It's my turn to cook, but I sa…
- anchor2_doc_order_rag score: 0.0000
  prediction: Talk to him about how he became a pilot.
  top_chunk: rank=1 score=0.4963 He started to rise. Ann Clotilde placed the flat of her hand on his chest and shoved. " Ooof! " he grunted. He sat down rather more forcibly than he had risen. "Don't get up because of me," she informed him. "It's my turn to cook, but I sa…

### contract_nli

- examples: 50
- disagreements: 18
- any-positive-score: 38

#### contract_nli / 7_nda-2

- query: Confidential Information shall only include technical information.
- references: Entailment
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5743 Confidential Information does not include information: (i) which is or becomes public knowledge and public property in any way without breach of this Agreement by the Recipient; (ii) which the Recipient can show has been known or has been…
- reorder_only_rag score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.5743 Confidential Information does not include information: (i) which is or becomes public knowledge and public property in any way without breach of this Agreement by the Recipient; (ii) which the Recipient can show has been known or has been…
- reverse_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5743 Confidential Information does not include information: (i) which is or becomes public knowledge and public property in any way without breach of this Agreement by the Recipient; (ii) which the Recipient can show has been known or has been…
- random_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5743 Confidential Information does not include information: (i) which is or becomes public knowledge and public property in any way without breach of this Agreement by the Recipient; (ii) which the Recipient can show has been known or has been…
- anchor1_doc_order_rag score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.5743 Confidential Information does not include information: (i) which is or becomes public knowledge and public property in any way without breach of this Agreement by the Recipient; (ii) which the Recipient can show has been known or has been…
- anchor2_doc_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5743 Confidential Information does not include information: (i) which is or becomes public knowledge and public property in any way without breach of this Agreement by the Recipient; (ii) which the Recipient can show has been known or has been…

#### contract_nli / 9_nda-2

- query: Confidential Information shall only include technical information.
- references: Entailment
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.4797 In addition, upon the completion of the services provided by VENDOR to BPS as outlined in this Agreement, VENDOR shall return or destroy, as BPS may instruct, all Confidential Information in VENDOR’S possession or control, whether in print…
- reorder_only_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.4797 In addition, upon the completion of the services provided by VENDOR to BPS as outlined in this Agreement, VENDOR shall return or destroy, as BPS may instruct, all Confidential Information in VENDOR’S possession or control, whether in print…
- reverse_order_rag score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.4797 In addition, upon the completion of the services provided by VENDOR to BPS as outlined in this Agreement, VENDOR shall return or destroy, as BPS may instruct, all Confidential Information in VENDOR’S possession or control, whether in print…
- random_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.4797 In addition, upon the completion of the services provided by VENDOR to BPS as outlined in this Agreement, VENDOR shall return or destroy, as BPS may instruct, all Confidential Information in VENDOR’S possession or control, whether in print…
- anchor1_doc_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.4797 In addition, upon the completion of the services provided by VENDOR to BPS as outlined in this Agreement, VENDOR shall return or destroy, as BPS may instruct, all Confidential Information in VENDOR’S possession or control, whether in print…
- anchor2_doc_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.4797 In addition, upon the completion of the services provided by VENDOR to BPS as outlined in this Agreement, VENDOR shall return or destroy, as BPS may instruct, all Confidential Information in VENDOR’S possession or control, whether in print…

#### contract_nli / 3_nda-1

- query: All Confidential Information shall be expressly identified by the Disclosing Party.
- references: Entailment
- best_methods: vanilla_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5949 In respect of Confidential Information disclosed in documentary form, model or any other tangible form, this shall be marked by the Disclosing Party as confidential or otherwise designated to show expressly or by necessary implication that…
- reorder_only_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5949 In respect of Confidential Information disclosed in documentary form, model or any other tangible form, this shall be marked by the Disclosing Party as confidential or otherwise designated to show expressly or by necessary implication that…
- reverse_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5949 In respect of Confidential Information disclosed in documentary form, model or any other tangible form, this shall be marked by the Disclosing Party as confidential or otherwise designated to show expressly or by necessary implication that…
- random_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5949 In respect of Confidential Information disclosed in documentary form, model or any other tangible form, this shall be marked by the Disclosing Party as confidential or otherwise designated to show expressly or by necessary implication that…
- anchor1_doc_order_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5949 In respect of Confidential Information disclosed in documentary form, model or any other tangible form, this shall be marked by the Disclosing Party as confidential or otherwise designated to show expressly or by necessary implication that…
- anchor2_doc_order_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5949 In respect of Confidential Information disclosed in documentary form, model or any other tangible form, this shall be marked by the Disclosing Party as confidential or otherwise designated to show expressly or by necessary implication that…

#### contract_nli / 3_nda-10

- query: Receiving Party shall not disclose the fact that Agreement was agreed or negotiated.
- references: Entailment
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag
- disagreement: True
- vanilla_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5796 In case of disagreement regarding said summary, the Receiving Party shall make any objections in writing within thirty (30) days of receipt of the written summary. “Disclosing Party” shall mean the Party that discloses Confidential Informa…
- reorder_only_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5796 In case of disagreement regarding said summary, the Receiving Party shall make any objections in writing within thirty (30) days of receipt of the written summary. “Disclosing Party” shall mean the Party that discloses Confidential Informa…
- reverse_order_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5796 In case of disagreement regarding said summary, the Receiving Party shall make any objections in writing within thirty (30) days of receipt of the written summary. “Disclosing Party” shall mean the Party that discloses Confidential Informa…
- random_order_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5796 In case of disagreement regarding said summary, the Receiving Party shall make any objections in writing within thirty (30) days of receipt of the written summary. “Disclosing Party” shall mean the Party that discloses Confidential Informa…
- anchor1_doc_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5796 In case of disagreement regarding said summary, the Receiving Party shall make any objections in writing within thirty (30) days of receipt of the written summary. “Disclosing Party” shall mean the Party that discloses Confidential Informa…
- anchor2_doc_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5796 In case of disagreement regarding said summary, the Receiving Party shall make any objections in writing within thirty (30) days of receipt of the written summary. “Disclosing Party” shall mean the Party that discloses Confidential Informa…

#### contract_nli / 3_nda-11

- query: Receiving Party shall not reverse engineer any objects which embody Disclosing Party's Confidential Information.
- references: Entailment
- best_methods: reorder_only_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5490 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
- reorder_only_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5490 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
- reverse_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5490 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
- random_order_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5490 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
- anchor1_doc_order_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5490 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
- anchor2_doc_order_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5490 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
