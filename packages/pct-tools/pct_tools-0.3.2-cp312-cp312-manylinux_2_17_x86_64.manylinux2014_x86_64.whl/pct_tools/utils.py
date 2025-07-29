from __future__ import annotations

import pct_tools._ext


def subsample_matrix_vector_pair(
    input_path: str, projection: str, output_path: str, subsampling_ratio: float, pixel_width: float
) -> None:
    """Subsample matrix and b-vector for a given projection.

    Args:
        input_path: The path to the input matrices.
        projection: The projection to subsample.
        output_path: The path to the output matrices.
        subsampling_ratio: The subsampling ratio.
    """
    return pct_tools._ext.subsample_matrix_vector_pair(
        input_path, projection, output_path, subsampling_ratio, f"{pixel_width}mm"
    )
