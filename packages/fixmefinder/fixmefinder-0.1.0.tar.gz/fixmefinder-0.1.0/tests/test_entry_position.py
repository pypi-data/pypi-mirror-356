from fixmefinder.entry import Position

def test_position():
    pos = Position(line=1, column=2)
    assert pos.line == 1
    assert pos.column == 2

def test_position_str():
    pos = Position(line=1, column=2)
    assert str(pos) == "1:2"
