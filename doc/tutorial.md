# SDK tutorial outline

## Welcome 

_The tutorial has a welcome section outlining the basic architecture_

_Topics covered:_
* _Tasks are run as containers. This allows you to write Release tasks using any language. We have support for Python3 and Go (soon) in the SDK_
* _SDK provides the tools to create container-based tasks_
* _Architecture: Release instance + Remote Runner_
* _Tasks are developed as container + traditional plugin jar containing metadata_

## Hello World Plugin

### Code & Test

### _Tutorial walks you through setting up a Python 3 project_

* **Install Python 3:** If you haven't already done so, you'll need to install Python 3 on your computer. You can download the latest version of Python from the official website at https://www.python.org/downloads/. Make sure to select the appropriate installer for your operating system.
* **Choose an IDE or Text Editor:** You can write Python code using any text editor, but using an IDE (Integrated Development Environment) will help you manage your project better. Some popular IDEs for Python include PyCharm, Visual Studio Code, and Spyder.
* **Create a new project:** Open your IDE and create a new project. This will typically involve creating a new folder where your project files will be stored.

### _Explains how to create a git project from template_

* **Install Git:** If you haven't already done so, you'll need to install Git on your computer. You can download the latest version of Git from the official website at https://git-scm.com/downloads. Make sure to select the appropriate installer for your operating system.
* **Open a Terminal or Command Prompt:** Open a terminal or command prompt on your computer.
* Navigate to the directory where you want to store the project: Navigate to the directory where you want to store the project on your computer using the command prompt or terminal.
* **Clone the repository:** Clone the repository by running the following command in your terminal:
* ``` 
    git clone https://github.com/xebialabs/xlr-container-helloworld-integration.git 
    ```
  Or download from https://github.com/xebialabs/xlr-container-helloworld-integration
* This will create a new directory with the name "xlr-container-helloworld-integration" in your current working directory, and clone the project files from the GitHub repository into that directory.
* **Install Dependencies:** Navigate to the project directory and install the dependencies required for the project using the following command:
* ``` 
    cd xlr-container-helloworld-integration
    pip install -r requirements.txt 
  ```
* This command will change your directory to the cloned repository and install the required Python packages listed in the requirements.txt file.


### _(Optional) Explains how to set up IDE_

* **Install PyCharm:** If you haven't already done so, you'll need to download and install PyCharm on your computer. You can download the latest version of PyCharm from the official website at https://www.jetbrains.com/pycharm/download/. Make sure to select the appropriate installer for your operating system.
* **Open the project in PyCharm:** Open PyCharm and select "Open" from the welcome screen. Navigate to the directory where you cloned the project and select it. Click "Open" to open the project in PyCharm.
* **Configure the project interpreter:** PyCharm needs to know which version of Python to use for your project. To configure the project interpreter, go to File > Settings > Project: xlr-container-helloworld-integration > Python Interpreter. Click on the gear icon and select "Add". From the dropdown menu, select "New Environment" and choose the appropriate version of Python. Click "OK" to create the new interpreter.

### _Explains project files for xlr-container-helloworld-integration_

* **resources/helloworld.png :** This file is the plugin icon for the project.
* **resources/plugin-version.properties :** This file contains the plugin name and version. The placeholder values will be replaced by the build script.
* **resources/synthetic.xml :** This file contains the task released inputs and output details. It defines the input and output fields for the task, as well as any additional properties or configurations that may be necessary.
* **src/base64_to_text.py :** This file contains the task logic for the project. It defines the behavior of the task and performs the necessary operations to convert base64-encoded text to plain text.
* **tests/test_base64_to_text.py :** This file contains the test case for the task. It includes various tests to ensure that the task logic is working correctly and handling various inputs and edge cases appropriately.
* **build.bat and build.sh :** These files build the plugin jar and publish the image to a registry. 
* **Dockerfile :** This file is used to create an image for the plugin logic. It includes the necessary steps to build and package the plugin logic in a containerized format.
* **project.properties :** This file is used to configure the plugin name, version, and registry details. It includes properties such as PLUGIN, VERSION, REGISTRY_URL, and REGISTRY_ORG, which are used by the build scripts.
* **README.md :** This file is the readme for the project. It includes information about the project, its purpose, and how to use it. It also includes any relevant installation, configuration, and usage instructions.
* **requirements.txt :** It includes a list of Python packages and their respective versions that are required to run the project. These packages can be installed using the pip package manager.

### _Explains coding for xlr-container-helloworld-integration_

#### _Explains synthetic.xml :_

  ```xml
  <synthetic xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xmlns="http://www.xebialabs.com/deployit/synthetic"
           xsi:schemaLocation="http://www.xebialabs.com/deployit/synthetic synthetic.xsd">
    <type type="HelloWorld.BaseTask" extends="xlrelease.ContainerTask" virtual="true">
        <!-- Container image - location of the task logic -->
        <property name="image" required="true" hidden="true" default="@registry.url@/@registry.org@/@project.name@:@project.version@" transient="true"/>
        <!-- Required capabilities required by all the tasks-->
        <property name="defaultRequiredCapabilities" default="container" required="true" kind="set_of_string" hidden="true" transient="true"/>
        <property name="additionalCapabilities" default="container" required="false" kind="set_of_string" hidden="true" transient="true"/>
        <!-- Task UI properties -->
        <property name="iconLocation" default="helloworld.png" hidden="true"/>
        <property name="taskColor" hidden="true" default="#667385"/>
    </type>
    <type type="HelloWorld.Base64ToText" extends="HelloWorld.BaseTask" description="Decode Base64 to text.">
        <property name="base64Value" category="input"  default="SGVsbG8gV29ybGQ=" description="Enter the text"/>
        <property name="textValue" category="output" description="Decoded text value"/>
    </type>
  </synthetic>
  ```
  * The synthetic.xml file that describes the task released inputs and output details for the HelloWorld.Base64ToText task.
  * **<type>** Defines a custom task type with a unique name, a parent type to extend, and any additional properties or configurations that the task requires. 
  * **HelloWorld.BaseTask** type defines a container image property and default capabilities for task.
  * **HelloWorld.Base64ToText** type defines properties for input and output values for task.
  * **HelloWorld** is a unique name for integration.
  * **Base64ToText** is a user-defined python class name. The SDK will find the Base64ToText class in src folder and create the instance.

#### _Explains base64_to_text.py :_
  ```python
    import logging
    import requests
    from digitalai.release.container import BaseTask
    
    logger = logging.getLogger('Digitalai')
    
    class Base64ToText(BaseTask):
    
        def __init__(self, params):
            super().__init__()
            self.params = params
            self.textValue = None
    
        def execute(self) -> None:
            try:
                base64_value = self.params['base64Value']
                response = requests.get(f'https://httpbin.org/base64/{base64_value}')
                response.raise_for_status()
                if 'Incorrect Base64 data' in response.text:
                    raise ValueError(response.text)
                self.textValue = response.text
            except Exception as e:
                logger.error("Unexpected error occurred.", exc_info=True)
                self.set_exit_code(1)
                self.set_error_message(str(e))
            finally:
                output_properties = self.get_output_properties()
                output_properties["textValue"] = self.textValue
  ```
  * The **Base64ToText** class is a subclass of BaseTask abstract class, which represents a task that can be executed.   
  * This task is specifically designed to convert a given Base64 encoded value to plain text.
  * The **Base64ToText** class has the following attributes:
    * **params**: A dictionary containing the parameters required for executing the task. This value will be passed by the SDK at runtime.
    * **textValue**: A variable that stores the resulting plain text value obtained after decoding the Base64 encoded value.  
  * The **Base64ToTex**t class has the following methods:
    * **__init__(self, params)**: Initializes an instance of the Base64ToText class. 
      * **super().__init__()**: It calls the __init__() method of its superclass BaseTask. It must be present.
      * sets the params and textValue attributes to their default values.
    * **execute(self)**: This method is an implementation of the abstract method **execute()** defined in the BaseTask class. It represents the main logic of the task. This method does the following:
      * It retrieves the base64Value parameter from the params dictionary.
      * It makes a GET request to https://httpbin.org/base64/{base64_value} endpoint with base64_value as the value of the Base64 encoded string.
      * It checks whether the response returned contains the message "Incorrect Base64 data". If yes, it raises a ValueError with the response text.
      * If the response is successful, it sets the textValue attribute with the plain text obtained by decoding the Base64 encoded string.
      * If any exception occurs during execution, an error message is logged using the **logger** object and the exit code of the task is set to 1 using the **set_exit_code()** method from **BaseTask**. Additionally, the error message is set using the **set_error_message()** method from **BaseTask**.
      * Finally, the **finally** block is executed, where the textValue attribute is added to the output properties dictionary using the **get_output_properties()** method from **BaseTask**. This dictionary is used to store the output of the task, which can be accessed by other tasks in the workflow.
  * The **BaseTask** abstract class is a blueprint for defining tasks in the SDK. It has several methods and attributes that can be utilized by subclasses of the BaseTask class. 
  * **BaseTask** abstract class contains the following methods and attributes:
    * **__init__(self):** Initializes an instance of the BaseTask class. It creates an OutputContext object with an initial exit code of 0 and an empty dictionary of output properties.
    * **execute_task(self) -> None**: Executes the task by calling the execute method. If an AbortException is raised during execution, the task's exit code is set to 1, and the program exits with a status code of 1. If any other exception is raised, the task's exit code is also set to 1.
    * **execute(self) -> None**: This is an abstract method that must be implemented by subclasses of BaseTask. It represents the main logic of the task.
    * **abort(self) -> None**: Sets the task's exit code to 1 and exits the program with a status code of 1.
    * **get_output_context(self) -> OutputContext**: Returns the OutputContext object associated with the task.
    * **get_output_properties(self) -> Dict[str, Any]**: Returns the output properties dictionary of the task's OutputContext object.
    * **set_exit_code(self, value) -> None**: Sets the exit code of the task's OutputContext object.
    * **set_error_message(self, value) -> None**: Sets the error message of the task's OutputContext object.
    * **add_comment(self, comment: str) -> None**: Logs a comment of the task.
    * **set_status_line(self, status_line: str) -> None**: Set the status of the task.
    * **add_reporting_record(self, reporting_record: Any) -> None**: Adds a reporting record to the OutputContext.

### _Explains how to run local tests_

#### _Explains test_base64_to_text.py :_
  ```python
    import unittest
    from src.base64_to_text import Base64ToText
    
    class TestBase64ToText(unittest.TestCase):
    
        def test_valid_base64Value(self):
            params = {'task_id': 'task_1', 'base64Value': 'SGVsbG8gV29ybGQ='}
            expected_output = 'Hello World'
            base64_to_text = Base64ToText(params)
            base64_to_text.execute()
            output_properties = base64_to_text.get_output_properties()
            actual_output = output_properties['textValue']
            self.assertEqual(actual_output, expected_output)
    
        def test_invalid_base64Value(self):
            params = {'task_id': 'task_2', 'base64Value': '1SGVsbG8gV29ybGQ='}
            expected_output = None
            base64_to_text = Base64ToText(params)
            base64_to_text.execute()
            output_properties = base64_to_text.get_output_properties()
            actual_output = output_properties['textValue']
            self.assertEqual(actual_output, expected_output)
    
    if __name__ == '__main__':
        unittest.main()
  ```
* This code provides a simple test suite for the Base64ToText class which converts a Base64 encoded string to plain text. The test suite contains two test cases, one with a valid Base64 encoded string and another with an invalid string.
* To run the test suite, Then, open a terminal or command prompt and navigate to the directory containing the file. Finally, run the following command:
* ```python -m unittest test_base64_to_text.py ```
* This command will execute the test suite and report the results in the terminal. If all tests pass, you should see an output like this:
* ``` Ran 2 tests in 0.001s OK```

### _(Optional) Explains how to run integration tests in container test framework_

### Build & Run

#### _Explains how to package a plugin and publish the image_
* Configure the plugin and registry details in the **project.properties**
* Open a command prompt and navigate to the root directory of your project.
* Run the build script to build the plugin jar.
  * Unix/macOS ``` sh build.sh ```
  * Windows ``` build.bat ```
  * This command will build a JAR file named **xlr-container-helloworld-integration-1.0.0.jar** in the 'build' folder.
* Run the build script to build the plugin jar and pushes a Docker image.
  * Unix/macOS ``` sh build.sh --buildImage ```
  * Windows ``` build.bat --buildImage```
  * This command will build a JAR file and push a Docker image named **xlr-container-helloworld-integration:1.0.0** to the specified registry.

#### _Explains how to install Remote Runner into an existing Kubernetes environment using xl kube install_
* _Configure Release and create token_
* _Launch Remote Runner_
* _Check if it self-registers in Release_

#### _Explains how to install plugin jar into Release_
* To install a new plugin or a new version of an existing plugin, do the following steps:
  * On the navigation bar in Digital.ai Release, click the **Settings** icon, and then click **Manage plugins**.
  * Click the **Installed** plugins tab.
  * Click **Upload** and then select and upload the plugin file from your local machine.
  * After you upload a plugin, you must restart your Digital.ai Release instance.

#### _Explains how to create a template and run_
* Create a template with the task **Hello World : Base64 To Text** and run it!

#### _Explains how to troubleshoot if task isn’t picked up_

## Integration plugin

### Jenkins plugin guided tour
* _How to define a Server_
* _How to use secrets and communicate with a third-party server_
* _How to model a long-running task using Python3 constructs_
* _How to do status line updates and task comments_
* _How to use live logging_

### Other features
* _How to access the Release API with bundled endpoints_

## Demo

_Show Release Onboarding flow_

_This highlights the following new tasks_
* _Webhook task with Oauth2 (not a container task but very useful) to interact with Digital.ai Platform API_
* _Create secrets in Vault and use either secrets directly or Vault reference_
* _Kubernetes and Kustomize tasks_
* _Postgresql task_
* _Keytool task_
* _XL apply task_

_Tasks that use API libraries (Kubernetes) or command-line tools (xl-cli, postgres, kustomize) used to be virtually impossible to create._

_Maybe rewrite to install a different Kubernetes app, not Release, to prevent ‘meta-level’ speak of using a “release in Release to create an instance of Release”_
