function output = typedFunction(input)
    % Example function with typed inputs and outputs
    arguments (Input)
        input (1,1) string % The input variable
    end
    arguments (Output)
        output (1,:) char % The output variable
    end
    output = char(input);
end
