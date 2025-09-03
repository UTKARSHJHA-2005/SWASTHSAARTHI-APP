@echo off
echo Stopping Gradle Daemon...
gradlew --stop

echo Deleting Gradle transforms cache...
rmdir /S /Q "D:\Gradle\caches\8.14.3\transforms"

echo Deleting CMake .cxx build cache...
rmdir /S /Q "D:\CODING\SwasthSaarthi\android\.cxx"

echo Running gradlew clean...
gradlew clean

echo Done! Now you can run: npx react-native run-android
pause
