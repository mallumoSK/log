# log

## simple kotlin library for logging android and desktop projects

## Library available at: [maven gradle](https://github.com/mallumoSK/log/packages/386680)

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
####  if is library user in android project BUT in junit test, this prevent writing output to android logger output
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
//in console: 
// (LoggerTest.kt:20) timeStamp--> lastStamp logging start
// (LoggerTest.kt:22) timeStamp--> lastStamp: 200ms
```
