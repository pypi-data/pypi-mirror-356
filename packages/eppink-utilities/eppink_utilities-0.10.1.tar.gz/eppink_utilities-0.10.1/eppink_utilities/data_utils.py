import numpy as np
from .math_utils import average

def data_row_exists(contents, new_row, column=0):
    """
    Check if the specified column of `new_row` matches the same column of any row in `contents`.

    Parameters:
        new_row (list): A list representing the row to check.
        contents (list of lists): The existing rows to search within, where each row is a list.
        column (int, optional): The index of the column to compare. Defaults to 0.

    Returns:
        tuple: (exists, index, matched_row)
            exists (bool): True if a matching value is found in the specified column, else False.
            index (int or None): The index of the matching row in `contents` if found, else None.
            matched_row (list or None): The matched row from `contents` if found, else None.

    Notes:
        - Matching is based on the value in the specified column.
        - Assumes `new_row` and each row in `contents` have enough columns to access the specified index.
        - Raises IndexError if `column` is out of range for any row.
    """
    key = new_row[column]
    for i, row in enumerate(contents):
        if row and row[column] == key:
            return True, i, row
    return False, None, None

def data_exact_row_exists(contents, new_row, case_sensitive=False, type_sensitive=False):
    """
    Check if a fully identical row exists in `contents`, with options for case and type sensitivity.

    Parameters:
        new_row (list): A list representing the row to check.
        contents (list of lists): The existing rows to search within, where each row is a list.
        case_sensitive (bool, optional): If True, string comparisons are case-sensitive. Defaults to False.
        type_sensitive (bool, optional): If True, type mismatches cause non-match. Defaults to False.

    Returns:
        tuple: (exists, matched_indices)
            exists (bool): True if one or more matches are found based on the given sensitivity options.
            matched_indices (list): A list of indices in `contents` where rows match `new_row` based on sensitivity.

    Notes:
        - Matching requires the same number of elements in each row.
        - If `case_sensitive` is False, string comparisons are case-insensitive.
        - If `type_sensitive` is False, values with equal string representations are considered equal.
    """


    matched_indices = [i for i, row in enumerate(contents) if data_rows_match(row, new_row, case_sensitive==case_sensitive, type_sensitive=type_sensitive)]
    exists = len(matched_indices) > 0
    return exists, matched_indices

def data_rows_match(row1, row2, case_sensitive=False, type_sensitive=False):
    """
    Compares two rows (lists, tuples, etc.) element-wise to determine if they match.

    Parameters:
        row1 (iterable): The first row to compare.
        row2 (iterable): The second row to compare.
        case_sensitive (bool): If True, string comparisons are case-sensitive.
                               If False (default), strings are compared case-insensitively.
        type_sensitive (bool): If True, values are compared with type sensitivity (e.g., 1 != "1").
                               If False (default), values are converted to strings before comparison.

    Returns:
        bool: True if the rows match element-wise according to the specified sensitivity flags,
              False otherwise.
    """
    if len(row1) != len(row2):
        return False
    for v1, v2 in zip(row1, row2):
        if type_sensitive:
            if v1 != v2:
                return False
        else:
            s1, s2 = str(v1), str(v2)
            if case_sensitive:
                if s1 != s2:
                    return False
            else:
                if s1.lower() != s2.lower():
                    return False
    return True

def data_remove_rows(contents, indices):
    """
    Remove multiple rows from contents based on a list of indices.

    Parameters:
        contents (list of lists): The CSV data as a list of rows.
        indices (list or set of int): Indices of rows to remove.

    Returns:
        list: New list with specified rows removed.

    Notes:
        - Indices that are out of range are ignored.
        - The order of remaining rows is preserved.
    """
    indices_set = set(indices)  # For faster lookup
    return [row for i, row in enumerate(contents) if i not in indices_set]

def data_columns_combine(*args, check_rows=True):
    """
    Combine multiple 1D column vectors or 2D matrices into a single 2D array (column-wise).

    Parameters:
        *args: Each argument can be:
            - A 1D NumPy array or list (treated as a column)
            - A 2D NumPy array or list of lists (multiple columns)
            - None or empty arrays/lists are skipped
        check_rows (bool): If True, all inputs must have the same number of rows (vertical elements)

    Returns:
        np.ndarray: Combined 2D array of shape (n_rows, total_columns)

    Raises:
        ValueError: If an input is a row vector or if row counts mismatch (when check_rows=True)
    """
    cols = []
    row_counts = []

    for i, item in enumerate(args):
        if item is None:
            continue

        try:
            arr = np.asarray(item)
        except Exception as e:
            raise ValueError(f"Input {i} could not be converted to an array — possibly a malformed or ragged list: {item}") from e


        if arr.size == 0:
            continue

        if arr.ndim == 1:
            arr = arr.reshape(-1, 1)

        elif arr.ndim == 2:
            rows, cols_ = arr.shape
            # Reject row vector
            if rows == 1 and cols_ > 1:
                raise ValueError(f"Input {i} looks like a row vector with shape {arr.shape}. "
                                 f"Did you mean to transpose it?")
        else:
            raise ValueError(f"Input {i} has too many dimensions: {arr.shape}")

        cols.append(arr)
        row_counts.append(arr.shape[0])

    if not cols:
        return np.empty((0, 0))

    if check_rows and len(set(row_counts)) != 1:
        raise ValueError(f"Inconsistent number of rows across inputs: {row_counts}")

    try:
        return np.hstack(cols)
    except ValueError as e:
        raise ValueError(f"Column stacking failed — inputs may have inconsistent row counts. "
                        f"Set check_rows=True to catch this early.\nOriginal error: {e}")

def data_bin(data, mode='range', *, dt=None, bin_column=None, returnmode='indices'):
    """
    Bin rows of data based on continuous ranges or discrete values.

    Parameters:
        data (np.ndarray): 2D array of shape (n_rows, n_cols).
        mode (str): 'range' for numeric range binning, 'value' for discrete value binning.
        dt (float, optional): Bin width for 'range' mode (required if mode='range').
        bin_column (int, optional): Column index for 'value' mode (required if mode='value').
        returnmode (str): 'indices' to return bin indices array, 'binned' to return list of arrays per bin.

    Returns:
        If returnmode='indices':
            bin_indices (np.ndarray): Array of shape (n_rows,) assigning each row to a bin index.
                                      Rows outside bins get -1.
            bin_labels (np.ndarray): 
                - For 'range': 1D array of bin edges, length = number_of_bins + 1
                - For 'value': 1D array of unique discrete values used as bins

        If returnmode='binned':
            binned_data (list of np.ndarray): List with one array per bin containing rows in that bin.
            bin_labels (np.ndarray): same as above
    """
    data = np.asarray(data)
    n_rows, n_cols = data.shape

    if mode == 'range':
        if dt is None:
            raise ValueError("Parameter 'dt' must be provided for 'range' mode.")
        
        values = data[:, 0]  # or extend to specify which col later
        vmin = np.floor(np.nanmin(values))
        vmax = np.ceil(np.nanmax(values))
        bin_edges = np.arange(vmin, vmax + dt, dt)

        inds = np.digitize(values, bin_edges, right=False) - 1
        inds[(values < bin_edges[0]) | (values >= bin_edges[-1])] = -1

    elif mode == 'value':
        if bin_column is None:
            raise ValueError("Parameter 'bin_column' must be provided for 'value' mode.")

        values = data[:, bin_column]
        unique_vals = np.unique(values)
        val_to_bin = {val: i for i, val in enumerate(unique_vals)}
        inds = np.array([val_to_bin.get(v, -1) for v in values])

    else:
        raise ValueError(f"Unsupported mode '{mode}'. Use 'range' or 'value'.")

    if returnmode == 'indices':
        return inds, bin_edges if mode == 'range' else unique_vals

    elif returnmode == 'binned':
        # group rows per bin index (skip -1)
        bins = []
        nbins = (len(bin_edges) - 1) if mode == 'range' else len(unique_vals)
        for b in range(nbins):
            bins.append(data[inds == b])
        bin_labels = bin_edges if mode == 'range' else unique_vals
        return bins, bin_labels

    else:
        raise ValueError("returnmode must be either 'indices' or 'binned'")

def dataset_combine(*datasets, avgMode='trapezoidal', dt):
    """
    Merge multiple datasets by time binning and trapezoidal averaging.

    Parameters:
        *datasets: Each dataset is a 2D array-like of shape (n_rows, n_columns),
                   where column 0 is time (in seconds).
        dt (float): Width of time bins.
        avgMode (str): Averaging mode ('arithmetic' or 'trapezoidal').

    Returns:
        tuple: (header: list[str], data: np.ndarray, full_data: list[list])
    """
    import numpy as np

    headers = []
    arrays = []

    for d in datasets:
        # Handle case where header is included (e.g. from CSV)
        if isinstance(d, list) and isinstance(d[0], list) and isinstance(d[0][0], str):
            header_row, d = d[0], d[1:]
            headers.extend(header_row[1:])  # Skip time column
            d = np.array(d, dtype=float)
        else:
            d = np.array(d, dtype=float)
            headers.extend([f"Var{i}" for i in range(1, d.shape[1])])  # fallback names

        arrays.append(d)

    if not arrays:
        return [], np.empty((0, 0)), []

    # Determine bin edges
    t_min = min(np.nanmin(d[:, 0]) for d in arrays)
    t_max = max(np.nanmax(d[:, 0]) for d in arrays)
    bin_edges = np.arange(np.floor(t_min), np.ceil(t_max) + dt, dt)
    n_bins = len(bin_edges) - 1
    t_out = bin_edges[:-1].reshape(-1, 1)  # (n_bins, 1)

    merged_columns = [t_out]

    for data in arrays:
        t = data[:, 0]
        features = data[:, 1:]

        inds = np.digitize(t, bin_edges) - 1
        inds[(t < bin_edges[0]) | (t >= bin_edges[-1])] = -1

        binned_means = np.full((n_bins, features.shape[1]), np.nan)

        for b in range(n_bins):
            mask = inds == b
            if np.any(mask):
                binned_means[b] = average(
                    features[mask],
                    mode=avgMode,
                    time=t[mask]
                )

        merged_columns.append(binned_means)

    data = np.hstack(merged_columns)
    header = ["Time [s]"] + headers

    # Combine header + data for full_data as list-of-lists
    full_data = [header] + data.tolist()

    return header, data, full_data

def dataset_SplitHeaderFromData(dataset):
    """
    Splits the header row from a dataset if present.

    Parameters:
        dataset (list of list): Raw dataset where the first row may be a header.

    Returns:
        tuple: (header, data)
            - header (list or None): The header row if detected, else None.
            - data (list of list): The remaining dataset with only numeric rows.
    """
    if not dataset:
        return None, []

    first_row = dataset[0]

    def is_row_numeric(row):
        try:
            [float(cell) for cell in row]
            return True
        except ValueError:
            return False

    if is_row_numeric(first_row):
        return None, dataset  # No header, all data is numeric
    else:
        return first_row, dataset[1:]  # Header exists


if __name__ == "__main__":
    import numpy as np

    # Simulated CSV-style data with headers
    data1 = [['Time [s]', 'T1', 'T2']]
    data2 = [['Time [s]', 'P1']]

    # Add 16 rows to data1 (timestamps 0 to 15)
    for i in range(16):
        data1.append([str(i), str(20 + i * 0.5), str(21 + i * 0.3)])

    # Add 15 rows to data2 (timestamps 0 to 14)
    for i in range(15):
        data2.append([str(i), str(1.0 + i * 0.1)])

    # Test with header-containing string data
    header, data, full = dataset_combine(data1, data2, dt=1, avgMode="arithmetic")

    print("Test: Header-containing datasets")
    print("Header:", header)
    print("Data shape:", data.shape)
    print("First 5 rows of data:\n", data[:5])
    print("First 5 rows of full output:\n", full[:5])

