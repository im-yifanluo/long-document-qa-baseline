# Comparison Report

Run tier: `subset`

## Score Summary

| Task | Metric | vanilla_rag | reorder_only_rag | reverse_order_rag | random_order_rag | anchor1_doc_order_rag | anchor2_doc_order_rag | reorder_only_rag_minus_vanilla_rag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| qmsum | rouge | 15.4723 | 17.7533 | 15.5235 | 15.6500 | 17.4419 | 16.6657 | +2.2810 |
| qasper | f1 | 35.6440 | 41.4484 | 38.9560 | 30.9980 | 37.0943 | 36.6150 | +5.8044 |
| narrative_qa | f1 | 16.4705 | 16.3083 | 12.2325 | 16.8970 | 17.2424 | 17.0221 | -0.1622 |
| quality | exact_match | 48.0000 | 64.0000 | 56.0000 | 60.0000 | 62.0000 | 62.0000 | +16.0000 |
| contract_nli | exact_match | 68.0000 | 56.0000 | 56.0000 | 58.0000 | 64.0000 | 64.0000 | -12.0000 |

## Runtime Summary

| Method | Total seconds | Total minutes | Seconds / example | Examples / second |
| --- | --- | --- | --- | --- |
| vanilla_rag | 671.47 | 11.19 | 2.6859 | 0.3723 |
| reorder_only_rag | 529.04 | 8.82 | 2.1162 | 0.4726 |
| reverse_order_rag | 521.49 | 8.69 | 2.0860 | 0.4794 |
| random_order_rag | 672.87 | 11.21 | 2.6915 | 0.3715 |
| anchor1_doc_order_rag | 632.10 | 10.54 | 2.5284 | 0.3955 |
| anchor2_doc_order_rag | 636.84 | 10.61 | 2.5474 | 0.3926 |

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
- vanilla_rag score: 0.0000
  prediction: Based on the provided context, it seems that the group agreed to use the manually marked transcripts as a form of ground truth. Specifically, Professor E mentioned, "The idea of the manual marking was to say 'OK this, i you know, it's really here.'" This suggests that the manually marked transcripts were used to identify and mark specific instances for comparison and validation purposes.
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- reorder_only_rag score: 9.7507
  prediction: Based on the provided context, it was agreed that there was a forty-five-minute piece of transcription that was sent to IBM for comparison, and a larger piece of recorded data that was put on CD-ROM and sent to IBM for transcription. Additionally, it was mentioned that there were about ten hours of meetings that had been recorded and sent to IBM for transcription, though the exact amount of trans…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- reverse_order_rag score: 11.8388
  prediction: Based on the provided context, it appears that a sample of meeting transcripts was sent to IBM for transcription as a comparison point. Specifically, a 45-minute piece was transcribed and then sent to IBM, and a larger piece was recorded, put on CD-ROM, and sent to IBM for transcription. Additionally, there was a discussion about using the transcribed data for validation purposes, with the idea o…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- random_order_rag score: 6.8699
  prediction: Based on the provided context, it appears that some sample transcripts were sent to IBM for transcription. Professor E mentions, "That piece was then uh sent to IBM so they could transcribe so we have some comparison point." This indicates that a sample, likely a transcribed piece of the recorded meetings, was sent to IBM for their transcription, providing a comparison point for the accuracy of t…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- anchor1_doc_order_rag score: 0.0000
  prediction: Based on the provided context, it was agreed that there was a forty-five-minute piece of transcription that was sent to IBM for comparison, and a larger piece of recorded data that was put on CD-ROM and sent to IBM for transcription. Additionally, it was mentioned that about ten hours of meetings had been recorded and transcribed, and these were sent to IBM for comparison. Professor E also mentio…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- anchor2_doc_order_rag score: 0.0000
  prediction: Based on the provided context, it was agreed that there was a forty-five-minute piece of transcription that was sent to IBM for comparison, and a larger piece of recorded data that was put on CD-ROM and sent to IBM for transcription. Additionally, it was mentioned that there are about ten hours of other data that is not yet transcribed.
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…

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
- reverse_order_rag score: 4.1767
  prediction: Based on the context provided, the system would be involved in demos that are part of the applied project, as well as a potential institute-wide demo. Specifically: 1. There are current demos that the team has been working on, which are part of the applied project. These demos are important for the funding and requirements of the project. 2. There is a plan to have a more formal institute-wide de…
  top_chunk: rank=1 score=0.3783 Professor C: and , s deliberately . So , the reason I 'd like you to understand uh what 's going on in this demo system is not because it 's important to the research . It 's just for closure . So that if we come up with a question of " co…
- random_order_rag score: 7.8745
  prediction: Based on the context provided, the system would be involved in demos for the Fall, with the requirements for these demos being taken care of as of later that week. Additionally, there is mention of a Texas speech version of the system, which is simpler and planned for completion in October, but this is too late for the current project. The system is also designed to work with a virtual touch scre…
  top_chunk: rank=1 score=0.3783 Professor C: and , s deliberately . So , the reason I 'd like you to understand uh what 's going on in this demo system is not because it 's important to the research . It 's just for closure . So that if we come up with a question of " co…
- anchor1_doc_order_rag score: 8.2366
  prediction: The system would be involved in demos for funding requirements, specifically for the Fall demo requirements, which are considered to be taken care of as of later that week. There is also a plan to set up an internal demo that could potentially be expanded to an institute-wide demo, where someone could demonstrate the system to others, such as when someone on the streets asks about SmartKom. Addit…
  top_chunk: rank=1 score=0.3783 Professor C: and , s deliberately . So , the reason I 'd like you to understand uh what 's going on in this demo system is not because it 's important to the research . It 's just for closure . So that if we come up with a question of " co…
- anchor2_doc_order_rag score: 8.0022
  prediction: The system would be involved in demos for the Fall, with the demo requirements for that period being taken care of as of later that week. Additionally, there is a suggestion to set up an internal demo that could be shown to anyone interested, which might even be expanded to an institute-wide demo where people can see what SmartKom is about. There is also a plan to give a talk in the big room to i…
  top_chunk: rank=1 score=0.3783 Professor C: and , s deliberately . So , the reason I 'd like you to understand uh what 's going on in this demo system is not because it 's important to the research . It 's just for closure . So that if we come up with a question of " co…

#### qmsum / va-gq-5

- query: What were the main discussion points of the meeting?
- references: The group discussed topics including a potential collaboration with another ICSI member regarding the analysis of inference structures, efforts by speaker mn005 to detect speaker overlap, the current status of recordings and transcriptions, and future efforts to collect meeting data. In addition to weekly meetings by the BMR group, efforts are in progress to record meetings by other ICSI research…
- best_methods: anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 8.3574
  prediction: The main discussion points of the meeting included: 1. **Recording Meetings**: The group discussed recording meetings, particularly those of the Network Services and Applications group, and the potential for recording other meetings at ICSI that might have more emotional or conflict aspects. 2. **Data Collection and Analysis**: There was a discussion about the amount of data collected so far, the…
  top_chunk: rank=1 score=0.3285 Uh , we {disfmarker} I think the things that we talk about in this meeting uh tend to be a mixture of uh procedural uh mundane things and uh research points and um I was thinking I think it was a meeting a couple of weeks ago that we {disf…
- reorder_only_rag score: 7.1647
  prediction: The main discussion points of the meeting included: 1. **Data Collection and Transcription**: The group discussed the amount of data collected so far, including meetings from different groups and the possibility of recording more meetings. They also talked about the transcription process and the time it takes to transcribe the data. 2. **Acoustic Event Detection**: PhD D discussed their work on d…
  top_chunk: rank=1 score=0.3285 Uh , we {disfmarker} I think the things that we talk about in this meeting uh tend to be a mixture of uh procedural uh mundane things and uh research points and um I was thinking I think it was a meeting a couple of weeks ago that we {disf…
- reverse_order_rag score: 5.7072
  prediction: The main discussion points of the meeting included: 1. Recording meetings for data collection, particularly from radio and television stations. 2. Exploring the possibility of recording meetings from other departments and groups on campus. 3. Discussing the feasibility of recording meetings that have some level of conflict or emotional aspects. 4. Considering the use of the recorded meetings for…
  top_chunk: rank=1 score=0.3285 Uh , we {disfmarker} I think the things that we talk about in this meeting uh tend to be a mixture of uh procedural uh mundane things and uh research points and um I was thinking I think it was a meeting a couple of weeks ago that we {disf…
- random_order_rag score: 6.0119
  prediction: The main discussion points of the meeting included: 1. **Data Collection and Transcription**: The group discussed the process of collecting and transcribing audio data, particularly focusing on the time-consuming nature of manual marking of speaker overlaps and the potential for using close-miking techniques to infer overlaps. 2. **Acoustic Event Detection**: There was a discussion on detecting o…
  top_chunk: rank=1 score=0.3285 Uh , we {disfmarker} I think the things that we talk about in this meeting uh tend to be a mixture of uh procedural uh mundane things and uh research points and um I was thinking I think it was a meeting a couple of weeks ago that we {disf…
- anchor1_doc_order_rag score: 8.1593
  prediction: The main discussion points of the meeting included: 1. **Meeting Recording and Data Collection**: The group discussed recording meetings, particularly those of the natural language group, the network services and applications group, and the morning meetings. They also talked about recording meetings from other departments and possibly local broadcast media. 2. **Data Analysis and Transcription**:…
  top_chunk: rank=1 score=0.3285 Uh , we {disfmarker} I think the things that we talk about in this meeting uh tend to be a mixture of uh procedural uh mundane things and uh research points and um I was thinking I think it was a meeting a couple of weeks ago that we {disf…
- anchor2_doc_order_rag score: 8.9922
  prediction: The main discussion points of the meeting included: 1. **Meeting Recording and Data Collection**: The group discussed recording meetings, particularly those of the natural language group, the network services and applications group, and the morning meetings. They also talked about the potential to record meetings from outside their group and the possibility of collecting up to 50-60 hours of data…
  top_chunk: rank=1 score=0.3285 Uh , we {disfmarker} I think the things that we talk about in this meeting uh tend to be a mixture of uh procedural uh mundane things and uh research points and um I was thinking I think it was a meeting a couple of weeks ago that we {disf…

#### qmsum / va-sq-46

- query: What were the problems encountered with SmartKom system?
- references: The translation of SmartKom to english is in its final stages. The synthesis module will be the last one to do, after the english syntax trees are completed. The system is still buggy and unstable, but it will soon be ready for a demonstration.
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 9.3185
  prediction: Based on the context provided, some problems encountered with the SmartKom system include: 1. The system was not fully functional and required a lot of setup to work. Specifically, it was mentioned that "the version that is, the full version that's on the server does not work" and "you need to do a lot of stuff to make it work." 2. The system was described as "brittle" and required multiple chang…
  top_chunk: rank=1 score=0.3394 The {disfmarker} we got to the point where we can now speak into the SmartKom system , and it 'll go all the way through and then say something like " Roman numeral one , am Smarticus . " It actually says , " Roemisch einz , am Smarticus ,…
- reorder_only_rag score: 7.9484
  prediction: The problems encountered with the SmartKom system included instability, the need for extensive manual configuration, and the fact that it did not work without shortcuts. Specifically, the system required a lot of manual intervention to make it work, and even developers like Tilman and Ralf noted that there was never a fully working version without these shortcuts. Additionally, the system was des…
  top_chunk: rank=1 score=0.3394 The {disfmarker} we got to the point where we can now speak into the SmartKom system , and it 'll go all the way through and then say something like " Roman numeral one , am Smarticus . " It actually says , " Roemisch einz , am Smarticus ,…
- reverse_order_rag score: 5.9925
  prediction: Based on the provided context, some problems encountered with the SmartKom system include: 1. **Instability**: The system is described as unstable, requiring extra XML messages to be piped in from left and right before it works properly. 2. **Complexity and Messiness**: The system is described as messy, but once understood, it is comprehensible. 3. **Brittleness**: The system is brittle and requi…
  top_chunk: rank=1 score=0.3394 The {disfmarker} we got to the point where we can now speak into the SmartKom system , and it 'll go all the way through and then say something like " Roman numeral one , am Smarticus . " It actually says , " Roemisch einz , am Smarticus ,…
- random_order_rag score: 5.4335
  prediction: Based on the provided context, the problems encountered with the SmartKom system include: 1. **Brittleness and Complexity**: The system is described as brittle, requiring significant manual intervention to get it running. Specifically, it was mentioned that "you need to do a lot of stuff to make it work" and that "they actually have to make 20 changes on seventeen modules before they actually can…
  top_chunk: rank=1 score=0.3394 The {disfmarker} we got to the point where we can now speak into the SmartKom system , and it 'll go all the way through and then say something like " Roman numeral one , am Smarticus . " It actually says , " Roemisch einz , am Smarticus ,…
- anchor1_doc_order_rag score: 5.2820
  prediction: The problems encountered with the SmartKom system included: 1. Instability: The system was described as unstable, with many issues that needed to be resolved. 2. Complexity: The system required a lot of setup and configuration to work properly. For example, it needed to be piped in with extra XML messages from left and right. 3. Shortcomings in the German version: The full version on the server d…
  top_chunk: rank=1 score=0.3394 The {disfmarker} we got to the point where we can now speak into the SmartKom system , and it 'll go all the way through and then say something like " Roman numeral one , am Smarticus . " It actually says , " Roemisch einz , am Smarticus ,…
- anchor2_doc_order_rag score: 5.3659
  prediction: The problems encountered with the SmartKom system included: 1. **Complexity and Instability**: The system was described as unstable, requiring a lot of manual adjustments to make it work properly. For instance, it needed to be "piped in extra XML messages from left and right" to function correctly. 2. **Shortcomings in the Full Version**: The full version of the system on the server did not work,…
  top_chunk: rank=1 score=0.3394 The {disfmarker} we got to the point where we can now speak into the SmartKom system , and it 'll go all the way through and then say something like " Roman numeral one , am Smarticus . " It actually says , " Roemisch einz , am Smarticus ,…

#### qmsum / va-sq-2

- query: What was said on speech overlap?
- references: Efforts by speaker mn005 are in progress to detect overlapping speech. For a single transcribed meeting, speaker mn005 reported approximately 300 cases of overlap. Future work will involve manually deriving time marks from sections of overlapping speech for the same meeting, and then experimenting with different measures, e.g. energy increase, to determine a set of acoustically salient features f…
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 9.4551
  prediction: PhD D mentioned finding three hundred overlapping speech events in forty-five minutes of session recordings. PhD D considered the entirety of the overlapping zone where three or more speakers were talking together as one acoustic event. PhD D also noted that this process was very time-consuming, and suggested focusing only on marking the speaker overlaps to make progress. Professor E and others d…
  top_chunk: rank=1 score=0.4702 Eh almost eh three hundred eh in one session Grad G: Oh , God ! PhD D: in five {disfmarker} eh in forty - five minutes . PhD A: Three hundred overlapping speech {disfmarker} PhD D: Alm - Three hundred overlapping zone . Grad G: Ugh . PhD C…
- reorder_only_rag score: 5.0616
  prediction: Based on the provided context, the discussion around speech overlap involved several key points: 1. **Definition and Counting of Overlaps**: PhD D mentioned finding 300 overlapping speech zones in a 45-minute session, but when questioned, clarified that this was for the entire session, not just the 45 minutes initially discussed. The overlaps were marked by Jane, another participant. 2. **Manual…
  top_chunk: rank=1 score=0.4702 Eh almost eh three hundred eh in one session Grad G: Oh , God ! PhD D: in five {disfmarker} eh in forty - five minutes . PhD A: Three hundred overlapping speech {disfmarker} PhD D: Alm - Three hundred overlapping zone . Grad G: Ugh . PhD C…
- reverse_order_rag score: 6.4024
  prediction: Based on the provided context, the discussion around speech overlap involved several points: 1. **Recording and Transcription**: Professor E and others discussed the possibility of recording distant microphone channels to capture speech overlaps. They also talked about the need for transcriptions and the challenges of manual marking of overlaps. 2. **Overlap Marking**: PhD D mentioned that they h…
  top_chunk: rank=1 score=0.4702 Eh almost eh three hundred eh in one session Grad G: Oh , God ! PhD D: in five {disfmarker} eh in forty - five minutes . PhD A: Three hundred overlapping speech {disfmarker} PhD D: Alm - Three hundred overlapping zone . Grad G: Ugh . PhD C…
- random_order_rag score: 5.0217
  prediction: Based on the provided context, the discussion around speech overlap primarily centered around the following points: 1. **Definition and Counting of Overlaps**: PhD D mentioned finding 1,000 acoustic events, including overlaps, in a 12-minute session. Professor E asked how many of those were silent sections, and PhD D responded that they were not silent but too much speech. 2. **Manual Marking vs.…
  top_chunk: rank=1 score=0.4702 Eh almost eh three hundred eh in one session Grad G: Oh , God ! PhD D: in five {disfmarker} eh in forty - five minutes . PhD A: Three hundred overlapping speech {disfmarker} PhD D: Alm - Three hundred overlapping zone . Grad G: Ugh . PhD C…
- anchor1_doc_order_rag score: 7.9356
  prediction: The discussion centered around the identification and analysis of speech overlaps in recorded meetings. PhD D mentioned finding three hundred overlapping speech events in a forty-five minute session, which was later clarified to be across the entire session, not just the twelve minutes initially discussed. The team was working on identifying overlapping speech zones and other acoustic events, suc…
  top_chunk: rank=1 score=0.4702 Eh almost eh three hundred eh in one session Grad G: Oh , God ! PhD D: in five {disfmarker} eh in forty - five minutes . PhD A: Three hundred overlapping speech {disfmarker} PhD D: Alm - Three hundred overlapping zone . Grad G: Ugh . PhD C…
- anchor2_doc_order_rag score: 9.3660
  prediction: The discussion centered around the concept of speech overlap in recordings, particularly in meetings. PhD D mentioned finding three hundred overlapping speech events in a forty-five minute session, which was later clarified to be across the entire session, not just the twelve minutes initially discussed. The team was trying to define and quantify overlapping speech and other acoustic events. They…
  top_chunk: rank=1 score=0.4702 Eh almost eh three hundred eh in one session Grad G: Oh , God ! PhD D: in five {disfmarker} eh in forty - five minutes . PhD A: Three hundred overlapping speech {disfmarker} PhD D: Alm - Three hundred overlapping zone . Grad G: Ugh . PhD C…

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
  prediction: BERT outperforms other systems in recall and achieves the highest F1-score in some experiments.
  top_chunk: rank=1 score=0.5670 A fact worth highlighting is that, according to these results, BERT achieves a precision lower than the rest of the systems (i.e., it makes more false positive predictions); in exchange, it obtains a remarkably higher recall. Noticeably, i…
- random_order_rag score: 0.0000
  prediction: BERT outperforms them again.
  top_chunk: rank=1 score=0.5670 A fact worth highlighting is that, according to these results, BERT achieves a precision lower than the rest of the systems (i.e., it makes more false positive predictions); in exchange, it obtains a remarkably higher recall. Noticeably, i…
- anchor1_doc_order_rag score: 0.0000
  prediction: BERT-based model shows the highest robustness to training-data scarcity, loosing only 7 points of F1-score when trained on 230 instances instead of 21,371.
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

#### qasper / a87a009c242d57c51fc94fe312af5e02070f898b

- query: What predictive model do they build?
- references: logistic regression models | logistic regression models based on unigram bag-of-words features (BOW), sentiment signals (SENT), the linguistic features from our earlier analyses (LING), and combinations of these features.
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 15.7895
  prediction: We build a predictive model that uses linguistic features to classify dogmatic posts from Reddit.
  top_chunk: rank=1 score=0.4665 A predictive model further validates our feature sets, and also allows us to analyze dogmatism in millions of other Reddit comments in a scalable way, with multiple uses in ongoing, downstream analyses. Prediction task. Our goal is (1) to…
- reorder_only_rag score: 5.2632
  prediction: We build a predictive model that uses linguistic feature sets to predict dogmatism in comments.
  top_chunk: rank=1 score=0.4665 A predictive model further validates our feature sets, and also allows us to analyze dogmatism in millions of other Reddit comments in a scalable way, with multiple uses in ongoing, downstream analyses. Prediction task. Our goal is (1) to…
- reverse_order_rag score: 5.8824
  prediction: We train a predictive model to classify dogmatic posts from Reddit.
  top_chunk: rank=1 score=0.4665 A predictive model further validates our feature sets, and also allows us to analyze dogmatism in millions of other Reddit comments in a scalable way, with multiple uses in ongoing, downstream analyses. Prediction task. Our goal is (1) to…
- random_order_rag score: 5.8824
  prediction: We build a predictive model to classify dogmatic posts from Reddit.
  top_chunk: rank=1 score=0.4665 A predictive model further validates our feature sets, and also allows us to analyze dogmatism in millions of other Reddit comments in a scalable way, with multiple uses in ongoing, downstream analyses. Prediction task. Our goal is (1) to…
- anchor1_doc_order_rag score: 14.2857
  prediction: We train a predictive model to classify dogmatic posts from Reddit, one of the most popular discussion communities on the web.
  top_chunk: rank=1 score=0.4665 A predictive model further validates our feature sets, and also allows us to analyze dogmatism in millions of other Reddit comments in a scalable way, with multiple uses in ongoing, downstream analyses. Prediction task. Our goal is (1) to…
- anchor2_doc_order_rag score: 0.0000
  prediction: We build a predictive model that analyzes new content.
  top_chunk: rank=1 score=0.4665 A predictive model further validates our feature sets, and also allows us to analyze dogmatism in millions of other Reddit comments in a scalable way, with multiple uses in ongoing, downstream analyses. Prediction task. Our goal is (1) to…

### narrative_qa

- examples: 50
- disagreements: 48
- any-positive-score: 33

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_1

- query: Where is the boarding-house located?
- references: Paris
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house.
  top_chunk: rank=1 score=0.3975 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…
- reorder_only_rag score: 0.0000
  prediction: in the Boulevard Haussman
  top_chunk: rank=1 score=0.3975 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…
- reverse_order_rag score: 0.0000
  prediction: in the Boulevard Haussman
  top_chunk: rank=1 score=0.3975 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…
- random_order_rag score: 0.0000
  prediction: the Boulevard Haussman
  top_chunk: rank=1 score=0.3975 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…
- anchor1_doc_order_rag score: 0.0000
  prediction: from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house.
  top_chunk: rank=1 score=0.3975 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…
- anchor2_doc_order_rag score: 0.0000
  prediction: from the depths of a second-rate boarding-house.
  top_chunk: rank=1 score=0.3975 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_12

- query: Where is Herr professor from?
- references: Germany
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: German
  top_chunk: rank=1 score=0.2680 But at such a time as this there is always one person who seems interested in what I say--a German gentleman, a professor, who sits next to me at dinner, and whom I must tell you more about another time. He is very learned, and has a great…
- reorder_only_rag score: 0.0000
  prediction: He is a German gentleman, a professor, or doctor.
  top_chunk: rank=1 score=0.2680 But at such a time as this there is always one person who seems interested in what I say--a German gentleman, a professor, who sits next to me at dinner, and whom I must tell you more about another time. He is very learned, and has a great…
- reverse_order_rag score: 0.0000
  prediction: He is a German professor.
  top_chunk: rank=1 score=0.2680 But at such a time as this there is always one person who seems interested in what I say--a German gentleman, a professor, who sits next to me at dinner, and whom I must tell you more about another time. He is very learned, and has a great…
- random_order_rag score: 0.0000
  prediction: German
  top_chunk: rank=1 score=0.2680 But at such a time as this there is always one person who seems interested in what I say--a German gentleman, a professor, who sits next to me at dinner, and whom I must tell you more about another time. He is very learned, and has a great…
- anchor1_doc_order_rag score: 0.0000
  prediction: Pomeranian
  top_chunk: rank=1 score=0.2680 But at such a time as this there is always one person who seems interested in what I say--a German gentleman, a professor, who sits next to me at dinner, and whom I must tell you more about another time. He is very learned, and has a great…
- anchor2_doc_order_rag score: 0.0000
  prediction: German
  top_chunk: rank=1 score=0.2680 But at such a time as this there is always one person who seems interested in what I say--a German gentleman, a professor, who sits next to me at dinner, and whom I must tell you more about another time. He is very learned, and has a great…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_17

- query: What name does Herr Professor call Leon?
- references: Simian
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too.
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…
- reorder_only_rag score: 0.0000
  prediction: Herr Professor calls Leon "le petit Leon" or "my little Leon".
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…
- reverse_order_rag score: 0.0000
  prediction: intellectual broom
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…
- random_order_rag score: 0.0000
  prediction: insatiable little Leon
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…
- anchor1_doc_order_rag score: 0.0000
  prediction: homunculus
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…
- anchor2_doc_order_rag score: 0.0000
  prediction: Mr. Verdier
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_18

- query: Which traveler finds the other travelers "sub-human"?
- references: Herr Professor
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: She seems to think she can tell me everything, because I told her I was travelling for general culture. Well, I _do_ want to know so much that it seems sometimes as if I wanted to know everything; and yet there are some things that I think I don't want to know. But, as a general thing, everything is intensely interesting; I don't mean only everything that this French lady tells me, but everything…
  top_chunk: rank=1 score=0.3351 But this New England maiden is, in her way, a strange type: she is travelling all over Europe alone--"to see it," she says, "for herself." For herself! What can that stiff slim self of hers do with such sights, such visions!
- reorder_only_rag score: 0.0000
  prediction: He appears to me less human than simian, and whenever I hear him talk I seem to myself to have paused in the street to listen to the shrill clatter of a hand-organ, to which the gambols of a hairy _homunculus_ form an accompaniment.
  top_chunk: rank=1 score=0.3351 But this New England maiden is, in her way, a strange type: she is travelling all over Europe alone--"to see it," she says, "for herself." For herself! What can that stiff slim self of hers do with such sights, such visions!
- reverse_order_rag score: 0.0000
  prediction: They are not very sure that there are any Germans; they have already forgotten the convincing proofs of the fact that were presented to them nine years ago. A German was something disagreeable, which they determined to keep out of their conception of things. I therefore think that we are wrong to govern ourselves upon the hypothesis of the _revanche_; the French nature is too shallow for that lar…
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

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_22

- query: What doesn't Miranda like about Europe?
- references: how women are treated | the Old World treatment of its women
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: She is very cross (mamma writes me) about coming abroad, and doesn't seem at all to mind the expense that papa has been put to--talks very ill-naturedly about losing the hunting, etc. She expected to begin to hunt in December, and wants to know whether anybody keeps hounds at Hyeres.
  top_chunk: rank=1 score=0.4467 will brighten for the deep-lunged children of the Fatherland! CHAPTER IX MIRANDA HOPE TO HER MOTHER. October 22d Dear Mother--I am off in a day or two to visit some new country; I haven't yet decided which. I have satisfied myself with reg…
- reorder_only_rag score: 0.0000
  prediction: She doesn't like that Americans sometimes express surprise that she should be travelling round alone.
  top_chunk: rank=1 score=0.4467 will brighten for the deep-lunged children of the Fatherland! CHAPTER IX MIRANDA HOPE TO HER MOTHER. October 22d Dear Mother--I am off in a day or two to visit some new country; I haven't yet decided which. I have satisfied myself with reg…
- reverse_order_rag score: 0.0000
  prediction: Miranda doesn't like that some Americans express surprise that she should be travelling round alone.
  top_chunk: rank=1 score=0.4467 will brighten for the deep-lunged children of the Fatherland! CHAPTER IX MIRANDA HOPE TO HER MOTHER. October 22d Dear Mother--I am off in a day or two to visit some new country; I haven't yet decided which. I have satisfied myself with reg…
- random_order_rag score: 0.0000
  prediction: She doesn't like that Americans sometimes express surprise that she should be travelling round alone.
  top_chunk: rank=1 score=0.4467 will brighten for the deep-lunged children of the Fatherland! CHAPTER IX MIRANDA HOPE TO HER MOTHER. October 22d Dear Mother--I am off in a day or two to visit some new country; I haven't yet decided which. I have satisfied myself with reg…
- anchor1_doc_order_rag score: 0.0000
  prediction: She doesn't like that Americans sometimes express surprise that she should be travelling round alone.
  top_chunk: rank=1 score=0.4467 will brighten for the deep-lunged children of the Fatherland! CHAPTER IX MIRANDA HOPE TO HER MOTHER. October 22d Dear Mother--I am off in a day or two to visit some new country; I haven't yet decided which. I have satisfied myself with reg…
- anchor2_doc_order_rag score: 0.0000
  prediction: She doesn't like that Americans sometimes express surprise that she should be travelling round alone.
  top_chunk: rank=1 score=0.4467 will brighten for the deep-lunged children of the Fatherland! CHAPTER IX MIRANDA HOPE TO HER MOTHER. October 22d Dear Mother--I am off in a day or two to visit some new country; I haven't yet decided which. I have satisfied myself with reg…

### quality

- examples: 50
- disagreements: 25
- any-positive-score: 35

#### quality / 30029_F5N22U40_3

- query: How was Korvin able to avoid disclosing the true intent of his mission under the lie detector questioning? (A) While he was strapped down in the lie-detector, Korvin subtly switched the wire that indicated a truth with the one that indicated a lie. (B) Korvin said truths that literally answered the Tr'en's questions but evaded the intent behind their questions. . (C) The Tr'en hadn't tested the l…
- references: Korvin said truths that literally answered the Tr'en's questions but evaded the intent behind their questions. .
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: B Korvin said truths that literally answered the Tr'en's questions but evaded the intent behind their questions.
  top_chunk: rank=1 score=0.5941 True, every night the guards came in and gave him a concentrated lesson in the local language, but Korvin failed to get much pleasure out of that, being unconscious at the time. But now he was equipped to discuss almost anything from philo…
- reorder_only_rag score: 0.0000
  prediction: B Korvin said truths that literally answered the Tr'en's questions but evaded the intent behind their questions.
  top_chunk: rank=1 score=0.5941 True, every night the guards came in and gave him a concentrated lesson in the local language, but Korvin failed to get much pleasure out of that, being unconscious at the time. But now he was equipped to discuss almost anything from philo…
- reverse_order_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.5941 True, every night the guards came in and gave him a concentrated lesson in the local language, but Korvin failed to get much pleasure out of that, being unconscious at the time. But now he was equipped to discuss almost anything from philo…
- random_order_rag score: 0.0000
  prediction: B Korvin said truths that literally answered the Tr'en's questions but evaded the intent behind their questions.
  top_chunk: rank=1 score=0.5941 True, every night the guards came in and gave him a concentrated lesson in the local language, but Korvin failed to get much pleasure out of that, being unconscious at the time. But now he was equipped to discuss almost anything from philo…
- anchor1_doc_order_rag score: 0.0000
  prediction: B Korvin said truths that literally answered the Tr'en's questions but evaded the intent behind their questions.
  top_chunk: rank=1 score=0.5941 True, every night the guards came in and gave him a concentrated lesson in the local language, but Korvin failed to get much pleasure out of that, being unconscious at the time. But now he was equipped to discuss almost anything from philo…
- anchor2_doc_order_rag score: 0.0000
  prediction: B Korvin said truths that literally answered the Tr'en's questions but evaded the intent behind their questions.
  top_chunk: rank=1 score=0.5941 True, every night the guards came in and gave him a concentrated lesson in the local language, but Korvin failed to get much pleasure out of that, being unconscious at the time. But now he was equipped to discuss almost anything from philo…

#### quality / 30029_F5N22U40_6

- query: Are there indications that the Tr'en would be interested in attacking Earth? Why or why not? (A) Both A and C are correct. (B) No, because Korvin sends a mission back to Earth Central saying that the Tr'en won't come marauding out into space. (C) Yes, because the expert mentions the idea of conquering Earth with Korvin's aid. (D) Yes, because the ruler says the he wants to know about Earth's weap…
- references: Yes, because the ruler says the he wants to know about Earth's weapons, plans, and fortifications.
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.5556 If you didn't, you never had a second chance to try. But Korvin meant exactly what he'd said. He was going to obey the commands of the Ruler of the Tr'en—and remove the Tr'en threat from the rest of the galaxy forever. That, after all, was…
- reorder_only_rag score: 0.0000
  prediction: D
  top_chunk: rank=1 score=0.5556 If you didn't, you never had a second chance to try. But Korvin meant exactly what he'd said. He was going to obey the commands of the Ruler of the Tr'en—and remove the Tr'en threat from the rest of the galaxy forever. That, after all, was…
- reverse_order_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.5556 If you didn't, you never had a second chance to try. But Korvin meant exactly what he'd said. He was going to obey the commands of the Ruler of the Tr'en—and remove the Tr'en threat from the rest of the galaxy forever. That, after all, was…
- random_order_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.5556 If you didn't, you never had a second chance to try. But Korvin meant exactly what he'd said. He was going to obey the commands of the Ruler of the Tr'en—and remove the Tr'en threat from the rest of the galaxy forever. That, after all, was…
- anchor1_doc_order_rag score: 0.0000
  prediction: D
  top_chunk: rank=1 score=0.5556 If you didn't, you never had a second chance to try. But Korvin meant exactly what he'd said. He was going to obey the commands of the Ruler of the Tr'en—and remove the Tr'en threat from the rest of the galaxy forever. That, after all, was…
- anchor2_doc_order_rag score: 0.0000
  prediction: Both A and C are correct.
  top_chunk: rank=1 score=0.5556 If you didn't, you never had a second chance to try. But Korvin meant exactly what he'd said. He was going to obey the commands of the Ruler of the Tr'en—and remove the Tr'en threat from the rest of the galaxy forever. That, after all, was…

#### quality / 52845_75VB1ISR_2

- query: Why does Deirdre get so upset when Blake Past suggests she go to prom with the young man? (A) Because Blake is trying to guilt Deirdre into going with the young man by telling her that it'll ease her conscience. (B) Because Deirdre has fallen in love with Blake, despite his age, and wants him to take her to the prom. (C) Because Blake is acting like he's her father, which is a sensitive topic for…
- references: Because Deirdre has fallen in love with Blake, despite his age, and wants him to take her to the prom.
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Because Blake is acting like he's her father, which is a sensitive topic for Deirdre because she lost her real parents.
  top_chunk: rank=1 score=0.6406 Lord, he must have been feeling old to have pictured himself like that! Deirdre was speaking. "Yes," she was saying, "at nine o'clock. And I should very much like for you to come." Blake Past shook his head. "Proms aren't for parents. You…
- reorder_only_rag score: 0.0000
  prediction: Because Blake is trying to guilt Deirdre into going with the young man by telling her that it'll ease his conscience.
  top_chunk: rank=1 score=0.6406 Lord, he must have been feeling old to have pictured himself like that! Deirdre was speaking. "Yes," she was saying, "at nine o'clock. And I should very much like for you to come." Blake Past shook his head. "Proms aren't for parents. You…
- reverse_order_rag score: 0.0000
  prediction: Because the young man gave up his right arm in order to afford tickets to the prom, and this disgusts Deirdre.
  top_chunk: rank=1 score=0.6406 Lord, he must have been feeling old to have pictured himself like that! Deirdre was speaking. "Yes," she was saying, "at nine o'clock. And I should very much like for you to come." Blake Past shook his head. "Proms aren't for parents. You…
- random_order_rag score: 0.0000
  prediction: Because Blake is acting like he's her father, which is a sensitive topic for Deirdre because she lost her real parents.
  top_chunk: rank=1 score=0.6406 Lord, he must have been feeling old to have pictured himself like that! Deirdre was speaking. "Yes," she was saying, "at nine o'clock. And I should very much like for you to come." Blake Past shook his head. "Proms aren't for parents. You…
- anchor1_doc_order_rag score: 0.0000
  prediction: Because Blake is trying to guilt Deirdre into going with the young man by telling her that it'll ease his conscience.
  top_chunk: rank=1 score=0.6406 Lord, he must have been feeling old to have pictured himself like that! Deirdre was speaking. "Yes," she was saying, "at nine o'clock. And I should very much like for you to come." Blake Past shook his head. "Proms aren't for parents. You…
- anchor2_doc_order_rag score: 0.0000
  prediction: Because Blake is acting like he's her father, which is a sensitive topic for Deirdre because she lost her real parents.
  top_chunk: rank=1 score=0.6406 Lord, he must have been feeling old to have pictured himself like that! Deirdre was speaking. "Yes," she was saying, "at nine o'clock. And I should very much like for you to come." Blake Past shook his head. "Proms aren't for parents. You…

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
  prediction: B
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

#### quality / 63401_ZCP5ZDGL_4

- query: What was Ann intending to do with Johnathan under the trees before the other women showed up? (A) Sleep with him. (B) Convince him to help her cook dinner. (C) Ask him to be her boyfriend. (D) Talk to him about how he became a pilot.
- references: Sleep with him.
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.4963 He started to rise. Ann Clotilde placed the flat of her hand on his chest and shoved. " Ooof! " he grunted. He sat down rather more forcibly than he had risen. "Don't get up because of me," she informed him. "It's my turn to cook, but I sa…
- reorder_only_rag score: 0.0000
  prediction: She said in an angry voice: "He's mine. I found him. Leave him alone."
  top_chunk: rank=1 score=0.4963 He started to rise. Ann Clotilde placed the flat of her hand on his chest and shoved. " Ooof! " he grunted. He sat down rather more forcibly than he had risen. "Don't get up because of me," she informed him. "It's my turn to cook, but I sa…
- reverse_order_rag score: 0.0000
  prediction: Talk to him about how he became a pilot.
  top_chunk: rank=1 score=0.4963 He started to rise. Ann Clotilde placed the flat of her hand on his chest and shoved. " Ooof! " he grunted. He sat down rather more forcibly than he had risen. "Don't get up because of me," she informed him. "It's my turn to cook, but I sa…
- random_order_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.4963 He started to rise. Ann Clotilde placed the flat of her hand on his chest and shoved. " Ooof! " he grunted. He sat down rather more forcibly than he had risen. "Don't get up because of me," she informed him. "It's my turn to cook, but I sa…
- anchor1_doc_order_rag score: 0.0000
  prediction: Don't get up because of me, Dinner can wait. Jonathan do you know that you are irresistible?
  top_chunk: rank=1 score=0.4963 He started to rise. Ann Clotilde placed the flat of her hand on his chest and shoved. " Ooof! " he grunted. He sat down rather more forcibly than he had risen. "Don't get up because of me," she informed him. "It's my turn to cook, but I sa…
- anchor2_doc_order_rag score: 0.0000
  prediction: Don't get up because of me, Dinner can wait. Jonathan do you know that you are irresistible?
  top_chunk: rank=1 score=0.4963 He started to rise. Ann Clotilde placed the flat of her hand on his chest and shoved. " Ooof! " he grunted. He sat down rather more forcibly than he had risen. "Don't get up because of me," she informed him. "It's my turn to cook, but I sa…

### contract_nli

- examples: 50
- disagreements: 18
- any-positive-score: 37

#### contract_nli / 7_nda-2

- query: Confidential Information shall only include technical information.
- references: Entailment
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.5743 Confidential Information does not include information: (i) which is or becomes public knowledge and public property in any way without breach of this Agreement by the Recipient; (ii) which the Recipient can show has been known or has been…
- reorder_only_rag score: 0.0000
  prediction: Not mentioned
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
