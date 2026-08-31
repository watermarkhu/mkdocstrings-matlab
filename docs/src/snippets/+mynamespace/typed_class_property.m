function output = typed_class_property(opts)
    % Example function with name-value arguments from a class property.
    %
    % # Examples
    %
    % ```matlab
    % output = typed_class_property();
    % ```
    arguments (Input)
        opts.?mynamespace.classA
            % Name-value arguments matching the properties of `classA`.
    end
    arguments (Output)
        output (1,:) char % The output variable
    end
    output = char(1);
end