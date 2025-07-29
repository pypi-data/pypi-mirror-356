# qa_filter/data_handler.py

import pandas as pd
import uuid
import os
from typing import List, Dict, Optional, Union

class DataHandler:
    def __init__(self, config: Dict):
        self.config = config
        self.df: Optional[pd.DataFrame] = None

    def _preprocess_text(self, text: str) -> str:
        if not isinstance(text, str):
            text = str(text) # Ensure text is string
        text = text.strip()
        text = " ".join(text.split()) # Normalize whitespace
        # text = text.lower() # Lowercasing might be better done just before semantic comparison
        return text

    def load_data(self, 
                  csv_path: str, 
                  q_col: Optional[str] = None, 
                  a_col: Optional[str] = None, 
                  qa_col: Optional[str] = None, 
                  encoding: str = "utf-8") -> pd.DataFrame:
        """
        Loads data from a CSV file.
        Prioritizes qa_col if provided, otherwise uses q_col and a_col.
        """
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Input CSV file not found: {csv_path}")

        try:
            df = pd.read_csv(csv_path, encoding=encoding, dtype=str).fillna('')
        except Exception as e:
            raise ValueError(f"Error reading CSV file {csv_path} with encoding {encoding}: {e}")

        df['id'] = [str(uuid.uuid4()) for _ in range(len(df))]
        df['status'] = 'selected' # Initial status
        df['rejection_reason'] = ''
        df['original_question'] = ''
        df['original_answer'] = ''
        df['original_text_combined'] = ''
        df['processed_text_minimal'] = ''

        if qa_col and qa_col in df.columns:
            if not q_col and not a_col: # Only qa_col is specified
                df['original_question'] = df[qa_col] # Treat whole qa_col as question for simplicity if q/a not distinct
                df['original_answer'] = '' # Or leave it empty, or some placeholder
            else: # qa_col might be present but user still specifies q_col and a_col
                if q_col and q_col in df.columns:
                     df['original_question'] = df[q_col]
                if a_col and a_col in df.columns:
                     df['original_answer'] = df[a_col]

            df['original_text_combined'] = df[qa_col]
            df['processed_text_minimal'] = df[qa_col].astype(str).apply(self._preprocess_text)

        elif q_col and a_col and q_col in df.columns and a_col in df.columns:
            df['original_question'] = df[q_col]
            df['original_answer'] = df[a_col]
            # Ensure Q and A are strings before concatenation
            df['original_text_combined'] = df[q_col].astype(str) + " " + df[a_col].astype(str)
            df['processed_text_minimal'] = df['original_text_combined'].apply(self._preprocess_text)
        
        elif q_col and q_col in df.columns: # Only q_col provided
            print(f"Warning: Only question column '{q_col}' provided. Answer column is missing.")
            df['original_question'] = df[q_col]
            df['original_text_combined'] = df[q_col]
            df['processed_text_minimal'] = df[q_col].astype(str).apply(self._preprocess_text)
        
        else:
            cols_available = ", ".join(df.columns)
            raise ValueError(
                "Insufficient column specification. "
                f"Please provide 'qa_col' or both 'q_col' and 'a_col'. "
                f"Provided: q_col='{q_col}', a_col='{a_col}', qa_col='{qa_col}'. "
                f"Available columns: {cols_available}"
            )
        
        # Handle cases where specified columns might not exist or be empty, leading to empty processed_text_minimal
        # This can be filtered out later by a length filter.
        df['processed_text_minimal'] = df['processed_text_minimal'].fillna('')

        self.df = df
        return self.df

    def save_data(self, df_to_save: pd.DataFrame, output_filename: str) -> str:
        """
        Saves the DataFrame to a CSV file in the configured output directory.
        """
        output_dir = self.config.get('output_dir', 'filtered_results')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, output_filename)
        
        # Determine columns to save based on config
        config_cols = self.config.get('output_csv', {}).get('columns', [])
        if not config_cols: # Default if not specified or empty
            config_cols = ['original_question', 'original_answer', 'processed_text_minimal']

        # Ensure only existing columns are selected
        save_columns = [col for col in config_cols if col in df_to_save.columns]
        
        # If essential columns like 'id', 'status', 'rejection_reason' are not in config_cols, 
        # but might be useful for debugging or further processing, one could add them.
        # For now, strictly adhere to config_cols.

        if not save_columns:
            print(f"Warning: No columns specified in config's output_csv.columns match the DataFrame columns. Saving all columns.")
            df_to_save.to_csv(output_path, index=False, encoding='utf-8-sig')
        else:
            df_to_save[save_columns].to_csv(output_path, index=False, encoding='utf-8-sig')
            
        print(f"Filtered data saved to: {output_path}")
        return output_path

    def get_dataframe(self) -> Optional[pd.DataFrame]:
        return self.df

    def update_status(self, ids_to_update: List[str], status: str, reason: str):
        if self.df is not None:
            self.df.loc[self.df['id'].isin(ids_to_update), 'status'] = status
            self.df.loc[self.df['id'].isin(ids_to_update), 'rejection_reason'] = reason
        else:
            print("Warning: DataFrame not loaded. Cannot update status.")

    def get_selected_data(self) -> pd.DataFrame:
        if self.df is None:
            return pd.DataFrame()
        return self.df[self.df['status'] == 'selected'].copy()

    def get_rejected_data(self) -> pd.DataFrame:
        if self.df is None:
            return pd.DataFrame()
        return self.df[self.df['status'] != 'selected'].copy()