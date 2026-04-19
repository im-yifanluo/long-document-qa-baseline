# Comparison Report

Run tier: `subset`

## Score Summary

| Task | Metric | vanilla_rag | reorder_only_rag | reverse_order_rag | random_order_rag | anchor1_doc_order_rag | anchor2_doc_order_rag | reorder_only_rag_minus_vanilla_rag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| qmsum | rouge | 15.7102 | 16.0649 | 16.1656 | 15.3977 | 15.8620 | 15.5549 | +0.3547 |
| qasper | f1 | 29.2815 | 38.8096 | 32.8572 | 33.9657 | 33.9821 | 29.7282 | +9.5281 |
| narrative_qa | f1 | 10.8842 | 13.3109 | 8.2304 | 6.1055 | 8.6179 | 10.4853 | +2.4267 |
| quality | exact_match | 44.0000 | 42.0000 | 42.0000 | 44.0000 | 42.0000 | 40.0000 | -2.0000 |
| contract_nli | exact_match | 66.0000 | 58.0000 | 58.0000 | 58.0000 | 66.0000 | 64.0000 | -8.0000 |

## Runtime Summary

| Method | Total seconds | Total minutes | Seconds / example | Examples / second |
| --- | --- | --- | --- | --- |
| vanilla_rag | 393.31 | 6.56 | 1.5732 | 0.6356 |
| reorder_only_rag | 392.73 | 6.55 | 1.5709 | 0.6366 |
| reverse_order_rag | 387.76 | 6.46 | 1.5510 | 0.6447 |
| random_order_rag | 385.34 | 6.42 | 1.5414 | 0.6488 |
| anchor1_doc_order_rag | 383.61 | 6.39 | 1.5344 | 0.6517 |
| anchor2_doc_order_rag | 380.42 | 6.34 | 1.5217 | 0.6572 |

## Example Previews

### qmsum

- examples: 50
- disagreements: 50
- any-positive-score: 48

#### qmsum / va-sq-1

- query: What was agreed upon on sample transcripts?
- references: To save time, speaker mn005 will only mark the sample of transcribed data for regions of overlapping speech, as opposed to marking all acoustic events. The digits extraction task will be delegated to whomever is working on acoustics for the Meeting Recorder project.
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Based on the provided context, it was agreed that there is a forty-five minute piece that Jane transcribed, which was then sent to IBM for transcription, providing a comparison point. Additionally, there is a larger piece recorded and put on CD-ROM and sent to IBM, but the extent of the transcription for this larger piece is unknown. The group also discussed the possibility that transcripts of sp…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- reorder_only_rag score: 0.0000
  prediction: Based on the provided context, it was agreed that there is a forty-five minute piece that Jane transcribed, which was then sent to IBM for transcription, providing a comparison point. Additionally, there is a larger piece that has been recorded and put on CD-ROM and sent to IBM, but the transcription status of this larger piece is unknown. The group also discussed the idea of manually marking the…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- reverse_order_rag score: 0.0000
  prediction: Based on the provided context, it seems that the group agreed to use a sample transcript as a ground truth. Specifically, they mentioned a 45-minute piece transcribed by Jane, which was then sent to IBM for comparison. Additionally, a larger piece was recorded, transcribed, and sent to IBM as well. The idea is to use these transcriptions as a reference point for comparison.
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- random_order_rag score: 0.0000
  prediction: Based on the provided context, it was agreed that Grad G would collect the digit forms and write down the transcripts. Professor E suggested starting by giving the transcript number, and there was a plan to have a forty-five minute piece that had been transcribed and sent to IBM for comparison. Additionally, a larger piece had been recorded and put on CD-ROM and sent to IBM, but the transcription…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- anchor1_doc_order_rag score: 0.0000
  prediction: Based on the provided context, it was agreed that there is a forty-five minute piece that Jane transcribed, which was then sent to IBM for transcription, providing a comparison point. Additionally, there is a larger piece that has been recorded and put on CD-ROM and sent to IBM for transcription, but the extent of the transcription (twenty-five to thirty hours) is unknown. The group also discusse…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…
- anchor2_doc_order_rag score: 0.0000
  prediction: Based on the provided context, it was agreed that there is a forty-five minute piece that Jane transcribed, which was then sent to IBM for transcription, providing a comparison point. Additionally, there is a larger piece that has been recorded and put on CD-ROM and sent to IBM for transcription, but the extent of the transcription (twenty-five to thirty hours) is unknown. The group also discusse…
  top_chunk: rank=1 score=0.3319 Grad G: I 'm gonna collect the digit forms and write it down . Postdoc B: OK . PhD C: Oh , OK . Grad G: So {disfmarker} So they should be right with what 's on the digit forms . OK , so I 'll go ahead and start with digits . u And I should…

#### qmsum / va-sq-4

- query: What was the future of data collection?
- references: The group aims to collect over 100 hours of Meeting Recorder data in total. Speaker consent forms are being revised. It was suggested that subjects should sign a new consent form after 10 recording sessions.
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Based on the provided context, the future of data collection involves potentially collecting more audio data by recording additional meetings. PhD C suggests recording two or three more meetings a week just to have the data, even if they are not doing the digitization at the moment. Additionally, there is a consideration to look into the existing data to see if there are any useful insights befor…
  top_chunk: rank=1 score=0.3866 I wanted to ask another a a aspect of the data collection . There 'd be no reason why a person couldn't get together several uh , you know , friends , and come and argue about a topic if they wanted to , right ?
- reorder_only_rag score: 0.0000
  prediction: Based on the provided context, the future of data collection involves potentially increasing the amount of audio data by recording a few more meetings per week, even if the transcribers do not perform digitization. This approach is seen as politically beneficial, especially for proposals, as it demonstrates that a significant amount of audio data has been collected. Additionally, there is a sugge…
  top_chunk: rank=1 score=0.3866 I wanted to ask another a a aspect of the data collection . There 'd be no reason why a person couldn't get together several uh , you know , friends , and come and argue about a topic if they wanted to , right ?
- reverse_order_rag score: 0.0000
  prediction: The future of data collection involves potentially collecting more audio data by having participants argue about a topic, even if they do not necessarily provide digitized responses. The goal is to gather a significant amount of audio data, which can be politically beneficial for the institution, especially when putting in a proposal. Additionally, there is a suggestion to look into the existing…
  top_chunk: rank=1 score=0.3866 I wanted to ask another a a aspect of the data collection . There 'd be no reason why a person couldn't get together several uh , you know , friends , and come and argue about a topic if they wanted to , right ?
- random_order_rag score: 0.0000
  prediction: The future of data collection involves looking into the data that has already been collected, with the help of Jane, to see if there are any useful insights before investing too much effort into future data collection projects. There is also a suggestion that someone could gather friends to argue about a topic, which would contribute to the data collection. However, the specific amount of data th…
  top_chunk: rank=1 score=0.3866 I wanted to ask another a a aspect of the data collection . There 'd be no reason why a person couldn't get together several uh , you know , friends , and come and argue about a topic if they wanted to , right ?
- anchor1_doc_order_rag score: 0.0000
  prediction: The future of data collection involves potentially collecting more audio data by recording a few more meetings per week, even if the transcribers do not perform digitization tasks. This approach is seen as politically beneficial, especially for proposals, as it demonstrates that a significant amount of audio data has been collected. Additionally, there is a suggestion to explore the existing data…
  top_chunk: rank=1 score=0.3866 I wanted to ask another a a aspect of the data collection . There 'd be no reason why a person couldn't get together several uh , you know , friends , and come and argue about a topic if they wanted to , right ?
- anchor2_doc_order_rag score: 0.0000
  prediction: Based on the provided context, the future of data collection involves potentially recording more meetings to increase the amount of data available. Specifically, PhD C suggests recording two or three more meetings a week, even if the transcribers are not doing the digitization work, just to accumulate more data. Professor E seems to support the idea of looking into the existing data and consideri…
  top_chunk: rank=1 score=0.3866 I wanted to ask another a a aspect of the data collection . There 'd be no reason why a person couldn't get together several uh , you know , friends , and come and argue about a topic if they wanted to , right ?

#### qmsum / va-sq-35

- query: Summarize the discussion about user requirements.
- references: According to a market survey, there were several things that users didn't like in current remote controls. First of all, users find them very ugly. Second, the current remote controls were not so easy to use and the facilities that they offered did not match what people really wanted. Third, people were very frustrated with their remote controls because sometimes they just couldn't find them. The…
- best_methods: reverse_order_rag
- disagreement: True
- vanilla_rag score: 5.3728
  prediction: The discussion centered around user requirements for a new remote control design. Key points included: 1. **Power Button Usage**: The power button is used infrequently, only once per session, but is considered very important. There was a suggestion to conduct research on how many users need to access specific channels (e.g., channel 25 to 64) to determine if these features are necessary. 2. **Fun…
  top_chunk: rank=1 score=0.3915 Marketing: this is of course , depends on that . And um I don't have any conclusion , I didn't have time the meeting was very tight , so that's basically my findings . And uh , if you have any question ? Project Manager: Mm I think it's go…
- reorder_only_rag score: 0.0000
  prediction: The discussion centered around user requirements for a new remote control, particularly focusing on the power button and target audience. Marketing emphasized the infrequent use of the power button, suggesting it should still be included for user convenience. The team agreed to target young people as they might be more interested in a new device. There was a suggestion to conduct research on how…
  top_chunk: rank=1 score=0.3915 Marketing: this is of course , depends on that . And um I don't have any conclusion , I didn't have time the meeting was very tight , so that's basically my findings . And uh , if you have any question ? Project Manager: Mm I think it's go…
- reverse_order_rag score: 7.7210
  prediction: The discussion centered around user requirements for a new remote control device. Key points included: 1. **Speaker Integration**: The User Interface suggested including speakers in the remote control, with the idea that users could shout to control the device, which the Marketing team agreed was a good idea. 2. **Functionality and Device Universality**: The Industrial Designer proposed limiting…
  top_chunk: rank=1 score=0.3915 Marketing: this is of course , depends on that . And um I don't have any conclusion , I didn't have time the meeting was very tight , so that's basically my findings . And uh , if you have any question ? Project Manager: Mm I think it's go…
- random_order_rag score: 5.8179
  prediction: The discussion centered around user requirements for a new remote control device. The Marketing expert highlighted that the power button is used infrequently but is very important, suggesting it should be easily accessible. The User Interface expert proposed including speakers in the remote, which was met with a positive response from Marketing. Marketing also suggested focusing on young people a…
  top_chunk: rank=1 score=0.3915 Marketing: this is of course , depends on that . And um I don't have any conclusion , I didn't have time the meeting was very tight , so that's basically my findings . And uh , if you have any question ? Project Manager: Mm I think it's go…
- anchor1_doc_order_rag score: 5.8096
  prediction: The discussion centered around user requirements for a new remote control device. Key points included: 1. **Power Button Usage**: The power button is used infrequently, only once per session, but is considered very important for user satisfaction. 2. **Target Audience**: There was agreement to target young people as they are more likely to be interested in a new device. 3. **Functionality**: The…
  top_chunk: rank=1 score=0.3915 Marketing: this is of course , depends on that . And um I don't have any conclusion , I didn't have time the meeting was very tight , so that's basically my findings . And uh , if you have any question ? Project Manager: Mm I think it's go…
- anchor2_doc_order_rag score: 5.8096
  prediction: The discussion centered around user requirements for a new remote control device. Key points included: 1. **Power Button Usage**: The power button is used infrequently, only once per session, but is considered very important for user satisfaction. 2. **Target Audience**: There was agreement to target young people as they are more likely to be interested in a new device. 3. **Functionality**: The…
  top_chunk: rank=1 score=0.3915 Marketing: this is of course , depends on that . And um I don't have any conclusion , I didn't have time the meeting was very tight , so that's basically my findings . And uh , if you have any question ? Project Manager: Mm I think it's go…

#### qmsum / va-sq-18

- query: Summarize the group's plan of their marketing strategy.
- references: For fear that the exorbitant price of 25 euros of the remote control would shock the potential consumers, Project Manager proposed to trade off some functions for a lower price. Additionally, Project Manager mentioned an American computer electronics store to show that shipping products overseas can also make profits and then added this to the whole plan.
- best_methods: anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: The group plans to create fashionable, ordinary products that are typically not given much thought, aiming to make them as appealing as high-end brands like John Lewis or department stores such as Debenhams. Their strategy involves transforming mundane items into stylish, desirable products to enhance their market appeal.
  top_chunk: rank=1 score=0.3665 if you wanna write all five go for it but name one of them that you could um . Oh , we skipped introductions . Nice . I'm a excellent Project Manager . Um . Marketing: {vocalsound} Project Manager: I'm Marty , Industrial Designer: {vocalso…
- reorder_only_rag score: 6.3730
  prediction: Based on the provided context, the group's plan for their marketing strategy involves taking ordinary products that people don't typically think about and making them appealing and fashionable. They aim to emulate the style and quality associated with well-known brands like John Lewis or Debenhams. The conversation suggests they are in the early stages of brainstorming and planning, focusing on i…
  top_chunk: rank=1 score=0.3665 if you wanna write all five go for it but name one of them that you could um . Oh , we skipped introductions . Nice . I'm a excellent Project Manager . Um . Marketing: {vocalsound} Project Manager: I'm Marty , Industrial Designer: {vocalso…
- reverse_order_rag score: 6.7137
  prediction: The group plans to brainstorm and develop a marketing strategy for their project. They aim to focus on making ordinary items fashionable and appealing, aligning with their corporate strategy. The team will consider various aspects such as how to sell the product and potentially use classical music and Family Guy DVDs as themes or references. They also discuss incorporating personal interests, lik…
  top_chunk: rank=1 score=0.3665 if you wanna write all five go for it but name one of them that you could um . Oh , we skipped introductions . Nice . I'm a excellent Project Manager . Um . Marketing: {vocalsound} Project Manager: I'm Marty , Industrial Designer: {vocalso…
- random_order_rag score: 0.0000
  prediction: The group plans to make ordinary stuff fashionable and appealing, aligning with a corporate strategy to make their products as nice as those from well-known brands like John Lewis or Debenhams. Their goal is to transform everyday items into desirable products through creative marketing and design.
  top_chunk: rank=1 score=0.3665 if you wanna write all five go for it but name one of them that you could um . Oh , we skipped introductions . Nice . I'm a excellent Project Manager . Um . Marketing: {vocalsound} Project Manager: I'm Marty , Industrial Designer: {vocalso…
- anchor1_doc_order_rag score: 0.0000
  prediction: The group plans to focus on making ordinary products fashionable and appealing, aligning with their corporate strategy. They aim to take items that people don't typically think about and enhance them to be as nice and attractive as high-end products from stores like John Lewis or Debenhams. The team will brainstorm ideas and consider how to effectively market these products to achieve their goal…
  top_chunk: rank=1 score=0.3665 if you wanna write all five go for it but name one of them that you could um . Oh , we skipped introductions . Nice . I'm a excellent Project Manager . Um . Marketing: {vocalsound} Project Manager: I'm Marty , Industrial Designer: {vocalso…
- anchor2_doc_order_rag score: 7.7540
  prediction: The group plans to make ordinary products more fashionable to appeal to a broader audience. Their strategy involves taking items that people don't usually think about and making them aesthetically pleasing, similar to how John Lewis or Debenhams present their products. They aim to sell their concept by having the project manager and the team think about what they can do and what they want to achi…
  top_chunk: rank=1 score=0.3665 if you wanna write all five go for it but name one of them that you could um . Oh , we skipped introductions . Nice . I'm a excellent Project Manager . Um . Marketing: {vocalsound} Project Manager: I'm Marty , Industrial Designer: {vocalso…

#### qmsum / va-sq-2

- query: What was said on speech overlap?
- references: Efforts by speaker mn005 are in progress to detect overlapping speech. For a single transcribed meeting, speaker mn005 reported approximately 300 cases of overlap. Future work will involve manually deriving time marks from sections of overlapping speech for the same meeting, and then experimenting with different measures, e.g. energy increase, to determine a set of acoustically salient features f…
- best_methods: random_order_rag
- disagreement: True
- vanilla_rag score: 6.1466
  prediction: Based on the provided context, PhD D explained that they consider the overlapping zone where the voices of multiple speakers overlap. They noted that they do not distinguish between the number of speakers during this overlap. PhD C suggested that speaker overlap could potentially be inferred from the relative energy in the speech, implying that it might not need to be marked entirely by hand. PhD…
  top_chunk: rank=1 score=0.4702 Eh almost eh three hundred eh in one session Grad G: Oh , God ! PhD D: in five {disfmarker} eh in forty - five minutes . PhD A: Three hundred overlapping speech {disfmarker} PhD D: Alm - Three hundred overlapping zone . Grad G: Ugh . PhD C…
- reorder_only_rag score: 9.0999
  prediction: PhD D's objective is to study overlapping speech zones, and they found almost three hundred overlapping speech events in one session within forty-five minutes. This amounts to about six overlapping speech events per minute. PhD D does not distinguish between the number of speakers during these overlaps. Professor E suggests marking only the speaker overlaps to save time, as manually marking all e…
  top_chunk: rank=1 score=0.4702 Eh almost eh three hundred eh in one session Grad G: Oh , God ! PhD D: in five {disfmarker} eh in forty - five minutes . PhD A: Three hundred overlapping speech {disfmarker} PhD D: Alm - Three hundred overlapping zone . Grad G: Ugh . PhD C…
- reverse_order_rag score: 7.4096
  prediction: Based on the provided context, PhD D explained that they consider the entirety of the time there is voice overlap as overlapping speech. They mentioned that in one session, they found almost three hundred overlapping speech zones in forty-five minutes. Additionally, PhD D stated their objective is to study overlapping zones, and in twelve minutes, they found one thousand acoustic events, which li…
  top_chunk: rank=1 score=0.4702 Eh almost eh three hundred eh in one session Grad G: Oh , God ! PhD D: in five {disfmarker} eh in forty - five minutes . PhD A: Three hundred overlapping speech {disfmarker} PhD D: Alm - Three hundred overlapping zone . Grad G: Ugh . PhD C…
- random_order_rag score: 9.5444
  prediction: Based on the provided context, several points were made regarding speech overlap: 1. PhD D mentioned that they consider the entirety of the voice to have overlapped at some point. 2. PhD C suggested that speaker overlap could be inferred from the relative energy in the audio, implying that manual marking might not be necessary. 3. Professor E pointed out that manually marking speaker overlaps is…
  top_chunk: rank=1 score=0.4702 Eh almost eh three hundred eh in one session Grad G: Oh , God ! PhD D: in five {disfmarker} eh in forty - five minutes . PhD A: Three hundred overlapping speech {disfmarker} PhD D: Alm - Three hundred overlapping zone . Grad G: Ugh . PhD C…
- anchor1_doc_order_rag score: 0.0000
  prediction: PhD D mentioned studying the overlapping zone and found one thousand acoustic events in twelve minutes. The overlapping zone refers to instances where voices overlap, and PhD D does not distinguish between the number of speakers during these overlaps. Professor E suggested marking only the speaker overlaps to save time, to which PhD D agreed. PhD C proposed inferring speaker overlaps from relativ…
  top_chunk: rank=1 score=0.4702 Eh almost eh three hundred eh in one session Grad G: Oh , God ! PhD D: in five {disfmarker} eh in forty - five minutes . PhD A: Three hundred overlapping speech {disfmarker} PhD D: Alm - Three hundred overlapping zone . Grad G: Ugh . PhD C…
- anchor2_doc_order_rag score: 8.5027
  prediction: PhD D discussed the issue of overlapping speech in a session, noting that there were almost three hundred overlapping speech instances in one session within forty-five minutes. PhD D defined the overlapping zone as the entire time during which voices overlapped, without distinguishing between the number of speakers. PhD D also mentioned finding one thousand acoustic events in twelve minutes, whic…
  top_chunk: rank=1 score=0.4702 Eh almost eh three hundred eh in one session Grad G: Oh , God ! PhD D: in five {disfmarker} eh in forty - five minutes . PhD A: Three hundred overlapping speech {disfmarker} PhD D: Alm - Three hundred overlapping zone . Grad G: Ugh . PhD C…

### qasper

- examples: 50
- disagreements: 38
- any-positive-score: 43

#### qasper / 71e4ba4e87e6596aeca187127c0d088df6570c57

- query: What evaluations methods do they take?
- references: Unanswerable | Unanswerable
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: After inspecting a subset of the Flickr30K data, I have grouped these inferences into six categories (image examples between parentheses).
  top_chunk: rank=1 score=0.2777 A next step would be to see whether these observations also hold for other age groups, i.e. children and adults. INLINEFORM0 Other methods It may be difficult to spot patterns by just looking at a collection of images. Another method is to…
- reorder_only_rag score: 0.0000
  prediction: tag all descriptions with part-of-speech information
  top_chunk: rank=1 score=0.2777 A next step would be to see whether these observations also hold for other age groups, i.e. children and adults. INLINEFORM0 Other methods It may be difficult to spot patterns by just looking at a collection of images. Another method is to…
- reverse_order_rag score: 0.0000
  prediction: tag all descriptions with part-of-speech information
  top_chunk: rank=1 score=0.2777 A next step would be to see whether these observations also hold for other age groups, i.e. children and adults. INLINEFORM0 Other methods It may be difficult to spot patterns by just looking at a collection of images. Another method is to…
- random_order_rag score: 0.0000
  prediction: After inspecting a subset of the Flickr30K data, I have grouped these inferences into six categories. Finally, I will discuss several methods to analyze the data in order to detect biases.
  top_chunk: rank=1 score=0.2777 A next step would be to see whether these observations also hold for other age groups, i.e. children and adults. INLINEFORM0 Other methods It may be difficult to spot patterns by just looking at a collection of images. Another method is to…
- anchor1_doc_order_rag score: 0.0000
  prediction: After inspecting a subset of the Flickr30K data, I have grouped these inferences into six categories (image examples between parentheses).
  top_chunk: rank=1 score=0.2777 A next step would be to see whether these observations also hold for other age groups, i.e. children and adults. INLINEFORM0 Other methods It may be difficult to spot patterns by just looking at a collection of images. Another method is to…
- anchor2_doc_order_rag score: 0.0000
  prediction: After inspecting a subset of the Flickr30K data, I have grouped these inferences into six categories (image examples between parentheses).
  top_chunk: rank=1 score=0.2777 A next step would be to see whether these observations also hold for other age groups, i.e. children and adults. INLINEFORM0 Other methods It may be difficult to spot patterns by just looking at a collection of images. Another method is to…

#### qasper / a313e98994fc039a82aa2447c411dda92c65a470

- query: How do they match words before reordering them?
- references: Unanswerable | CFILT-preorder system
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: pre-ordering English sentences (assisting language sentences) to match the word-order of the source language and train the parent model on this pre-ordered corpus
  top_chunk: rank=1 score=0.4351 One of the pre-ordering rule swaps the position of the noun phrase followed by a transitive verb with the transitive verb. The original and the resulting re-ordered parse tree will be as shown in the Table TABREF5 . Applying this reorderin…
- reorder_only_rag score: 0.0000
  prediction: One of the pre-ordering rule swaps the position of the noun phrase followed by a transitive verb with the transitive verb.
  top_chunk: rank=1 score=0.4351 One of the pre-ordering rule swaps the position of the noun phrase followed by a transitive verb with the transitive verb. The original and the resulting re-ordered parse tree will be as shown in the Table TABREF5 . Applying this reorderin…
- reverse_order_rag score: 0.0000
  prediction: pre-ordering the assisting language to match the word order of the source language
  top_chunk: rank=1 score=0.4351 One of the pre-ordering rule swaps the position of the noun phrase followed by a transitive verb with the transitive verb. The original and the resulting re-ordered parse tree will be as shown in the Table TABREF5 . Applying this reorderin…
- random_order_rag score: 0.0000
  prediction: pre-order English sentences (assisting language sentences) to match the word-order of the source language and train the parent model on this pre-ordered corpus.
  top_chunk: rank=1 score=0.4351 One of the pre-ordering rule swaps the position of the noun phrase followed by a transitive verb with the transitive verb. The original and the resulting re-ordered parse tree will be as shown in the Table TABREF5 . Applying this reorderin…
- anchor1_doc_order_rag score: 0.0000
  prediction: Applying the reordering rule to swap the position of the noun phrase followed by a transitive verb with the transitive verb.
  top_chunk: rank=1 score=0.4351 One of the pre-ordering rule swaps the position of the noun phrase followed by a transitive verb with the transitive verb. The original and the resulting re-ordered parse tree will be as shown in the Table TABREF5 . Applying this reorderin…
- anchor2_doc_order_rag score: 0.0000
  prediction: They match words before reordering them by pre-ordering English sentences to match the word-order of the source language.
  top_chunk: rank=1 score=0.4351 One of the pre-ordering rule swaps the position of the noun phrase followed by a transitive verb with the transitive verb. The original and the resulting re-ordered parse tree will be as shown in the Table TABREF5 . Applying this reorderin…

#### qasper / ef4dba073d24042f24886580ae77add5326f2130

- query: What accuracy does the proposed system achieve?
- references: F1 scores of 85.99 on the DL-PS data, 75.15 on the EC-MT data and 71.53 on the EC-UQ data | F1 of 85.99 on the DL-PS dataset (dialog domain); 75.15 on EC-MT and 71.53 on EC-UQ (e-commerce domain)
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: The context does not provide the accuracy achieved by the proposed system.
  top_chunk: rank=1 score=0.3082 It is one biggest challenge to build a powerful NER system on such a low quality annotated data. Although we can obtain high quality annotations for each input sentence by majority voting, it can be a waste of human labors to achieve such…
- reorder_only_rag score: 0.0000
  prediction: The context does not provide the specific accuracy achieved by the proposed system.
  top_chunk: rank=1 score=0.3082 It is one biggest challenge to build a powerful NER system on such a low quality annotated data. Although we can obtain high quality annotations for each input sentence by majority voting, it can be a waste of human labors to achieve such…
- reverse_order_rag score: 0.0000
  prediction: The context does not provide the accuracy achieved by the proposed system.
  top_chunk: rank=1 score=0.3082 It is one biggest challenge to build a powerful NER system on such a low quality annotated data. Although we can obtain high quality annotations for each input sentence by majority voting, it can be a waste of human labors to achieve such…
- random_order_rag score: 0.0000
  prediction: The context does not provide the accuracy achieved by the proposed system.
  top_chunk: rank=1 score=0.3082 It is one biggest challenge to build a powerful NER system on such a low quality annotated data. Although we can obtain high quality annotations for each input sentence by majority voting, it can be a waste of human labors to achieve such…
- anchor1_doc_order_rag score: 0.0000
  prediction: The context does not provide the accuracy achieved by the proposed system.
  top_chunk: rank=1 score=0.3082 It is one biggest challenge to build a powerful NER system on such a low quality annotated data. Although we can obtain high quality annotations for each input sentence by majority voting, it can be a waste of human labors to achieve such…
- anchor2_doc_order_rag score: 0.0000
  prediction: The context does not provide the accuracy achieved by the proposed system.
  top_chunk: rank=1 score=0.3082 It is one biggest challenge to build a powerful NER system on such a low quality annotated data. Although we can obtain high quality annotations for each input sentence by majority voting, it can be a waste of human labors to achieve such…

#### qasper / fb2b536dc8e442dffab408db992b971e86548158

- query: What is the interannotator agreement for the human evaluation?
- references: Unanswerable | Unanswerable
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.3259 The opinons expressed are those of the authors and do not represent the views of the institute or the U.S. Department of Education
- reorder_only_rag score: 0.0000
  prediction: Not provided
  top_chunk: rank=1 score=0.3259 The opinons expressed are those of the authors and do not represent the views of the institute or the U.S. Department of Education
- reverse_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.3259 The opinons expressed are those of the authors and do not represent the views of the institute or the U.S. Department of Education
- random_order_rag score: 0.0000
  prediction: The context does not provide information about the interannotator agreement for the human evaluation.
  top_chunk: rank=1 score=0.3259 The opinons expressed are those of the authors and do not represent the views of the institute or the U.S. Department of Education
- anchor1_doc_order_rag score: 0.0000
  prediction: Not provided
  top_chunk: rank=1 score=0.3259 The opinons expressed are those of the authors and do not represent the views of the institute or the U.S. Department of Education
- anchor2_doc_order_rag score: 0.0000
  prediction: Not provided
  top_chunk: rank=1 score=0.3259 The opinons expressed are those of the authors and do not represent the views of the institute or the U.S. Department of Education

#### qasper / a87a009c242d57c51fc94fe312af5e02070f898b

- query: What predictive model do they build?
- references: logistic regression models | logistic regression models based on unigram bag-of-words features (BOW), sentiment signals (SENT), the linguistic features from our earlier analyses (LING), and combinations of these features.
- best_methods: anchor1_doc_order_rag
- disagreement: True
- vanilla_rag score: 5.7143
  prediction: We present a statistical model of dogmatism that addresses two complementary goals.
  top_chunk: rank=1 score=0.4665 A predictive model further validates our feature sets, and also allows us to analyze dogmatism in millions of other Reddit comments in a scalable way, with multiple uses in ongoing, downstream analyses. Prediction task. Our goal is (1) to…
- reorder_only_rag score: 6.2500
  prediction: a predictive model to classify dogmatic posts from Reddit
  top_chunk: rank=1 score=0.4665 A predictive model further validates our feature sets, and also allows us to analyze dogmatism in millions of other Reddit comments in a scalable way, with multiple uses in ongoing, downstream analyses. Prediction task. Our goal is (1) to…
- reverse_order_rag score: 0.0000
  prediction: a predictive model that analyzes new content
  top_chunk: rank=1 score=0.4665 A predictive model further validates our feature sets, and also allows us to analyze dogmatism in millions of other Reddit comments in a scalable way, with multiple uses in ongoing, downstream analyses. Prediction task. Our goal is (1) to…
- random_order_rag score: 5.8824
  prediction: We build a predictive model to classify dogmatic posts from Reddit.
  top_chunk: rank=1 score=0.4665 A predictive model further validates our feature sets, and also allows us to analyze dogmatism in millions of other Reddit comments in a scalable way, with multiple uses in ongoing, downstream analyses. Prediction task. Our goal is (1) to…
- anchor1_doc_order_rag score: 7.1429
  prediction: a statistical model of dogmatism
  top_chunk: rank=1 score=0.4665 A predictive model further validates our feature sets, and also allows us to analyze dogmatism in millions of other Reddit comments in a scalable way, with multiple uses in ongoing, downstream analyses. Prediction task. Our goal is (1) to…
- anchor2_doc_order_rag score: 5.7143
  prediction: We present a statistical model of dogmatism that addresses two complementary goals.
  top_chunk: rank=1 score=0.4665 A predictive model further validates our feature sets, and also allows us to analyze dogmatism in millions of other Reddit comments in a scalable way, with multiple uses in ongoing, downstream analyses. Prediction task. Our goal is (1) to…

### narrative_qa

- examples: 50
- disagreements: 41
- any-positive-score: 23

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_10

- query: Where is Miranda Hope from?
- references: Bangor, Maine
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: New England
  top_chunk: rank=1 score=0.4013 will brighten for the deep-lunged children of the Fatherland! CHAPTER IX MIRANDA HOPE TO HER MOTHER. October 22d Dear Mother--I am off in a day or two to visit some new country; I haven't yet decided which. I have satisfied myself with reg…
- reorder_only_rag score: 0.0000
  prediction: New England
  top_chunk: rank=1 score=0.4013 will brighten for the deep-lunged children of the Fatherland! CHAPTER IX MIRANDA HOPE TO HER MOTHER. October 22d Dear Mother--I am off in a day or two to visit some new country; I haven't yet decided which. I have satisfied myself with reg…
- reverse_order_rag score: 0.0000
  prediction: the heart of New England.
  top_chunk: rank=1 score=0.4013 will brighten for the deep-lunged children of the Fatherland! CHAPTER IX MIRANDA HOPE TO HER MOTHER. October 22d Dear Mother--I am off in a day or two to visit some new country; I haven't yet decided which. I have satisfied myself with reg…
- random_order_rag score: 0.0000
  prediction: the heart of New England
  top_chunk: rank=1 score=0.4013 will brighten for the deep-lunged children of the Fatherland! CHAPTER IX MIRANDA HOPE TO HER MOTHER. October 22d Dear Mother--I am off in a day or two to visit some new country; I haven't yet decided which. I have satisfied myself with reg…
- anchor1_doc_order_rag score: 0.0000
  prediction: the heart of New England
  top_chunk: rank=1 score=0.4013 will brighten for the deep-lunged children of the Fatherland! CHAPTER IX MIRANDA HOPE TO HER MOTHER. October 22d Dear Mother--I am off in a day or two to visit some new country; I haven't yet decided which. I have satisfied myself with reg…
- anchor2_doc_order_rag score: 0.0000
  prediction: New England
  top_chunk: rank=1 score=0.4013 will brighten for the deep-lunged children of the Fatherland! CHAPTER IX MIRANDA HOPE TO HER MOTHER. October 22d Dear Mother--I am off in a day or two to visit some new country; I haven't yet decided which. I have satisfied myself with reg…

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
  prediction: Vermont, or Minnesota, or some such place.
  top_chunk: rank=1 score=0.4222 FROM MISS VIOLET RAY, IN PARIS, TO MISS AGNES RICH, IN NEW YORK. September 21st. We had hardly got here when father received a telegram saying he would have to come right back to New York. It was for something about his business--I don't k…
- random_order_rag score: 0.0000
  prediction: Paris
  top_chunk: rank=1 score=0.4222 FROM MISS VIOLET RAY, IN PARIS, TO MISS AGNES RICH, IN NEW YORK. September 21st. We had hardly got here when father received a telegram saying he would have to come right back to New York. It was for something about his business--I don't k…
- anchor1_doc_order_rag score: 0.0000
  prediction: Paris
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
  prediction: Shall I help thee a little? Take three adorable girls . . . three, my good Prosper--the mystic number--neither more nor less. Take them and place thy insatiable little Leon in the midst of them! Is the situation sufficiently indicated, and do you apprehend the motives of my felicity?
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…
- reverse_order_rag score: 0.0000
  prediction: He
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…
- random_order_rag score: 0.0000
  prediction: He
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…
- anchor1_doc_order_rag score: 0.0000
  prediction: insatiable little Leon
  top_chunk: rank=1 score=0.2747 He chaffs her tremendously about her radicalism, and he is so immensely clever that she can't answer him, though she is rather clever too. There is also a Frenchman, a nephew, or cousin, or something, of the person of the house, who is ext…
- anchor2_doc_order_rag score: 0.0000
  prediction: insatiable little Leon
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
  prediction: She is making the _tour du monde_ entirely alone, without even a soubrette to carry the ensign, for the purpose of seeing for herself _a quoi s'en tenir sur les hommes et les choses--on les hommes_ particularly.
  top_chunk: rank=1 score=0.3351 But this New England maiden is, in her way, a strange type: she is travelling all over Europe alone--"to see it," she says, "for herself." For herself! What can that stiff slim self of hers do with such sights, such visions!
- reverse_order_rag score: 0.0000
  prediction: He appears to me less human than simian, and whenever I hear him talk I seem to myself to have paused in the street to listen to the shrill clatter of a hand-organ, to which the gambols of a hairy _homunculus_ form an accompaniment.
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

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_21

- query: Where is Miranda from, according to the story?
- references: Bangor, Maine | Bangor Maine
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: New England
  top_chunk: rank=1 score=0.3908 My _cousine_ is really admirable; the shop deserves to succeed. Miss Miranda is tall and rather flat; she is too pale; she hasn't the adorable _rougeurs_ of the little Anglaise.
- reorder_only_rag score: 0.0000
  prediction: New England
  top_chunk: rank=1 score=0.3908 My _cousine_ is really admirable; the shop deserves to succeed. Miss Miranda is tall and rather flat; she is too pale; she hasn't the adorable _rougeurs_ of the little Anglaise.
- reverse_order_rag score: 0.0000
  prediction: Anglaise
  top_chunk: rank=1 score=0.3908 My _cousine_ is really admirable; the shop deserves to succeed. Miss Miranda is tall and rather flat; she is too pale; she hasn't the adorable _rougeurs_ of the little Anglaise.
- random_order_rag score: 0.0000
  prediction: New England
  top_chunk: rank=1 score=0.3908 My _cousine_ is really admirable; the shop deserves to succeed. Miss Miranda is tall and rather flat; she is too pale; she hasn't the adorable _rougeurs_ of the little Anglaise.
- anchor1_doc_order_rag score: 0.0000
  prediction: the heart of New England
  top_chunk: rank=1 score=0.3908 My _cousine_ is really admirable; the shop deserves to succeed. Miss Miranda is tall and rather flat; she is too pale; she hasn't the adorable _rougeurs_ of the little Anglaise.
- anchor2_doc_order_rag score: 0.0000
  prediction: the heart of New England
  top_chunk: rank=1 score=0.3908 My _cousine_ is really admirable; the shop deserves to succeed. Miss Miranda is tall and rather flat; she is too pale; she hasn't the adorable _rougeurs_ of the little Anglaise.

### quality

- examples: 50
- disagreements: 23
- any-positive-score: 27

#### quality / 30029_F5N22U40_3

- query: How was Korvin able to avoid disclosing the true intent of his mission under the lie detector questioning? (A) While he was strapped down in the lie-detector, Korvin subtly switched the wire that indicated a truth with the one that indicated a lie. (B) Korvin said truths that literally answered the Tr'en's questions but evaded the intent behind their questions. . (C) The Tr'en hadn't tested the l…
- references: Korvin said truths that literally answered the Tr'en's questions but evaded the intent behind their questions. .
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.5941 True, every night the guards came in and gave him a concentrated lesson in the local language, but Korvin failed to get much pleasure out of that, being unconscious at the time. But now he was equipped to discuss almost anything from philo…
- reorder_only_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.5941 True, every night the guards came in and gave him a concentrated lesson in the local language, but Korvin failed to get much pleasure out of that, being unconscious at the time. But now he was equipped to discuss almost anything from philo…
- reverse_order_rag score: 0.0000
  prediction: B Korvin said truths that literally answered the Tr'en's questions but evaded the intent behind their questions.
  top_chunk: rank=1 score=0.5941 True, every night the guards came in and gave him a concentrated lesson in the local language, but Korvin failed to get much pleasure out of that, being unconscious at the time. But now he was equipped to discuss almost anything from philo…
- random_order_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.5941 True, every night the guards came in and gave him a concentrated lesson in the local language, but Korvin failed to get much pleasure out of that, being unconscious at the time. But now he was equipped to discuss almost anything from philo…
- anchor1_doc_order_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.5941 True, every night the guards came in and gave him a concentrated lesson in the local language, but Korvin failed to get much pleasure out of that, being unconscious at the time. But now he was equipped to discuss almost anything from philo…
- anchor2_doc_order_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.5941 True, every night the guards came in and gave him a concentrated lesson in the local language, but Korvin failed to get much pleasure out of that, being unconscious at the time. But now he was equipped to discuss almost anything from philo…

#### quality / 52845_75VB1ISR_1

- query: How much time has passed between Blake's night with Eldoria and his search for Sabrina York in his mind-world? (A) 7 years (B) 10 hours (C) 12 years (D) 1 hour
- references: 10 hours
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: C
  top_chunk: rank=1 score=0.4728 It was a remarkably detailed materialization, and his quarry's footprints stood out clearly in the duplicated sand. Sabrina York did not even know the rudiments of the art of throwing off a mind-tracker. It would have done her but little g…
- reorder_only_rag score: 0.0000
  prediction: 12 years
  top_chunk: rank=1 score=0.4728 It was a remarkably detailed materialization, and his quarry's footprints stood out clearly in the duplicated sand. Sabrina York did not even know the rudiments of the art of throwing off a mind-tracker. It would have done her but little g…
- reverse_order_rag score: 0.0000
  prediction: 12 years
  top_chunk: rank=1 score=0.4728 It was a remarkably detailed materialization, and his quarry's footprints stood out clearly in the duplicated sand. Sabrina York did not even know the rudiments of the art of throwing off a mind-tracker. It would have done her but little g…
- random_order_rag score: 0.0000
  prediction: 12 years
  top_chunk: rank=1 score=0.4728 It was a remarkably detailed materialization, and his quarry's footprints stood out clearly in the duplicated sand. Sabrina York did not even know the rudiments of the art of throwing off a mind-tracker. It would have done her but little g…
- anchor1_doc_order_rag score: 0.0000
  prediction: C
  top_chunk: rank=1 score=0.4728 It was a remarkably detailed materialization, and his quarry's footprints stood out clearly in the duplicated sand. Sabrina York did not even know the rudiments of the art of throwing off a mind-tracker. It would have done her but little g…
- anchor2_doc_order_rag score: 0.0000
  prediction: C
  top_chunk: rank=1 score=0.4728 It was a remarkably detailed materialization, and his quarry's footprints stood out clearly in the duplicated sand. Sabrina York did not even know the rudiments of the art of throwing off a mind-tracker. It would have done her but little g…

#### quality / 52845_75VB1ISR_2

- query: Why does Deirdre get so upset when Blake Past suggests she go to prom with the young man? (A) Because Blake is trying to guilt Deirdre into going with the young man by telling her that it'll ease her conscience. (B) Because Deirdre has fallen in love with Blake, despite his age, and wants him to take her to the prom. (C) Because Blake is acting like he's her father, which is a sensitive topic for…
- references: Because Deirdre has fallen in love with Blake, despite his age, and wants him to take her to the prom.
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: C
  top_chunk: rank=1 score=0.6406 Lord, he must have been feeling old to have pictured himself like that! Deirdre was speaking. "Yes," she was saying, "at nine o'clock. And I should very much like for you to come." Blake Past shook his head. "Proms aren't for parents. You…
- reorder_only_rag score: 0.0000
  prediction: Because Blake is acting like he's her father, which is a sensitive topic for Deirdre because she lost her real parents.
  top_chunk: rank=1 score=0.6406 Lord, he must have been feeling old to have pictured himself like that! Deirdre was speaking. "Yes," she was saying, "at nine o'clock. And I should very much like for you to come." Blake Past shook his head. "Proms aren't for parents. You…
- reverse_order_rag score: 0.0000
  prediction: Because Blake is acting like he's her father, which is a sensitive topic for Deirdre because she lost her real parents.
  top_chunk: rank=1 score=0.6406 Lord, he must have been feeling old to have pictured himself like that! Deirdre was speaking. "Yes," she was saying, "at nine o'clock. And I should very much like for you to come." Blake Past shook his head. "Proms aren't for parents. You…
- random_order_rag score: 0.0000
  prediction: Because Blake is acting like he's her father, which is a sensitive topic for Deirdre because she lost her real parents.
  top_chunk: rank=1 score=0.6406 Lord, he must have been feeling old to have pictured himself like that! Deirdre was speaking. "Yes," she was saying, "at nine o'clock. And I should very much like for you to come." Blake Past shook his head. "Proms aren't for parents. You…
- anchor1_doc_order_rag score: 0.0000
  prediction: C
  top_chunk: rank=1 score=0.6406 Lord, he must have been feeling old to have pictured himself like that! Deirdre was speaking. "Yes," she was saying, "at nine o'clock. And I should very much like for you to come." Blake Past shook his head. "Proms aren't for parents. You…
- anchor2_doc_order_rag score: 0.0000
  prediction: Because Blake is acting like he's her father, which is a sensitive topic for Deirdre because she lost her real parents.
  top_chunk: rank=1 score=0.6406 Lord, he must have been feeling old to have pictured himself like that! Deirdre was speaking. "Yes," she was saying, "at nine o'clock. And I should very much like for you to come." Blake Past shook his head. "Proms aren't for parents. You…

#### quality / 52845_75VB1ISR_3

- query: Why does shame flame in Blake's cheeks when Deirdre goes to prepare Eldoria's dias? (A) He is embarrassed at the thought that Deirdre might enter the room while he is sleeping with Eldoria. (B) He feels that prostitution is morally reprehensible. (C) He feels guilty about sleeping with Eldoria when there's a child in the hut, Deirdre, who knows exactly what's going on. (D) He feels guilty about w…
- references: He feels guilty about sleeping with Eldoria when there's a child in the hut, Deirdre, who knows exactly what's going on.
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.5885 Shame flamed in Blake's cheeks, and for a moment he considered leaving; then he remembered Eldoria's dance, and he went right on sitting where he was. Presently the girl returned, and not long afterward the cloying scent of native incense…
- reorder_only_rag score: 0.0000
  prediction: C
  top_chunk: rank=1 score=0.5885 Shame flamed in Blake's cheeks, and for a moment he considered leaving; then he remembered Eldoria's dance, and he went right on sitting where he was. Presently the girl returned, and not long afterward the cloying scent of native incense…
- reverse_order_rag score: 0.0000
  prediction: D
  top_chunk: rank=1 score=0.5885 Shame flamed in Blake's cheeks, and for a moment he considered leaving; then he remembered Eldoria's dance, and he went right on sitting where he was. Presently the girl returned, and not long afterward the cloying scent of native incense…
- random_order_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.5885 Shame flamed in Blake's cheeks, and for a moment he considered leaving; then he remembered Eldoria's dance, and he went right on sitting where he was. Presently the girl returned, and not long afterward the cloying scent of native incense…
- anchor1_doc_order_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.5885 Shame flamed in Blake's cheeks, and for a moment he considered leaving; then he remembered Eldoria's dance, and he went right on sitting where he was. Presently the girl returned, and not long afterward the cloying scent of native incense…
- anchor2_doc_order_rag score: 0.0000
  prediction: B
  top_chunk: rank=1 score=0.5885 Shame flamed in Blake's cheeks, and for a moment he considered leaving; then he remembered Eldoria's dance, and he went right on sitting where he was. Presently the girl returned, and not long afterward the cloying scent of native incense…

#### quality / 62139_J05FWZR6_7

- query: Why was the new cook so upset that the Skipper decided to surrender? (A) He realized that if they surrendered they would be sent to concentration camps and he would no longer be able to continue cooking. (B) He realized that Skipper was more devoted to his own survival than to the Federation. (C) He spent his whole life in the Belt and he wanted to experience his first space fight. (D) He realize…
- references: He realized by surrendering, the Alliance could use their ship to sneak into Federation territory unnoticed.
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: D
  top_chunk: rank=1 score=0.4695 I stepped forward hastily. I said, "Excuse me, sir, shall I handle this?" Then, because the skipper was still struggling for words: "You," I said to the little fellow, "are a cook?" "One of the best!" he claimed complacently. "You're willi…
- reorder_only_rag score: 0.0000
  prediction: D
  top_chunk: rank=1 score=0.4695 I stepped forward hastily. I said, "Excuse me, sir, shall I handle this?" Then, because the skipper was still struggling for words: "You," I said to the little fellow, "are a cook?" "One of the best!" he claimed complacently. "You're willi…
- reverse_order_rag score: 0.0000
  prediction: C
  top_chunk: rank=1 score=0.4695 I stepped forward hastily. I said, "Excuse me, sir, shall I handle this?" Then, because the skipper was still struggling for words: "You," I said to the little fellow, "are a cook?" "One of the best!" he claimed complacently. "You're willi…
- random_order_rag score: 0.0000
  prediction: D
  top_chunk: rank=1 score=0.4695 I stepped forward hastily. I said, "Excuse me, sir, shall I handle this?" Then, because the skipper was still struggling for words: "You," I said to the little fellow, "are a cook?" "One of the best!" he claimed complacently. "You're willi…
- anchor1_doc_order_rag score: 0.0000
  prediction: D
  top_chunk: rank=1 score=0.4695 I stepped forward hastily. I said, "Excuse me, sir, shall I handle this?" Then, because the skipper was still struggling for words: "You," I said to the little fellow, "are a cook?" "One of the best!" he claimed complacently. "You're willi…
- anchor2_doc_order_rag score: 0.0000
  prediction: D
  top_chunk: rank=1 score=0.4695 I stepped forward hastily. I said, "Excuse me, sir, shall I handle this?" Then, because the skipper was still struggling for words: "You," I said to the little fellow, "are a cook?" "One of the best!" he claimed complacently. "You're willi…

### contract_nli

- examples: 50
- disagreements: 13
- any-positive-score: 37

#### contract_nli / 3_nda-15

- query: Agreement shall not grant Receiving Party any right to Confidential Information.
- references: Entailment
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.6255 The Receiving Party undertakes to permit access to the Confidential Information only to its Representatives or employees who require access to such Information solely for the fulfilment of the Permitted Purpose, and furnished on a need-to-…
- reorder_only_rag score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.6255 The Receiving Party undertakes to permit access to the Confidential Information only to its Representatives or employees who require access to such Information solely for the fulfilment of the Permitted Purpose, and furnished on a need-to-…
- reverse_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.6255 The Receiving Party undertakes to permit access to the Confidential Information only to its Representatives or employees who require access to such Information solely for the fulfilment of the Permitted Purpose, and furnished on a need-to-…
- random_order_rag score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.6255 The Receiving Party undertakes to permit access to the Confidential Information only to its Representatives or employees who require access to such Information solely for the fulfilment of the Permitted Purpose, and furnished on a need-to-…
- anchor1_doc_order_rag score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.6255 The Receiving Party undertakes to permit access to the Confidential Information only to its Representatives or employees who require access to such Information solely for the fulfilment of the Permitted Purpose, and furnished on a need-to-…
- anchor2_doc_order_rag score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.6255 The Receiving Party undertakes to permit access to the Confidential Information only to its Representatives or employees who require access to such Information solely for the fulfilment of the Permitted Purpose, and furnished on a need-to-…

#### contract_nli / 3_nda-11

- query: Receiving Party shall not reverse engineer any objects which embody Disclosing Party's Confidential Information.
- references: Entailment
- best_methods: vanilla_rag, reverse_order_rag, random_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.5490 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
- reorder_only_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5490 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
- reverse_order_rag score: 100.0000
  prediction: Entailment
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

#### contract_nli / 3_nda-2

- query: Confidential Information shall only include technical information.
- references: Contradiction
- best_methods: anchor1_doc_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5592 Definition and interpretation In this Agreement, the following terms will have the respective meanings: “Confidential Information” shall mean scientific, research, technical or business information pertaining to the Field, including but no…
- reorder_only_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5592 Definition and interpretation In this Agreement, the following terms will have the respective meanings: “Confidential Information” shall mean scientific, research, technical or business information pertaining to the Field, including but no…
- reverse_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5592 Definition and interpretation In this Agreement, the following terms will have the respective meanings: “Confidential Information” shall mean scientific, research, technical or business information pertaining to the Field, including but no…
- random_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5592 Definition and interpretation In this Agreement, the following terms will have the respective meanings: “Confidential Information” shall mean scientific, research, technical or business information pertaining to the Field, including but no…
- anchor1_doc_order_rag score: 100.0000
  prediction: Contradiction
  top_chunk: rank=1 score=0.5592 Definition and interpretation In this Agreement, the following terms will have the respective meanings: “Confidential Information” shall mean scientific, research, technical or business information pertaining to the Field, including but no…
- anchor2_doc_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.5592 Definition and interpretation In this Agreement, the following terms will have the respective meanings: “Confidential Information” shall mean scientific, research, technical or business information pertaining to the Field, including but no…

#### contract_nli / 3_nda-20

- query: Receiving Party may retain some Confidential Information even after the return or destruction of Confidential Information.
- references: Entailment
- best_methods: vanilla_rag, reorder_only_rag, reverse_order_rag, anchor1_doc_order_rag, anchor2_doc_order_rag
- disagreement: True
- vanilla_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.6587 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
- reorder_only_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.6587 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
- reverse_order_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.6587 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
- random_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.6587 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
- anchor1_doc_order_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.6587 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…
- anchor2_doc_order_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.6587 5. Return of information and property The Receiving Party acknowledges and agrees that the Confidential Information is and remains the property of the Disclosing Party. The Receiving party must, at the end of this Agreement or within seven…

#### contract_nli / 3_nda-4

- query: Receiving Party shall not use any Confidential Information for any purpose other than the purposes stated in Agreement.
- references: Entailment
- best_methods: reverse_order_rag
- disagreement: True
- vanilla_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.6021 The Receiving Party undertakes to permit access to the Confidential Information only to its Representatives or employees who require access to such Information solely for the fulfilment of the Permitted Purpose, and furnished on a need-to-…
- reorder_only_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.6021 The Receiving Party undertakes to permit access to the Confidential Information only to its Representatives or employees who require access to such Information solely for the fulfilment of the Permitted Purpose, and furnished on a need-to-…
- reverse_order_rag score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=0.6021 The Receiving Party undertakes to permit access to the Confidential Information only to its Representatives or employees who require access to such Information solely for the fulfilment of the Permitted Purpose, and furnished on a need-to-…
- random_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.6021 The Receiving Party undertakes to permit access to the Confidential Information only to its Representatives or employees who require access to such Information solely for the fulfilment of the Permitted Purpose, and furnished on a need-to-…
- anchor1_doc_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.6021 The Receiving Party undertakes to permit access to the Confidential Information only to its Representatives or employees who require access to such Information solely for the fulfilment of the Permitted Purpose, and furnished on a need-to-…
- anchor2_doc_order_rag score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=0.6021 The Receiving Party undertakes to permit access to the Confidential Information only to its Representatives or employees who require access to such Information solely for the fulfilment of the Permitted Purpose, and furnished on a need-to-…
