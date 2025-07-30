import io
from pathlib import Path
from tempfile import SpooledTemporaryFile

import pandas as pd
import tqdm

from qcogclient.httpclient import ReadableFile


class LoadedCSV:
    file: ReadableFile
    number_of_columns: int
    number_of_rows: int


def load_csv(
    file: Path | str,
    *,
    chunk_size: int = 1024 * 1024,
) -> LoadedCSV:
    """
    Load a CSV file into a file-like object and compute its dimensions.
    Returns a LoadedCSV object containing the file and its dimensions.
    """
    if isinstance(file, str):
        file = Path(file)

    retval = SpooledTemporaryFile()
    total_chunks = file.stat().st_size // chunk_size
    current_chunk = 0
    percentage = 0

    # Initialize counters
    number_of_rows = 0
    number_of_columns = 0
    first_line = True

    with tqdm.tqdm(total=total_chunks, desc="Loading CSV", unit="chunk") as pbar:
        with file.open("rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break

                # Count rows and columns in this chunk
                lines = chunk.split(b"\n")
                for line in lines:
                    if line.strip():  # Skip empty lines
                        if first_line:
                            number_of_columns = len(line.split(b","))
                            first_line = False
                        number_of_rows += 1

                retval.write(chunk)
                current_chunk += 1
                percentage = round(current_chunk / total_chunks * 100)
                pbar.update(1)
                pbar.set_postfix(percentage=percentage)
                pbar.refresh()

        retval.seek(0)

        return {  # type: ignore
            "file": retval,
            "number_of_columns": number_of_columns,
            "number_of_rows": number_of_rows,
        }


def load_dataframe(
    file: pd.DataFrame,
    *,
    index: bool = False,
) -> ReadableFile:
    """
    Load a pandas DataFrame into a file-like object.
    """

    retval = io.BytesIO()
    file.to_csv(retval, index=index)
    retval.seek(0)
    return retval
