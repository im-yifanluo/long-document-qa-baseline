# Comparison Report

Run tier: `subset`

## Score Summary

| Task | Metric | raptor |
| --- | --- | --- |
| qasper | f1 | 56.2477 |
| narrative_qa | f1 | 11.4620 |
| quality | exact_match | 66.6667 |
| contract_nli | exact_match | 80.0000 |

## Example Previews

### qasper

- examples: 15
- disagreements: 0
- any-positive-score: 12

#### qasper / 2df4a045a9cd7b44874340b6fdf9308d3c55327a

- query: What crowdsourcing platform is used?
- references: Unanswerable | They did not use any platform, instead they hired undergraduate students to do the annotation.
- best_methods: raptor
- disagreement: False
- raptor score: 0.0000
  prediction: Amazon Mechanical Turk
  top_chunk: rank=1 score=n/a In recent years, a series of work have focused on how to use crowdsourcing data efficiently in tasks such as classification BIBREF19 , BIBREF20 , and compare quality of crowd and expert labels BIBREF21

#### qasper / a313e98994fc039a82aa2447c411dda92c65a470

- query: How do they match words before reordering them?
- references: Unanswerable | CFILT-preorder system
- best_methods: raptor
- disagreement: False
- raptor score: 0.0000
  prediction: using a bilingual dictionary (Google Translate word translation in our case)
  top_chunk: rank=1 score=n/a For representing English and other source languages into a common space, we translate each word in the source language into English using a bilingual dictionary (Google Translate word translation in our case) In an end-to-end solution, it…

#### qasper / b5e4866f0685299f1d7af267bbcc4afe2aab806f

- query: what is the source of the news sentences?
- references: ilur.am | links between Wikipedia articles to generate sequences of named-entity annotated tokens
- best_methods: raptor
- disagreement: False
- raptor score: 0.0000
  prediction: over a dozen Armenian news websites and blogs
  top_chunk: rank=1 score=n/a which is likely caused by the inconsistent style of linking in Armenian Wikipedia (in the article ԱՄՆ մշակույթ (Culture of the United States)

#### qasper / b6ae8e10c6a0d34c834f18f66ab730b670fb528c

- query: what are the topics pulled from Reddit?
- references: politics, business, science, and AskReddit, and 1000 additional posts from the Reddit frontpage. | training data has posts from politics, business, science and other popular topics; the trained model is applied to millions of unannotated posts on all of Reddit
- best_methods: raptor
- disagreement: False
- raptor score: 18.6047
  prediction: topics such as abortion or climate change, to world news and relationship advice, to the future of artificial intelligence
  top_chunk: rank=1 score=n/a We train a predictive model to classify dogmatic posts from Reddit, one of the most popular discussion communities on the web Posts on Reddit capture discussion and debate across a diverse set of domains and topics – users talk about every…

#### qasper / 9eabb54c2408dac24f00f92cf1061258c7ea2e1a

- query: Which information about text structure is included in the corpus?
- references: paragraphs, lines, Information on physical page segmentation (for PDFs only), paragraph segmentation, and line segmentation | paragraph, lines, textspan element (paragraph segmentation, line segmentation, Information on physical page segmentation(for PDF only))
- best_methods: raptor
- disagreement: False
- raptor score: 34.7826
  prediction: Information on text structure (e g , paragraphs, lines)
  top_chunk: rank=1 score=n/a The remainder of this paper is structured as follows: Section SECREF2 presents previous corpora used for automatic readability assessment and text simplification Section SECREF3 describes our corpus, introducing its novel aspects and prese…

### narrative_qa

- examples: 15
- disagreements: 0
- any-positive-score: 3

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_0

- query: Which character comes from Bangor, Maine?
- references: Miranda Hope.
- best_methods: raptor
- disagreement: False
- raptor score: 0.0000
  prediction: The narrator comes from Bangor, Maine.
  top_chunk: rank=1 score=n/a I never supposed, when I left Bangor, that I was coming to Europe to learn _English_ If I do learn it, I don't think you will understand me when I get back, and I don't think you'll like it much I should be a good deal criticised if I spok…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_1

- query: Where is the boarding-house located?
- references: Paris
- best_methods: raptor
- disagreement: False
- raptor score: 0.0000
  prediction: Boulevard Haussman
  top_chunk: rank=1 score=n/a I came here to stay about three days ago, and by this time I have seen a great deal of them The price of board struck me as rather high; but I must remember that a quantity of conversation is thrown in I have a very pretty little room--wit…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_11

- query: Where is Violet Ray from?
- references: New York
- best_methods: raptor
- disagreement: False
- raptor score: 0.0000
  prediction: Bangor
  top_chunk: rank=1 score=n/a wide open; skirting the edge of obscene abysses without suspecting them; pushing through brambles without tearing her robe; exciting, without knowing it, the most injurious suspicions; and always holding her course, passionless, stainless,…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_12

- query: Where is Herr professor from?
- references: Germany
- best_methods: raptor
- disagreement: False
- raptor score: 0.0000
  prediction: Göttingen
  top_chunk: rank=1 score=n/a credit of his native country; little perceiving the truly sinister impression it made upon me ) What strikes one in it is that it is a phenomenon to the best of my knowledge--and you know what my knowledge is--unprecedented and unique in t…

#### narrative_qa / 8cb9a3afd8d542c798c3a34fd1a9afa0a77931c2_13

- query: Where is Leon Verdier from?
- references: France
- best_methods: raptor
- disagreement: False
- raptor score: 0.0000
  prediction: French
  top_chunk: rank=1 score=n/a credit of his native country; little perceiving the truly sinister impression it made upon me ) What strikes one in it is that it is a phenomenon to the best of my knowledge--and you know what my knowledge is--unprecedented and unique in t…

### quality

- examples: 15
- disagreements: 0
- any-positive-score: 10

#### quality / 30029_F5N22U40_3

- query: How was Korvin able to avoid disclosing the true intent of his mission under the lie detector questioning? (A) While he was strapped down in the lie-detector, Korvin subtly switched the wire that indicated a truth with the one that indicated a lie. (B) Korvin said truths that literally answered the Tr'en's questions but evaded the intent behind their questions. . (C) The Tr'en hadn't tested the l…
- references: Korvin said truths that literally answered the Tr'en's questions but evaded the intent behind their questions. .
- best_methods: raptor
- disagreement: False
- raptor score: 0.0000
  prediction: B Korvin said truths that literally answered the Tr'en's questions but evaded the intent behind their questions.
  top_chunk: rank=1 score=n/a Korvin, a captive strapped to a lie-detector, faces the Ruler and Tr'en guards. The Ruler, assured by their experts in logic (referred to as "right-saying"), believes they can't be tricked. These experts arrive and assert their capability…

#### quality / 30029_F5N22U40_6

- query: Are there indications that the Tr'en would be interested in attacking Earth? Why or why not? (A) Both A and C are correct. (B) No, because Korvin sends a mission back to Earth Central saying that the Tr'en won't come marauding out into space. (C) Yes, because the expert mentions the idea of conquering Earth with Korvin's aid. (D) Yes, because the ruler says the he wants to know about Earth's weap…
- references: Yes, because the ruler says the he wants to know about Earth's weapons, plans, and fortifications.
- best_methods: raptor
- disagreement: False
- raptor score: 0.0000
  prediction: No, because Korvin sends a mission back to Earth Central saying that the Tr'en won't come marauding out into space.
  top_chunk: rank=1 score=n/a But, after all, the Tr'en knew their business, better than anyone else could know it They had the technique and the logic and the training He hoped they were right The Ruler was frowning at him Korvin did his best to look receptive "Why di…

#### quality / 52845_75VB1ISR_2

- query: Why does Deirdre get so upset when Blake Past suggests she go to prom with the young man? (A) Because Blake is trying to guilt Deirdre into going with the young man by telling her that it'll ease her conscience. (B) Because Deirdre has fallen in love with Blake, despite his age, and wants him to take her to the prom. (C) Because Blake is acting like he's her father, which is a sensitive topic for…
- references: Because Deirdre has fallen in love with Blake, despite his age, and wants him to take her to the prom.
- best_methods: raptor
- disagreement: False
- raptor score: 0.0000
  prediction: Because Blake is acting like he's her father, which is a sensitive topic for Deirdre because she lost her real parents.
  top_chunk: rank=1 score=n/a Blake, observing a dance, is captivated by a woman who joins him after the dance, ordering Martian wine with sophistication. She asks if he wants a night, and Blake agrees, but she demands three thousand quandoes. Meanwhile, Blake Past, li…

#### quality / 52845_75VB1ISR_3

- query: Why does shame flame in Blake's cheeks when Deirdre goes to prepare Eldoria's dias? (A) He is embarrassed at the thought that Deirdre might enter the room while he is sleeping with Eldoria. (B) He feels that prostitution is morally reprehensible. (C) He feels guilty about sleeping with Eldoria when there's a child in the hut, Deirdre, who knows exactly what's going on. (D) He feels guilty about w…
- references: He feels guilty about sleeping with Eldoria when there's a child in the hut, Deirdre, who knows exactly what's going on.
- best_methods: raptor
- disagreement: False
- raptor score: 0.0000
  prediction: He feels that prostitution is morally reprehensible.
  top_chunk: rank=1 score=n/a "Nathan," Blake said "Nathan Blake " "Eldoria will be arriving soon I must go and prepare her dais " She got up, parted the arras, and slipped into the next room Shame flamed in Blake's cheeks, and for a moment he considered leaving; then…

#### quality / 52845_75VB1ISR_4

- query: Why did Blake create the three female super-images of Miss Stoddart, Officer Finch, and Vera Velvetskin? (A) He feels guilty about having slept with Eldoria which perpetuated the demand for female prostitution. (B) Even though he is a psycheye, he feels guilty about hunting down Sabrina York. (C) He is still grieving his mother's death and regrets not being a more loving son. (D) He feels guilty…
- references: He feels guilty about hurting Deirdre's feelings after her graduation when he ignored their romantic connection, and instead, played the part of a parent.
- best_methods: raptor
- disagreement: False
- raptor score: 0.0000
  prediction: D He feels guilty about hurting Deirdre's feelings after her graduation when he ignored their romantic connection, and instead, played the part of a parent.
  top_chunk: rank=1 score=n/a that Blake was less well-adjusted than he considered himself to be, why had he created three such malevolent super-images as Miss Stoddart, Officer Finch, and Vera Velvetskin They followed him off the campus into a vicarious memory-image o…

### contract_nli

- examples: 15
- disagreements: 0
- any-positive-score: 12

#### contract_nli / 3_nda-13

- query: Receiving Party may acquire information similar to Confidential Information from a third party.
- references: Entailment
- best_methods: raptor
- disagreement: False
- raptor score: 0.0000
  prediction: Not mentioned
  top_chunk: rank=1 score=n/a The Receiving Party undertakes to permit access to the Confidential Information only to its Representatives or employees who require access to such Information solely for the fulfilment of the Permitted Purpose, and furnished on a need-to-…

#### contract_nli / 3_nda-7

- query: Receiving Party may share some Confidential Information with some third-parties (including consultants, agents and professional advisors).
- references: Entailment
- best_methods: raptor
- disagreement: False
- raptor score: 0.0000
  prediction: Contradiction
  top_chunk: rank=1 score=n/a a) To take proper and reasonable measures to ensure the secrecy of the Confidential Information; b) Not to disclose, or allow it to be disclosed, in whole or in part to any third party without the prior written consent of the Disclosing Pa…

#### contract_nli / 3_nda-8

- query: Receiving Party shall notify Disclosing Party in case Receiving Party is required by law, regulation or judicial process to disclose any Confidential Information.
- references: Not mentioned
- best_methods: raptor
- disagreement: False
- raptor score: 0.0000
  prediction: Entailment
  top_chunk: rank=1 score=n/a The Receiving Party undertakes to permit access to the Confidential Information only to its Representatives or employees who require access to such Information solely for the fulfilment of the Permitted Purpose, and furnished on a need-to-…

#### contract_nli / 3_nda-1

- query: All Confidential Information shall be expressly identified by the Disclosing Party.
- references: Entailment
- best_methods: raptor
- disagreement: False
- raptor score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=n/a a) To take proper and reasonable measures to ensure the secrecy of the Confidential Information; b) Not to disclose, or allow it to be disclosed, in whole or in part to any third party without the prior written consent of the Disclosing Pa…

#### contract_nli / 3_nda-10

- query: Receiving Party shall not disclose the fact that Agreement was agreed or negotiated.
- references: Entailment
- best_methods: raptor
- disagreement: False
- raptor score: 100.0000
  prediction: Entailment
  top_chunk: rank=1 score=n/a The Receiving Party undertakes to permit access to the Confidential Information only to its Representatives or employees who require access to such Information solely for the fulfilment of the Permitted Purpose, and furnished on a need-to-…
