<a name="Vivamus"></a>
<a name= "viverra" ></a>
<a id=risus></a>

[Correct link](#Vivamus)
[Correct link](#viverra)
[Correct link](#risus)

> [Target not found. File is in directory above](Neque.md)
[Target not found. File is in directory above](porro.md)
[Target not found. File is in directory below](<Suspen disse.md>)
[Target not found. File is in directory below](feugiat.md)
[Target not found. File is in directory down then up](hendrerit.md)
[Target not found. File is in root directory](root.md) <- Not auto-fixable, because relative link exceeds "maximum directories down
[Target not found. File is both in up and down directory](Aenean.md) <- Not auto-fixable: two options

> [Target not found. File is in directory above](../bogus/Neque.md)
[Target not found. File is in directory above](../bogus/porro.md)
[Target not found. File is in directory below](<../bogus/Suspen disse.md>)
[Target not found. File is in directory below](../bogus/feugiat.md)
[Target not found. File is in directory down then up](../bogus/hendrerit.md)
[Target not found. File is in root directory](../bogus/root.md)  <- Not auto-fixable, because relative link exceeds "maximum directories down
[Target not found. File is both in up and down directory](../bogus/Aenean.md) <- Not auto-fixable: two options
[Should not trip the script](../../../../../../../../../../../../../../../../../../../../Neque.md)

> [Target not found. File is in directory above](/fake/Neque.md)
[Target not found. File is in directory above](/fake/porro.md)
[Target not found. File is in directory below](</fake/Suspen disse.md>)
[Target not found. File is in directory below](/fake/feugiat.md)
[Target not found. File is in directory below](/fake/hendrerit.md)
[Target not found. File is in root directory](/fake/root.md)
[Target not found. File is both in up and down directory](/fake/Aenean.md) <- Not auto-fixable: two options


[Must be ignored](https://google.com)
[Must be ignored](file:///C/root.md)
[Must be ignored](email:root@root.md)


``` [Must be ignored](porro.md) ```