"""Pages, frames and other layout-related operations.

The "layout" consists of a stack of `Pages <tecplot.layout.Page>` identified by index or
`name <Page.name>`. Each `Page <tecplot.layout.Page>` consists of a single "workspace" which holds
a collection of `Frames <tecplot.layout.Frame>` that are laid out in relation to an area
called the `Paper`.

The |Tecplot Engine| is guaranteed to have at least one `Page <tecplot.layout.Page>` which is
holding onto at least one `Frame <tecplot.layout.Frame>`. It also has the concept of an active
`Frame <tecplot.layout.Frame>` and by extension, an active `Page <tecplot.layout.Page>`. Most, if not all operations
that require a handle to a `Frame <tecplot.layout.Frame>` will use the active `Frame <tecplot.layout.Frame>` by default.
This includes any function that operates on objects held by a `Frame <tecplot.layout.Frame>`
such as a `Cartesian3DFieldPlot` or `Dataset <tecplot.data.Dataset>`.
"""

from .frame import Frame
from .layout import (active_frame, active_page, add_page, aux_data, delete_page,
                     frames, next_page, num_pages, page, pages, next_page,
                     new_layout, load_layout, save_layout)
from .page import Page, Paper
