function [sumResult, productResult] = namespacefunction(a, b, c)
    % NAMESPACEFUNCTION A function to calculate the sum and product of inputs
    %
    % Syntax:
    %   [sumResult, productResult] = namespacefunction(a, b, c)
    %
    % Inputs:
    %   a - First input number
    %   b - Second input number
    %   c - Third input number
    %
    % Outputs:
    %   sumResult - Sum of all inputs
    %   productResult - Product of all inputs

    % Calculate the sum of all inputs
    sumResult = a + b + c;
    
    % Calculate the product of all inputs
    productResult = a * b * c;
end
