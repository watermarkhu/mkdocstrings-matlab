classdef DocumentationFramework
    % DocumentationFramework - A class that represents the state of a documentation framework.
    %
    %   This class provides a way to manage and organize documentation for a software project.
    %   It allows users to create, update, and retrieve documentation for different components
    %   of the project.
    %
    %   Properties:
    %   - projectName: The name of the software project.
    %   - components: A cell array containing the names of the components in the project.
    %   - documentation: A struct that stores the documentation for each component.
    %
    %   Methods:
    %   - addComponent: Adds a new component to the documentation framework.
    %   - updateDocumentation: Updates the documentation for a specific component.
    %   - getDocumentation: Retrieves the documentation for a specific component.
    %
    %   ## Example
    %   
    %   ```matlab
    %    % Create a new documentation framework
    %    framework = DocumentationFramework('MyProject');
    %    % Add a component to the framework
    %    framework.addComponent('Component1');
    %    % Update the documentation for the component
    %    framework.updateDocumentation('Component1', 'This is the documentation for Component1.');
    %    % Retrieve the documentation for the component
    %    doc = framework.getDocumentation('Component1');
    %   ```
    %
    %   See also: addComponent, updateDocumentation, getDocumentation
    
    properties
        projectName
        components
        documentation
    end
    
    methods
        function obj = DocumentationFramework(projectName)
            % DocumentationFramework - Constructor for the DocumentationFramework class.
            %
            %   Syntax:
            %       obj = DocumentationFramework(projectName)
            %
            %   Inputs:
            %       - projectName: The name of the software project.
            %
            %   Example:
            %       framework = DocumentationFramework('MyProject');
            
            obj.projectName = projectName;
            obj.components = {};
            obj.documentation = struct();
        end
        
        function addComponent(obj, componentName)
            % addComponent - Adds a new component to the documentation framework.
            %
            %   Syntax:
            %       addComponent(obj, componentName)
            %
            %   Inputs:
            %       - componentName: The name of the component to be added.
            %
            %   Example:
            %       framework.addComponent('Component1');
            
            obj.components = [obj.components, componentName];
            obj.documentation.(componentName) = '';
        end
        
        function updateDocumentation(obj, componentName, docString)
            % updateDocumentation - Updates the documentation for a specific component.
            %
            %   Syntax:
            %       updateDocumentation(obj, componentName, docString)
            %
            %   Inputs:
            %       - componentName: The name of the component to update the documentation for.
            %       - docString: The new documentation string for the component.
            %
            %   Example:
            %       framework.updateDocumentation('Component1', 'This is the updated documentation for Component1.');
            
            obj.documentation.(componentName) = docString;
        end
        
        function doc = getDocumentation(obj, componentName)
            % getDocumentation - Retrieves the documentation for a specific component.
            %
            %   Syntax:
            %       doc = getDocumentation(obj, componentName)
            %
            %   Inputs:
            %       - componentName: The name of the component to retrieve the documentation for.
            %
            %   Outputs:
            %       - doc: The documentation string for the component.
            %
            %   Example:
            %       doc = framework.getDocumentation('Component1');
            
            doc = obj.documentation.(componentName);
        end
    end
end
