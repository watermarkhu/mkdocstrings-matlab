function result = matlab_startup(paths, expression)
% Add paths and evaluate an expression
%
% Parameters:
%     paths (string): Paths to add to the MATLAB path
%     expression (string): MATLAB startup expression

    arguments
        paths (1, :) string 
        expression (1, 1) string = string.empty() 
    end
    for path = paths
        addpath(genpath(path));
    end

    if ~isempty(expression)
        eval(expression);
    end

    result = nan;
end
