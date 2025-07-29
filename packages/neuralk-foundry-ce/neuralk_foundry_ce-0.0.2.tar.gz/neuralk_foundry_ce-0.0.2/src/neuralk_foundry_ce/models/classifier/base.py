from ...workflow import Field
from ..base import BaseModel
from ...utils.metrics import CrossEntropy, ROCAUC, Precision, Recall
from ...utils.metrics import HingeLossMetric, F1ScoreMetric, AccuracyScore


class ClassifierModel(BaseModel):
    name = 'classifier-model'
    inputs = [
        Field('y_classes', 'Original classes before label encoding', required=False),
        Field('categorical_features', 'Names of columns corresponding to categorical features')
    ]
    outputs = [Field('y_score', 'Class probability distribution for each sample')]

    @staticmethod
    def get_metrics():

        metrics = {
            "cross_entropy": CrossEntropy(),
            "roc_auc": ROCAUC(),
            "precision": Precision(),
            "recall": Recall(),
            "hinge_loss": HingeLossMetric(),
            "f1_score": F1ScoreMetric(),
            "accuracy": AccuracyScore(),
        }

        return metrics




