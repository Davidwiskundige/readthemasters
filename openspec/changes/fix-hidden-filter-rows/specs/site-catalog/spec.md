## ADDED Requirements

### Requirement: A filtered-out row is not rendered

Every client-side filter on the site SHALL remove the rows it excludes from the rendered list, not
merely mark them. The number of rows a visitor can see MUST equal the number the live count states,
on the catalog (`/`), the author index (`/authors/`) and the journal index (`/journals/`) alike, at
every viewport width.

This holds however a row is hidden. The implementation is free to use the `hidden` attribute, a
class, or removal from the DOM — but whichever it uses MUST survive the layout rules that page's
rows carry. A row styled with its own `display` rule (a flex card seating a portrait, a title-led
journal row) MUST still disappear when the filter excludes it: the `hidden` attribute alone does
not guarantee this, because a user-agent `[hidden]` rule loses to any author `display` rule.

#### Scenario: The catalog shows only the works it counts

- **WHEN** a visitor narrows the catalog with any facet, the free-text box, or the year range, and the count reads "N of M works"
- **THEN** exactly N cards are rendered and M − N are gone from the page — none of them occupying space, painting, or receiving a click

#### Scenario: A card with a portrait disappears when filtered out

- **WHEN** a catalog card excluded by the filter is one carrying an author portrait, at either the desktop or the phone layout
- **THEN** the whole card — portrait box included — is removed from the rendered list, at both widths, even though its layout rule sets a `display` value in each

#### Scenario: The author and journal indexes filter their rows too

- **WHEN** a visitor types in the author index's name/bio search box, or the journal index's journal search box
- **THEN** only the matching rows remain rendered, the live count matches the number visible, and the empty-state message appears when nothing matches

#### Scenario: A newly added filtered list inherits the guarantee

- **WHEN** a later change adds a list whose rows carry their own `display` rule and filters it client-side
- **THEN** its excluded rows disappear without that change having to add a rule of its own for them
