from fixmefinder.entry import Location, Position

def test_location():
    loc = Location(file="foo.py", start=Position(line=1, column=2), end=Position(line=3, column=4))
    assert loc.file == "foo.py"
    assert loc.start.line == 1
    assert loc.start.column == 2
    assert loc.end.line == 3
    assert loc.end.column == 4

def test_location_str():
    loc = Location(file="foo.py", start=Position(line=1, column=2), end=Position(line=3, column=4))
    assert str(loc) == "foo.py:1:2:3:4"