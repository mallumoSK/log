# log

## Simple kotlin library for logging android and desktop projects



![https://mallumo.jfrog.io/artifactory/gradle-dev-local/tk/mallumo/log/](https://img.shields.io/maven-metadata/v?color=%234caf50&metadataUrl=https%3A%2F%2Fmallumo.jfrog.io%2Fartifactory%2Fgradle-dev-local%2Ftk%2Fmallumo%2Flog%2Fmaven-metadata.xml&style=for-the-badge "Version")

```groovy
repositories {
    maven {
        url = uri("https://mallumo.jfrog.io/artifactory/gradle-dev-local")
    }
}

dependencies {
    implementation "tk.mallumo:log:$version"
}
```

### library dependency
```groovy
    implementation "org.jetbrains.kotlin:kotlin-stdlib:1.4.0"
    implementation 'com.google.code.gson:gson:2.8.6'
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
tk.mallumo.log.log("123") // in console will be output ([Name-Of-Class].kt:[Souce-Code-Line-Nuber]) [name-of-method]--> [input]
//in console: 
// (LoggerTest.kt:20) testFun--> 123
```

## Usage 2
```kotlin
data class Input(var itemx: String = "x")
tk.mallumo.log.log(input = Input(), prettyPrin = false)
//in console: 
// (LoggerTest.kt:20) testFun--> {"itemx":"x"}
```

## Usage 3
```kotlin
logTimeSpendStampStart()
Thread.sleep(200)
logTimeSpendStamp()
Thread.sleep(1)
logTimeSpendStamp()
//in console: 
// (LoggerTest.kt:20) timeStamp--> lastStamp logging start
// (LoggerTest.kt:22) timeStamp--> lastStamp: 200ms
// (LoggerTest.kt:24) timeStamp--> lastStamp: 1ms
```
