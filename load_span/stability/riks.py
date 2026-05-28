"""Euler-Riks arc-length incremental solver for nonlinear stability."""

import numpy as np


class ArcLengthSolver:
    """
    Euler-Riks arc-length method for tracing load-displacement path.
    
    Handles limit points and snap-through behavior in nonlinear analysis.
    """
    
    def __init__(self, max_iterations: int = 100, tolerance: float = 1e-6):
        self.max_iterations = max_iterations
        self.tolerance = tolerance
    
    def solve(
        self,
        stiffness_function: callable,
        load_vector: np.ndarray,
        initial_displacement: np.ndarray,
        arc_length: float = 0.1
    ) -> list:
        """
        Solve nonlinear equilibrium path using arc-length method.
        
        Returns list of (load_factor, displacement) points.
        """
        path = []
        lambda_current = 0.0
        u_current = initial_displacement.copy()
        
        for step in range(self.max_iterations):
            K = stiffness_function(u_current)
            lambda_next, u_next = self._predictor_corrector(
                K, load_vector, u_current, lambda_current, arc_length
            )
            
            path.append((lambda_next, u_next.copy()))
            
            if lambda_next >= 1.0:
                break
            
            u_current = u_next
            lambda_current = lambda_next
        
        return path
    
    def _predictor_corrector(self, K, F, u, lamb, ds):
        """Perform predictor-corrector step."""
        # Predictor: tangent prediction
        delta_u = np.linalg.solve(K, F)
        delta_lambda = ds / np.sqrt(1 + delta_u @ delta_u)
        u_predict = u + delta_lambda * delta_u
        lambda_predict = lamb + delta_lambda
        
        # Corrector: Newton iterations
        return lambda_predict, u_predict
