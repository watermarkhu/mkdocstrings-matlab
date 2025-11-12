function output = typed_function(input, options)
    % Example function with typed inputs and outputs
    arguments (Input)
        input (1,1) string % The input variable
        options.keyword (1,1) double = 0 % An optional keyword argument
    end
    arguments (Output)
        output (1,:) char % The output variable
    end
    output = char(input);
end
