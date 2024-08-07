# -*- coding: utf-8 -*-

# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Base classes for evaluation."""


import dataclasses
from typing import Dict, List, Optional, Union, TYPE_CHECKING

from google.cloud.aiplatform_v1beta1.services import (
    evaluation_service as gapic_evaluation_services,
)
from vertexai.preview.evaluation.metrics import (
    _base as metrics_base,
)

if TYPE_CHECKING:
    import pandas as pd


@dataclasses.dataclass
class EvaluationRunConfig:
    """Evaluation Run Configurations.

    Attributes:
      dataset: The dataset to evaluate.
      metrics: The list of metrics, or Metric instances to evaluate.
      column_map: The dictionary of column name overrides in the dataset.
      client: The evaluation service client.
      evaluation_service_qps: The custom QPS limit for the evaluation service.
      retry_timeout: How long to keep retrying the evaluation requests, in seconds.
    """

    dataset: "pd.DataFrame"
    metrics: List[Union[str, metrics_base._Metric]]
    column_map: Dict[str, str]
    client: gapic_evaluation_services.EvaluationServiceClient
    evaluation_service_qps: float
    retry_timeout: float

    def validate_dataset_column(self, column_name: str) -> None:
        """Validates that the column names in the column map are in the dataset.

        Args:
          column_name: The column name to validate.

        Raises:
          KeyError: If any of the column names are not in the dataset.
        """
        if self.column_map.get(column_name, column_name) not in self.dataset.columns:
            raise KeyError(
                f"Required column `{self.column_map.get(column_name, column_name)}`"
                " not found in the eval dataset. The columns in the provided dataset"
                f" are {self.dataset.columns}."
            )


@dataclasses.dataclass
class EvalResult:
    """Evaluation result.

    Attributes:
      summary_metrics: The summary evaluation metrics for the evaluation run.
      metrics_table: A table containing evaluation dataset, and metric results.
      metadata: The metadata for the evaluation run.
    """

    summary_metrics: Dict[str, float]
    metrics_table: Optional["pd.DataFrame"] = None
    metadata: Optional[Dict[str, str]] = None
