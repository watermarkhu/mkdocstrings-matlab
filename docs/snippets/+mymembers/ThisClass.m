classdef ThisClass < mymembers.BaseClass
    % Class docstring.
    methods
        function obj = other_method(obj, input)
            % Method docstring
        end
        function obj = method(obj, input)
            % Method docstring
        end
        function delete(obj)
            % Destructor docstring
        end
    end

    methods (Hidden)
        function obj = hidden_method(obj, input)
            % Hidden method docstring
        end
    end

    methods (Access = private)
        function obj = private_method(obj, input)
            % Private method docstring
        end
    end

    properties (SetAccess = private)
        private_property % Private property docstring
    end
end
