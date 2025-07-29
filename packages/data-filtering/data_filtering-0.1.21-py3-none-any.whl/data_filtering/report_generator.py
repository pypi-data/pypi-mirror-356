# qa_filter/report_generator.py

import os
import pandas as pd
from datetime import datetime
from typing import Dict, Any
from .data_handler import DataHandler
import json # for config overview in text report

try:
    from jinja2 import Environment, PackageLoader, select_autoescape # PackageLoader 사용
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False

class ReportGenerator:
    def __init__(self, config: Dict, data_handler: DataHandler, input_file_name: str = "N/A"):
        self.config = config
        self.data_handler = data_handler
        self.report_config = self.config.get('report', {})
        self.output_dir = self.config.get('output_dir', 'filtered_results')
        self.input_file_name = input_file_name # 입력 파일명 전달받기

        if not JINJA2_AVAILABLE and self.report_config.get('format', 'html') == 'html':
            print("Warning: Jinja2 is not installed, but HTML report format is selected. "
                  "HTML report generation will be skipped. Install Jinja2 (pip install Jinja2).")


    def _get_report_data(self, initial_df_info: Dict) -> Dict[str, Any]:
        """Gathers all data needed for the report."""
        df = self.data_handler.get_dataframe()
        if df is None:
            # df가 None일 경우, 최소한의 정보로 리포트 생성 시도
            return {
                "report_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "input_file_info": {"name": self.input_file_name, **initial_df_info},
                "summary": {
                    "total_loaded": initial_df_info.get("total_loaded", 0),
                    "total_selected": 0,
                    "total_rejected": 0,
                },
                "rejection_stats": {},
                "selected_samples": {"count": 0, "headers": [], "data": []},
                "rejected_samples": {"count": 0, "headers": [], "data": []},
                "config_overview": self._get_config_overview()
            }

        selected_df = self.data_handler.get_selected_data()
        rejected_df = self.data_handler.get_rejected_data()

        rejection_stats = {}
        if not rejected_df.empty and 'rejection_reason' in rejected_df.columns:
            rejection_stats = rejected_df['rejection_reason'].value_counts().to_dict()

        num_rejected_samples = self.report_config.get('include_rejected_samples', 0)
        rejected_sample_data = []
        rejected_sample_headers = []
        if not rejected_df.empty and num_rejected_samples > 0:
            sample_cols = ['original_question', 'original_answer', 'processed_text_minimal', 'rejection_reason']
            # 실제 존재하는 컬럼만 선택
            rejected_sample_headers = [col for col in sample_cols if col in rejected_df.columns]
            if rejected_sample_headers: # 헤더가 있어야 샘플 데이터 의미 있음
                 rejected_sample_data = rejected_df[rejected_sample_headers].head(num_rejected_samples).values.tolist()


        # 선택된 데이터 샘플도 추가 (예: 5개)
        num_selected_samples = self.report_config.get('include_selected_samples', 5) # 설정 추가 가능
        selected_sample_data = []
        selected_sample_headers = []
        if not selected_df.empty and num_selected_samples > 0:
            sample_cols = ['original_question', 'original_answer', 'processed_text_minimal']
            selected_sample_headers = [col for col in sample_cols if col in selected_df.columns]
            if selected_sample_headers:
                selected_sample_data = selected_df[selected_sample_headers].head(num_selected_samples).values.tolist()


        return {
            "report_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "input_file_info": {"name": self.input_file_name, **initial_df_info},
            "summary": {
                "total_loaded": initial_df_info.get("total_loaded", len(df)), # 로드된 아이템 수
                "total_selected": len(selected_df),
                "total_rejected": len(rejected_df),
            },
            "rejection_stats": rejection_stats,
            "selected_samples": {
                "count": num_selected_samples,
                "headers": selected_sample_headers,
                "data": selected_sample_data
            },
            "rejected_samples": {
                "count": num_rejected_samples,
                "headers": rejected_sample_headers,
                "data": rejected_sample_data
            },
            "config_overview": self._get_config_overview()
        }

    def _get_config_overview(self) -> Dict:
        """Returns a simplified overview of the configuration for the report."""
        # 중요하거나 요약이 필요한 설정만 포함
        overview = {
            "output_dir": self.config.get("output_dir"),
            "deduplication": self.config.get("deduplication", {}),
            "quality_filters": self.config.get("quality_filters", {}),
            "report_settings": self.report_config # report 섹션 자체를 포함
        }
        # 너무 길거나 민감한 정보는 제외하거나 요약할 수 있음 (예: semantic_model 전체 경로)
        if "semantic_model" in overview["deduplication"]:
             # 경로가 너무 길면 일부만 표시하거나, 파일명만 표시할 수 있음
            model_path = overview["deduplication"]["semantic_model"]
            if isinstance(model_path, str) and len(model_path) > 50:
                 overview["deduplication"]["semantic_model_short"] = "..." + model_path[-47:]
            else:
                 overview["deduplication"]["semantic_model_short"] = model_path
        return overview


    def _generate_html_report(self, report_data: Dict) -> str:
        if not JINJA2_AVAILABLE:
            return "Jinja2 is not installed. Cannot generate HTML report."

        # 현재 파일의 디렉토리를 기준으로 templates 폴더 경로 설정
        # qa_filter 모듈 내의 templates 폴더를 참조하도록 수정
        # __file__은 현재 스크립트(report_generator.py)의 경로
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        
        if not os.path.exists(os.path.join(template_dir, 'report_template.html')):
            return f"HTML template 'report_template.html' not found in {template_dir}."

        env = Environment(
            loader=PackageLoader('data_filtering', 'templates'), # 'data_filtering' 패키지 내 'templates' 폴더
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template('report_template.html')
        return template.render(report_data)

    def _generate_txt_report(self, report_data: Dict) -> str:
        lines = []
        lines.append("QA 데이터 필터링 리포트")
        lines.append("=" * 30)
        lines.append(f"리포트 생성 시간: {report_data['report_time']}")
        lines.append(f"입력 파일: {report_data['input_file_info'].get('name', 'N/A')}")
        lines.append("\n--- 요약 ---")
        lines.append(f"총 로드된 아이템 수: {report_data['summary']['total_loaded']}")
        lines.append(f"최종 선택된 아이템 수: {report_data['summary']['total_selected']}")
        lines.append(f"총 거부된 아이템 수: {report_data['summary']['total_rejected']}")

        lines.append("\n--- 거부 사유별 통계 ---")
        if report_data['rejection_stats']:
            for reason, count in report_data['rejection_stats'].items():
                lines.append(f"- {reason}: {count}")
        else:
            lines.append("거부된 아이템이 없습니다.")

        if report_data['selected_samples']['data']:
            lines.append(f"\n--- 선택된 데이터 샘플 (최대 {report_data['selected_samples']['count']}개) ---")
            # 간단히 첫 번째 컬럼(보통 질문)과 두 번째 컬럼(보통 답변)만 표시
            for row_idx, sample_row in enumerate(report_data['selected_samples']['data']):
                lines.append(f"샘플 {row_idx+1}:")
                if len(sample_row) > 0: lines.append(f"  Q: {str(sample_row[0])[:100]}...") # 첫번째 컬럼
                if len(sample_row) > 1: lines.append(f"  A: {str(sample_row[1])[:100]}...") # 두번째 컬럼
        
        if report_data['rejected_samples']['data']:
            lines.append(f"\n--- 거부된 데이터 샘플 (최대 {report_data['rejected_samples']['count']}개) ---")
            for row_idx, sample_row in enumerate(report_data['rejected_samples']['data']):
                lines.append(f"샘플 {row_idx+1}:")
                # 거부된 샘플은 original_question, original_answer, processed_text_minimal, rejection_reason 순으로 기대
                if len(sample_row) > 0: lines.append(f"  Q: {str(sample_row[0])[:70]}...")
                if len(sample_row) > 1: lines.append(f"  A: {str(sample_row[1])[:70]}...")
                if len(sample_row) > 2: lines.append(f"  Processed: {str(sample_row[2])[:70]}...")
                if len(sample_row) > 3: lines.append(f"  Reason: {sample_row[3]}")


        lines.append("\n--- 설정 정보 (일부) ---")
        # json.dumps for pretty printing dict in text
        lines.append(json.dumps(report_data['config_overview'], indent=2, ensure_ascii=False))
        
        return "\n".join(lines)

    def generate_report(self, initial_df_info: Dict) -> None:
        report_format = self.report_config.get('format', 'html').lower()
        report_filename_base = self.report_config.get('filename', 'filtering_report')
        
        os.makedirs(self.output_dir, exist_ok=True) # 출력 디렉토리 생성

        report_data = self._get_report_data(initial_df_info)
        
        report_content = ""
        file_extension = ""

        if report_format == 'html':
            if not JINJA2_AVAILABLE:
                print("Skipping HTML report generation as Jinja2 is not available.")
                # HTML 생성이 불가능하면 TXT로 fallback 할 수도 있음
                # report_format = 'txt' 
                # 또는 그냥 종료
                return
            report_content = self._generate_html_report(report_data)
            file_extension = ".html"
        elif report_format == 'txt':
            report_content = self._generate_txt_report(report_data)
            file_extension = ".txt"
        else:
            print(f"Unsupported report format: {report_format}. Supported formats are 'html' and 'txt'.")
            return

        if not report_content: # HTML 템플릿 못찾거나 하는 경우
             print("Report content is empty. Skipping file save.")
             return

        # 입력 파일명을 리포트 파일명에 추가 (선택적)
        # report_filename_with_input = f"{os.path.splitext(self.input_file_name)[0]}_{report_filename_base}{file_extension}"
        # 여기서는 설정 파일의 파일명만 사용
        report_full_filename = report_filename_base + file_extension
        report_path = os.path.join(self.output_dir, report_full_filename)

        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            print(f"Report generated successfully: {report_path}")
        except Exception as e:
            print(f"Error writing report to {report_path}: {e}")