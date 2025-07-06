function [outa, outb] = module_arguments(required, optional, options, varargin)
% Docstring for module_arguments.
%
% # Examples
%
% ```matlab
% [outa, outb] = module_arguments(1, 2, "withdefault", "foo", "nodefault", 'bar');
% ```
arguments (Input)
    required (1,1) double % Required parameter
    optional (1,1) double {mustBePositive} 
        % Optional parameter
    options.withdefault string = "withdefault" % name value pair 
        % with default value
    options.nodefault char % name value pair without default value
end
arguments (Input, Repeating)
    varargin % Repeating input parameter
end

arguments (Output)
    outa (1,1) double % Output parameter
    outb (1,1) double % Another output parameter
end
end 
