# Sanskrit Citation Identification

This repo contains annotated data for identification citations within Sanskrit texts.

### Markup pattern:

- Three hyphens (---) indicates a new prompt
- `<quote>...</quote>` identifies direct citation
- `<author>...</author>` indicates author's name or epithet.
- `<title>...</title>` identifies the title of a text.
- Each tag is given a unique ID attribute. e.g. '<quote id="q1">...</quote>'
- IDs given as ROOT mean that the citation comes later or earlier within the root text of the commentary.
- Authors and titles are connected to quotes by this ID and the attribute 'authorid' or 'titleid'. e.g., <quote id="q1" authorid="a1" titleid="t1">...</quote>.
- Attribute "type" can be added to the title: possible values are generic, chapter, 
- Attribute "type" can be added to the author: value includes 'speaker' where the author of the overall text cited is otherwise but the speaker of the passage cited is different (e.g., a bodhisattva being the speaker in a sūṭra).

### Edge Cases
- Author and generic title in a single compound with vocalic sandhi in between: <author id="a1">lūyīpādā</author><title id="t3" type="generic">bhisamaye</title>
- At least one case has two authors: <quote id="q1" titleid="t1" authorid="a1" authorid="a2">. Here a1 is attributed with t1, but a2 wrote the citation in a different text.
- Commentary with a root text emded.
