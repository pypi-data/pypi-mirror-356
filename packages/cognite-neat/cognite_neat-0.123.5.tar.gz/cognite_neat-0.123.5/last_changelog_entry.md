
### Fixed

- If there are multiple indices on one property Neat no longer raises an
error when reading the spreadsheet. For example,
`btree:code(cursorable=True),btree:standard(cursorable=True,order=1)` in
the Index column no longer raise an error.