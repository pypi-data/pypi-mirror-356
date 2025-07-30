from fixmefinder.entry import Entry, Location, Position

location = Location(
    file="foo.py",
    start=Position(line=1, column=2),
    end=Position(line=3, column=4),
)

def test_entry():
    entry = Entry(type="TODO", text="foo", location=location)
    assert entry.type == "TODO"
    assert entry.text == "foo"
    assert entry.issue_tracker_id is None
    assert entry.location == location

def test_entry_format():
    entry = Entry(type="TODO", text="foo", location=location)
    assert entry.format() == "# TODO: foo"

def test_entry_with_issue_tracker_id():
    entry = Entry(type="FIXME", text="bar", location=location, issue_tracker_id="123")
    assert entry.type == "FIXME"
    assert entry.text == "bar"
    assert entry.issue_tracker_id == "123"
    assert entry.format() == "# FIXME: (123) bar"
