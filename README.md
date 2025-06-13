# Sanskrit Citation Identification

This repo contains annotated data for identification citations within Sanskrit texts.

### Markup pattern:

- Three hyphens (---) indicates a new prompt
- `<quote>...</quote>` identifies direct citation
- `<author>...</author>` indicates author's name or epithet.
- `<title>...</title>` identifies the title of a text.
- Each tag is given a unique ID attribute. e.g. '<quote id="q1">...</quote>'
- Authors and titles are connected to quotes by this ID and the attribute 'authorid' or 'titleid'. e.g., <quote id="q1" authorid="a1" titleid="t1">...</quote>.
- Attribute "type" can also be added to the title: possible values are generic, 

### Edge Cases
Author and generic title in a single compound with vocalic sandhi in between: <author id="a1">lūyīpādā</author><title id="t3" type="generic">bhisamaye</title>
