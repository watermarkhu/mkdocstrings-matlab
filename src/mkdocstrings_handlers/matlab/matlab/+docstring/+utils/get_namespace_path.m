function path = get_namespace_path(object, parents)

    arguments
        object (1,1) matlab.metadata.Namespace
        parents (1,1) double {mustBeInteger, mustBeNonnegative} = 0
    end

    if ~isempty(object.ClassList)

        function_path = which(sprintf("%s.%s", object.Name, object.ClassList(1).Name));
        path = fileparts(function_path);
    elseif ~isempty(object.FunctionList)
        
        function_path = which(sprintf("%s.%s", object.Name, object.FunctionList(1).Name));
        path = fileparts(function_path);
    elseif ~isempty(object.InnerNamespaces)
        path = docstring.utils.get_namespace_path(...
            object.InnerNamespaces(1), parents + 1);
    else
        error("Cannot get path of namespace %s", object.Name);
    end

    for i = 1:parents
        path = fileparts(path);
    end
end
