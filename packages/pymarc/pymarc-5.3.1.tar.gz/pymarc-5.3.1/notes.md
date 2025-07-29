This release adds a new `fields` parameter to the Record constructor, which lets you pass in a list of Fields (so you don't have to add them later with `add_field()`:

```python
record = Record(
    fields=[
        Field(
            tag="245",
            indicators=Indicators("1", "0"),
            subfields=[
                Subfield(code="a", value="Python"),
                Subfield(code="c", value="Guido"),
            ],
        ),
        Field(
            tag="260",
            subfields=[
                Subfield(code="a", value="Amsterdam")
            ]
        ),
    ]
)
```

It also includes some code simplification and cleanup, and the replacement of black and flake8 with [ruff](https://docs.astral.sh/ruff/).
