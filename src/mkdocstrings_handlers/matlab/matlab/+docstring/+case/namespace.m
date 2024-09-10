function data = namespace(identifier)

    currentpath = split(pwd, filesep);

    name = identifier(2:end);
    
    if isfolder(identifier)
        for i = numel(currentpath):-1:1
            directory = currentpath(i);
            if isempty(directory)
                break
            elseif strcmp(directory(1), '+')
                name = sprintf("%s.%s", directory(2:end), name);
            else
                break
            end
        end
    end

    object = matlab.metadata.Namespace.fromName(name);

    if isempty(object)
        docstring.exception(identifier)
    end

    data = docstring.metadata.namespace(object);
    data.name = name;
end
