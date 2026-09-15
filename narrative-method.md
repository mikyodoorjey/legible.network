# Narrative map: method

Version: 2.0
Corrections window: open
Data: /data/narrative.json

## What the map is

The narrative map records how Bittensor is talked about, by whom, and how the talking changed. The core object is a narrator: a person, a foundation, or a subnet team. Each narrator's entry is built only from their own words on the record, dated and linked to the source, then read through a fixed framework so that narrators can be compared slot by slot. Across narrators the map traces metaphors: which frame appeared first, in whose mouth, who picked it up, and whether it is still in use.

It is a companion to the [Subnet Legibility Index](/). The index asks what a subnet shows a reader. The map asks what the people around the network say it is.

## Objects

| Object | What it is | Where it lives |
|---|---|---|
| Narrator | A person, institution, or subnet team with a public voice on Bittensor | one page each under /narrative/ |
| Statement | A verbatim quote of at most 60 words, dated, with a source URL, medium, and confidence | on the narrator's page and in the map |
| Source | The URL the quote was taken from, the outlet, the medium, a timestamp for audio or video, and an archive link when one exists | inside each statement |
| Slot | The framework position a statement evidences (below) | tags on each statement |
| Metaphor | A figurative frame, recorded in its exact wording and labelled in one to three words | the [metaphor index](/narrative/metaphors/) |
| Theme | A literal idea a statement carries, such as incentive design or permissionless entry | tags on each statement |
| Era | The dated phase of the network a statement falls in | tags on each statement |
| Relation | Agrees, borrows, argues, responds, introduces, from one narrator to another, backed by a statement | on the narrator's page |

## The framework

The framework is a brand strategy skeleton turned on the narrator. It does not describe Bittensor's brand. It describes this narrator's Bittensor: what they say it is for, what problem it answers, who they address, what they set it against, how they position it, what benefit they claim, what line they repeat, in what register, and what they call things.

| Section | Slots |
|---|---|
| 1. Foundation | mission, vision, values |
| 2. The problem | cultural, market, institutional |
| 3. The opportunity | tailwinds |
| 4. Audience | who they address and what they tell them |
| 5. Competitive positioning | what they set it against |
| 6. Positioning statement | category frame, differentiator, reason to believe |
| 7. Value proposition | functional, emotional, self-expressive |
| 8. Messaging hierarchy | the line they repeat, the proof they point to |
| 9. Voice | register; words used and avoided |
| 10. Narrator and network | how they describe their own relation to it |
| 11. Language conventions | terms and coinages |
| 12. Subnet frames | for subnet teams only: their subnet, and the network |

A slot is filled with a short synthesis written from the cited statements only, and every synthesis names the statements it rests on. A slot with no evidence is left out rather than filled.

## Eras

| Era | Dates | Marker |
|---|---|---|
| Whitepaper | to 2020 | before mainnet |
| Nakamoto | 2021 to early 2023 | mainnet, the Kusanagi and Nakamoto networks, no subnets |
| Finney | 2023 | the Finney network and the first subnets |
| Revolution | late 2023 to early 2025 | the Revolution upgrade, subnet expansion, the root network |
| Dynamic TAO | 2025 to mid 2026 | alpha tokens; emission follows price |
| Current | mid 2026 on | emission follows the price moving average |

## Sources, in the order a researcher looks

1. The narrator's own writing: blog, newsletter, docs, whitepaper, repositories they authored, and, for the foundation, bittensor.com and its archived captures.
2. Long-form interviews and podcasts with a transcript or a page. When only a video exists, the appearance is recorded and any quote from it is marked probable with the page the wording came from.
3. Posts on X, reached directly, through an archive, or through a mirror that returns the full primary text (the mirror is recorded as the archive link). A post reachable only through a third party's quotation is probable.
4. Talks, press interviews, and articles that quote the narrator directly. A quote in a reputable article is probable unless the primary source was reached.
5. Community writeups and paraphrases, recorded only when the wording is distinctive and nothing better exists. They never enter the map without the unverified flag.

Discord is not read. Private channels are not read. Nothing a narrator said off the record is recorded.

## Confidence

| Status | Meaning |
|---|---|
| verified | The researcher reached the primary source in the session and the words are on it |
| probable | A secondary source quotes the narrator, or the primary exists but could not be read (a video without a transcript, a post that would not render) |
| unverified | A community paraphrase or a quote with no reachable source; shown only when flagged |

Only verified and probable statements are counted in the map's totals by default. The map has a switch to include unverified statements and shows them with a red badge.

## How the research was done

Each narrator was researched by an agent working from one brief, with a cap of 40 searches and 60 fetches. The agent wrote statements verbatim with their sources, tagged them, filled the framework from those statements only, and wrote a genealogy by era citing statement ids. A validator rejects any file where a synthesis cites a statement that does not exist, a date does not match its era, a quote runs over 60 words, or a slot, era, or medium is outside the contract. The merge step joins metaphors across narrators by label and dates each one to its earliest sourced use.

Every source URL is then checked by a script before publication, and each statement carries the result: live, redirected, unreachable, or manual for hosts that cannot be checked by machine (X, Discord, Medium, the archive). A verified statement whose URL is unreachable at publication keeps its status, since the researcher reached it, but the badge says it may have moved.

The map is only as good as what could be reached. The coverage table below says, per narrator, what was found and what was not.

## Coverage

<!-- coverage:start -->
Pending.
<!-- coverage:end -->

## Corrections

A misattributed quote is removed first and argued after. Two routes:

- A [GitHub issue](https://github.com/mikyodoorjey/legible.network/issues/new?template=narrative-correction.yml) using the narrative correction form.
- Email to the address on the [about](/about/) page with the narrator, the statement id, what is wrong, and the URL of the primary source.

What qualifies: a quote whose wording differs from the source, a wrong date, a wrong speaker, a source that does not say what the entry says it says, a missing primary that would upgrade a probable statement, or a public statement the map should carry. What does not: an argument that a narrator meant something other than what they said. The map records the words; the reading is the reader's.

## Limits

Transcripts of podcasts and videos are often machine generated, and a quote from one carries that transcript's errors; the transcript kind is recorded on every statement. Posts on X frequently fail to fetch, and much of the early network's talk happened on Discord, which is not read. Statements were collected in English. The map is a sample of what could be reached in a bounded session, not a census of everything said. Absence from the map is not evidence of silence.

## Cite

Bittensor Narrative Map, version 2.0, Mikyö Clark, legible.network, 2026. Data is licensed CC BY 4.0; the code is MIT.
