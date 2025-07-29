# qa_filter/main_processor.py

import argparse
import os
import yaml
from typing import Dict, Optional, Any, Tuple
import pandas as pd

import pkg_resources # 또는 from importlib import resources

from .data_handler import DataHandler
from .quality_checker import QualityChecker
from .duplication_handler import DuplicationHandler
from .report_generator import ReportGenerator

DEFAULT_CONFIG_PATH = pkg_resources.resource_filename('data_filtering', 'config/default_settings.yaml')

class MainProcessor:
    def __init__(self, config_path: Optional[str] = None, **cli_kwargs):
        abs_config_path = None
        if config_path:
            abs_config_path = os.path.abspath(config_path)

        # 1. 기본 설정 로드
        if not os.path.exists(DEFAULT_CONFIG_PATH):
             raise FileNotFoundError(f"Default config not found: {DEFAULT_CONFIG_PATH}")
        with open(DEFAULT_CONFIG_PATH, 'r', encoding='utf-8') as f:
            base_config = yaml.safe_load(f)

        # 2. 사용자 YAML 파일 설정 로드 및 병합
        config_from_yaml = base_config.copy() # 기본 설정으로 시작
        if abs_config_path and os.path.exists(abs_config_path):
            with open(abs_config_path, 'r', encoding='utf-8') as f:
                user_yaml_settings = yaml.safe_load(f)
            config_from_yaml = self._deep_update(config_from_yaml, user_yaml_settings)
        elif abs_config_path:
            print(f"Warning: User-specified config file not found at {abs_config_path}. Using defaults/base.")

        # 3. cli_kwargs (run() 함수의 kwargs 포함)를 최종적으로 병합
        # 여기서 output_dir도 cli_kwargs에 있다면 덮어쓰게 됨
        final_merged_config = self._deep_update(config_from_yaml.copy(), {k: v for k, v in cli_kwargs.items() if v is not None})

        # 4. output_dir을 최종 결정하고 절대 경로화
        # 우선순위: cli_kwargs['output_dir'] -> YAML의 'output_dir' -> 기본 설정의 'output_dir' -> 'filtered_results'
        output_dir_value_to_abs = final_merged_config.get('output_dir', 'filtered_results') # 이미 cli_kwargs/YAML이 반영된 값
        
        self.config = final_merged_config
        self.config['output_dir'] = os.path.abspath(output_dir_value_to_abs)
        
        self.data_handler = DataHandler(self.config)

    def _deep_update(self, base_dict: Dict, update_dict: Dict) -> Dict:
        """Helper function to deeply update a dictionary."""
        for key, value in update_dict.items():
            if isinstance(value, dict) and key in base_dict and isinstance(base_dict[key], dict):
                base_dict[key] = self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
        return base_dict

    def _load_and_merge_configs(self, user_config_path: Optional[str] = None, **cli_kwargs) -> Dict:
        """Loads configurations in order: default, user_file (absolute path), cli_kwargs."""
        if not os.path.exists(DEFAULT_CONFIG_PATH):
             raise FileNotFoundError(f"Default configuration file not found at expected package path: {DEFAULT_CONFIG_PATH}")

        with open(DEFAULT_CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        if user_config_path: # 이미 절대 경로로 변환된 값 사용
            if os.path.exists(user_config_path):
                with open(user_config_path, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f)
                config = self._deep_update(config, user_config)
            else:
                print(f"Warning: User-specified config file not found at {user_config_path}. Using defaults.")

        # kwargs로 전달된 값 중 output_dir이 있다면, 그것도 CWD 기준으로 절대 경로화 하여 병합
        # 하지만 kwargs는 보통 __init__에서 먼저 처리되므로, 여기서는 이미 반영된 config를 사용
        # cli_kwargs는 __init__에서 이미 self.config에 병합 시도됨.
        # 여기서 cli_kwargs를 다시 병합하기보다, __init__에서 config['output_dir']을 절대경로화 하는 것이 더 적절.
        # (위 __init__ 수정안에서 이미 반영됨)
        config = self._deep_update(config, {k: v for k, v in cli_kwargs.items() if v is not None and k != 'output_dir'}) # output_dir은 이미 처리
        
        return config

    def process(self, input_csv_path: str, 
                q_col: Optional[str] = None, 
                a_col: Optional[str] = None, 
                qa_col: Optional[str] = None, 
                encoding: Optional[str] = None) -> None:
        """
        Main processing pipeline.
        CLI args for q_col, a_col, qa_col, encoding will override config file settings.
        """
        # 사용자가 제공한 input_csv_path를 CWD 기준으로 절대 경로화
        abs_input_csv_path = os.path.abspath(input_csv_path)

        print(f"Starting processing for: {abs_input_csv_path}") # 절대 경로 사용
        
        # Resolve effective input parameters
        effective_q_col = q_col if q_col is not None else self.config.get('q_col')
        effective_a_col = a_col if a_col is not None else self.config.get('a_col')
        effective_qa_col = qa_col if qa_col is not None else self.config.get('qa_col')
        effective_encoding = encoding if encoding is not None else self.config.get('encoding', 'utf-8')

        if not os.path.exists(abs_input_csv_path):
            print(f"Error: Input CSV file not found at {abs_input_csv_path}")
            return

        input_filename_for_report = os.path.basename(abs_input_csv_path)
        initial_df_info = {"total_loaded": 0, "path": abs_input_csv_path}

        try:
            print("Step 1: Loading data...")
            df = self.data_handler.load_data( # DataHandler는 이미 업데이트된 config를 사용 (output_dir 포함)
                abs_input_csv_path,
                q_col=effective_q_col,
                a_col=effective_a_col,
                qa_col=effective_qa_col,
                encoding=effective_encoding
            )
            initial_df_info["total_loaded"] = len(df)
            print(f"Successfully loaded {len(df)} rows.")
        except Exception as e:
            print(f"Error during data loading: {e}")
            report_generator = ReportGenerator(self.config, self.data_handler, input_filename_for_report)
            report_generator.generate_report(initial_df_info)
            return

        print("\nStep 2: Applying quality filters...")
        quality_checker = QualityChecker(self.config, self.data_handler)
        quality_checker.apply_filters()

        print("\nStep 3: Processing duplicates...")
        duplication_handler = DuplicationHandler(self.config, self.data_handler)
        duplication_handler.process_duplicates()

        print("\nStep 4: Saving selected data...")
        selected_df = self.data_handler.get_selected_data()
        output_csv_config = self.config.get('output_csv', {})
        output_filename = output_csv_config.get('filename', 'selected_qna_data.csv')
        
        # DataHandler.save_data는 이미 self.config에 저장된 절대 경로 output_dir을 사용
        if not selected_df.empty:
            saved_path = self.data_handler.save_data(selected_df, output_filename)
        else:
            print("No data selected after filtering. Output CSV will be empty or not created.")
            # output_dir이 없으면 ReportGenerator에서 생성 시도
            os.makedirs(self.config['output_dir'], exist_ok=True)
        
        print("\nStep 5: Generating report...")
        # ReportGenerator도 이미 self.config에 저장된 절대 경로 output_dir을 사용
        report_generator = ReportGenerator(self.config, self.data_handler, input_filename_for_report)
        report_generator.generate_report(initial_df_info)

        print("\nProcessing finished.")


def main_cli():
    parser = argparse.ArgumentParser(description="Filter and deduplicate Q&A text datasets from a CSV file.")
    parser.add_argument("input_csv_path", type=str, help="Path to the input CSV file (can be relative to current working directory).")
    parser.add_argument("--config", type=str, help="Path to a custom YAML configuration file (can be relative to CWD).")
    
    parser.add_argument("--q_col", type=str, help="Name of the question column in the CSV.")
    parser.add_argument("--a_col", type=str, help="Name of the answer column in the CSV.")
    parser.add_argument("--qa_col", type=str, help="Name of the combined question+answer column.")
    parser.add_argument("--encoding", type=str, help="Encoding of the input CSV file.")
    parser.add_argument("--output_dir", type=str, help="Directory to save results (can be relative to CWD). Overrides config.")
    
    args = parser.parse_args()

    # CLI 인자로 받은 output_dir이 있다면 kwargs로 전달하여 __init__에서 처리
    cli_provided_configs = {}
    if args.output_dir:
        cli_provided_configs['output_dir'] = args.output_dir
    # 다른 CLI 오버라이드도 kwargs로 전달 가능

    try:
        # config_path는 __init__에서 CWD 기준으로 절대경로화 됨
        processor = MainProcessor(config_path=args.config, **cli_provided_configs)
        # input_csv_path는 process 메서드에서 CWD 기준으로 절대경로화 됨
        processor.process(
            input_csv_path=args.input_csv_path,
            q_col=args.q_col,
            a_col=args.a_col,
            qa_col=args.qa_col,
            encoding=args.encoding
        )
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Configuration or Input Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main_cli()