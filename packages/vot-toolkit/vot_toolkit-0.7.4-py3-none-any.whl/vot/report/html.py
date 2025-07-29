"""HTML report generation. This module is used to generate HTML reports from the results of the experiments."""
import os
import io
import datetime
from typing import List

import dominate
from dominate.tags import h1, h2, table, thead, tbody, tr, th, td, div, p, li, ol, ul, span, style, link, script, video, a
from dominate.util import raw, text

from vot import toolkit_version, check_debug, get_logger
from vot.tracker import Tracker
from vot.dataset import Sequence
from vot.workspace import Storage
from vot.report.common import format_value, read_resource, merge_repeats
from vot.report import StyleManager, Table, Plot, Video
from vot.utilities.data import Grid

ORDER_CLASSES = {1: "first", 2: "second", 3: "third"}

def insert_cell(value, order):
    """Inserts a cell into the data table."""
    attrs = dict(data_sort_value=order, data_value=value)
    if order in ORDER_CLASSES:
        attrs["cls"] = ORDER_CLASSES[order]
    td(format_value(value), **attrs)

def table_cell(value):
    """Returns a cell for the data table."""
    if isinstance(value, str):
        return value
    elif isinstance(value, Tracker):
        return value.label
    elif isinstance(value, Sequence):
        return value.name
    return format_value(value)

def grid_table(data: Grid, rows: List[str], columns: List[str]):
    """Generates a table from a grid object."""

    assert data.dimensions == 2
    assert data.size(0) == len(rows) and data.size(1) == len(columns)

    with table() as element:
        with thead():
            with tr():
                th()
                [th(table_cell(column)) for column in columns]
        with tbody():
            for i, row in enumerate(rows):
                with tr():
                    th(table_cell(row))
                    for value in data.row(i):
                        if isinstance(value, tuple):
                            if len(value) == 1:
                                value = value[0]
                        insert_cell(value, None)

    return element

def generate_html_document(trackers: List[Tracker], sequences: List[Sequence], reports, storage: Storage, metadata: dict = None):
    """Generates an HTML document from the results of the experiments.
    
    Args:
        trackers (list): List of trackers.
        sequences (list): List of sequences.
        reports (dict): List of reports as tuples of (name, data).
        storage (Storage): Storage object.
        metadata (dict): Metadata dictionary.
    """

    def insert_video(data: Video):
        """Insert a video into the document."""
        name = data.identifier + ".mp4"

        with storage.write(name, binary=True) as handle:
            data.save(handle, "mp4")

        with video(src=name, controls=True, preload="auto", autoplay=False, loop=False, width="100%", height="100%"):
            raw("Your browser does not support the video tag.")

    def insert_figure(figure):
        """Inserts a matplotlib figure into the document."""
        buffer = io.StringIO()
        figure.save(buffer, "SVG")
        raw(buffer.getvalue())

    def insert_mplfigure(figure):
        """Inserts a matplotlib figure into the document."""
        buffer = io.StringIO()
        figure.savefig(buffer, format="SVG", bbox_inches='tight', pad_inches=0.01, dpi=200)
        raw(buffer.getvalue())

    def add_style(name, linked=False):
        """Adds a style to the document."""
        if linked:
            link(rel='stylesheet', href='file://' + os.path.join(os.path.dirname(__file__), name))
        else:
            style(read_resource(name))

    def add_script(name, linked=False):
        """Adds a script to the document."""
        if linked:
            script(type='text/javascript', src='file://' + os.path.join(os.path.dirname(__file__), name))
        else:
            with script(type='text/javascript'):
                raw("//<![CDATA[\n" + read_resource(name) + "\n//]]>")

    logger = get_logger()
    
    legend = StyleManager.default().legend(Tracker)

    doc = dominate.document(title='VOT report')

    linked = check_debug()

    with doc.head:
        add_style("pure.css", linked)
        add_style("report.css", linked)
        add_script("jquery.js", linked)
        add_script("table.js", linked)
        add_script("report.js", linked)

    # TODO: make table more general (now it assumes a tracker per row)
    def make_table(data: Table):
        """Generates a table from a Table object."""
        if len(data.header[2]) == 0:
            logger.debug("No measures found, skipping table")
        else:
            with table(cls="overview-table pure-table pure-table-horizontal pure-table-striped"):
                with thead():
                    with tr():
                        th()
                        [th(c[0].identifier, colspan=c[1]) for c in merge_repeats(data.header[0])]
                    with tr():
                        th()
                        [th(c[0].title, colspan=c[1]) for c in merge_repeats(data.header[1])]
                    with tr():
                        th("Trackers")
                        [th(c.abbreviation, data_sort="int" if order else "") for c, order in zip(data.header[2], data.order)]
                with tbody():
                    for tracker, row in data.data.items():
                        with tr(data_tracker=tracker.reference):
                            with td():
                                insert_mplfigure(legend.figure(tracker))
                                span(tracker.label)
                            for value, order in zip(row, data.order):
                                insert_cell(value, order[tracker] if not order is None else None)

    metadata = metadata or dict()
    metadata["Version"] = toolkit_version()
    metadata["Created"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    metadata["Trackers"] = ", ".join([tracker.label for tracker in trackers])
    metadata["Sequences"] = ", ".join([sequence.name for sequence in sequences])

    with doc:

        with div(id="wrapper"):

            h1("Analysis report document")

            with ul(id="metadata"):
                for key, value in metadata.items():
                    with li():
                        span(key)
                        text(": " + value)

            with div(id="index"):
                h2("Index")
                with ol():
                    for key, _ in reports.items():
                        li(a(key, href="#"+key))

            for key, section in reports.items():

                a(name=key)
                h2(key, cls="section")

                for item in section:
                    if isinstance(item, Table):
                        make_table(item)
                    elif isinstance(item, Plot):
                        with div(cls="plot"):
                            p(item.identifier)
                            insert_figure(item)
                    elif isinstance(item, Video):
                        with div(cls="video"):
                            p(item.identifier)
                            insert_video(item)
                    else:
                        logger.warning("Unsupported report item type %s", item)

            with div(id="footer"):
                text("Generated by ")
                a("VOT toolkit", href="https://github.com/votchallenge/toolkit")
                text(" version %s" % toolkit_version())

    with storage.write("report.html") as filehandle:
        filehandle.write(doc.render())
