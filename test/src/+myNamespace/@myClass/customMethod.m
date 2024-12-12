function [average, difference] = customMethod(obj, x, y)
    % CUSTOMMETHOD A method to calculate the average and difference of inputs
    %
    % Syntax:
    %   [average, difference] = obj.customMethod(x, y)
    %
    % Inputs:
    %   obj - The object instance
    %   x - First input number
    %   y - Second input number
    %
    % Outputs:
    %   average - Average of the inputs
    %   difference - Difference between the inputs

    % Calculate the average of the inputs
    average = (x + y) / 2;
    
    % Calculate the difference between the inputs
    difference = x - y;
end
