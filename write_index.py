import pathlib
import dominate

from datetime import datetime
from dominate.tags import *


def get_list_of_log_file_directories() -> list[str]:
    """Return a sorted list of valid log file directory names.

    Returns:
        A list of strings of all valid log file directories (i.e. those that themsevles contain an index.html file).
    """

    base_dir = pathlib.Path('log-files')
    dirs_list = [path.name for path in base_dir.iterdir() if path.is_dir() and (path / 'index.html').is_file()]

    return sorted(dirs_list, reverse=True)


def write_index_file(list_of_logs: list[str]) -> None:
    """Write an index.html file containing hyperlinks to the log file directories contained in this directory.              

    Args:
        list_of_logs: A list of strings of log file directories to put in the index file.

    Returns:
        None.
    """

    doc = dominate.document(title='Index of GProf profiling output')

    dates = [datetime.strptime(x, '%Y-%m-%d_%H-%M-%S') for x in list_of_logs]

    unique_dates = {datetime(year=date.year, month=date.month, day=1) for date in dates}
    unique_dates = sorted(list(unique_dates), reverse=True)

    with doc.head:
        link(rel='stylesheet', href='style.css')

    with doc:

        with div(id='title'):
            h1('Index of GProf profiling output')

        with div(id='list-by-month'):
            attr(cls='body')
            
            for unique_date in unique_dates:
                h2(unique_date.strftime("%B %Y"))

                with ul():

                    for path, date in zip(list_of_logs, dates):
                        if date.year == unique_date.year and date.month == unique_date.month:
                            li(a(path, href=f'{path}/index.html'))
    
    with open('log-files/index.html', 'w') as html_file:
        html_file.write(doc.render())


if __name__ == "__main__":

    list_of_logs = get_list_of_log_file_directories()
    write_index_file(list_of_logs)
