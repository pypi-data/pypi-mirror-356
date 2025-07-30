# The rationale for Wrappity

**TL;DR**: I frequently work with complex jsons and became so much annoyed with doing all the explicit checks to safely get the leaf values from the jsons so that I decided to handle this in a library.

## Processing someone else's input

Json data has become a de-facto standard for sharing all kinds of structures over the internet. Unlike XML, which traditionaly relied on strong document structure definition and enforcement (see [DTDs](https://en.wikipedia.org/wiki/Document_type_definition), [XSDs](https://en.wikipedia.org/wiki/XML_Schema_(W3C)), etc.), [JSON schema](https://json-schema.org) and similar initiatives are less prevalent.

This means that we can less rely on knowing which combinations (or ommisions) of data we can encounter when processing such data - what kind of variants we can - or would not need to - expect.

As a result we are forced into defensive coding where without knowing the schema of the document we're processing we better check every single part of the path we're accessing to avoid unexpected Exceptions (_everyone loves getting `KeyErrors` and `IndexErrors` for yet another part you forgot to check_).

It's proper, it's robust and we should do that - but it's also tedious, boilerplatey and makes the code less readable (_esp. if you're only a mediocre coder like I am_).

### Enter Wrappity

The main idea for Wrappity was:
- What if I could just go all the way deep into my datastructure and grab the leaf value - and if it's not there, it's ok to get `None` - I have a backup solution in such case, and I don't really care about anything else.

## Error handling in a different way


