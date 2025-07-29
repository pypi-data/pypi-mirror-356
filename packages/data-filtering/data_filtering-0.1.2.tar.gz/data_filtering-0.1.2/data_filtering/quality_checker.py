# qa_filter/quality_checker.py

import pandas as pd
from langdetect import detect_langs, LangDetectException
from typing import Dict
from .data_handler import DataHandler

class QualityChecker:
    def __init__(self, config: Dict, data_handler: DataHandler):
        self.config = config
        self.data_handler = data_handler
        self.quality_config = self.config.get('quality_filters', {})

    def apply_filters(self) -> None:
        """Applies all configured quality filters."""
        if self.data_handler.get_dataframe() is None or self.data_handler.get_dataframe().empty:
            print("DataFrame not loaded or empty in DataHandler. Skipping quality filters.")
            return
            
        print("Applying quality filters...")
        self._filter_by_length()
        self._filter_by_language()
        print("Quality filtering complete.")

    def _filter_by_length(self) -> None:
        length_config = self.quality_config.get('length')
        if not length_config or not length_config.get('enable', False): # 'enable' 확인 추가
            print("Length filter is disabled in the configuration.")
            return

        min_len = length_config.get('min', 0)
        max_len = length_config.get('max', float('inf'))
        
        df = self.data_handler.get_dataframe()
        # df가 None인 경우는 apply_filters에서 이미 처리했지만, 안전을 위해 한 번 더 확인
        if df is None or 'processed_text_minimal' not in df.columns:
            print("Warning: 'processed_text_minimal' column not found or DataFrame is None for length filtering.")
            return

        # Process only 'selected' items
        # status가 없는 경우 (최초 로드 직후) 또는 'selected'인 아이템 대상
        # selected_df = df[df['status'] == 'selected'].copy() # 이전 로직
        # 더 일반적으로, 아직 reject되지 않은 모든 row에 대해 길이 필터를 적용하도록 변경
        # 또는, status 컬럼이 없다면 모든 row에 대해 적용
        if 'status' in df.columns:
            target_df = df[df['status'] == 'selected'].copy()
        else: # status 컬럼이 아직 없을 수도 있음 (예: DataHandler 직후 QualityChecker가 처음 불릴 때)
              # 하지만 DataHandler에서 status를 'selected'로 초기화하므로 이 경우는 드묾.
              # 만약을 위해 모든 df를 대상으로 할 수 있으나, 'selected'가 명확.
            target_df = df.copy()


        if target_df.empty:
            print("No items currently in 'selected' status (or DataFrame is empty) to apply length filter.")
            return
            
        # Calculate length of 'processed_text_minimal'
        lengths = target_df['processed_text_minimal'].astype(str).str.len()

        # Filter by min length
        short_ids = target_df[lengths < min_len]['id'].tolist()
        if short_ids:
            reason = f"Too short (min: {min_len} chars)"
            self.data_handler.update_status(short_ids, 'rejected_length', reason)
            print(f"Rejected {len(short_ids)} items for being too short.")

        # Filter by max length (on items that are still 'selected' after min_len check)
        # Re-fetch selected items as status might have changed by the min_len filter
        current_df_state = self.data_handler.get_dataframe() # refresh df from data_handler
        if 'status' in current_df_state.columns:
            target_df_after_min = current_df_state[current_df_state['status'] == 'selected'].copy()
        else:
            target_df_after_min = current_df_state.copy()


        if target_df_after_min.empty:
            # print("No items remaining in 'selected' status after min length filter to apply max length filter.")
            return # 더 이상 처리할 'selected' 아이템이 없으면 종료

        lengths_after_min = target_df_after_min['processed_text_minimal'].astype(str).str.len()
        long_ids = target_df_after_min[lengths_after_min > max_len]['id'].tolist()
        if long_ids:
            reason = f"Too long (max: {max_len} chars)"
            self.data_handler.update_status(long_ids, 'rejected_length', reason)
            print(f"Rejected {len(long_ids)} items for being too long.")

    def _filter_by_language(self) -> None: # 이전과 동일, 필요시 'enable' 체크 로직 추가 가능
        lang_config = self.quality_config.get('language')
        if not lang_config or not lang_config.get('enable', False):
            print("Language filter is disabled in the configuration.")
            return

        target_lang = lang_config.get('target', 'ko')
        confidence_threshold = lang_config.get('confidence_threshold', 0.7)

        df = self.data_handler.get_dataframe()
        if df is None or 'processed_text_minimal' not in df.columns:
            print("Warning: 'processed_text_minimal' column not found or DataFrame is None for language filtering.")
            return

        if 'status' in df.columns:
            selected_df = df[df['status'] == 'selected'].copy()
        else:
            selected_df = df.copy()

        if selected_df.empty:
            print("No items currently in 'selected' status (or DataFrame is empty) to apply language filter.")
            return

        rejected_lang_ids = []
        
        for index, row in selected_df.iterrows():
            text_to_check = row['processed_text_minimal']
            # langdetect는 너무 짧은 텍스트에 대해 예외 발생 또는 부정확할 수 있음
            # 최소 5자 이상일 때만 시도 (이 값은 조절 가능)
            if not text_to_check or not isinstance(text_to_check, str) or len(text_to_check.strip()) < 5:
                # 매우 짧은 텍스트는 언어 필터로 거부하기보다 길이 필터에서 처리되도록 두거나,
                # 여기서 명시적으로 거부할 수도 있음 (예: 'rejected_language_too_short')
                # 현재는 그냥 넘어감 (길이 필터가 처리할 것으로 기대)
                continue
            
            try:
                detected_langs_list = detect_langs(text_to_check)
                if detected_langs_list:
                    top_lang = detected_langs_list[0]
                    lang_code = top_lang.lang
                    confidence = top_lang.prob
                    
                    if not (lang_code == target_lang and confidence >= confidence_threshold):
                        rejected_lang_ids.append(row['id'])
                else: 
                    rejected_lang_ids.append(row['id'])
            except LangDetectException:
                rejected_lang_ids.append(row['id'])
            except Exception as e: # 그 외 예외 처리
                print(f"Error detecting language for id {row['id']} (text: '{text_to_check[:30]}...'): {e}")
                rejected_lang_ids.append(row['id']) # 예외 발생 시 일단 거부 처리

        if rejected_lang_ids:
            reason = f"Language not '{target_lang}' or confidence < {confidence_threshold} or detection error"
            self.data_handler.update_status(rejected_lang_ids, 'rejected_language', reason)
            print(f"Rejected {len(rejected_lang_ids)} items based on language filter.")