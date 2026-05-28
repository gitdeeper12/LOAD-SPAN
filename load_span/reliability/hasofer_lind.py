"""Hasofer-Lind exact invariant reliability index (FORM)."""

import numpy as np
from typing import List, Callable


def compute_hasofer_lind_index(
    limit_state: Callable,
    mean_values: np.ndarray,
    std_values: np.ndarray,
    max_iter: int = 100,
    tolerance: float = 1e-6
) -> float:
    """
    Compute Hasofer-Lind reliability index using FORM.
    
    β_HL = min √(x^T · x) subject to g(x) = 0
    
    where x are standardized normal variables.
    """
    # Transform to standard normal space
    n_vars = len(mean_values)
    x = np.zeros(n_vars)
    
    for iteration in range(max_iter):
        # Compute limit state and gradient at current point
        g_val, gradient = evaluate_limit_state(limit_state, x, mean_values, std_values)
        
        if abs(g_val) < tolerance:
            break
        
        # Compute direction vector
        grad_norm = np.linalg.norm(gradient)
        if grad_norm < 1e-10:
            break
        
        alpha = -gradient / grad_norm
        
        # Compute step size
        beta = g_val / grad_norm
        
        # Update design point
        x_new = -beta * alpha
        
        if np.linalg.norm(x_new - x) < tolerance:
            x = x_new
            break
        
        x = x_new
    
    # Reliability index is distance from origin
    beta_hl = np.linalg.norm(x)
    
    return beta_hl


def evaluate_limit_state(
    limit_state: Callable,
    x: np.ndarray,
    mean_values: np.ndarray,
    std_values: np.ndarray
) -> tuple:
    """
    Evaluate limit state function and its gradient in original space.
    
    Returns (g_value, gradient)
    """
    # Transform from standard normal to original space
    original_vars = mean_values + x * std_values
    
    # Evaluate limit state
    g = limit_state(original_vars)
    
    # Compute gradient using finite differences
    epsilon = 1e-6
    gradient = np.zeros_like(x)
    
    for i in range(len(x)):
        x_perturbed = x.copy()
        x_perturbed[i] += epsilon
        
        original_perturbed = mean_values + x_perturbed * std_values
        g_perturbed = limit_state(original_perturbed)
        
        gradient[i] = (g_perturbed - g) / epsilon
    
    return g, gradient


class HasoferLindSolver:
    """Iterative Hasofer-Lind reliability index solver."""
    
    def __init__(self, target_beta: float = 3.8):
        self.target_beta = target_beta
        self.beta_history = []
    
    def solve(
        self,
        limit_state: Callable,
        means: np.ndarray,
        stds: np.ndarray,
        initial_guess: np.ndarray = None
    ) -> float:
        """Solve for reliability index."""
        n = len(means)
        
        if initial_guess is None:
            x = np.zeros(n)
        else:
            x = (initial_guess - means) / stds
        
        for iteration in range(50):
            self.beta_history.append(np.linalg.norm(x))
            
            g, grad = self._evaluate(limit_state, x, means, stds)
            
            if abs(g) < 1e-6:
                break
            
            grad_norm = np.linalg.norm(grad)
            if grad_norm < 1e-10:
                break
            
            alpha = -grad / grad_norm
            beta_new = g / grad_norm
            
            x = -beta_new * alpha
        
        return np.linalg.norm(x)
    
    def _evaluate(self, limit_state, x, means, stds):
        """Evaluate limit state and gradient."""
        original = means + x * stds
        g = limit_state(original)
        
        epsilon = 1e-6
        grad = np.zeros_like(x)
        
        for i in range(len(x)):
            x_pert = x.copy()
            x_pert[i] += epsilon
            original_pert = means + x_pert * stds
            g_pert = limit_state(original_pert)
            grad[i] = (g_pert - g) / epsilon
        
        return g, grad
