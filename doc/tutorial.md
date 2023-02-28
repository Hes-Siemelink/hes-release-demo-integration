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

#### _Explains synthetic.xml : _

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
  * **Base64ToText** is a user-defined python class name. The SDK will find the Base64ToText class in src folder and create the instance.

### _Explains how to run local tests_

_(Optional) Explains how to run integration tests in container test framework_

### Build & Run

_Explains how to package a plugin_

_Explains how to install Remote Runner into an existing Kubernetes environment using xl kube install_
* _Configure Release and create token_
* _Launch Remote Runner_
* _Check if it self-registers in Release_

_Explains how to install plugin jar into Release_

_Explains how to publish container to be picked up by Remote Runner_

_Explains how to create a template and run_

_Explains how to troubleshoot if task isn’t picked up_

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
