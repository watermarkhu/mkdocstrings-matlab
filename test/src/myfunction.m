% Leading comment
%{
And another comment
%}
%% Section
% another

function [output1, output2] = myfunction(input1, input2, options)
% Perform some operation using the input arguments.
%
% Args:
%   input1: No input annotatoin
%   input2 (string): has string annotatoin
%
% Returns:
%   output1: Overruled documentation of output1
%   output2 (double): Overruled documentation of output2
arguments (Input)
    input1 (1, 1) double {mustBeNumeric} % Description of input1.
    input2 (1, 1) {mustBeNumeric} = 1 % Description of input2.
        % Some more comments
    options.Option1 (1, 1) string = 42 % Some additional information about input1.
    options.Option2 {mustBeNumeric} = 42 % Some additional information about input2.
end
arguments (Output)
    output1 (1, 1) double % Description of output1.
    output2 (1, :) double % Description of output2.
end
% Create an instance of the DocumentationFramework class
framework = DocumentationFramework();

% Perform some operation using the input arguments
result1 = framework.doSomething(input1);
result2 = framework.doSomethingElse(input2);

% Assign the results to the output arguments
output1 = result1;
output2 = result2;

end
