import torch.nn as nn
import torch
import torch.nn.functional as F

"""
The IrisClassificationModel torch module. This is the computation graph that was used to
train the model. Refer to:
https://github.com/ritual-net/simple-ml-models/tree/main/iris_classification
"""


class IrisClassificationModel(nn.Module):
    def __init__(self, input_dim: int) -> None:
        super(IrisClassificationModel, self).__init__()
        self.layer1 = nn.Linear(input_dim, 50)
        self.layer2 = nn.Linear(50, 50)
        self.layer3 = nn.Linear(50, 3)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        x = F.softmax(self.layer3(x), dim=1)
        return x
