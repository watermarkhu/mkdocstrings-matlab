import matlab.engine
from matlab.engine import MatlabExecutionError


__all__ = ["MatlabEngine", "MatlabExecutionError"]


MatlabEngine = matlab.engine.start_matlab
