# qa_filter/__init__.py
from typing import Optional

from .data_handler import DataHandler
from .quality_checker import QualityChecker
from .duplication_handler import DuplicationHandler
from .report_generator import ReportGenerator
from .main_processor import MainProcessor # 추가

# 라이브러리 사용자를 위한 간편 실행 함수
def run(input_csv_path: str, 
        config_path: Optional[str] = None,
        q_col: Optional[str] = None, 
        a_col: Optional[str] = None, 
        qa_col: Optional[str] = None, 
        encoding: Optional[str] = None,
        **kwargs  # For other config overrides directly
       ) -> None:
    """
    Runs the QA filtering and deduplication process.

    Args:
        input_csv_path: Path to the input CSV file.
        config_path: Path to a custom YAML configuration file.
        q_col: Name of the question column. Overrides config.
        a_col: Name of the answer column. Overrides config.
        qa_col: Name of the combined Q+A column. Overrides config.
        encoding: File encoding. Overrides config.
        **kwargs: Additional configuration options to override default or file settings.
                  Example: output_dir="new_results", 
                           deduplication={'semantic_threshold': 0.85}
    """
    try:
        # kwargs can be used to pass config overrides directly
        # The MainProcessor's _load_and_merge_configs handles deep merging of kwargs if structured.
        # For simplicity, if kwargs contain nested structures, ensure _load_and_merge_configs handles them.
        # Current _load_and_merge_configs handles flat kwargs for top-level keys.
        # For more complex overrides via kwargs, it might need adjustment or users pass nested dicts.
        
        processor = MainProcessor(config_path=config_path, **kwargs)
        processor.process(
            input_csv_path=input_csv_path,
            q_col=q_col,
            a_col=a_col,
            qa_col=qa_col,
            encoding=encoding
        )
    except Exception as e:
        print(f"An error occurred during data_filtering.run: {e}")
        # Optionally re-raise or handle more gracefully
        raise