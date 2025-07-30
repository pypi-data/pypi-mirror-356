import logging
from typing import Optional

import numpy as np
import pandas as pd
import torch
from tqdm import tqdm

logger = logging.getLogger(__name__)

# Add device variable to use gpu (incl mps) if available
device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "mps" if torch.backends.mps.is_available() else "cpu"
)


def reweight(
    original_weights: np.ndarray,
    loss_matrix: pd.DataFrame,
    targets_array: np.ndarray,
    dropout_rate: Optional[float] = 0.1,
    epochs: Optional[int] = 2_000,
    noise_level: Optional[float] = 10.0,
    subsample_every: Optional[int] = 50,
    learning_rate: Optional[float] = 1e-3,
) -> tuple[np.ndarray, np.ndarray]:
    """Reweight the original weights based on the loss matrix and targets.

    Args:
        original_weights (np.ndarray): Original weights to be reweighted.
        loss_matrix (pd.DataFrame): DataFrame containing the loss matrix.
        targets_array (np.ndarray): Array of target values.
        dropout_rate (float): Optional probability of dropping weights during training.
        epochs (int): Optional number of epochs for training.
        noise_level (float): Optional level of noise to add to the original weights.
        subsample_every (int): Optional frequency of subsampling during training.
        learning_rate (float): Optional learning rate for the optimizer.

    Returns:
        np.ndarray: Reweighted weights.
        np.ndarray: Indices of the original weights that were kept after subsampling.
    """
    target_names = np.array(loss_matrix.columns)

    logger.info(
        f"Starting calibration process for targets {target_names}: {targets_array}"
    )
    logger.info(
        f"Original weights - mean: {original_weights.mean():.4f}, "
        f"std: {original_weights.std():.4f}"
    )

    loss_matrix = torch.tensor(
        loss_matrix.values, dtype=torch.float32, device=device
    )
    original_indices = np.arange(loss_matrix.shape[0])

    targets_array = torch.tensor(
        targets_array, dtype=torch.float32, device=device
    )
    random_noise = np.random.random(original_weights.shape) * noise_level
    weights = torch.tensor(
        np.log(original_weights + random_noise),
        requires_grad=True,
        dtype=torch.float32,
        device=device,
    )

    logger.info(
        f"Initial weights after noise - mean: {torch.exp(weights).mean().item():.4f}, "
        f"std: {torch.exp(weights).std():.4f}"
    )

    def loss(weights: torch.Tensor) -> torch.Tensor:
        """Calculate the loss based on the current weights and targets.

        Args:
            weights (torch.Tensor): Current weights in log space.

        Returns:
            torch.Tensor: Mean squared relative error between estimated and target values.
        """
        estimate = weights @ loss_matrix
        rel_error = (
            ((estimate - targets_array) + 1) / (targets_array + 1)
        ) ** 2
        return rel_error.mean()

    def pct_close(
        weights: torch.Tensor,
        t: Optional[float] = 0.1,
    ) -> float:
        """Calculate the percentage of estimates close to targets.

        Args:
            weights (torch.Tensor): Current weights in log space.
            t (float): Threshold for closeness.

        Returns:
            float: Percentage of estimates within the threshold.
        """
        estimate = weights @ loss_matrix
        abs_error = torch.abs((estimate - targets_array) / (1 + targets_array))
        return (abs_error < t).sum() / abs_error.numel()

    def dropout_weights(weights: torch.Tensor, p: float) -> torch.Tensor:
        """Apply dropout to the weights.

        Args:
            weights (torch.Tensor): Current weights in log space.
            p (float): Probability of dropping weights.

        Returns:
            torch.Tensor: Weights after applying dropout.
        """
        if p == 0:
            return weights
        total_weight = weights.sum()
        mask = torch.rand_like(weights) < p
        masked_weights = weights.clone()
        masked_weights[mask] = 0
        masked_weights = masked_weights / masked_weights.sum() * total_weight
        return masked_weights

    optimizer = torch.optim.Adam([weights], lr=learning_rate)

    iterator = tqdm(range(epochs), desc="Reweighting progress", unit="epoch")

    loss_over_epochs = []
    l = None
    for i in iterator:
        if i % 10 == 0:
            if l == None:
                l = loss(torch.exp(weights))
                close = pct_close(torch.exp(weights))
            loss_over_epochs.append(l.item())
            iterator.set_postfix(
                {
                    "loss": l.item(),
                    "count_observations": loss_matrix.shape[0],
                    "weights_mean": torch.exp(weights).mean().item(),
                    "weights_std": torch.exp(weights).std().item(),
                    "weights_min": torch.exp(weights).min().item(),
                }
            )

            logger.info(f"Within 10% from targets: {close:.2%} \n")

            if len(loss_over_epochs) > 1:
                loss_change = loss_over_epochs[-2] - l.item()
                logger.info(
                    f"Epoch {i:4d}: Loss = {l.item():.6f}, "
                    f"Change = {loss_change:.6f} "
                    f"({'improving' if loss_change > 0 else 'worsening'})"
                )

        optimizer.zero_grad()
        running_loss = None
        for j in range(2):
            weights_ = dropout_weights(weights, dropout_rate)
            l = loss(torch.exp(weights_))
            close = pct_close(torch.exp(weights_))
            if running_loss is None:
                running_loss = l
            else:
                running_loss += l
        l = running_loss / 2

        l.backward()
        optimizer.step()

        if subsample_every > 0 and i % subsample_every == 0 and i > 0:
            weight_values = np.exp(weights.detach().cpu().numpy())

            k = 100
            # indices = indices of weights with values < 1
            indices = np.where(weight_values >= k)[0]
            loss_matrix = loss_matrix[indices, :]
            weights = weights[indices]

            logger.info(
                f"Epoch {i}: Subsampling - kept {len(indices)} observations, "
                f"removed {original_indices - len(indices)} (weights < {k})"
            )

            loss_matrix = torch.tensor(
                loss_matrix.detach().cpu(), dtype=torch.float32, device=device
            )
            weights = torch.tensor(
                weights.detach().cpu(),
                dtype=torch.float32,
                device=device,
                requires_grad=True,
            )

            original_indices = original_indices[indices]
            optimizer = torch.optim.Adam([weights], lr=learning_rate)

    logger.info(f"Reweighting completed. Final sample size: {len(weights)}")

    return torch.exp(weights).detach().cpu().numpy(), original_indices
