from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    train_filepath: str
    test_filepath: str

@dataclass
class DataValidationArtifact:
    validation_status: bool

    valid_train_filepath: str
    valid_test_filepath: str

    invalid_train_filepath: str
    invalid_test_filepath: str

    drift_report_filepath: str

@dataclass
class DataTransformationArtifact:
    transformed_train_filepath: str
    transformed_test_filepath: str
    transformed_object_filepath: str

@dataclass
class ClassificationMetricsArtifact:
    f1_score: float
    precision_score: float
    recall_score: float

@dataclass
class ModelTrainerArtifact:
    final_trained_model_filepath: str
    train_metric_artifact: ClassificationMetricsArtifact
    test_metric_artifact: ClassificationMetricsArtifact