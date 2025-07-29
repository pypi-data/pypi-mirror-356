# import pandas as pd
# import numpy as np

# class Comparator:
#     """
#     A comparator for comparing specified columns between two pandas DataFrames,
#     typically representing two periods of portfolio data.
#     """

#     def __init__(self):
#         """Initialize the comparator with no state."""
#         pass

#     @staticmethod
#     def calculate_pct_change(old_val, new_val):
#         """Calculate percentage change between two values."""
#         if pd.isna(old_val) or pd.isna(new_val):
#             return np.nan
#         if old_val == 0:
#             return np.inf if new_val != 0 else 0
#         return ((new_val - old_val) / abs(old_val)) * 100

#     def compare_dataframes(self, df1, df2, key_columns, compare_columns, show_all=False, top_n=100):
#         """
#         Compare two DataFrames using composite key and specified compare_columns.

#         Parameters:
#         - df1, df2: pandas DataFrames for the two periods.
#         - key_columns: List of column names that uniquely identify each row.
#         - compare_columns: List of column names to compare.
#         - show_all: If True, include rows without changes.
#         - top_n: Number of rows to return per column.

#         Returns:
#         A dict mapping each compared column to a dict with:
#         {'data': pd.DataFrame(changes), 'top_n': top_n}
#         """
#         # Create a composite key for alignment
#         df1 = df1.copy()
#         df2 = df2.copy()

#         # Check key columns exist
#         for col in key_columns:
#             if col not in df1.columns:
#                 print(f"ERROR: Key column '{col}' not found in df1")
#                 return {}
#             if col not in df2.columns:
#                 print(f"ERROR: Key column '{col}' not found in df2")
#                 return {}

#         # Check compare columns exist
#         for col in compare_columns:
#             if col not in df1.columns:
#                 print(f"WARNING: Compare column '{col}' not found in df1")
#             if col not in df2.columns:
#                 print(f"WARNING: Compare column '{col}' not found in df2")

#         try:
#             df1['composite_key'] = df1[key_columns].astype(str).agg('|'.join, axis=1)
#             df2['composite_key'] = df2[key_columns].astype(str).agg('|'.join, axis=1)
#         except Exception as e:
#             print(f"ERROR creating composite key: {e}")
#             return {}

#         df1 = df1.set_index('composite_key')
#         df2 = df2.set_index('composite_key')

#         common_keys = set(df1.index).intersection(df2.index)
#         print(f"DEBUG: Found {len(common_keys)} common composite keys")

#         results = {}

#         for col in compare_columns:
#             if col not in df1.columns or col not in df2.columns:
#                 print(f"Skipping column '{col}' since it is missing in one of the dataframes")
#                 continue

#             records = []
#             for key in common_keys:
#                 try:
#                     val1 = df1.at[key, col]
#                     val2 = df2.at[key, col]
#                 except KeyError as e:
#                     print(f"WARNING: KeyError accessing column '{col}' for key '{key}': {e}")
#                     continue

#                 # Both NaN
#                 if pd.isna(val1) and pd.isna(val2):
#                     if show_all:
#                         records.append({'key': key, f'{col}_before': val1, f'{col}_after': val2})
#                     continue

#                 if show_all or val1 != val2:
#                     rec = {'key': key, f'{col}_before': val1, f'{col}_after': val2}

#                     # Check if values are numeric before calculating changes
#                     try:
#                         if pd.api.types.is_number(val1) and pd.api.types.is_number(val2):
#                             rec['absolute_change'] = val2 - val1
#                             rec['pct_change'] = self.calculate_pct_change(val1, val2)
#                     except Exception as e:
#                         print(f"WARNING: Error checking numeric dtype or calculating changes for key '{key}', column '{col}': {e}")

#                     records.append(rec)

#             if records:
#                 changes_df = pd.DataFrame(records)
#                 results[col] = {'data': changes_df, 'top_n': top_n}
#                 print(f"DEBUG: Column '{col}' - found {len(records)} changes")

#         if not results:
#             print("INFO: No differences found based on given parameters")

#         return results

#     def display_comparison(self, comparison_results):
#         """
#         Display comparison results in a tabular format in the console.
#         """
#         if not comparison_results:
#             print("No comparison results to display.")
#             return

#         for col, result in comparison_results.items():
#             df = result['data']
#             top_n = result.get('top_n', 100)

#             print(f"\n=== Changes in '{col}' ===")
#             print(f"Total rows with changes: {len(df)}")

#             if 'absolute_change' in df.columns:
#                 # Sort by absolute change magnitude
#                 df_sorted = df.reindex(df['absolute_change'].abs().sort_values(ascending=False).index)
#                 print(df_sorted.head(top_n))
#             else:
#                 print(df.head(top_n))







# import pandas as pd
# import numpy as np

# class Comparator:
#     """
#     A comparator for comparing specified columns between two pandas DataFrames,
#     typically representing two periods of portfolio data.
#     """

#     def __init__(self):
#         """Initialize the comparator with no state."""
#         pass

#     @staticmethod
#     def calculate_pct_change(old_val, new_val):
#         """Calculate percentage change between two values."""
#         if pd.isna(old_val) or pd.isna(new_val):
#             return np.nan
#         if old_val == 0:
#             return np.inf if new_val != 0 else 0
#         return ((new_val - old_val) / abs(old_val)) * 100

#     def compare_dataframes(self, df1, df2, key_columns, compare_columns, show_all=False, top_n=100):
#         """
#         Compare two DataFrames using composite key and specified compare_columns.

#         Returns a dict mapping each compared column to a dict with:
#         {'data': pd.DataFrame(changes), 'top_n': top_n}
#         """
#         df1 = df1.copy()
#         df2 = df2.copy()

#         for col in key_columns:
#             if col not in df1.columns or col not in df2.columns:
#                 print(f"ERROR: Key column '{col}' not found in both dataframes")
#                 return {}

#         for col in compare_columns:
#             if col not in df1.columns:
#                 print(f"WARNING: Compare column '{col}' not found in df1")
#             if col not in df2.columns:
#                 print(f"WARNING: Compare column '{col}' not found in df2")

#         try:
#             df1['composite_key'] = df1[key_columns].astype(str).agg('|'.join, axis=1)
#             df2['composite_key'] = df2[key_columns].astype(str).agg('|'.join, axis=1)
#         except Exception as e:
#             print(f"ERROR creating composite key: {e}")
#             return {}

#         df1 = df1.set_index('composite_key')
#         df2 = df2.set_index('composite_key')

#         common_keys = set(df1.index).intersection(df2.index)
#         print(f"DEBUG: Found {len(common_keys)} common composite keys")

#         results = {}

#         for col in compare_columns:
#             if col not in df1.columns or col not in df2.columns:
#                 print(f"Skipping column '{col}' since it is missing in one of the dataframes")
#                 continue

#             records = []
#             for key in common_keys:
#                 try:
#                     val1s = df1.loc[key, col]
#                     val2s = df2.loc[key, col]

#                     val1_list = val1s.tolist() if isinstance(val1s, pd.Series) else [val1s]
#                     val2_list = val2s.tolist() if isinstance(val2s, pd.Series) else [val2s]

#                     if show_all or val1_list != val2_list:
#                         rec = {
#                             'key': key,
#                             f'{col}_before': val1_list,
#                             f'{col}_after': val2_list,
#                             'note': 'multiple values found' if len(val1_list) > 1 or len(val2_list) > 1 else ''
#                         }

#                         try:
#                             val1_mean = np.mean(val1_list)
#                             val2_mean = np.mean(val2_list)

#                             if pd.api.types.is_number(val1_mean) and pd.api.types.is_number(val2_mean):
#                                 rec['absolute_change'] = val2_mean - val1_mean
#                                 rec['pct_change'] = self.calculate_pct_change(val1_mean, val2_mean)
#                         except Exception as e:
#                             print(f"WARNING: Error calculating numeric diff for key '{key}', column '{col}': {e}")

#                         records.append(rec)
#                 except KeyError as e:
#                     print(f"WARNING: KeyError accessing '{col}' for key '{key}': {e}")
#                     continue

#             if records:
#                 changes_df = pd.DataFrame(records)
#                 results[col] = {'data': changes_df, 'top_n': top_n}
#                 print(f"DEBUG: Column '{col}' - found {len(records)} changes")

#         if not results:
#             print("INFO: No differences found based on given parameters")

#         return results

#     def display_comparison(self, comparison_results):
#         """
#         Display comparison results in a tabular format in the console.
#         """
#         if not comparison_results:
#             print("No comparison results to display.")
#             return

#         for col, result in comparison_results.items():
#             df = result['data']
#             top_n = result.get('top_n', 100)

#             print(f"\n=== Changes in '{col}' ===")
#             print(f"Total rows with changes: {len(df)}")

#             if 'absolute_change' in df.columns:
#                 df_sorted = df.reindex(df['absolute_change'].abs().sort_values(ascending=False).index)
#                 print(df_sorted.head(top_n))
#             else:
#                 print(df.head(top_n))












# import pandas as pd
# import numpy as np

# class Comparator:
#     """
#     A comparator for comparing specified columns between two pandas DataFrames,
#     typically representing two periods of portfolio data.
#     """

#     def __init__(self):
#         pass

#     @staticmethod
#     def calculate_pct_change(old_val, new_val):
#         """Calculate percentage change between two values."""
#         if pd.isna(old_val) or pd.isna(new_val):
#             return np.nan
#         if old_val == 0:
#             return None  # ← safer: avoids inf
#         return ((new_val - old_val) / abs(old_val)) * 100


#     def compare_dataframes(self, df1, df2, key_columns, compare_columns, show_all=False, top_n=100):
#         """
#         Compare two DataFrames using composite key and specified compare_columns.

#         Parameters:
#         - df1, df2: pandas DataFrames for the two periods.
#         - key_columns: List of column names that uniquely identify each row.
#         - compare_columns: List of column names to compare.
#         - show_all: If True, include rows without changes.
#         - top_n: Number of rows to return per column.

#         Returns:
#         A dict mapping each compared column to a dict with:
#         {'data': pd.DataFrame(changes), 'top_n': top_n}
#         """
#         df1 = df1.copy()
#         df2 = df2.copy()

#         for col in key_columns:
#             if col not in df1.columns or col not in df2.columns:
#                 print(f"ERROR: Key column '{col}' not found in both dataframes")
#                 return {}

#         for col in compare_columns:
#             if col not in df1.columns or col not in df2.columns:
#                 print(f"WARNING: Compare column '{col}' not found in one of the dataframes")

#         df1['composite_key'] = df1[key_columns].astype(str).agg('|'.join, axis=1)
#         df2['composite_key'] = df2[key_columns].astype(str).agg('|'.join, axis=1)

#         # Check for duplicate keys
#         if df1['composite_key'].duplicated().any():
#             print("WARNING: Duplicate keys found in df1")
#         if df2['composite_key'].duplicated().any():
#             print("WARNING: Duplicate keys found in df2")

#         df1 = df1.set_index('composite_key')
#         df2 = df2.set_index('composite_key')

#         common_keys = set(df1.index).intersection(df2.index)
#         print(f"DEBUG: Found {len(common_keys)} common composite keys")

#         results = {}

#         for col in compare_columns:
#             if col not in df1.columns or col not in df2.columns:
#                 continue

#             records = []
#             for key in common_keys:
#                 rows1 = df1.loc[[key]] if isinstance(df1.loc[key], pd.Series) else df1.loc[key]
#                 rows2 = df2.loc[[key]] if isinstance(df2.loc[key], pd.Series) else df2.loc[key]

#                 if isinstance(rows1, pd.Series):
#                     rows1 = pd.DataFrame([rows1])
#                 if isinstance(rows2, pd.Series):
#                     rows2 = pd.DataFrame([rows2])

#                 max_len = max(len(rows1), len(rows2))
#                 for i in range(max_len):
#                     val1 = rows1.iloc[i][col] if i < len(rows1) else np.nan
#                     val2 = rows2.iloc[i][col] if i < len(rows2) else np.nan

#                     if pd.isna(val1) and pd.isna(val2):
#                         if show_all:
#                             records.append({'key': key, f'{col}_before': val1, f'{col}_after': val2})
#                         continue

#                     if show_all or val1 != val2:
#                         rec = {'key': key, f'{col}_before': val1, f'{col}_after': val2}

#                         if pd.api.types.is_numeric_dtype(type(val1)) and pd.api.types.is_numeric_dtype(type(val2)):
#                             try:
#                                 rec['absolute_change'] = val2 - val1
#                                 rec['pct_change'] = self.calculate_pct_change(val1, val2)
#                             except Exception:
#                                 pass  # silently skip if computation fails

#                         records.append(rec)

#             if records:
#                 changes_df = pd.DataFrame(records)
#                 results[col] = {'data': changes_df, 'top_n': top_n}
#                 print(f"DEBUG: Column '{col}' - found {len(records)} changes")

#         if not results:
#             print("INFO: No differences found based on given parameters")

#         return results

#     def display_comparison(self, comparison_results):
#         """   
#         Display comparison results in a tabular format in the console.
#         """
#         if not comparison_results:
#             print("No comparison results to display.")
#             return

#         for col, result in comparison_results.items():
#             df = result['data']
#             top_n = result.get('top_n', 100)

#             print(f"\n=== Changes in '{col}' ===")
#             print(f"Total rows with changes: {len(df)}")

#             if 'absolute_change' in df.columns:
#                 df_sorted = df.reindex(df['absolute_change'].abs().sort_values(ascending=False).index)
#                 print(df_sorted.head(top_n))
#             else:
#                 print(df.head(top_n))






















import pandas as pd
import numpy as np

class Comparator:
    """
    A comparator for comparing specified columns between two pandas DataFrames,
    typically representing two periods of portfolio data.
    """

    def __init__(self):
        pass

    @staticmethod
    def calculate_pct_change(old_val, new_val):
        """Calculate percentage change between two values."""
        if pd.isna(old_val) or pd.isna(new_val):
            return np.nan
        if old_val == 0:
            return None  # safer than inf
        return ((new_val - old_val) / abs(old_val)) * 100

    def compare_dataframes(self, df1, df2, key_columns, compare_columns, show_all=False, top_n=100):
        """
        Compare two DataFrames using composite key and specified compare_columns.
        Returns a dict mapping each compared column to {'data': DataFrame, 'top_n': int}
        """
        df1 = df1.copy()
        df2 = df2.copy()

        for col in key_columns:
            if col not in df1.columns or col not in df2.columns:
                print(f"ERROR: Key column '{col}' not found in both dataframes")
                return {}

        for col in compare_columns:
            if col not in df1.columns or col not in df2.columns:
                print(f"WARNING: Compare column '{col}' not found in one of the dataframes")

        df1['composite_key'] = df1[key_columns].astype(str).agg('|'.join, axis=1)
        df2['composite_key'] = df2[key_columns].astype(str).agg('|'.join, axis=1)

        if df1['composite_key'].duplicated().any():
            print("WARNING: Duplicate keys found in df1")
        if df2['composite_key'].duplicated().any():
            print("WARNING: Duplicate keys found in df2")

        df1 = df1.set_index('composite_key')
        df2 = df2.set_index('composite_key')

        common_keys = set(df1.index).intersection(df2.index)
        print(f"DEBUG: Found {len(common_keys)} common composite keys")

        results = {}

        for col in compare_columns:
            if col not in df1.columns or col not in df2.columns:
                continue

            records = []
            for key in common_keys:
                rows1 = df1.loc[[key]] if isinstance(df1.loc[key], pd.Series) else df1.loc[key]
                rows2 = df2.loc[[key]] if isinstance(df2.loc[key], pd.Series) else df2.loc[key]

                if isinstance(rows1, pd.Series):
                    rows1 = pd.DataFrame([rows1])
                if isinstance(rows2, pd.Series):
                    rows2 = pd.DataFrame([rows2])

                max_len = max(len(rows1), len(rows2))
                for i in range(max_len):
                    val1 = rows1.iloc[i][col] if i < len(rows1) else np.nan
                    val2 = rows2.iloc[i][col] if i < len(rows2) else np.nan

                    if pd.isna(val1) and pd.isna(val2):
                        if show_all:
                            records.append({'key': key, f'{col}_before': val1, f'{col}_after': val2})
                        continue

                    if show_all or val1 != val2:
                        rec = {'key': key, f'{col}_before': val1, f'{col}_after': val2}

                        if pd.api.types.is_numeric_dtype(type(val1)) and pd.api.types.is_numeric_dtype(type(val2)):
                            try:
                                rec['absolute_change'] = val2 - val1
                                rec['pct_change'] = self.calculate_pct_change(val1, val2)
                            except Exception:
                                pass

                        records.append(rec)

            if records:
                changes_df = pd.DataFrame(records)
                results[col] = {'data': changes_df, 'top_n': top_n}
                print(f"DEBUG: Column '{col}' - found {len(records)} changes")

        if not results:
            print("INFO: No differences found based on given parameters")

        return results

    def display_comparison(self, comparison_results):
        """
        Display comparison results in a tabular format in the console.
        """
        if not comparison_results:
            print("No comparison results to display.")
            return

        for col, result in comparison_results.items():
            df = result['data']
            top_n = result.get('top_n', 100)

            print(f"\n=== Changes in '{col}' ===")
            print(f"Total rows with changes: {len(df)}")

            if 'absolute_change' in df.columns:
                df_sorted = df.reindex(df['absolute_change'].abs().sort_values(ascending=False).index)
                display(df_sorted.head(top_n))  # `display()` renders nicely in Colab & Jupyter
            else:
                display(df.head(top_n))

    def export_to_excel(self, comparison_results, filename="comparison_results.xlsx", auto_download=True):
        """
        Export comparison results to an Excel file.
        Works in both Colab and Jupyter.

        Parameters:
        - comparison_results: dict from compare_dataframes
        - filename: name for the Excel file
        - auto_download: auto-download in Colab (optional)
        """
        if not comparison_results:
            print("No data to export.")
            return

        with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
            for col_name, result in comparison_results.items():
                df = result.get("data")
                if isinstance(df, pd.DataFrame):
                    # Ensure valid Excel sheet name
                    sheet_name = col_name[:31]
                    df.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"Exported results to '{filename}'")

        try:
            from google.colab import files
            if auto_download:
                files.download(filename)
        except ImportError:
            # Not in Colab
            pass
