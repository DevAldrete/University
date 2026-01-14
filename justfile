# https://just.systems

default:
    echo 'Hello, world!'

new-java-project:
  mvn archetype:generate -DgroupId=com.devaldrete -DartifactId=aprende-java-01-hello -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false
