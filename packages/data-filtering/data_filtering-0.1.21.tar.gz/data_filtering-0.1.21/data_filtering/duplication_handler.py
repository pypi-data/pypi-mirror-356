import logging
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Set

import numpy as np
import pandas as pd

# scipy는 의미적 중복 클러스터링에만 필요하므로, 필요 시점에 import 오류를 처리합니다.
try:
    from scipy.cluster.hierarchy import fcluster, linkage
    from scipy.spatial.distance import pdist
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

# sentence-transformers 가용성 확인
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False


from .data_handler import DataHandler

# 로깅 설정
logger = logging.getLogger(__name__)


class EmbeddingProvider(ABC):
    """텍스트 임베딩 제공자를 위한 추상 기본 클래스 (Abstract Base Class)."""

    @abstractmethod
    def encode(self, texts: List[str], **kwargs: Any) -> np.ndarray:
        """
        주어진 텍스트 목록을 임베딩 벡터로 변환합니다.

        Args:
            texts: 인코딩할 텍스트 문자열의 리스트.
            **kwargs: 각 구현체에 특화된 추가 인자.

        Returns:
            (n_texts, embedding_dim) 형태의 2D NumPy 배열.
        """
        pass

    @staticmethod
    def normalize_embeddings(embeddings: np.ndarray) -> np.ndarray:
        """
        임베딩 벡터를 단위 길이(unit length)로 정규화합니다.
        코사인 유사도 계산 시 성능을 최적화하는 데 사용됩니다.

        Args:
            embeddings: 정규화할 임베딩 벡터 배열.

        Returns:
            정규화된 임베딩 벡터 배열.
        """
        if embeddings.shape[0] == 0:
            return embeddings
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        return embeddings / np.clip(norms, 1e-12, None)


class SentenceTransformerProvider(EmbeddingProvider):
    """'sentence-transformers' 라이브러리를 사용하는 임베딩 제공자."""

    def __init__(self, model_name: str, **kwargs: Any):
        """
        SentenceTransformer 모델로 프로바이더를 초기화합니다.

        Args:
            model_name: 불러올 모델의 이름 또는 경로.
            **kwargs: SentenceTransformer 모델에 전달될 추가 인자 (예: device).
        """
        try:
            if not SENTENCE_TRANSFORMERS_AVAILABLE:
                raise ImportError("sentence-transformers가 설치되지 않았습니다.")   
            self.model = SentenceTransformer(model_name, **kwargs)
            self._embedding_dim = self.model.get_sentence_embedding_dimension()
        except ImportError as e:
            raise ImportError(
                "SentenceTransformerProvider를 사용하려면 'sentence-transformers'가 필요합니다. "
                "'pip install sentence-transformers'로 설치해주세요."
            ) from e

    def encode(self, texts: List[str], **kwargs: Any) -> np.ndarray:
        """
        'sentence-transformers'를 사용하여 텍스트를 인코딩합니다.

        Args:
            texts: 인코딩할 텍스트 리스트.
            **kwargs: `model.encode`에 전달될 추가 인자.

        Returns:
            (n_texts, embedding_dim) 형태의 임베딩 배열.
        """
        if not texts:
            return np.zeros((0, self._embedding_dim), dtype=np.float32)
        
        embeddings = self.model.encode(
            texts, show_progress_bar=False, **kwargs
        )
        return np.asarray(embeddings, dtype=np.float32)


class _BaseAPIEmbeddingProvider(EmbeddingProvider):
    """OpenAI API 호환 엔드포인트를 사용하는 임베딩 제공자를 위한 기본 클래스."""

    def __init__(
        self,
        model_name: str,
        api_key: Optional[str] = None,
        max_retries: int = 3,
        **kwargs: Any,
    ):
        """
        API 클라이언트를 초기화하고 'instructor'로 패치합니다.

        Args:
            model_name: 사용할 임베딩 모델의 이름.
            api_key: API 키. 제공되지 않으면 환경 변수를 사용합니다.
            max_retries: API 호출 실패 시 최대 재시도 횟수.
            **kwargs: OpenAI 클라이언트 초기화에 사용될 추가 인자 (base_url, timeout 등).
        """
        try:
            import instructor
            from openai import OpenAI

            # 환경 변수 우선 순위: OPENAI_API_KEY -> GOOGLE_API_KEY
            api_key = api_key or os.getenv("OPENAI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError(
                    "API 키가 필요합니다. config 파일에 api_key를 명시하거나 "
                    "OPENAI_API_KEY 또는 GOOGLE_API_KEY 환경 변수를 설정해주세요."
                )

            client = OpenAI(
                api_key=api_key,
                max_retries=max_retries,
                **kwargs
            )
            self.client = instructor.patch(client)
            self.model_name = model_name
            self._embedding_dim: Optional[int] = None

        except ImportError as e:
            raise ImportError(
                "API 프로바이더를 사용하려면 'openai'와 'instructor' 패키지가 필요합니다. "
                "'pip install openai instructor'로 설치해주세요."
            ) from e

    def encode(self, texts: List[str], batch_size: int = 32, **kwargs: Any) -> np.ndarray:
        """
        API를 사용하여 텍스트를 배치로 인코딩하며, 자동 재시도를 지원합니다.

        Args:
            texts: 인코딩할 텍스트 리스트.
            batch_size: 각 API 호출에 포함될 텍스트의 수.
            **kwargs: `embeddings.create` API 호출에 전달될 추가 인자.

        Returns:
            (n_texts, embedding_dim) 형태의 임베딩 배열.
        """
        if not texts:
            dim = self._embedding_dim or 0
            return np.zeros((0, dim), dtype=np.float32)

        all_embeddings: List[np.ndarray] = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            try:
                response = self.client.embeddings.create(
                    model=self.model_name, input=batch, **kwargs
                )
                batch_embeddings = [np.array(data.embedding, dtype=np.float32) for data in response.data]
                
                if not batch_embeddings:
                    continue

                if self._embedding_dim is None and batch_embeddings:
                    self._embedding_dim = len(batch_embeddings[0])

                all_embeddings.extend(batch_embeddings)

            except Exception as e:
                logger.error(
                    f"인덱스 {i}에서 시작하는 배치에 대한 임베딩 생성 실패 (자동 재시도 후): {e}"
                )
                if self._embedding_dim:
                    logger.warning(f"실패한 배치를 0-벡터로 대체합니다. (차원: {self._embedding_dim})")
                    all_embeddings.extend([np.zeros(self._embedding_dim, dtype=np.float32)] * len(batch))
                else:
                    # 첫 배치부터 실패하면 차원을 알 수 없어 진행이 무의미하므로 오류 발생
                    raise RuntimeError(
                        "첫 API 호출부터 실패하여 임베딩 차원을 알 수 없습니다. "
                        "API 키 또는 모델 이름을 확인해주세요."
                    ) from e
        
        if not all_embeddings:
            return np.zeros((0, self._embedding_dim or 0), dtype=np.float32)

        return np.stack(all_embeddings)


class OpenAIEmbeddingProvider(_BaseAPIEmbeddingProvider):
    """OpenAI의 임베딩 API를 사용하는 제공자."""

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)


class GeminiEmbeddingProvider(_BaseAPIEmbeddingProvider):
    """Google의 Gemini 임베딩 API를 사용하는 제공자 (OpenAI 호환 엔드포인트)."""
    
    def __init__(self, **kwargs: Any):
        # Gemini의 기본 모델 이름과 URL을 설정 파일에서 오버라이드할 수 있도록 함
        kwargs.setdefault('model_name', 'models/embedding-001')
        kwargs.setdefault('base_url', 'https://generativelanguage.googleapis.com/v1beta')
        super().__init__(**kwargs)


def get_embedding_provider(backend: str, **kwargs: Any) -> EmbeddingProvider:
    """설정에 맞는 임베딩 프로바이더 인스턴스를 생성하는 팩토리 함수."""
    provider_map = {
        "sentence_transformers": SentenceTransformerProvider,
        "openai": OpenAIEmbeddingProvider,
        "gemini": GeminiEmbeddingProvider,
    }
    if backend not in provider_map:
        raise ValueError(f"지원하지 않는 임베딩 백엔드입니다: {backend}")
    
    # model_name은 대부분의 프로바이더에 필수적이므로 확인
    if 'model_name' not in kwargs:
        logger.warning(f"'{backend}' 설정에 'model_name'이 지정되지 않았습니다. 기본값이 사용될 수 있습니다.")

    return provider_map[backend](**kwargs)


class DuplicationHandler:
    """데이터셋의 정확한 중복 및 의미적 중복을 처리하는 클래스."""

    def __init__(self, config: Dict[str, Any], data_handler: DataHandler):
        """
        DuplicationHandler를 초기화합니다.

        Args:
            config: 'deduplication' 키를 포함하는 전체 설정 딕셔셔리.
            data_handler: 데이터를 관리하는 DataHandler 인스턴스.
        """
        self.config = config
        self.data_handler = data_handler
        self.dedup_config = self.config.get("deduplication", {})
        self.embedding_provider: Optional[EmbeddingProvider] = None
        
        # 임베딩 실행 시 사용할 파라미터를 저장할 변수
        self.embedding_encode_kwargs: Dict[str, Any] = {}

        if self.dedup_config.get("enable_semantic", False):
            self._initialize_embedding_provider()

    def _initialize_embedding_provider(self) -> None:
        """설정 파일에 기반하여 적절한 임베딩 프로바이더를 초기화합니다."""
        embedding_config = self.dedup_config.get("embedding", {})
        backend = embedding_config.get("backend")
        
        if not backend:
            logger.error("설정 파일에 임베딩 백엔드(embedding.backend)가 지정되지 않았습니다.")
            return

        try:
            provider_config = embedding_config.get(backend, {}).copy() # 원본 수정을 방지하기 위해 복사

            # --- 오류 해결을 위한 핵심 로직 ---
            # encode() 시점에 사용할 파라미터를 분리하고, init()에 필요한 것만 남김
            # API 기반 프로바이더들은 batch_size를 encode 시점에 사용
            if backend in ['openai', 'gemini']:
                batch_size = provider_config.pop('batch_size', 32) # pop으로 제거하고 기본값 설정
                self.embedding_encode_kwargs['batch_size'] = batch_size
            
            # SentenceTransformerProvider는 device 같은 파라미터를 init 시점에 사용하므로
            # 특별히 제거할 파라미터가 없음.
            # --------------------------------

            self.embedding_provider = get_embedding_provider(
                backend=backend, **provider_config # init에 필요한 인자만 전달
            )
            logger.info(f"'{backend}' 백엔드의 임베딩 프로바이더를 성공적으로 초기화했습니다.")
        except (ImportError, ValueError, Exception) as e:
            logger.error(f"'{backend}' 임베딩 프로바이더 초기화 실패: {e}")
            self.embedding_provider = None

    def process_duplicates(self) -> None:
        """설정에 따라 중복 처리 플로우를 실행합니다."""
        if not self.data_handler.get_dataframe() is not None:
            logger.warning("데이터프레임이 로드되지 않아 중복 처리를 건너뜁니다.")
            return

        logger.info("중복 데이터 처리를 시작합니다...")
        if self.dedup_config.get("enable_exact", False):
            self._remove_exact_duplicates()

        if self.dedup_config.get("enable_semantic", False):
            if self.embedding_provider:
                self._remove_semantic_duplicates()
            else:
                logger.warning(
                    "의미적 중복 제거가 활성화되었지만, 임베딩 프로바이더가 "
                    "초기화되지 않아 해당 단계를 건너뜁니다."
                )
        
        logger.info("중복 데이터 처리를 완료했습니다.")

    def _apply_keep_criterion(self, duplicate_group_df: pd.DataFrame, criterion: str) -> str:
        """
        중복 그룹에 'keep' 기준을 적용하여 보존할 항목의 ID를 반환합니다.

        Args:
            duplicate_group_df: 'id'와 'processed_text_minimal' 컬럼을 포함하는,
                                중복된 항목으로 구성된 데이터프레임.
            criterion: 보존 기준 ('first', 'longest').

        Returns:
            보존할 항목의 ID (문자열).
        """
        if 'id' not in duplicate_group_df.columns:
            raise KeyError("데이터프레임에 'id' 컬럼이 없습니다.")

        if criterion == 'longest':
            lengths = duplicate_group_df['processed_text_minimal'].astype(str).str.len()
            # idxmax()는 가장 큰 값의 첫 번째 인덱스를 반환. 동점 시 순서가 빠른 것이 선택됨.
            item_to_keep_id = duplicate_group_df.loc[lengths.idxmax()]['id']
        else: # 'first' 또는 알 수 없는 기준일 경우 기본값
            if criterion != 'first':
                logger.warning(f"알 수 없는 보존 기준 '{criterion}'. 'first'를 기본값으로 사용합니다.")
            # 그룹 내 첫 번째 항목을 유지 (pandas groupby는 원본 순서를 유지함)
            item_to_keep_id = duplicate_group_df.iloc[0]['id']
        
        return str(item_to_keep_id)

    def _update_duplicate_status(self, duplicate_ids: List[str], duplicate_type: str, reason: str) -> None:
        """중복으로 판별된 항목들의 상태를 업데이트합니다."""
        if duplicate_ids:
            self.data_handler.update_status(duplicate_ids, f'rejected_{duplicate_type}_duplicate', reason)
            logger.info(f"{len(duplicate_ids)}개의 항목을 '{duplicate_type}' 중복으로 표시했습니다.")
        else:
            logger.info(f"'{duplicate_type}' 타입의 중복 항목이 발견되지 않았습니다.")

    def _remove_exact_duplicates(self) -> None:
        """'processed_text_minimal' 열을 기준으로 정확히 일치하는 중복을 제거합니다."""
        logger.info("정확한 중복 항목을 확인합니다...")
        selected_df = self.data_handler.get_selected_data()
        
        if selected_df is None or selected_df.empty:
            logger.warning("정확한 중복을 확인할 'selected' 상태의 항목이 없습니다.")
            return

        duplicates = selected_df[selected_df.duplicated('processed_text_minimal', keep=False)]
        if duplicates.empty:
            logger.info("정확한 중복 항목이 없습니다.")
            return

        criterion = self.dedup_config.get('keep_criterion', 'first')
        ids_to_reject = []
        
        # 'sort=False'는 원본 데이터의 순서를 유지하여 'first' 기준이 올바르게 작동하도록 보장.
        for _, group in duplicates.groupby('processed_text_minimal', sort=False):
            if len(group) > 1:
                item_to_keep_id = self._apply_keep_criterion(group, criterion)
                ids_to_reject.extend([str(id_val) for id_val in group['id'] if str(id_val) != item_to_keep_id])
        
        reason = f"정확한 중복 (보존 기준: {criterion})"
        self._update_duplicate_status(ids_to_reject, 'exact', reason)

    def _find_semantic_duplicate_clusters(self, embeddings: np.ndarray, threshold: float) -> List[np.ndarray]:
        """
        계층적 군집화를 사용하여 의미적으로 유사한 항목들의 클러스터를 찾습니다.

        Args:
            embeddings: 텍스트 임베딩 배열.
            threshold: 유사도 임계값. 1.0에 가까울수록 엄격합니다.

        Returns:
            중복된 항목의 인덱스로 구성된 클러스터 리스트.
        """
        if not SCIPY_AVAILABLE:
            raise ImportError(
                "의미적 중복 제거를 위해서는 'scipy' 라이브러리가 필요합니다. "
                "'pip install scipy'로 설치해주세요."
            )
        
        # 1. 0-벡터가 아닌 유효한 임베딩만 필터링하고, 그 원래 위치를 저장합니다.
        # 벡터의 절댓값의 합이 0보다 크면 유효한 벡터로 간주합니다.
        non_zero_mask = np.abs(embeddings).sum(axis=1) > 1e-9
        valid_indices = np.where(non_zero_mask)[0]
        
        # 비교할 유효한 임베딩이 2개 미만이면 중복이 있을 수 없습니다.
        if len(valid_indices) < 2:
            return []
            
        valid_embeddings = embeddings[valid_indices]

        # 2. 유효한 임베딩에 대해서만 클러스터링을 수행합니다.
        distance_threshold = 1 - threshold
        
        # pdist는 코사인 거리를 계산. (1 - 코사인 유사도)
        distances = pdist(valid_embeddings, metric='cosine')

        # 드물게 다른 이유로 NaN이 발생할 경우를 대비한 안전장치
        if np.isnan(distances).any():
            logger.warning("거리 행렬에 예기치 않은 NaN 값이 포함되어 있습니다. "
                           "해당 값을 최대 거리(1.0)로 대체하여 계속 진행합니다.")
            distances = np.nan_to_num(distances, nan=1.0)

        # linkage는 계층적 클러스터링을 수행. 'average'는 클러스터 간 평균 거리를 사용.
        Z = linkage(distances, method='average')
        
        # 거리 임계값을 기준으로 클러스터 레이블 할당
        # 이 레이블은 'valid_embeddings' 기준의 로컬 인덱스에 해당합니다.
        local_cluster_labels = fcluster(Z, t=distance_threshold, criterion='distance')

        # 3. 로컬 클러스터 결과를 원래 인덱스로 다시 매핑합니다.
        unique_labels, counts = np.unique(local_cluster_labels, return_counts=True)
        
        final_clusters = []
        # 클러스터 크기가 1보다 큰 (즉, 중복이 있는) 그룹만 처리합니다.
        for label in unique_labels[counts > 1]:
            # 이 클러스터에 속하는 항목들의 로컬 인덱스를 찾습니다.
            local_indices_in_cluster = np.where(local_cluster_labels == label)[0]
            
            # 로컬 인덱스를 원래의 전체 인덱스(iloc)로 변환합니다.
            original_indices = valid_indices[local_indices_in_cluster]
            final_clusters.append(original_indices)
        
        return final_clusters

    def _get_embeddings_for_df(self, df: pd.DataFrame) -> np.ndarray:
        """
        데이터프레임의 텍스트에 대한 임베딩을 생성합니다.
        빈 문자열은 API 호출에서 제외하고, 결과 배열에서 0-벡터로 처리하여
        인덱스 정렬을 유지합니다.

        Args:
            df: 'processed_text_minimal' 컬럼을 포함하는 데이터프레임.

        Returns:
            입력 데이터프레임과 행의 개수가 동일한 임베딩 배열.
            빈 텍스트에 해당하는 행은 0-벡터로 채워집니다.
        """
        texts = df['processed_text_minimal']
        non_empty_mask = (texts != '') & (texts.notna())
        
        # 비어있지 않은 텍스트와 그에 해당하는 iloc 인덱스를 추출
        texts_to_encode = texts[non_empty_mask].tolist()
        iloc_positions = np.where(non_empty_mask)[0]

        if not texts_to_encode:
            logger.warning("임베딩할 텍스트가 없습니다. 모든 텍스트가 비어있을 수 있습니다.")
            # 임베딩 차원을 알 수 없으므로 (0,0) 형태의 빈 배열 반환
            return np.zeros((len(df), 0), dtype=np.float32)

        # 비어있지 않은 텍스트에 대해서만 인코딩 수행
        logger.info(f"{len(texts_to_encode)}개의 비어있지 않은 텍스트에 대한 임베딩을 생성합니다...")
        encoded_embeddings = self.embedding_provider.encode(
            texts_to_encode, **self.embedding_encode_kwargs
        )

        if encoded_embeddings.shape[0] == 0:
            logger.warning("임베딩 결과가 비어있습니다.")
            return np.zeros((len(df), 0), dtype=np.float32)

        # 전체 데이터프레임 크기에 맞는 0-벡터 배열 생성
        embedding_dim = encoded_embeddings.shape[1]
        full_embeddings = np.zeros((len(df), embedding_dim), dtype=np.float32)

        # 계산된 임베딩을 올바른 위치에 삽입
        full_embeddings[iloc_positions] = encoded_embeddings

        return full_embeddings

    def _remove_semantic_duplicates(self) -> None:
        """임베딩과 유사도 임계값을 사용하여 의미적으로 중복된 항목을 제거합니다."""
        logger.info("의미적 중복 항목 탐지를 시작합니다...")
        selected_df = self.data_handler.get_selected_data()

        if selected_df is None or len(selected_df) < 2:
            logger.info("의미적 중복을 비교할 항목이 부족합니다.")
            return

        threshold = self.dedup_config.get('semantic_threshold', 0.90)
        criterion = self.dedup_config.get('keep_criterion', 'first')
        
        try:
            embeddings = self._get_embeddings_for_df(selected_df)
            
            if embeddings.shape[1] == 0: # 임베딩 차원이 0이면 진행 불가
                logger.warning("유효한 임베딩이 생성되지 않아 의미적 중복 제거를 중단합니다.")
                return
            
            logger.info("임베딩을 기반으로 중복 클러스터를 찾습니다...")
            duplicate_clusters = self._find_semantic_duplicate_clusters(embeddings, threshold)
            
            if not duplicate_clusters:
                logger.info(f"유사도 임계값({threshold}) 기준으로 의미적 중복 항목이 발견되지 않았습니다.")
                return
            
            logger.info(f"{len(duplicate_clusters)}개의 의미적 중복 클러스터를 발견했습니다.")
            
            ids_to_reject = set()
            for cluster_indices in duplicate_clusters:
                # iloc를 사용하여 클러스터에 해당하는 행을 선택
                group_df = selected_df.iloc[cluster_indices]
                item_to_keep_id = self._apply_keep_criterion(group_df, criterion)
                
                for item_id in group_df['id']:
                    if str(item_id) != item_to_keep_id:
                        ids_to_reject.add(str(item_id))

            reason = f"의미적 중복 (유사도 ≥ {threshold:.2f}, 보존 기준: {criterion})"
            self._update_duplicate_status(list(ids_to_reject), 'semantic', reason)
                
        except ImportError as e:
            logger.error(e)
        except Exception as e:
            logger.error(f"의미적 중복 제거 중 오류 발생: {e}", exc_info=True)