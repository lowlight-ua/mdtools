The following should not be treated as anchors:

<b name="lorem">
```<a name="lorem"></a>```
`<a name="lorem"></a>`

<a name=auctor mauris></a>

# Donec: laoreet! Magna.

[Only first word of the anchor should be matched. This link is OK](#auctor)

[Anchor not found. Anchor is in the file in directory above](#lorem)
[Anchor not found. File is in directory above](#fusce)
[Anchor not found. File is in directory below](#malesuada)
[Anchor not found. File is in directory below](<#vulpu tate>)
[Anchor not found. File is in directory down then up](#tempus)
[Anchor not found. File is in directory down then up](#scelerisque) <- Not auto-fixable, because there are two options
[Anchor not found. File is in root directory](#dolor) <- Not auto-fixable, because relative link exceeds "maximum directories down

[Link to heading in this file. OK](#donec-laoreet-magna)

[Anchor not found. Heading is in the file in directory above](#mauris-convallis-ornare)
[Anchor not found. Heading is in the file in directory below](#commodo-nisi-aliquet)