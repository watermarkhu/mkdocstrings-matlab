function data = class(identifier)

    if isMATLABReleaseOlderThan('R2024a')
        metaclass = @meta.class.fromName;
    else
        metaclass = @matlab.metadata.Class.fromName;
    end

    object = metaclass(identifier);
    data = docstring.metadata.class(object);

end
