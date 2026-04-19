# Comparison Report

Run tier: `subset`

## Score Summary

| Task | Metric | vanilla_rag | reorder_only_rag | reverse_order_rag | random_order_rag | anchor1_doc_order_rag | anchor2_doc_order_rag | reorder_only_rag_minus_vanilla_rag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| qmsum | rouge | 16.9832 | 17.4723 | 16.9875 | 17.6387 | 17.1003 | 16.7975 | +0.4891 |
| qasper | f1 | 38.0341 | 39.1336 | 33.8247 | 36.4718 | 36.8734 | 34.9787 | +1.0995 |
| narrative_qa | f1 | 12.8197 | 10.3269 | 15.5806 | 12.5528 | 14.5706 | 15.8238 | -2.4928 |
| quality | exact_match | 44.0000 | 52.0000 | 48.0000 | 50.0000 | 48.0000 | 44.0000 | +8.0000 |
| contract_nli | exact_match | 66.0000 | 58.0000 | 56.0000 | 56.0000 | 66.0000 | 68.0000 | -8.0000 |

## Runtime Summary

| Method | Total seconds | Total minutes | Seconds / example | Examples / second |
| --- | --- | --- | --- | --- |
| vanilla_rag | 418.49 | 6.97 | 1.6740 | 0.5974 |
| reorder_only_rag | 443.29 | 7.39 | 1.7732 | 0.5640 |
| reverse_order_rag | 418.64 | 6.98 | 1.6746 | 0.5972 |
| random_order_rag | 420.23 | 7.00 | 1.6809 | 0.5949 |
| anchor1_doc_order_rag | 424.97 | 7.08 | 1.6999 | 0.5883 |
| anchor2_doc_order_rag | 416.96 | 6.95 | 1.6678 | 0.5996 |

## Example Previews

### qmsum

- examples: 50
- disagreements: 50
- any-positive-score: 50

#### qmsum / va-gq-5

- query: What were the main discussion points of the meeting?
- references: The group discussed topics including a potential collaboration with another ICSI member regarding the analysis of inference structures, efforts by speaker mn005 to detect speaker overlap, the current status of recordings and transcriptions, and future efforts to collect meeting data. In addition to weekly meetings by the BMR group, efforts are in progress to record meetings by other ICSI research…
- best_methods: random_order_rag
- disagreement: True
- vanilla_rag score: 7.6235
  prediction: The main discussion points of the meeting included the recording of meetings, particularly those of the network services and applications group, which would start the following week. There was also a discussion about data collection, specifically the number of overlaps between speakers and the potential for recording meetings with more emotional or conflicting aspects. Additionally, the group tal…
  top_chunk: rank=1 score=0.3285 Uh , we {disfmarker} I think the things that we talk about in this meeting uh tend to be a mixture of uh procedural uh mundane things and uh research points and um I was thinking I think it was a meeting a couple of weeks ago that we {disf…
- reorder_only_rag score: 0.0000
  prediction: The main discussion points of the meeting included the nature of overlaps and interruptions during meetings, the recording of meetings for research purposes, and the collection of data on meeting interactions. Participants also discussed the frequency of their meetings, the types of meetings that could be recorded (such as those with conflicts or strong opinions), and the potential for recording…
  top_chunk: rank=1 score=0.3285 Uh , we {disfmarker} I think the things that we talk about in this meeting uh tend to be a mixture of uh procedural uh mundane things and uh research points and um I was thinking I think it was a meeting a couple of weeks ago that we {disf…
- reverse_order_rag score: 7.7537
  prediction: The main discussion points of the meeting included potential data collection for recording meetings, particularly those with some kind of conflict or emotional aspects. There was also a discussion about the types of meetings that could be recorded, such as those happening at ICSI and the network services and applications group meetings that would start being recorded the following week. Additiona…
  top_chunk: rank=1 score=0.3285 Uh , we {disfmarker} I think the things that we talk about in this meeting uh tend to be a mixture of uh procedural uh mundane things and uh research points and um I was thinking I think it was a meeting a couple of weeks ago that we {disf…
- random_order_rag score: 8.0186
  prediction: The main discussion points of the meeting included the status of their disk space and the need to wrap up, the number of overlaps in speech during a specific time period, the idea of recording more meetings at ICSI, particularly those with emotional aspects or conflicts, and the exploration of using the data collected for research purposes, such as analyzing energy patterns in meetings and the us…
  top_chunk: rank=1 score=0.3285 Uh , we {disfmarker} I think the things that we talk about in this meeting uh tend to be a mixture of uh procedural uh mundane things and uh research points and um I was thinking I think it was a meeting a couple of weeks ago that we {disf…
- anchor1_doc_order_rag score: 0.0000
  prediction: The main discussion points of the meeting included the nature of overlaps and interruptions during meetings, the recording of meetings for research purposes, and the collection of data on meeting interactions. Participants also discussed the frequency of their meetings, the types of meetings that could be recorded (such as those with conflicts or strong opinions), and the potential for recording…
  top_chunk: rank=1 score=0.3285 Uh , we {disfmarker} I think the things that we talk about in this meeting uh tend to be a mixture of uh procedural uh mundane things and uh research points and um I was thinking I think it was a meeting a couple of weeks ago that we {disf…
- anchor2_doc_order_rag score: 0.0000
  prediction: The main discussion points of the meeting included the nature of overlaps and interruptions during meetings, the need for a Meeting Recorder to capture discussions accurately, the frequency and recording of meetings, and the collection of data for analysis. The participants also discussed potential projects related to energy detection in meetings and the possibility of recording meetings with mor…
  top_chunk: rank=1 score=0.3285 Uh , we {disfmarker} I think the things that we talk about in this meeting uh tend to be a mixture of uh procedural uh mundane things and uh research points and um I was thinking I think it was a meeting a couple of weeks ago that we {disf…

#### qmsum / va-sq-2

- query: What was said on speech overlap?
- references: Efforts by speaker mn005 are in progress to detect overlapping speech. For a single transcribed meeting, speaker mn005 reported approximately 300 cases of overlap. Future work will involve manually deriving time marks from sections of overlapping speech for the same meeting, and then experimenting with different measures, e.g. energy increase, to determine a set of acoustically salient features f…
- best_methods: reorder_only_rag
- disagreement: True
- vanilla_rag score: 6.9446
  prediction: The discussion centered around the challenge of manually marking speech overlaps in recordings. PhD D mentioned finding three hundred overlapping speech events in a session lasting forty-five minutes, which was described as very time-consuming. PhD D defined an "overlapping zone" as a period where three or more speakers are talking together, and an "acoustic event" as the overlapping zone or any…
  top_chunk: rank=1 score=0.4702 Eh almost eh three hundred eh in one session Grad G: Oh , God ! PhD D: in five {disfmarker} eh in forty - five minutes . PhD A: Three hundred overlapping speech {disfmarker} PhD D: Alm - Three hundred overlapping zone . Grad G: Ugh . PhD C…
- reorder_only_rag score: 8.3437
  prediction: PhD D mentioned that they found almost three hundred overlapping speech zones in one session lasting forty-five minutes. This amounts to about three hundred overlapping speech events in twelve minutes of recorded speech. PhD D considers an acoustic event to be the overlapping zone where three or more speakers are talking together, without distinguishing between the number of speakers involved. Th…
  top_chunk: rank=1 score=0.4702 Eh almost eh three hundred eh in one session Grad G: Oh , God ! PhD D: in five {disfmarker} eh in forty - five minutes . PhD A: Three hundred overlapping speech {disfmarker} PhD D: Alm - Three hundred overlapping zone . Grad G: Ugh . PhD C…
- reverse_order_rag score: 6.6553
  prediction: The discussion centered around the need to mark speaker overlaps in transcriptions, particularly in multi-channel transcriptions where people are not used to dealing with such data. PhD D mentioned that they had transcribed only twelve minutes of a session and had found three hundred speaker overlaps in that time. Professor E suggested that marking overlaps by hand is time-consuming and proposed…
  top_chunk: rank=1 score=0.4702 Eh almost eh three hundred eh in one session Grad G: Oh , God ! PhD D: in five {disfmarker} eh in forty - five minutes . PhD A: Three hundred overlapping speech {disfmarker} PhD D: Alm - Three hundred overlapping zone . Grad G: Ugh . PhD C…
- random_order_rag score: 7.5929
  prediction: The discussion centered around the identification and marking of speech overlaps in recorded sessions. PhD D mentioned finding three hundred speaker overlaps in forty-five minutes of recording, which equates to about three hundred overlaps in twelve minutes of work. The team debated whether to mark all acoustic events or just the overlaps of speech. PhD D argued for marking all overlaps as a sing…
  top_chunk: rank=1 score=0.4702 Eh almost eh three hundred eh in one session Grad G: Oh , God ! PhD D: in five {disfmarker} eh in forty - five minutes . PhD A: Three hundred overlapping speech {disfmarker} PhD D: Alm - Three hundred overlapping zone . Grad G: Ugh . PhD C…
- anchor1_doc_order_rag score: 0.0000
  prediction: The discussion centered around the identification and analysis of speech overlaps in recorded sessions. PhD D mentioned finding one thousand acoustic events in twelve minutes, with a focus on overlapping zones where three or more speakers are talking simultaneously. The team debated the definition and counting of these overlaps, with PhD D considering all instances of multiple voices speaking tog…
  top_chunk: rank=1 score=0.4702 Eh almost eh three hundred eh in one session Grad G: Oh , God ! PhD D: in five {disfmarker} eh in forty - five minutes . PhD A: Three hundred overlapping speech {disfmarker} PhD D: Alm - Three hundred overlapping zone . Grad G: Ugh . PhD C…
- anchor2_doc_order_rag score: 7.9445
  prediction: The discussion centered around the concept of speech overlap in a recorded session. PhD D mentioned finding three hundred overlapping speech zones in a session that lasted forty-five minutes, which was later clarified to be in twelve minutes. PhD D defined an overlapping zone as a period where three or more speakers are talking together, considering it as one acoustic event without any distinctio…
  top_chunk: rank=1 score=0.4702 Eh almost eh three hundred eh in one session Grad G: Oh , God ! PhD D: in five {disfmarker} eh in forty - five minutes . PhD A: Three hundred overlapping speech {disfmarker} PhD D: Alm - Three hundred overlapping zone . Grad G: Ugh . PhD C…

#### qmsum / va-sq-35

- query: Summarize the discussion about user requirements.
- references: According to a market survey, there were several things that users didn't like in current remote controls. First of all, users find them very ugly. Second, the current remote controls were not so easy to use and the facilities that they offered did not match what people really wanted. Third, people were very frustrated with their remote controls because sometimes they just couldn't find them. The…
- best_methods: random_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: The discussion centered around user requirements for a new remote control, particularly focusing on the preferences and behaviors of the target users. Marketing emphasized that young people are early adopters and more likely to be interested in a new device. The power button is used infrequently, but its presence is important for user satisfaction. Channel selection is a very important feature, w…
  top_chunk: rank=1 score=0.3915 Marketing: this is of course , depends on that . And um I don't have any conclusion , I didn't have time the meeting was very tight , so that's basically my findings . And uh , if you have any question ? Project Manager: Mm I think it's go…
- reorder_only_rag score: 5.2054
  prediction: The discussion about user requirements centered around understanding the needs of the target users for the new remote control project. Marketing presented insights based on user preferences and behaviors, highlighting that the power button is used infrequently, while channel selection and volume control are more commonly used. The team agreed that the remote control should cater to young users, w…
  top_chunk: rank=1 score=0.3915 Marketing: this is of course , depends on that . And um I don't have any conclusion , I didn't have time the meeting was very tight , so that's basically my findings . And uh , if you have any question ? Project Manager: Mm I think it's go…
- reverse_order_rag score: 7.5688
  prediction: The discussion centered around understanding user requirements for a new remote control device. Key points included: 1. **User Interface and Interference**: There was a concern about the remote control interfering with other devices, such as lights turning on with clapping. This was noted as something that already exists. 2. **Speaker Integration**: The team considered whether the remote control…
  top_chunk: rank=1 score=0.3915 Marketing: this is of course , depends on that . And um I don't have any conclusion , I didn't have time the meeting was very tight , so that's basically my findings . And uh , if you have any question ? Project Manager: Mm I think it's go…
- random_order_rag score: 9.0377
  prediction: The discussion centered around user requirements for a new remote control design, particularly focusing on the functions that users find most useful and those that are less important. Key points included: 1. **Power Button Usage**: The power button is used infrequently but is very important, as users want a clear and easy-to-find button to turn the device on or off. 2. **Channel Selection**: Chan…
  top_chunk: rank=1 score=0.3915 Marketing: this is of course , depends on that . And um I don't have any conclusion , I didn't have time the meeting was very tight , so that's basically my findings . And uh , if you have any question ? Project Manager: Mm I think it's go…
- anchor1_doc_order_rag score: 7.3738
  prediction: The discussion about user requirements centered around understanding the needs of remote control users to inform the design of a new remote control, particularly a universal remote control. Marketing presented insights based on user preferences and frustrations, highlighting that the power button is used infrequently, while channel selection and volume control are more commonly used. The team agr…
  top_chunk: rank=1 score=0.3915 Marketing: this is of course , depends on that . And um I don't have any conclusion , I didn't have time the meeting was very tight , so that's basically my findings . And uh , if you have any question ? Project Manager: Mm I think it's go…
- anchor2_doc_order_rag score: 0.0000
  prediction: The discussion about user requirements centered around understanding the needs of the target users for the new remote control design. Marketing presented insights based on user preferences and frustrations, highlighting that the power button is used infrequently, while channel selection and volume control are more frequently used. The team agreed that the design should cater to young users, who a…
  top_chunk: rank=1 score=0.3915 Marketing: this is of course , depends on that . And um I don't have any conclusion , I didn't have time the meeting was very tight , so that's basically my findings . And uh , if you have any question ? Project Manager: Mm I think it's go…

#### qmsum / va-sq-18

- query: Summarize the group's plan of their marketing strategy.
- references: For fear that the exorbitant price of 25 euros of the remote control would shock the potential consumers, Project Manager proposed to trade off some functions for a lower price. Additionally, Project Manager mentioned an American computer electronics store to show that shipping products overseas can also make profits and then added this to the whole plan.
- best_methods: reverse_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: The group plans to develop a marketing strategy that focuses on making ordinary products fashionable and appealing, aligning with the corporate strategy of enhancing everyday items to match the quality of well-known brands like John Lewis or Debenhams. They aim to tap into their collective knowledge to identify user needs and preferences, and to negotiate between what users want and what they can…
  top_chunk: rank=1 score=0.3665 if you wanna write all five go for it but name one of them that you could um . Oh , we skipped introductions . Nice . I'm a excellent Project Manager . Um . Marketing: {vocalsound} Project Manager: I'm Marty , Industrial Designer: {vocalso…
- reorder_only_rag score: 7.2262
  prediction: The group plans to develop a marketing strategy that focuses on making ordinary products fashionable and appealing, aligning with the corporate strategy of enhancing the perceived niceness of everyday items. They aim to consider user needs and preferences in their product development, and will discuss trade-offs and specific instructions in their next meeting. The team will also explore innovativ…
  top_chunk: rank=1 score=0.3665 if you wanna write all five go for it but name one of them that you could um . Oh , we skipped introductions . Nice . I'm a excellent Project Manager . Um . Marketing: {vocalsound} Project Manager: I'm Marty , Industrial Designer: {vocalso…
- reverse_order_rag score: 9.4678
  prediction: The group plans to develop a marketing strategy that aims to make ordinary products fashionable and appealing, similar to the approach of high-end retailers like John Lewis, Debenhams, and others. They intend to discuss user needs and preferences in their next meeting to better understand what customers want and can afford. The team will consider creating a product that is affordable, such as a r…
  top_chunk: rank=1 score=0.3665 if you wanna write all five go for it but name one of them that you could um . Oh , we skipped introductions . Nice . I'm a excellent Project Manager . Um . Marketing: {vocalsound} Project Manager: I'm Marty , Industrial Designer: {vocalso…
- random_order_rag score: 0.0000
  prediction: The group plans to develop a marketing strategy that focuses on making ordinary products fashionable and appealing, aligning with the corporate strategy of enhancing everyday items to match the quality of well-known brands like John Lewis or Debenhams. They aim to consider user preferences and capabilities, and will discuss these aspects in their next meeting to negotiate trade-offs. The strategy…
  top_chunk: rank=1 score=0.3665 if you wanna write all five go for it but name one of them that you could um . Oh , we skipped introductions . Nice . I'm a excellent Project Manager . Um . Marketing: {vocalsound} Project Manager: I'm Marty , Industrial Designer: {vocalso…
- anchor1_doc_order_rag score: 6.9272
  prediction: The group plans to develop a marketing strategy that transforms ordinary, unremarkable products into fashionable items, aiming to make them appealing like those found in high-end stores such as John Lewis or Debenhams. They will focus on user needs and negotiate between what users want and what is feasible. The team will discuss trade-offs and specific instructions will be sent via email. They al…
  top_chunk: rank=1 score=0.3665 if you wanna write all five go for it but name one of them that you could um . Oh , we skipped introductions . Nice . I'm a excellent Project Manager . Um . Marketing: {vocalsound} Project Manager: I'm Marty , Industrial Designer: {vocalso…
- anchor2_doc_order_rag score: 0.0000
  prediction: The group plans to develop a marketing strategy that focuses on making ordinary, unremarkable products fashionable and appealing, aiming to compete with high-end retailers like John Lewis, Debenhams, and others. They intend to base their strategy on user needs and preferences, discussing and negotiating what users want and can afford. The team will document their initial ideas and trade-offs in p…
  top_chunk: rank=1 score=0.3665 if you wanna write all five go for it but name one of them that you could um . Oh , we skipped introductions . Nice . I'm a excellent Project Manager . Um . Marketing: {vocalsound} Project Manager: I'm Marty , Industrial Designer: {vocalso…

#### qmsum / va-sq-1

- query: What was agreed upon on sample transcripts?
- references: To save time, speaker mn005 will only mark the sample of transcribed data for regions of overlapping speech, as opposed to marking all acoustic events. The digits extraction task will be delegated to whomever is working on acoustics for the Meeting Recorder project.
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 10.1809
  prediction: Based on the provided context, it was agreed that a sample of transcripts would be used as a comparison point. Specifically, Professor E mentioned that "There's this forty-five minute piece that Jane transcribed. That piece was then uh sent to IBM so they could transcribe so we have some comparison point." This indicates that the sample transcript was sent to IBM for an independent transcription…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- reorder_only_rag score: 7.2582
  prediction: Based on the provided context, it appears that a sample transcript was manually marked to serve as a ground truth. Specifically, Professor E mentioned that a piece of the transcript, forty-five minutes in length, was transcribed and then sent to IBM for comparison. Additionally, there is a larger piece that has been recorded and put on CD-ROM and sent to IBM for transcription. Professor E also no…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- reverse_order_rag score: 0.0000
  prediction: Based on the provided context, it was agreed that a sample transcript would be sent to IBM for transcription as a comparison point. Specifically, Professor E mentioned, "That piece was then uh sent to IBM so they could transcribe so we have some comparison point." This indicates that a segment of the recorded meeting was sent to IBM for an external transcription to serve as a reference for qualit…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- random_order_rag score: 9.4689
  prediction: Based on the provided context, it was agreed that a sample of the transcripts would be sent to IBM for transcription as a comparison point. Specifically, a forty-five-minute piece that Jane transcribed was sent to IBM, and a larger piece that was recorded and put on CD-ROM was also sent to IBM for transcription.
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- anchor1_doc_order_rag score: 7.5691
  prediction: Based on the provided context, it appears that a sample transcript was manually marked to serve as a ground truth. Professor E mentioned, "The idea of the manual marking was to say 'OK this, i you know, it's really here.'" This manual marking was done to identify certain phenomena in the transcripts, and a piece of the transcript was sent to IBM for transcription to have a comparison point. Addit…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- anchor2_doc_order_rag score: 0.0000
  prediction: Based on the provided context, it appears that a sample transcript was manually marked to serve as a ground truth. Professor E mentioned, "The idea of the manual marking was to say 'OK this, i you know, it's really here.'" This manual marking was done to identify certain phenomena in the transcripts for research purposes. Additionally, a forty-five-minute piece was transcribed and sent to IBM for…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…

### qasper

- examples: 50
- disagreements: 45
- any-positive-score: 47

#### qasper / 71e4ba4e87e6596aeca187127c0d088df6570c57

- query: What evaluations methods do they take?
- references: Unanswerable | Unanswerable
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Another method is to tag all descriptions with part-of-speech information, so that it becomes possible to see e.g. which adjectives are most commonly used for particular nouns.
  top_chunk: rank=1 score=0.2777 A next step would be to see whether these observations also hold for other age groups, i.e. children and adults. INLINEFORM0 Other methods It may be difficult to spot patterns by just looking at a collection of images. Another method is to…
- reorder_only_rag score: 0.0000
  prediction: They take several evaluations methods including: - Manually inspecting a subset of the Flickr30K data to group inferences into categories - Counting the proportion of descriptions that contain markers for ethnicity - Tagging all descriptions with part-of-speech information - Applying Louvain clustering to the coreference graph to analyze referring expressions
  top_chunk: rank=1 score=0.2777 A next step would be to see whether these observations also hold for other age groups, i.e. children and adults. INLINEFORM0 Other methods It may be difficult to spot patterns by just looking at a collection of images. Another method is to…
- reverse_order_rag score: 0.0000
  prediction: The authors applied Louvain clustering BIBREF9 to the coreference graph, resulting in clusters of expressions that refer to similar entities. They also looked at methods to manually detect stereotypes, biases, and odd phrases, and applied part-of-speech tagging to descriptions. Additionally, they inspected a subset of the Flickr30K data to group inferences into six categories and used counting me…
  top_chunk: rank=1 score=0.2777 A next step would be to see whether these observations also hold for other age groups, i.e. children and adults. INLINEFORM0 Other methods It may be difficult to spot patterns by just looking at a collection of images. Another method is to…
- random_order_rag score: 0.0000
  prediction: Another method is to tag all descriptions with part-of-speech information, so that it becomes possible to see e.g. which adjectives are most commonly used for particular nouns.
  top_chunk: rank=1 score=0.2777 A next step would be to see whether these observations also hold for other age groups, i.e. children and adults. INLINEFORM0 Other methods It may be difficult to spot patterns by just looking at a collection of images. Another method is to…
- anchor1_doc_order_rag score: 0.0000
  prediction: Following this, I applied Louvain clustering BIBREF9 to the coreference graph, resulting in clusters of expressions that refer to similar entities.
  top_chunk: rank=1 score=0.2777 A next step would be to see whether these observations also hold for other age groups, i.e. children and adults. INLINEFORM0 Other methods It may be difficult to spot patterns by just looking at a collection of images. Another method is to…
- anchor2_doc_order_rag score: 0.0000
  prediction: After inspecting a subset of the Flickr30K data, I have grouped these inferences into six categories (image examples between parentheses):
  top_chunk: rank=1 score=0.2777 A next step would be to see whether these observations also hold for other age groups, i.e. children and adults. INLINEFORM0 Other methods It may be difficult to spot patterns by just looking at a collection of images. Another method is to…

#### qasper / fb2b536dc8e442dffab408db992b971e86548158

- query: What is the interannotator agreement for the human evaluation?
- references: Unanswerable | Unanswerable
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: The context does not provide the interannotator agreement for the human evaluation.
  top_chunk: rank=1 score=0.3259 The opinons expressed are those of the authors and do not represent the views of the institute or the U.S. Department of Education
- reorder_only_rag score: 0.0000
  prediction: Not provided
  top_chunk: rank=1 score=0.3259 The opinons expressed are those of the authors and do not represent the views of the institute or the U.S. Department of Education
- reverse_order_rag score: 0.0000
  prediction: Not provided
  top_chunk: rank=1 score=0.3259 The opinons expressed are those of the authors and do not represent the views of the institute or the U.S. Department of Education
- random_order_rag score: 0.0000
  prediction: Not provided in the context.
  top_chunk: rank=1 score=0.3259 The opinons expressed are those of the authors and do not represent the views of the institute or the U.S. Department of Education
- anchor1_doc_order_rag score: 0.0000
  prediction: Not provided
  top_chunk: rank=1 score=0.3259 The opinons expressed are those of the authors and do not represent the views of the institute or the U.S. Department of Education
- anchor2_doc_order_rag score: 0.0000
  prediction: Not provided
  top_chunk: rank=1 score=0.3259 The opinons expressed are those of the authors and do not represent the views of the institute or the U.S. Department of Education

#### qasper / c0bee6539eb6956a7347daa9d2419b367bd02064

- query: Does BERT reach the best performance among all the algorithms compared?
- references: No | No
- best_methods: vanilla_rag
- disagreement: True
- vanilla_rag score: 3.5088
  prediction: No, BERT does not reach the best performance among all the algorithms compared. It is noted that BERT is very competitive and often outperforms other systems, but in some cases, it is not the absolute best. For example, in the MEDDOCAN shared task, BERT is only 0.3 F1-score points behind the shared task winning system and would have achieved the second position.
  top_chunk: rank=1 score=0.5670 A fact worth highlighting is that, according to these results, BERT achieves a precision lower than the rest of the systems (i.e., it makes more false positive predictions); in exchange, it obtains a remarkably higher recall. Noticeably, i…
- reorder_only_rag score: 0.0000
  prediction: BERT outperforms its competitors in terms of recall and F1-score, but is not always the most precise.
  top_chunk: rank=1 score=0.5670 A fact worth highlighting is that, according to these results, BERT achieves a precision lower than the rest of the systems (i.e., it makes more false positive predictions); in exchange, it obtains a remarkably higher recall. Noticeably, i…
- reverse_order_rag score: 0.0000
  prediction: BERT remains only 0.3 F1-score points behind, and would have achieved the second position among all the MEDDOCAN shared task competitors.
  top_chunk: rank=1 score=0.5670 A fact worth highlighting is that, according to these results, BERT achieves a precision lower than the rest of the systems (i.e., it makes more false positive predictions); in exchange, it obtains a remarkably higher recall. Noticeably, i…
- random_order_rag score: 0.0000
  prediction: BERT outperforms them again.
  top_chunk: rank=1 score=0.5670 A fact worth highlighting is that, according to these results, BERT achieves a precision lower than the rest of the systems (i.e., it makes more false positive predictions); in exchange, it obtains a remarkably higher recall. Noticeably, i…
- anchor1_doc_order_rag score: 0.0000
  prediction: BERT outperforms its competitors in terms of recall and F1-score.
  top_chunk: rank=1 score=0.5670 A fact worth highlighting is that, according to these results, BERT achieves a precision lower than the rest of the systems (i.e., it makes more false positive predictions); in exchange, it obtains a remarkably higher recall. Noticeably, i…
- anchor2_doc_order_rag score: 0.0000
  prediction: BERT outperforms its competitors in terms of recall and F1-score.
  top_chunk: rank=1 score=0.5670 A fact worth highlighting is that, according to these results, BERT achieves a precision lower than the rest of the systems (i.e., it makes more false positive predictions); in exchange, it obtains a remarkably higher recall. Noticeably, i…

#### qasper / ef4dba073d24042f24886580ae77add5326f2130

- query: What accuracy does the proposed system achieve?
- references: F1 scores of 85.99 on the DL-PS data, 75.15 on the EC-MT data and 71.53 on the EC-UQ data | F1 of 85.99 on the DL-PS dataset (dialog domain); 75.15 on EC-MT and 71.53 on EC-UQ (e-commerce domain)
- best_methods: reverse_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: The context does not provide the specific accuracy achieved by the proposed system.
  top_chunk: rank=1 score=0.3082 It is one biggest challenge to build a powerful NER system on such a low quality annotated data. Although we can obtain high quality annotations for each input sentence by majority voting, it can be a waste of human labors to achieve such…
- reorder_only_rag score: 0.0000
  prediction: The context does not provide the specific accuracy achieved by the proposed system.
  top_chunk: rank=1 score=0.3082 It is one biggest challenge to build a powerful NER system on such a low quality annotated data. Although we can obtain high quality annotations for each input sentence by majority voting, it can be a waste of human labors to achieve such…
- reverse_order_rag score: 14.2857
  prediction: The context does not provide specific accuracy or F1 scores for the proposed system.
  top_chunk: rank=1 score=0.3082 It is one biggest challenge to build a powerful NER system on such a low quality annotated data. Although we can obtain high quality annotations for each input sentence by majority voting, it can be a waste of human labors to achieve such…
- random_order_rag score: 0.0000
  prediction: The context does not provide the specific accuracy achieved by the proposed system.
  top_chunk: rank=1 score=0.3082 It is one biggest challenge to build a powerful NER system on such a low quality annotated data. Although we can obtain high quality annotations for each input sentence by majority voting, it can be a waste of human labors to achieve such…
- anchor1_doc_order_rag score: 0.0000
  prediction: The context does not provide specific accuracy figures for the proposed system.
  top_chunk: rank=1 score=0.3082 It is one biggest challenge to build a powerful NER system on such a low quality annotated data. Although we can obtain high quality annotations for each input sentence by majority voting, it can be a waste of human labors to achieve such…
- anchor2_doc_order_rag score: 0.0000
  prediction: The context does not provide the specific accuracy achieved by the proposed system.
  top_chunk: rank=1 score=0.3082 It is one biggest challenge to build a powerful NER system on such a low quality annotated data. Although we can obtain high quality annotations for each input sentence by majority voting, it can be a waste of human labors to achieve such…

#### qasper / d3aa0449708cc861a51551b128d73e11d62207d2

- query: What they use in their propsoed framework?
- references: break the relation names into word sequences, relation-level and word-level relation representations, bidirectional LSTMs (BiLSTMs), residual learning method | break the relation names into word sequences for question-relation matching, build both relation-level and word-level relation representations, use deep bidirectional LSTMs (BiLSTMs) to learn different levels of question representations, r…
- best_methods: reorder_only_rag, reverse_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: BiLSTM
  top_chunk: rank=1 score=0.3045 {episode_written} or {starring_roles, series} (when the target is a chain like in Figure 1 (b)).
- reorder_only_rag score: 17.3913
  prediction: Hierarchical Matching between Relation and Question
  top_chunk: rank=1 score=0.3045 {episode_written} or {starring_roles, series} (when the target is a chain like in Figure 1 (b)).
- reverse_order_rag score: 17.3913
  prediction: Hierarchical Matching between Relation and Question
  top_chunk: rank=1 score=0.3045 {episode_written} or {starring_roles, series} (when the target is a chain like in Figure 1 (b)).
- random_order_rag score: 15.1899
  prediction: We transform each token above to its word embedding then use two BiLSTMs (with shared parameters) to get their hidden representations $[\mathbf {B}^{word}_{1:M_1}:\mathbf {B}^{rel}_{1:M_2}]$ (each row vector $\mathbf {\beta }_i$ is the concatenation between forward/backward representations at $i$ ).
  top_chunk: rank=1 score=0.3045 {episode_written} or {starring_roles, series} (when the target is a chain like in Figure 1 (b)).
- anchor1_doc_order_rag score: 17.3913
  prediction: Hierarchical Matching between Relation and Question
  top_chunk: rank=1 score=0.3045 {episode_written} or {starring_roles, series} (when the target is a chain like in Figure 1 (b)).
- anchor2_doc_order_rag score: 17.3913
  prediction: Hierarchical Matching between Relation and Question
  top_chunk: rank=1 score=0.3045 {episode_written} or {starring_roles, series} (when the target is a chain like in Figure 1 (b)).

### narrative_qa

- examples: 50
- disagreements: 46
- any-positive-score: 26

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_1

- query: Where is the boarding-house located?
- references: Paris
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: in the Faubourg St. Germain
  top_chunk: rank=1 score=0.3975 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…
- reorder_only_rag score: 0.0000
  prediction: in the Faubourg St. Germain
  top_chunk: rank=1 score=0.3975 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…
- reverse_order_rag score: 0.0000
  prediction: Faubourg St. Germain
  top_chunk: rank=1 score=0.3975 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…
- random_order_rag score: 0.0000
  prediction: Faubourg St. Germain
  top_chunk: rank=1 score=0.3975 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…
- anchor1_doc_order_rag score: 0.0000
  prediction: in the Faubourg St. Germain
  top_chunk: rank=1 score=0.3975 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…
- anchor2_doc_order_rag score: 0.0000
  prediction: in the Faubourg St. Germain
  top_chunk: rank=1 score=0.3975 At last they made arrangements, and I was transported to the establishment from which I now write you. I write you from the bosom of a Parisian menage--from the depths of a second-rate boarding-house. Father only left Paris after he had se…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_11

- query: Where is Violet Ray from?
- references: New York
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Paris
  top_chunk: rank=1 score=0.4222 FROM MISS VIOLET RAY, IN PARIS, TO MISS AGNES RICH, IN NEW YORK. September 21st. We had hardly got here when father received a telegram saying he would have to come right back to New York. It was for something about his business--I don't k…
- reorder_only_rag score: 0.0000
  prediction: Paris
  top_chunk: rank=1 score=0.4222 FROM MISS VIOLET RAY, IN PARIS, TO MISS AGNES RICH, IN NEW YORK. September 21st. We had hardly got here when father received a telegram saying he would have to come right back to New York. It was for something about his business--I don't k…
- reverse_order_rag score: 0.0000
  prediction: Paris
  top_chunk: rank=1 score=0.4222 FROM MISS VIOLET RAY, IN PARIS, TO MISS AGNES RICH, IN NEW YORK. September 21st. We had hardly got here when father received a telegram saying he would have to come right back to New York. It was for something about his business--I don't k…
- random_order_rag score: 0.0000
  prediction: Paris
  top_chunk: rank=1 score=0.4222 FROM MISS VIOLET RAY, IN PARIS, TO MISS AGNES RICH, IN NEW YORK. September 21st. We had hardly got here when father received a telegram saying he would have to come right back to New York. It was for something about his business--I don't k…
- anchor1_doc_order_rag score: 0.0000
  prediction: Bangor
  top_chunk: rank=1 score=0.4222 FROM MISS VIOLET RAY, IN PARIS, TO MISS AGNES RICH, IN NEW YORK. September 21st. We had hardly got here when father received a telegram saying he would have to come right back to New York. It was for something about his business--I don't k…
- anchor2_doc_order_rag score: 0.0000
  prediction: Paris
  top_chunk: rank=1 score=0.4222 FROM MISS VIOLET RAY, IN PARIS, TO MISS AGNES RICH, IN NEW YORK. September 21st. We had hardly got here when father received a telegram saying he would have to come right back to New York. It was for something about his business--I don't k…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_17

- query: What name does Herr Professor call Leon?
- references: Simian
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: insatiable little Leon
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…
- reorder_only_rag score: 0.0000
  prediction: _dis donc, mon gras Prosper_
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…
- reverse_order_rag score: 0.0000
  prediction: insatiable little Leon
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…
- random_order_rag score: 0.0000
  prediction: "insatiable little Leon"
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…
- anchor1_doc_order_rag score: 0.0000
  prediction: _dis donc, mon gras Prosper_
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…
- anchor2_doc_order_rag score: 0.0000
  prediction: "my good Prosper"
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_18

- query: Which traveler finds the other travelers "sub-human"?
- references: Herr Professor
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: He appears to me less human than simian, and whenever I hear him talk I seem to myself to have paused in the street to listen to the shrill clatter of a hand-organ, to which the gambols of a hairy _homunculus_ form an accompaniment.
  top_chunk: rank=1 score=0.3351 But this New England maiden is, in her way, a strange type: she is travelling all over Europe alone--"to see it," she says, "for herself." For herself! What can that stiff slim self of hers do with such sights, such visions!
- reorder_only_rag score: 0.0000
  prediction: This, I confess, has been something of a surprise to me, and I have not yet made up my mind as to the fundamental cause of the anomaly.
  top_chunk: rank=1 score=0.3351 But this New England maiden is, in her way, a strange type: she is travelling all over Europe alone--"to see it," she says, "for herself." For herself! What can that stiff slim self of hers do with such sights, such visions!
- reverse_order_rag score: 0.0000
  prediction: He appears to me less human than simian, and whenever I hear him talk I seem to myself to have paused in the street to listen to the shrill clatter of a hand-organ, to which the gambols of a hairy _homunculus_ form an accompaniment.
  top_chunk: rank=1 score=0.3351 But this New England maiden is, in her way, a strange type: she is travelling all over Europe alone--"to see it," she says, "for herself." For herself! What can that stiff slim self of hers do with such sights, such visions!
- random_order_rag score: 0.0000
  prediction: He appears to me less human than simian, and whenever I hear him talk I seem to myself to have paused in the street to listen to the shrill clatter of a hand-organ, to which the gambols of a hairy _homunculus_ form an accompaniment.
  top_chunk: rank=1 score=0.3351 But this New England maiden is, in her way, a strange type: she is travelling all over Europe alone--"to see it," she says, "for herself." For herself! What can that stiff slim self of hers do with such sights, such visions!
- anchor1_doc_order_rag score: 0.0000
  prediction: This, I confess, has been something of a surprise to me, and I have not yet made up my mind as to the fundamental cause of the anomaly. My determination to take up my abode in a French interior was largely dictated by the supposition that I should be substantially disagreeable to its inmates.
  top_chunk: rank=1 score=0.3351 But this New England maiden is, in her way, a strange type: she is travelling all over Europe alone--"to see it," she says, "for herself." For herself! What can that stiff slim self of hers do with such sights, such visions!
- anchor2_doc_order_rag score: 0.0000
  prediction: This, I confess, has been something of a surprise to me, and I have not yet made up my mind as to the fundamental cause of the anomaly.
  top_chunk: rank=1 score=0.3351 But this New England maiden is, in her way, a strange type: she is travelling all over Europe alone--"to see it," she says, "for herself." For herself! What can that stiff slim self of hers do with such sights, such visions!

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_19

- query: What does Evelyn Vane claim Leverett is always talking about?
- references: The color of the sky
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: its being "a real Corot day," etc.
  top_chunk: rank=1 score=0.3699 You know I told you, in writing some time ago, that I had tried to get some insight into the position of woman in England, and, being here with Miss Vane, it has seemed to me to be a good opportunity to get a little more. I have asked her…
- reorder_only_rag score: 0.0000
  prediction: "a real Corot day" etc.
  top_chunk: rank=1 score=0.3699 You know I told you, in writing some time ago, that I had tried to get some insight into the position of woman in England, and, being here with Miss Vane, it has seemed to me to be a good opportunity to get a little more. I have asked her…
- reverse_order_rag score: 0.0000
  prediction: "a real Corot day," etc.
  top_chunk: rank=1 score=0.3699 You know I told you, in writing some time ago, that I had tried to get some insight into the position of woman in England, and, being here with Miss Vane, it has seemed to me to be a good opportunity to get a little more. I have asked her…
- random_order_rag score: 0.0000
  prediction: "a real Corot day," etc.
  top_chunk: rank=1 score=0.3699 You know I told you, in writing some time ago, that I had tried to get some insight into the position of woman in England, and, being here with Miss Vane, it has seemed to me to be a good opportunity to get a little more. I have asked her…
- anchor1_doc_order_rag score: 0.0000
  prediction: he talks about its being "a real Corot day," etc.
  top_chunk: rank=1 score=0.3699 You know I told you, in writing some time ago, that I had tried to get some insight into the position of woman in England, and, being here with Miss Vane, it has seemed to me to be a good opportunity to get a little more. I have asked her…
- anchor2_doc_order_rag score: 0.0000
  prediction: he talks about its being "a real Corot day," etc.
  top_chunk: rank=1 score=0.3699 You know I told you, in writing some time ago, that I had tried to get some insight into the position of woman in England, and, being here with Miss Vane, it has seemed to me to be a good opportunity to get a little more. I have asked her…

### quality

- examples: 50
- disagreements: 26
- any-positive-score: 31

#### quality / 30029_F5N22U40_4

- query: What is the most likely reason for Korvin's solitude in jail? (A) Solitary confinement was part of Korvin's punishment. (B) There weren't any other prisoners in the jail because virtually all of the Tr'en obey the Ruler. Those who don't obey are executed. (C) The Tr'en didn't want Korvin to interact with the other Tr'en prisoners because there was a chance that together they might incite an upris…
- references: There weren't any other prisoners in the jail because virtually all of the Tr'en obey the Ruler. Those who don't obey are executed.
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.5857 The Wonders of Tr'en, according to all the advance reports, were likely to be pretty boring, but they'd have been better than nothing. In any decently-run jail, he told himself with indignation, there would at least have been other prisone…
- reorder_only_rag score: 0.0000
  prediction: The Tr'en are so logical and mathematic that they don't see the need for social interaction
  top_chunk: rank=1 score=0.5857 The Wonders of Tr'en, according to all the advance reports, were likely to be pretty boring, but they'd have been better than nothing. In any decently-run jail, he told himself with indignation, there would at least have been other prisone…
- reverse_order_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.5857 The Wonders of Tr'en, according to all the advance reports, were likely to be pretty boring, but they'd have been better than nothing. In any decently-run jail, he told himself with indignation, there would at least have been other prisone…
- random_order_rag score: 0.0000
  prediction: The Tr'en are so logical and mathematic that they don't see the need for social interaction.
  top_chunk: rank=1 score=0.5857 The Wonders of Tr'en, according to all the advance reports, were likely to be pretty boring, but they'd have been better than nothing. In any decently-run jail, he told himself with indignation, there would at least have been other prisone…
- anchor1_doc_order_rag score: 0.0000
  prediction: B
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
  prediction: Both A and C are correct.
  top_chunk: rank=1 score=0.5556 If you didn't, you never had a second chance to try. But Korvin meant exactly what he'd said. He was going to obey the commands of the Ruler of the Tr'en—and remove the Tr'en threat from the rest of the galaxy forever. That, after all, was…
- reorder_only_rag score: 0.0000
  prediction: Both A and C are correct.
  top_chunk: rank=1 score=0.5556 If you didn't, you never had a second chance to try. But Korvin meant exactly what he'd said. He was going to obey the commands of the Ruler of the Tr'en—and remove the Tr'en threat from the rest of the galaxy forever. That, after all, was…
- reverse_order_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.5556 If you didn't, you never had a second chance to try. But Korvin meant exactly what he'd said. He was going to obey the commands of the Ruler of the Tr'en—and remove the Tr'en threat from the rest of the galaxy forever. That, after all, was…
- random_order_rag score: 0.0000
  prediction: Both A and C are correct.
  top_chunk: rank=1 score=0.5556 If you didn't, you never had a second chance to try. But Korvin meant exactly what he'd said. He was going to obey the commands of the Ruler of the Tr'en—and remove the Tr'en threat from the rest of the galaxy forever. That, after all, was…
- anchor1_doc_order_rag score: 0.0000
  prediction: Both A and C are correct.
  top_chunk: rank=1 score=0.5556 If you didn't, you never had a second chance to try. But Korvin meant exactly what he'd said. He was going to obey the commands of the Ruler of the Tr'en—and remove the Tr'en threat from the rest of the galaxy forever. That, after all, was…
- anchor2_doc_order_rag score: 0.0000
  prediction: Both A and C are correct.
  top_chunk: rank=1 score=0.5556 If you didn't, you never had a second chance to try. But Korvin meant exactly what he'd said. He was going to obey the commands of the Ruler of the Tr'en—and remove the Tr'en threat from the rest of the galaxy forever. That, after all, was…

#### quality / 62139_J05FWZR6_7

- query: Why was the new cook so upset that the Skipper decided to surrender? (A) He realized that if they surrendered they would be sent to concentration camps and he would no longer be able to continue cooking. (B) He realized that Skipper was more devoted to his own survival than to the Federation. (C) He spent his whole life in the Belt and he wanted to experience his first space fight. (D) He realize…
- references: He realized by surrendering, the Alliance could use their ship to sneak into Federation territory unnoticed.
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: He realized that if they surrendered they would be sent to concentration camps and he would no longer be able to continue cooking.
  top_chunk: rank=1 score=0.4695 I stepped forward hastily. I said, "Excuse me, sir, shall I handle this?" Then, because the skipper was still struggling for words: "You," I said to the little fellow, "are a cook?" "One of the best!" he claimed complacently. "You're willi…
- reorder_only_rag score: 0.0000
  prediction: He realized that if they surrendered they would be sent to concentration camps and he would no longer be able to continue cooking.
  top_chunk: rank=1 score=0.4695 I stepped forward hastily. I said, "Excuse me, sir, shall I handle this?" Then, because the skipper was still struggling for words: "You," I said to the little fellow, "are a cook?" "One of the best!" he claimed complacently. "You're willi…
- reverse_order_rag score: 0.0000
  prediction: A
  top_chunk: rank=1 score=0.4695 I stepped forward hastily. I said, "Excuse me, sir, shall I handle this?" Then, because the skipper was still struggling for words: "You," I said to the little fellow, "are a cook?" "One of the best!" he claimed complacently. "You're willi…
- random_order_rag score: 0.0000
  prediction: He realized that if they surrendered they would be sent to concentration camps and he would no longer be able to continue cooking.
  top_chunk: rank=1 score=0.4695 I stepped forward hastily. I said, "Excuse me, sir, shall I handle this?" Then, because the skipper was still struggling for words: "You," I said to the little fellow, "are a cook?" "One of the best!" he claimed complacently. "You're willi…
- anchor1_doc_order_rag score: 0.0000
  prediction: He realized that if they surrendered they would be sent to concentration camps and he would no longer be able to continue cooking.
  top_chunk: rank=1 score=0.4695 I stepped forward hastily. I said, "Excuse me, sir, shall I handle this?" Then, because the skipper was still struggling for words: "You," I said to the little fellow, "are a cook?" "One of the best!" he claimed complacently. "You're willi…
- anchor2_doc_order_rag score: 0.0000
  prediction: He realized that if they surrendered they would be sent to concentration camps and he would no longer be able to continue cooking.
  top_chunk: rank=1 score=0.4695 I stepped forward hastily. I said, "Excuse me, sir, shall I handle this?" Then, because the skipper was still struggling for words: "You," I said to the little fellow, "are a cook?" "One of the best!" he claimed complacently. "You're willi…

#### quality / 62139_J05FWZR6_9

- query: What would've happened if the new cook had told the Skipper about the ekalastron deposits earlier? (A) The text doesn't indicate how the Skipper would've acted in a different scenario. (B) The Skipper still would've ignored the new cook's advice. (C) The Skipper would have mulled over the information for a few days before deciding to switch their course from Vesta to Iris. (D) The Skipper's would…
- references: The Skipper's would have set course for Iris from the beginning.
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: The text doesn't indicate how the Skipper would've acted in a different scenario.
  top_chunk: rank=1 score=0.5666 Why should there be?" "Well, for one thing," wrangled our pint-sized cook, "because rich ekalastron deposits were recently discovered on Vesta. For another, because Vesta's orbit is now going into aphelion stage, which will favor a concent…
- reorder_only_rag score: 0.0000
  prediction: The Skipper still would've ignored the new cook's advice.
  top_chunk: rank=1 score=0.5666 Why should there be?" "Well, for one thing," wrangled our pint-sized cook, "because rich ekalastron deposits were recently discovered on Vesta. For another, because Vesta's orbit is now going into aphelion stage, which will favor a concent…
- reverse_order_rag score: 0.0000
  prediction: The text doesn't indicate how the Skipper would've acted in a different scenario.
  top_chunk: rank=1 score=0.5666 Why should there be?" "Well, for one thing," wrangled our pint-sized cook, "because rich ekalastron deposits were recently discovered on Vesta. For another, because Vesta's orbit is now going into aphelion stage, which will favor a concent…
- random_order_rag score: 0.0000
  prediction: The text doesn't indicate how the Skipper would've acted in a different scenario.
  top_chunk: rank=1 score=0.5666 Why should there be?" "Well, for one thing," wrangled our pint-sized cook, "because rich ekalastron deposits were recently discovered on Vesta. For another, because Vesta's orbit is now going into aphelion stage, which will favor a concent…
- anchor1_doc_order_rag score: 0.0000
  prediction: The Skipper still would've ignored the new cook's advice.
  top_chunk: rank=1 score=0.5666 Why should there be?" "Well, for one thing," wrangled our pint-sized cook, "because rich ekalastron deposits were recently discovered on Vesta. For another, because Vesta's orbit is now going into aphelion stage, which will favor a concent…
- anchor2_doc_order_rag score: 0.0000
  prediction: The text doesn't indicate how the Skipper would've acted in a different scenario.
  top_chunk: rank=1 score=0.5666 Why should there be?" "Well, for one thing," wrangled our pint-sized cook, "because rich ekalastron deposits were recently discovered on Vesta. For another, because Vesta's orbit is now going into aphelion stage, which will favor a concent…

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
  prediction: No, because the nurse said that Stevens died of a head injury an hour before Duane woke up.
  top_chunk: rank=1 score=0.6365 Duane got up, retrieving the two heat guns, and stared at him. " They tell me I killed Stevens the same way ," he thought. " I'm getting in a rut! " But Andrias was not dead, though he was out as cold as the void beyond Pluto. The thick ca…
- anchor1_doc_order_rag score: 0.0000
  prediction: No, because the nurse said that Stevens died of a head injury an hour before Duane woke up.
  top_chunk: rank=1 score=0.6365 Duane got up, retrieving the two heat guns, and stared at him. " They tell me I killed Stevens the same way ," he thought. " I'm getting in a rut! " But Andrias was not dead, though he was out as cold as the void beyond Pluto. The thick ca…
- anchor2_doc_order_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.6365 Duane got up, retrieving the two heat guns, and stared at him. " They tell me I killed Stevens the same way ," he thought. " I'm getting in a rut! " But Andrias was not dead, though he was out as cold as the void beyond Pluto. The thick ca…

### contract_nli

- examples: 50
- disagreements: 18
- any-positive-score: 38

#### contract_nli / 3_nda-7

- query: Receiving Party may share some Confidential Information with some third-parties (including consultants, agents and professional advisors).
- references: Entailment
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.5105 c) is lawfully disclosed or made available to the Receiving Party by a third party having no obligation to the Disclosing Party to maintain the confidentiality of such information; d) was independently developed or derived by the Receiving…
- reorder_only_rag score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.5105 c) is lawfully disclosed or made available to the Receiving Party by a third party having no obligation to the Disclosing Party to maintain the confidentiality of such information; d) was independently developed or derived by the Receiving…
- reverse_order_rag score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.5105 c) is lawfully disclosed or made available to the Receiving Party by a third party having no obligation to the Disclosing Party to maintain the confidentiality of such information; d) was independently developed or derived by the Receiving…
- random_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5105 c) is lawfully disclosed or made available to the Receiving Party by a third party having no obligation to the Disclosing Party to maintain the confidentiality of such information; d) was independently developed or derived by the Receiving…
- anchor1_doc_order_rag score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.5105 c) is lawfully disclosed or made available to the Receiving Party by a third party having no obligation to the Disclosing Party to maintain the confidentiality of such information; d) was independently developed or derived by the Receiving…
- anchor2_doc_order_rag score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.5105 c) is lawfully disclosed or made available to the Receiving Party by a third party having no obligation to the Disclosing Party to maintain the confidentiality of such information; d) was independently developed or derived by the Receiving…

#### contract_nli / 7_nda-17

- query: Receiving Party may create a copy of some Confidential Information in some circumstances.
- references: Contradiction
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5525 1.2 (a) 'Confidential Information' shall mean all information received from the other party which the latter has indicated in writing or labelled to be “Confidential”, “Proprietary Information” or with any other comparable legend to simila…
- reorder_only_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5525 1.2 (a) 'Confidential Information' shall mean all information received from the other party which the latter has indicated in writing or labelled to be “Confidential”, “Proprietary Information” or with any other comparable legend to simila…
- reverse_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5525 1.2 (a) 'Confidential Information' shall mean all information received from the other party which the latter has indicated in writing or labelled to be “Confidential”, “Proprietary Information” or with any other comparable legend to simila…
- random_order_rag score: 0.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5525 1.2 (a) 'Confidential Information' shall mean all information received from the other party which the latter has indicated in writing or labelled to be “Confidential”, “Proprietary Information” or with any other comparable legend to simila…
- anchor1_doc_order_rag score: 0.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5525 1.2 (a) 'Confidential Information' shall mean all information received from the other party which the latter has indicated in writing or labelled to be “Confidential”, “Proprietary Information” or with any other comparable legend to simila…
- anchor2_doc_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5525 1.2 (a) 'Confidential Information' shall mean all information received from the other party which the latter has indicated in writing or labelled to be “Confidential”, “Proprietary Information” or with any other comparable legend to simila…

#### contract_nli / 3_nda-1

- query: All Confidential Information shall be expressly identified by the Disclosing Party.
- references: Entailment
- best_methods: anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Not mentioned
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

#### contract_nli / 3_nda-11

- query: Receiving Party shall not reverse engineer any objects which embody Disclosing Party's Confidential Information.
- references: Entailment
- best_methods: reorder_only_rag, reverse_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5490 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
- reorder_only_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5490 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
- reverse_order_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5490 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
- random_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5490 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
- anchor1_doc_order_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5490 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
- anchor2_doc_order_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5490 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…

#### contract_nli / 3_nda-12

- query: Receiving Party may independently develop information similar to Confidential Information.
- references: Entailment
- best_methods: vanilla_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5296 c) is lawfully disclosed or made available to the Receiving Party by a third party having no obligation to the Disclosing Party to maintain the confidentiality of such information; d) was independently developed or derived by the Receiving…
- reorder_only_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5296 c) is lawfully disclosed or made available to the Receiving Party by a third party having no obligation to the Disclosing Party to maintain the confidentiality of such information; d) was independently developed or derived by the Receiving…
- reverse_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5296 c) is lawfully disclosed or made available to the Receiving Party by a third party having no obligation to the Disclosing Party to maintain the confidentiality of such information; d) was independently developed or derived by the Receiving…
- random_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5296 c) is lawfully disclosed or made available to the Receiving Party by a third party having no obligation to the Disclosing Party to maintain the confidentiality of such information; d) was independently developed or derived by the Receiving…
- anchor1_doc_order_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5296 c) is lawfully disclosed or made available to the Receiving Party by a third party having no obligation to the Disclosing Party to maintain the confidentiality of such information; d) was independently developed or derived by the Receiving…
- anchor2_doc_order_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5296 c) is lawfully disclosed or made available to the Receiving Party by a third party having no obligation to the Disclosing Party to maintain the confidentiality of such information; d) was independently developed or derived by the Receiving…
