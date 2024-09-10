function data = func(identifier)

    object = matlab.internal.metafunction(identifier);
    data = docstring.metadata.func(object);
end
