import Kratos
from typing import overload

@overload
def Distribution(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]:
    """Distribution(*args, **kwargs)
    Overloaded function.

    1. Distribution(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538ce6270>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]

    2. Distribution(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538e26e30>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]

    3. Distribution(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538c86db0>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]

    4. Distribution(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f35425a55f0>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]
    """
@overload
def Distribution(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]:
    """Distribution(*args, **kwargs)
    Overloaded function.

    1. Distribution(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538ce6270>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]

    2. Distribution(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538e26e30>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]

    3. Distribution(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538c86db0>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]

    4. Distribution(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f35425a55f0>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]
    """
@overload
def Distribution(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]:
    """Distribution(*args, **kwargs)
    Overloaded function.

    1. Distribution(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538ce6270>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]

    2. Distribution(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538e26e30>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]

    3. Distribution(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538c86db0>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]

    4. Distribution(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f35425a55f0>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]
    """
@overload
def Distribution(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]:
    """Distribution(*args, **kwargs)
    Overloaded function.

    1. Distribution(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538ce6270>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]

    2. Distribution(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538e26e30>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]

    3. Distribution(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538c86db0>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]

    4. Distribution(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f35425a55f0>) -> tuple[float, float, list[float], list[int], list[float], list[float], list[float]]
    """
@overload
def Max(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, int]:
    """Max(*args, **kwargs)
    Overloaded function.

    1. Max(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538ce4cb0>) -> tuple[float, int]

    2. Max(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538e27fb0>) -> tuple[float, int]

    3. Max(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538e265b0>) -> tuple[float, int]

    4. Max(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538ce4e70>) -> tuple[float, int]
    """
@overload
def Max(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, int]:
    """Max(*args, **kwargs)
    Overloaded function.

    1. Max(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538ce4cb0>) -> tuple[float, int]

    2. Max(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538e27fb0>) -> tuple[float, int]

    3. Max(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538e265b0>) -> tuple[float, int]

    4. Max(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538ce4e70>) -> tuple[float, int]
    """
@overload
def Max(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, int]:
    """Max(*args, **kwargs)
    Overloaded function.

    1. Max(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538ce4cb0>) -> tuple[float, int]

    2. Max(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538e27fb0>) -> tuple[float, int]

    3. Max(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538e265b0>) -> tuple[float, int]

    4. Max(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538ce4e70>) -> tuple[float, int]
    """
@overload
def Max(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, int]:
    """Max(*args, **kwargs)
    Overloaded function.

    1. Max(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538ce4cb0>) -> tuple[float, int]

    2. Max(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538e27fb0>) -> tuple[float, int]

    3. Max(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538e265b0>) -> tuple[float, int]

    4. Max(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538ce4e70>) -> tuple[float, int]
    """
@overload
def Mean(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """Mean(*args, **kwargs)
    Overloaded function.

    1. Mean(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3542528eb0>) -> float

    2. Mean(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538dbccf0>) -> float

    3. Mean(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538c81c70>) -> float

    4. Mean(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538cd9d70>) -> float
    """
@overload
def Mean(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """Mean(*args, **kwargs)
    Overloaded function.

    1. Mean(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3542528eb0>) -> float

    2. Mean(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538dbccf0>) -> float

    3. Mean(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538c81c70>) -> float

    4. Mean(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538cd9d70>) -> float
    """
@overload
def Mean(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """Mean(*args, **kwargs)
    Overloaded function.

    1. Mean(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3542528eb0>) -> float

    2. Mean(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538dbccf0>) -> float

    3. Mean(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538c81c70>) -> float

    4. Mean(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538cd9d70>) -> float
    """
@overload
def Mean(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """Mean(*args, **kwargs)
    Overloaded function.

    1. Mean(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3542528eb0>) -> float

    2. Mean(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538dbccf0>) -> float

    3. Mean(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538c81c70>) -> float

    4. Mean(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538cd9d70>) -> float
    """
@overload
def Median(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """Median(*args, **kwargs)
    Overloaded function.

    1. Median(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3542529e30>) -> float

    2. Median(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538ce4bb0>) -> float

    3. Median(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538ce48b0>) -> float

    4. Median(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3542550070>) -> float
    """
@overload
def Median(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """Median(*args, **kwargs)
    Overloaded function.

    1. Median(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3542529e30>) -> float

    2. Median(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538ce4bb0>) -> float

    3. Median(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538ce48b0>) -> float

    4. Median(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3542550070>) -> float
    """
@overload
def Median(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """Median(*args, **kwargs)
    Overloaded function.

    1. Median(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3542529e30>) -> float

    2. Median(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538ce4bb0>) -> float

    3. Median(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538ce48b0>) -> float

    4. Median(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3542550070>) -> float
    """
@overload
def Median(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """Median(*args, **kwargs)
    Overloaded function.

    1. Median(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3542529e30>) -> float

    2. Median(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538ce4bb0>) -> float

    3. Median(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538ce48b0>) -> float

    4. Median(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3542550070>) -> float
    """
@overload
def Min(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, int]:
    """Min(*args, **kwargs)
    Overloaded function.

    1. Min(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538dc3e70>) -> tuple[float, int]

    2. Min(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f35427abfb0>) -> tuple[float, int]

    3. Min(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538e638f0>) -> tuple[float, int]

    4. Min(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538c80cf0>) -> tuple[float, int]
    """
@overload
def Min(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, int]:
    """Min(*args, **kwargs)
    Overloaded function.

    1. Min(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538dc3e70>) -> tuple[float, int]

    2. Min(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f35427abfb0>) -> tuple[float, int]

    3. Min(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538e638f0>) -> tuple[float, int]

    4. Min(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538c80cf0>) -> tuple[float, int]
    """
@overload
def Min(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, int]:
    """Min(*args, **kwargs)
    Overloaded function.

    1. Min(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538dc3e70>) -> tuple[float, int]

    2. Min(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f35427abfb0>) -> tuple[float, int]

    3. Min(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538e638f0>) -> tuple[float, int]

    4. Min(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538c80cf0>) -> tuple[float, int]
    """
@overload
def Min(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, int]:
    """Min(*args, **kwargs)
    Overloaded function.

    1. Min(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538dc3e70>) -> tuple[float, int]

    2. Min(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f35427abfb0>) -> tuple[float, int]

    3. Min(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538e638f0>) -> tuple[float, int]

    4. Min(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538c80cf0>) -> tuple[float, int]
    """
@overload
def RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """RootMeanSquare(*args, **kwargs)
    Overloaded function.

    1. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538c9fb70>) -> float

    2. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f35424e2bf0>) -> float

    3. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f35424d27b0>) -> float

    4. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538d73af0>) -> float
    """
@overload
def RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """RootMeanSquare(*args, **kwargs)
    Overloaded function.

    1. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538c9fb70>) -> float

    2. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f35424e2bf0>) -> float

    3. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f35424d27b0>) -> float

    4. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538d73af0>) -> float
    """
@overload
def RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """RootMeanSquare(*args, **kwargs)
    Overloaded function.

    1. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538c9fb70>) -> float

    2. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f35424e2bf0>) -> float

    3. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f35424d27b0>) -> float

    4. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538d73af0>) -> float
    """
@overload
def RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """RootMeanSquare(*args, **kwargs)
    Overloaded function.

    1. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538c9fb70>) -> float

    2. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f35424e2bf0>) -> float

    3. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f35424d27b0>) -> float

    4. RootMeanSquare(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538d73af0>) -> float
    """
@overload
def Sum(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """Sum(*args, **kwargs)
    Overloaded function.

    1. Sum(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538d9fb70>) -> float

    2. Sum(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3542547170>) -> float

    3. Sum(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3542547470>) -> float

    4. Sum(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f35425478f0>) -> float
    """
@overload
def Sum(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """Sum(*args, **kwargs)
    Overloaded function.

    1. Sum(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538d9fb70>) -> float

    2. Sum(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3542547170>) -> float

    3. Sum(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3542547470>) -> float

    4. Sum(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f35425478f0>) -> float
    """
@overload
def Sum(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """Sum(*args, **kwargs)
    Overloaded function.

    1. Sum(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538d9fb70>) -> float

    2. Sum(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3542547170>) -> float

    3. Sum(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3542547470>) -> float

    4. Sum(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f35425478f0>) -> float
    """
@overload
def Sum(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> float:
    """Sum(*args, **kwargs)
    Overloaded function.

    1. Sum(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538d9fb70>) -> float

    2. Sum(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3542547170>) -> float

    3. Sum(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3542547470>) -> float

    4. Sum(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f35425478f0>) -> float
    """
@overload
def Variance(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, float]:
    """Variance(*args, **kwargs)
    Overloaded function.

    1. Variance(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f35427aa5b0>) -> tuple[float, float]

    2. Variance(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538cda730>) -> tuple[float, float]

    3. Variance(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538cda7b0>) -> tuple[float, float]

    4. Variance(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538cda8f0>) -> tuple[float, float]
    """
@overload
def Variance(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, float]:
    """Variance(*args, **kwargs)
    Overloaded function.

    1. Variance(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f35427aa5b0>) -> tuple[float, float]

    2. Variance(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538cda730>) -> tuple[float, float]

    3. Variance(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538cda7b0>) -> tuple[float, float]

    4. Variance(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538cda8f0>) -> tuple[float, float]
    """
@overload
def Variance(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, float]:
    """Variance(*args, **kwargs)
    Overloaded function.

    1. Variance(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f35427aa5b0>) -> tuple[float, float]

    2. Variance(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538cda730>) -> tuple[float, float]

    3. Variance(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538cda7b0>) -> tuple[float, float]

    4. Variance(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538cda8f0>) -> tuple[float, float]
    """
@overload
def Variance(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = ...) -> tuple[float, float]:
    """Variance(*args, **kwargs)
    Overloaded function.

    1. Variance(model_part: Kratos.ModelPart, variable: Kratos.DoubleVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f35427aa5b0>) -> tuple[float, float]

    2. Variance(model_part: Kratos.ModelPart, variable: Kratos.Array1DVariable3, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538cda730>) -> tuple[float, float]

    3. Variance(model_part: Kratos.ModelPart, variable: Kratos.VectorVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538cda7b0>) -> tuple[float, float]

    4. Variance(model_part: Kratos.ModelPart, variable: Kratos.MatrixVariable, norm_type: str, parameters: Kratos.Parameters = <Kratos.Parameters object at 0x7f3538cda8f0>) -> tuple[float, float]
    """
