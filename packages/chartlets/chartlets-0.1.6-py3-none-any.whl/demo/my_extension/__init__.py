from chartlets import Extension
from .my_panel_1 import panel as my_panel_1
from .my_panel_2 import panel as my_panel_2
from .my_panel_3 import panel as my_panel_3
from .my_panel_4 import panel as my_panel_4
from .my_panel_5 import panel as my_panel_5
from .my_panel_6 import panel as my_panel_6
from .my_panel_7 import panel as my_panel_7


ext = Extension(__name__)
ext.add(my_panel_1)
ext.add(my_panel_2)
ext.add(my_panel_3)
ext.add(my_panel_4)
ext.add(my_panel_5)
ext.add(my_panel_6)
ext.add(my_panel_7)
