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
- Attribute "type" can be added to the quote tag with the value "possiblyauthorial". This indicates that a verse or series of verses appears similar to a quote, but may be composed by the author himself. 
- Attribute "authorid2" can be used if a single qutation is given with multiple authors: e.g., author gives the Bhagavān and Nāgārjuna as sources.

### Edge Cases
- Author and generic title in a single compound with vocalic sandhi in between: <author id="a1">lūyīpādā</author><title id="t3" type="generic">bhisamaye</title>
- Commentary with a root text emded.
- Some verses in prose are probably authorial but we can't be certain.
- Sometimes an opponent's position is phrased as him speaking, but it does not correspond to an actual quote: it is a kind of paraphrase.
- Mokṣākaragupta, for example, frequently cites the Nyāyabindu, and it is probably known to his readers, but he does not mark this in any way.
