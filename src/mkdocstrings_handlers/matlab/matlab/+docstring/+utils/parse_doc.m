function doc = parse_doc(object, combine)

arguments
    object (1,1) % meta.MetaData matlab.metadata.MetaData
    combine (1,1) logical = true
end

if isempty(object.DetailedDescription) || strcmp(object.DetailedDescription, "")
    doc = object.Description;
else
    if combine
        doc = sprintf("%s\n%s", object.Description, ...
            docstring.utils.dedent(object.DetailedDescription));
    else
        doc = docstring.utils.dedent(object.DetailedDescription);
    end
    
end

end

