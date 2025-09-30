classdef Thing
% Class docstring

methods 
    function obj = Thing(value)
        % Initialize a thing.
        arguments
            value % The thing's value.
        end
        obj.value = value;
    end
end

properties (Access = private)
    value % The thing's value.
end

end
