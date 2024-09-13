function data = builtin(identifier)
    if isMATLABReleaseOlderThan('R2024a')
        metaclass = @meta.class.fromName;
    else
        metaclass = @matlab.metadata.Class.fromName;
    end

    object = metaclass(identifier);

    if isempty(object)
        data.name = identifier;
        data.type = 'function';
        data.doc = help(identifier);
        data.location = string(which(identifier));
        data.inputs = struct.empty();
        data.outputs = struct.empty();
        if ~contains(identifier, '.internal.')
            data.help = sprintf('https://mathworks.com/help/matlab/ref/%s.html', lower(identifier));
        end
    else
        data = docstring.metadata.class(object, 'builtin', true);
        if ~contains(identifier, '.internal.')
            data.help = sprintf('https://mathworks.com/help/matlab/ref/%s-class.html', lower(identifier));
        end
    end
    data.builtin = true;
end
