from ..base import BaseModel
from ...utils.metrics import L1Loss, L2Loss, HuberLoss, RSquared


class RegressorModel(BaseModel):
    name = 'regressor-model'

    @staticmethod
    def get_metrics():

        metrics = {
            "l1_loss": L1Loss(),
            "l2_loss": L2Loss(),
            "huber_loss": HuberLoss(),
            "r_squared": RSquared(),
        }

        return metrics




