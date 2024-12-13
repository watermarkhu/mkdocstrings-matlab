classdef myClass
    % MYCLASS A class with methods for various calculations
    %
    % Methods:
    %   calculateSumAndDifference: Calculate the sum and difference of inputs
    %   calculateProductAndQuotient: Calculate the product and quotient of inputs

    methods
        function [sumResult, diffResult] = calculateSumAndDifference(obj, num1, num2)
            % CALCULATESUMANDDIFFERENCE Calculate the sum and difference of inputs
            %
            % Inputs:
            %   obj - The object instance
            %   num1 - First input number
            %   num2 - Second input number
            %
            % Outputs:
            %   sumResult - Sum of the inputs
            %   diffResult - Difference between the inputs

            % Calculate the sum of the inputs
            sumResult = num1 + num2;
            
            % Calculate the difference between the inputs
            diffResult = num1 - num2;
        end

        function [productResult, quotientResult] = calculateProductAndQuotient(obj, numA, numB)
            % CALCULATEPRODUCTANDQUOTIENT Calculate the product and quotient of inputs
            %
            % Inputs:
            %   obj - The object instance
            %   numA - First input number
            %   numB - Second input number
            %
            % Outputs:
            %   productResult - Product of the inputs
            %   quotientResult - Quotient of the inputs

            % Calculate the product of the inputs
            productResult = numA * numB;
            
            % Calculate the quotient of the inputs
            quotientResult = numA / numB;
        end
    end
end
