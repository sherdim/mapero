# Author: Zacarias F. Ojeda <zojeda@gmail.com>
# License: new BSD Style.


def round_rect(gc, radio=5, position=[100,100], bounds=[100,60], inset=3):
    dx, dy = bounds
    x, y = position
    x+=inset
    y+=inset
    dx-=2*inset
    dy-=2*inset
    gc.move_to( x+radio, y+dy)
    gc.line_to( x+dx-radio, y+dy)
    gc.arc_to( x+dx, y+dy, x+dx, y+dy-radio, radio )
    gc.line_to( x+dx, y+radio)
    gc.arc_to(x+dx, y, x+dx-radio, y, radio)
    gc.line_to( x+radio, y)
    gc.arc_to( x, y, x, y+radio, radio)
    gc.line_to( x, y+dy-radio )
    gc.arc_to( x, y+dy, x+radio, y+dy, radio)
