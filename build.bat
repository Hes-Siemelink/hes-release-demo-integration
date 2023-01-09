@echo off

:: Parse command line arguments
set buildImage=false
for %%i in (%*) do (
  if "%%i" == "--buildImage" (
    set buildImage=true
  )
)

:: Remove the tmp directory and create it again
rd /S /Q tmp
mkdir tmp 2>nul

:: Read project properties from project.properties file and set them as variables
for /f "tokens=1,2 delims==" %%G in (project.properties) do (set %%G=%%H)

:: Copy the resources directory contents to tmp
xcopy /E /I resources tmp

:: Replace placeholders in synthetic.xml with values from project.properties
setlocal enabledelayedexpansion
(for /f "delims=" %%i in (tmp\synthetic.xml) do (
    set "line=%%i"
    set "line=!line:@project.name@=%PLUGIN%!"
    set "line=!line:@project.version@=%VERSION%!"
    set "line=!line:@registry.url@=%REGISTRY_URL%!"
    set "line=!line:@registry.org@=%REGISTRY_ORG%!"
    echo(!line!
))>"tmp\synthetic.xml.bak"
move tmp\synthetic.xml.bak tmp\synthetic.xml
:: Replace placeholders in plugin-version.properties with values from project.properties
(for /f "delims=" %%i in (tmp\plugin-version.properties) do (
    set "line=%%i"
    set "line=!line:@project.name@=%PLUGIN%!"
    set "line=!line:@project.version@=%VERSION%!"
    echo(!line!
))>"tmp\plugin-version.properties.bak"
move tmp\plugin-version.properties.bak tmp\plugin-version.properties
endlocal

:: Create the build directory and remove any previously created jar file
mkdir build 2>nul
del "build\%PLUGIN%-%VERSION%.jar" 2>nul

:: Create a jar file from the contents of the tmp directory and place it in the build directory
cd tmp
tar -cvf "..\build\%PLUGIN%-%VERSION%.jar" *
cd ..

:: Remove the tmp directory
rd /S /Q tmp

:: If the --buildImage flag was passed, build and push a Docker image
if %buildImage%==true (
    docker build --tag "%REGISTRY_URL%/%REGISTRY_ORG%/%PLUGIN%:%VERSION%" .
    docker image push "%REGISTRY_URL%/%REGISTRY_ORG%/%PLUGIN%:%VERSION%"
)
