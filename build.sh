#!/bin/bash

# Parse command line arguments
buildImage=false
while [ $# -gt 0 ]; do
  case "$1" in
    "--buildImage")
      buildImage=true
      ;;
  esac
  shift
done

# Remove the tmp directory and create it again
rm -rf tmp
mkdir tmp 2>/dev/null

#Remove all the carriage returns
sed 's/\r$//' project.properties > tmp/project.properties

# Read project properties from project.properties file and set them as variables
. ./tmp/project.properties

# Remove project.properties from tmp
rm tmp/project.properties

# Copy the resources directory contents to tmp
cp -R resources/. tmp/

# Replace placeholders in synthetic.xml & plugin-version.properties with values from project.properties
if [ "$(uname)" = "Darwin" ]; then
  echo "Detected MAC OS X platform"

  sed -i '' 's/@project.name@/'"$PLUGIN"'/g' tmp/plugin-version.properties
  sed -i '' 's/@project.version@/'"$VERSION"'/g' tmp/plugin-version.properties
  sed -i '' 's/@project.name@/'"$PLUGIN"'/g' tmp/synthetic.xml
  sed -i '' 's/@project.version@/'"$VERSION"'/g' tmp/synthetic.xml
  sed -i '' 's/@registry.url@/'"$REGISTRY_URL"'/g' tmp/synthetic.xml
  sed -i '' 's/@registry.org@/'"$REGISTRY_ORG"'/g' tmp/synthetic.xml
elif [ "$(expr substr $(uname -s) 1 5)" = "Linux" ]; then
  echo "Detected GNU/Linux platform"

  sed -i.bak 's/@project.name@/'"$PLUGIN"'/g' tmp/plugin-version.properties
  sed -i.bak 's/@project.version@/'"$VERSION"'/g' tmp/plugin-version.properties
  sed -i.bak 's/@project.name@/'"$PLUGIN"'/g' tmp/synthetic.xml
  sed -i.bak 's/@project.version@/'"$VERSION"'/g' tmp/synthetic.xml
  sed -i.bak 's/@registry.url@/'"$REGISTRY_URL"'/g' tmp/synthetic.xml
  sed -i.bak 's/@registry.org@/'"$REGISTRY_ORG"'/g' tmp/synthetic.xml
  rm tmp/synthetic.xml.bak
  rm tmp/plugin-version.properties.bak
fi

# Create the build directory and remove any previously created jar file
mkdir build 2>/dev/null
rm -f "build/$PLUGIN-$VERSION.jar" 2>/dev/null

# Create a jar file from the contents of the tmp directory and place it in the build directory
cd tmp
tar -cvf "../build/$PLUGIN-$VERSION.jar" *
cd ..

# Remove the tmp directory
rm -rf tmp

# If the --buildImage flag was passed, build and push a Docker image
if $buildImage; then
  docker build --tag "$REGISTRY_URL/$REGISTRY_ORG/$PLUGIN:$VERSION" .
  docker image push "$REGISTRY_URL/$REGISTRY_ORG/$PLUGIN:$VERSION"
fi
