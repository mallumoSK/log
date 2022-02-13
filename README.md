# log

## Simple kotlin library for logging android and desktop projects

![https://mallumo.jfrog.io/artifactory/gradle-dev-local/tk/mallumo/log/](https://img.shields.io/maven-metadata/v?color=%234caf50&metadataUrl=https%3A%2F%2Fmallumo.jfrog.io%2Fartifactory%2Fgradle-dev-local%2Ftk%2Fmallumo%2Flog%2Fmaven-metadata.xml&style=for-the-badge "Version")

#### current version:
- KOTLIN: 1.6.10 ->1.6.10-10.1.0

#### older version:
 - KOTLIN: 1.6.0,  LOG:    10.0.0
 - KOTLIN: 1.5.10, LOG:    9.0.0
 - KOTLIN: 1.4.10, LOG:    8.3.0

```groovy
repositories {
    maven {
        url = uri("https://mallumo.jfrog.io/artifactory/gradle-dev-local")
    }
}

dependencies {
    implementation "tk.mallumo:log:$version_log"
}
```

### library dependency

```groovy
    implementation "org.jetbrains.kotlin:kotlin-stdlib:1.5.10"
implementation 'com.google.code.gson:gson:2.8.7'
```

### GLOBAL Enable / Disable by static variable:
```kotlin
tk.mallumo.log.LOGGER_IS_ENABLED
```

### Enable / Disable by static variable:
####  if is library used in android project BUT in junit test, this prevent writing output to android logger output
```kotlin
tk.mallumo.log.LOGGER_CONSOLE_FORCE
```

## Usage 1

```kotlin
tk.mallumo.log.logDEBUG("123")
// android-> in console will be output ([Name-Of-Class].kt:[Souce-Code-Line-Nuber]) [name-of-method]--> [input]
// desktop-> in console will be output (DEBUG: [Name-Of-Class].kt:[Souce-Code-Line-Nuber]) [name-of-method]--> [input]
//in console android: 
// (LoggerTest.kt:20) testFun--> 123
//in console desktop: 
//DEBUG: (LoggerTest.kt:20) testFun--> 123
```

## Usage 2
```kotlin
data class Input(var itemx: String = "x")
tk.mallumo.log.logWARN(input = Input(), prettyPrin = false)
//in console: 
// (LoggerTest.kt:20) testFun--> {"itemx":"x"}
```
