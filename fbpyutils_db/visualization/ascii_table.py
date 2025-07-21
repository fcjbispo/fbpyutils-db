from typing import Any, List
from fbpyutils_db import logger

def ascii_table(
    data: List[List[Any]],
    columns: List[str] = [],
    alignment: str = "left",
    numrows: int = None,
) -> List[str]:
    """
    Creates an ASCII table representation of the given data.

    Args:
        data (list): A list of lists representing the data rows.
        columns (list, optional): A list of column names. Defaults to an empty list.
        alignment (str, optional): The alignment of the table cells. Valid values are 'left', 'right', or 'center'. Defaults to 'left'.
        numrows (int, optional): The number of rows to display. If None, all rows are displayed. Defaults to None.

    Returns:
        list: A list of strings representing the ASCII table.

    Example:
        >>> data = [['John', 25, 'USA'], ['Alice', 30, 'Canada'], ['Bob', 40, 'UK']]
        >>> columns = ['Name', 'Age', 'Country']
        >>> table = ascii_table(data, columns=columns, alignment='center')
        >>> for line in table:
        ...     print(line)
        +-------+-----+---------+
        |  Name | Age | Country |
        +-------+-----+---------+
        |  John |  25 |   USA   |
        | Alice |  30 |  Canada |
        |  Bob  |  40 |    UK   |
        +-------+-----+---------+

    """
    logger.debug(f"Creating ASCII table with {len(data)} rows, {len(columns)} columns")
    logger.debug(f"Alignment: {alignment}, numrows: {numrows}")
    
    if len(data) == 0:
        logger.warning("Empty data provided to ascii_table")
        return None

    data = [list(e) for e in data]
    columns = list([c for c in columns])
    alignment = alignment or "left"

    def pad(x, size, char=" ", where="center"):
        char = char or " "
        where = where or "center"
        return (
            str(x).rjust(size, char)
            if where == "right"
            else (
                str(x).ljust(size, char)
                if where == "left"
                else str(x).center(size, char)
            )
        )

    def line(rows, sizes, where="center"):
        return (
            "|"
            + "|".join(
                [pad(rows[i], sizes[i], where=where) for i in range(0, len(rows))]
            )
            + "|"
        )

    col_lenghts = tuple(set([len(d) for d in data]))

    if len(col_lenghts) == 0:
        return None

    if len(col_lenghts) > 1:
        raise ValueError("Number of columns mismatch among rows.")

    if alignment not in ("left", "right", "center"):
        raise ValueError("Alignment valid values: left|right|center")

    if columns is None or len(columns) == 0:
        columns = [f"column_{i}" for i in range(0, col_lenghts[0])]

    if len(columns) != col_lenghts[0]:
        logger.error(f"Column length mismatch: data has {col_lenghts[0]} columns, but {len(columns)} provided")
        logger.debug(f"Column lengths: {col_lenghts}, columns: {columns}")
        raise ValueError(f"Number of columns mismatch with data row.")

    if numrows is None or numrows > len(data):
        numrows = len(data)
    xdata = [
        [row[i] for i in range(len(data[0])) if columns[i] in columns] for row in data
    ][0:numrows]

    max_sizes = list(
        max(n)
        for n in list(
            list(len(str(r[i])) for r in xdata) for i in range(0, len(xdata[0]))
        )
    )

    col_sizes = [len(str(c)) for c in columns]
    new_max_sizes = []
    for i, _ in enumerate(max_sizes):
        new_max_sizes.append(max(max_sizes[i], col_sizes[i]))
    max_sizes = new_max_sizes

    line_sep = "".join(["+" + "-" * i for i in max_sizes]) + "+"

    table = []
    table.append(line_sep)
    table.append(line(columns, max_sizes))
    table.append(line_sep)
    for row in data:
        table.append(line(row, max_sizes, where=alignment))
    table.append(line_sep)

    logger.debug(f"Successfully created ASCII table with {len(table)} lines")
    return table


def print_ascii_table(
    data: List[List[Any]],
    columns: List[str] = [],
    alignment: str = "left",
    numrows: int = None,
) -> None:
    """
    Prints the ASCII table representation of the given data.

    Args:
        data (list): A list of lists representing the data rows.
        columns (list, optional): A list of column names. Defaults to an empty list.
        alignment (str, optional): The alignment of the table cells. Valid values are 'left', 'right', or 'center'. Defaults to 'left'.

    Returns:
        None

    Example:
        >>> data = [['John', 25, 'USA'], ['Alice', 30, 'Canada'], ['Bob', 40, 'UK']]
        >>> columns = ['Name', 'Age', 'Country']
        >>> print_ascii_table(data, columns=columns, alignment='center')
        +-------+-----+---------+
        |  Name | Age | Country |
        +-------+-----+---------+
        |  John |  25 |   USA   |
        | Alice |  30 |  Canada |
        |  Bob  |  40 |    UK   |
        +-------+-----+---------+

    """
    if data is None:
        return None

    logger.info(f"Printing ASCII table with {len(data) if data else 0} rows")
    table = ascii_table(data, columns=columns, alignment=alignment, numrows=numrows)

    for line in table:
        print(line)
    logger.debug(f"Successfully printed ASCII table with {len(table)} lines")
