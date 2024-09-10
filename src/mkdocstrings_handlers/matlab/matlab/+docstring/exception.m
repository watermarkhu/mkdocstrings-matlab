function exception(identifier)

    notFoundException = MException('mkdocs:callerInput', '%s %s %s', ...
        'The input', identifier, 'could not be found on the MATLAB path');
    throwAsCaller(notFoundException)

end
