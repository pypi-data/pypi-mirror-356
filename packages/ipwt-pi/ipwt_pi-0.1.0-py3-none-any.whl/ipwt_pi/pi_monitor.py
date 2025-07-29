import torch
import math
from typing import Dict

def calculate_pi_from_components(
    epsilon: float,
    tau: float,
    surprise: float,
    alpha: float = 1.0,
    gamma: float = 0.5
) -> Dict[str, float]:
    normalized_error = epsilon / (tau + 1e-9)
    cognitive_cost = (1 - gamma) * normalized_error + gamma * surprise
    pi_score = math.exp(-alpha * cognitive_cost)

    return {
        "pi_score": pi_score,
        "normalized_error": normalized_error,
        "cognitive_cost": cognitive_cost,
        "epsilon": epsilon,
        "tau": tau,
        "surprise": surprise,
    }


class PIMonitor:
    def __init__(self, alpha: float = 1.0, gamma: float = 0.5):
        self.alpha = alpha
        self.gamma = gamma

    def _get_surprise(self, model: torch.nn.Module) -> float:
        if any(p.grad is None for p in model.parameters()):
            raise ValueError("Gradients not found. Please call loss_epsilon.backward() before calculate().")
        
        with torch.no_grad():
            total_norm = 0.0
            for p in model.parameters():
                if p.grad is not None:
                    param_norm = p.grad.data.norm(2)
                    total_norm += param_norm.item() ** 2
            return total_norm ** 0.5

    def _calculate_entropy(self, logits: torch.Tensor) -> float:
        probs = torch.softmax(logits, dim=-1)
        entropy = -torch.sum(probs * torch.log(probs + 1e-9), dim=-1)
        return entropy.mean().item()

    def calculate(
        self,
        model: torch.nn.Module,
        loss_epsilon: torch.Tensor,
        logits: torch.Tensor
    ) -> Dict[str, float]:
        epsilon = loss_epsilon.item()
        tau = self._calculate_entropy(logits)
        surprise = self._get_surprise(model)

        normalized_error = epsilon / (tau + 1e-9)
        cognitive_cost = (1 - self.gamma) * normalized_error + self.gamma * surprise
        pi_score = math.exp(-self.alpha * cognitive_cost)

        return {
            "pi_score": pi_score,
            "normalized_error": normalized_error,
            "surprise": surprise,
            "cognitive_cost": cognitive_cost,
            "epsilon": epsilon,
            "tau": tau,
        }
