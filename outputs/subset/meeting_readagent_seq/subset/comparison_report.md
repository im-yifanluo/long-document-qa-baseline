# Comparison Report

Run tier: `subset`

## Score Summary

| Task | Metric | read_agent_sequential |
| --- | --- | --- |
| qmsum | rouge | 17.0942 |
| narrative_qa | f1 | 12.8219 |
| quality | exact_match | 70.0000 |

## Example Previews

### qmsum

- examples: 50
- disagreements: 0
- any-positive-score: 50

#### qmsum / va-sq-4

- query: What was the future of data collection?
- references: The group aims to collect over 100 hours of Meeting Recorder data in total. Speaker consent forms are being revised. It was suggested that subjects should sign a new consent form after 10 recording sessions.
- best_methods: read_agent_sequential
- disagreement: False
- read_agent_sequential score: 4.5750
  prediction: The future of data collection involved several strategies: 1. **Expanding Recording Sessions**: The team planned to continue recording meetings at their institution, aiming to gather more data. They expected to collect three to four hours of recordings per week, with the goal of reaching a hundred hours over a few months. 2. **Exploring Additional Data Sources**: They considered recording meeting…
  top_chunk: rank=1 score=n/a Grad G: and , they sort of hummed and hawed and said " well maybe we could have meetings down here " , but then I got email from them that said " no , we decided we 're not really interested and we don't wanna come down and hold meetings .…

#### qmsum / va-sq-46

- query: What were the problems encountered with SmartKom system?
- references: The translation of SmartKom to english is in its final stages. The synthesis module will be the last one to do, after the english syntax trees are completed. The system is still buggy and unstable, but it will soon be ready for a demonstration.
- best_methods: read_agent_sequential
- disagreement: False
- read_agent_sequential score: 5.6031
  prediction: The SmartKom system encountered several issues as described in the text: 1. **Synthesis Module Issues**: There was a problem with the synthesis module, which was fixable by exchanging a few files since they were using the concept-to-speech approach. The phrase "Roman numeral one, am Smarticus" was mentioned as an example of an issue with the German synthesis module for English sentences. 2. **Bri…
  top_chunk: rank=1 score=n/a Grad E: And because we 're sticking to that structure , the synthesis module doesn't need to be changed . So all that f fancy stuff , and the Texas speech version of it , which is actually the simpler version , is gonna be done in October…

#### qmsum / va-sq-2

- query: What was said on speech overlap?
- references: Efforts by speaker mn005 are in progress to detect overlapping speech. For a single transcribed meeting, speaker mn005 reported approximately 300 cases of overlap. Future work will involve manually deriving time marks from sections of overlapping speech for the same meeting, and then experimenting with different measures, e.g. energy increase, to determine a set of acoustically salient features f…
- best_methods: read_agent_sequential
- disagreement: False
- read_agent_sequential score: 7.3200
  prediction: The context discusses several points related to speech overlap: 1. PhD D found almost three hundred speech overlaps in a forty-five-minute session. 2. The group discussed how to define an overlap event. PhD D considers an overlap event as any moment where there is more than one voice, including background noise, without distinguishing between the number of speakers. 3. There was a discussion on t…
  top_chunk: rank=1 score=n/a Postdoc B: For Grad G: So let 's say me and Jane are talking at the same time , and then Liz starts talking also over all of us . How many events would that be ? PhD D: So - I don't understand . Grad G: So , two people are talking , {comme…

#### qmsum / va-sq-47

- query: What demos would the system be involved in?
- references: The final english SmartKom demo will be presented to the whole institute once the system is de-bugged and stabilised.
- best_methods: read_agent_sequential
- disagreement: False
- read_agent_sequential score: 7.5478
  prediction: The system would be involved in internal demos where team members can showcase their work and progress, potentially explaining SmartKom to others within the institute. There's also a suggestion to set up a demo as an institute-wide event where the team can present a demo version of the project to a broader audience. Additionally, the group is thinking about future demos over the next six months,…
  top_chunk: rank=1 score=n/a Professor C: So , c sh we could set that up as actually an institute wide thing ? Just give a talk in the big room , and {disfmarker} and so peo people know what 's going on ? when you 're ready ? Grad E: Absolutely . Professor C: Yeah I m…

#### qmsum / va-gq-5

- query: What were the main discussion points of the meeting?
- references: The group discussed topics including a potential collaboration with another ICSI member regarding the analysis of inference structures, efforts by speaker mn005 to detect speaker overlap, the current status of recordings and transcriptions, and future efforts to collect meeting data. In addition to weekly meetings by the BMR group, efforts are in progress to record meetings by other ICSI research…
- best_methods: read_agent_sequential
- disagreement: False
- read_agent_sequential score: 8.8691
  prediction: The main discussion points of the meeting were: 1. **Technical Issues and Solutions**: The group discussed a technical issue with a system that was crashing when started and stopped repeatedly. They also talked about the initialization process and how to avoid causing crashes. 2. **Data Collection and Transcription**: There was a discussion about the process of collecting and transcribing data, i…
  top_chunk: rank=1 score=n/a Professor E: So . OK . Doesn't look like it crashed . That 's great . Grad G: So I think maybe what 's causing it to crash is I keep starting it and then stopping it to see if it 's working . And so I think starting it and then stopping it…

### narrative_qa

- examples: 50
- disagreements: 0
- any-positive-score: 11

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_1

- query: Where is the boarding-house located?
- references: Paris
- best_methods: read_agent_sequential
- disagreement: False
- read_agent_sequential score: 0.0000
  prediction: Boulevard Haussman
  top_chunk: rank=1 score=n/a You know I have always been intensely interested in Balzac, who never shrank from the reality, and whose almost _lurid_ pictures of Parisian life have often haunted me in my wanderings through the old wicked-looking streets on the other si…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_13

- query: Where is Leon Verdier from?
- references: France
- best_methods: read_agent_sequential
- disagreement: False
- read_agent_sequential score: 0.0000
  prediction: Paris
  top_chunk: rank=1 score=n/a You expected, perhaps, I was going to tell you that I had made my fortune, or that the Uncle Blondeau had at last decided to return into the breast of nature, after having constituted me his universal legatee. But I needn't remind you that…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_16

- query: What is William Platt's relationship to Miranda Hope?
- references: Platt is a Miranda's suitor | a previous suitor
- best_methods: read_agent_sequential
- disagreement: False
- read_agent_sequential score: 0.0000
  prediction: unclear from the context provided

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_17

- query: What name does Herr Professor call Leon?
- references: Simian
- best_methods: read_agent_sequential
- disagreement: False
- read_agent_sequential score: 0.0000
  prediction: Herr Professor does not call Leon by any specific name in the given text.

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_18

- query: Which traveler finds the other travelers "sub-human"?
- references: Herr Professor
- best_methods: read_agent_sequential
- disagreement: False
- read_agent_sequential score: 0.0000
  prediction: Dr. Rudolf Staub
  top_chunk: rank=1 score=n/a I mentioned to you before that my expectation of rough usage, in consequence of my German nationality, had proved completely unfounded. No one seems to know or to care what my nationality is, and I am treated, on the contrary, with the civ…

### quality

- examples: 50
- disagreements: 0
- any-positive-score: 35

#### quality / 30029_F5N22U40_2

- query: Why does the text mean when it says that Korvin was "unconscious" at the time of his lessons in the local language? (A) It means that the Tr'en put Korvin under drug hypnosis while they taught him their language. (B) It means that he was so bored out of his mind during the language lessons that he was hardly conscious. (C) It means that the Tr'en came into Korvin's cell while he slept in order to…
- references: It means that the Tr'en put Korvin under drug hypnosis while they taught him their language.
- best_methods: read_agent_sequential
- disagreement: False
- read_agent_sequential score: 0.0000
  prediction: It means that the Tr'en came into Korvin's cell while he slept in order to use their advanced technology which quickly teaches the unconscious mind.
  top_chunk: rank=1 score=n/a LOST IN TRANSLATION By LARRY M. HARRIS In language translation, you may get a literally accurate word-for-word translation ... but miss the meaning entirely. And in space-type translation ... the effect may be the same! Illustrated by Scho…

#### quality / 30029_F5N22U40_7

- query: The text says "The expert frowned horribly." What makes the expert's smile so horrible? (A) The frown indicates that he's close to detecting Korvin's true motivations. (B) The frown indicates that he knows that Korvin switched the wires on the lie detector. (C) The frown is a signal to the Ruler that Korvin is lying. (D) The frown is physically horrible because the Tr'en have fifty-eight, pointed…
- references: The frown is physically horrible because the Tr'en have fifty-eight, pointed teeth.
- best_methods: read_agent_sequential
- disagreement: False
- read_agent_sequential score: 0.0000
  prediction: The frown indicates that he's close to detecting Korvin's true motivations.

#### quality / 30029_F5N22U40_8

- query: How did the Ruler become the Ruler? (A) He was adopted by the previous Ruler. (B) He overthrew the previous Ruler. (C) He is the biological son of the previous Ruler. (D) He was elected as Ruler by the Tr'en.
- references: He was adopted by the previous Ruler.
- best_methods: read_agent_sequential
- disagreement: False
- read_agent_sequential score: 0.0000
  prediction: Such is his command.
  top_chunk: rank=1 score=n/a It wasn't quite "talk"; that was a general word in the Tr'en language, and Didyak had used a specific meaning, roughly: "gain information from, by peaceful and vocal means." Korvin filed it away for future reference. "Why did the Ruler not…

#### quality / 52845_75VB1ISR_2

- query: Why does Deirdre get so upset when Blake Past suggests she go to prom with the young man? (A) Because Blake is trying to guilt Deirdre into going with the young man by telling her that it'll ease her conscience. (B) Because Deirdre has fallen in love with Blake, despite his age, and wants him to take her to the prom. (C) Because Blake is acting like he's her father, which is a sensitive topic for…
- references: Because Deirdre has fallen in love with Blake, despite his age, and wants him to take her to the prom.
- best_methods: read_agent_sequential
- disagreement: False
- read_agent_sequential score: 0.0000
  prediction: Because Blake is acting like he's her father, which is a sensitive topic for Deirdre because she lost her real parents.
  top_chunk: rank=1 score=n/a Deirdre was speaking. "Yes," she was saying, "at nine o'clock. And I should very much like for you to come." Blake Past shook his head. "Proms aren't for parents. You know that as well as I do. That young man you were talking with a few mi…

#### quality / 52845_75VB1ISR_3

- query: Why does shame flame in Blake's cheeks when Deirdre goes to prepare Eldoria's dias? (A) He is embarrassed at the thought that Deirdre might enter the room while he is sleeping with Eldoria. (B) He feels that prostitution is morally reprehensible. (C) He feels guilty about sleeping with Eldoria when there's a child in the hut, Deirdre, who knows exactly what's going on. (D) He feels guilty about w…
- references: He feels guilty about sleeping with Eldoria when there's a child in the hut, Deirdre, who knows exactly what's going on.
- best_methods: read_agent_sequential
- disagreement: False
- read_agent_sequential score: 0.0000
  prediction: He feels that prostitution is morally reprehensible.
  top_chunk: rank=1 score=n/a She laughed. "I am here because I live here," she said. He tried to assimilate the information, but could not. Perceiving his difficulty, the girl went on, "My parents indentured themselves to the Great Starway Cartel and were assigned to…
