package tk.mallumo.log

import com.google.gson.GsonBuilder
import java.io.PrintWriter
import java.io.StringWriter
import java.lang.reflect.Method
import java.net.UnknownHostException

/**
 *
 * ### Global DISABLE / ENABLE logging
 * #### In android projects use as:
 *
 * LOGGER_IS_ENABLED = BuildConfig.DEBUG
 *
 * @see LOGGER_CONSOLE_FORCE
 */
var LOGGER_IS_ENABLED = true

/**
 * ### if is library user in android project BUT in junit test
 * this prevent writing output to android logger output
 */
var LOGGER_CONSOLE_FORCE = false

/**
 * ### time-counter
 */
private var lastStamp: Long = 0

/**
 * ### check if is library used in android project
 */
private fun isAndroid(): Boolean = loggerMethod != null && !LOGGER_CONSOLE_FORCE

/**
 * ### method reference of android function ```android.util.Log.e```
 */
private val loggerMethod: Method? by lazy {
    try {
        Class.forName("android.util.Log")
            .getDeclaredMethod("e", String::class.java, String::class.java)
    } catch (e: Throwable) {
        null
    }
}

/**
 * ### write to console output / android logger output three dashes
 * @see log with parameters
 * @see LOGGER_IS_ENABLED
 * @see LOGGER_CONSOLE_FORCE
 */
@Deprecated(
    message = "use log method with parameters",
    replaceWith = ReplaceWith("log(\"---\")")
)
fun log() {
    logData("---", false)
}

/**
 * ### start point for measure time in milliseconds
 * @see logTimeSpendStamp
 * @see LOGGER_IS_ENABLED
 * @see LOGGER_CONSOLE_FORCE
 */
@Suppress("unused")
fun logTimeSpendStampStart() {
    lastStamp = System.currentTimeMillis()
    logData("lastStamp logging start", false)

}

/**
 * ### entry point for measure time in milliseconds
 * ## Example
 * ```
 * logTimeSpendStampStart() //only time counter reset > "lastStamp logging start"
 *
 * repeat(20){
 *      delay(20) // do some job
 * }
 *
 * logTimeSpendStamp() // print into console spend time and reset counter > "lastStamp: (400ms)"
 *
 * delay(300) // do some job
 *
 * logTimeSpendStamp()  // print into console spend time and reset counter > "lastStamp: (300ms)"
 * ```
 * @see LOGGER_IS_ENABLED
 * @see LOGGER_CONSOLE_FORCE
 */
@Suppress("unused")
fun logTimeSpendStamp() {
    logData("lastStamp: ${System.currentTimeMillis() - lastStamp}ms", false)
    lastStamp = System.currentTimeMillis()
}

/**
 * ### Write into console / android logger serialized input with params:
 * - name of sourcecode class entry
 * - number of line in sourcecode
 * - name of function where is this function used
 *
 * @param input any object that can be serialized using the GSON library
 * @param prettyPrint if is true serialized input will has "pretty" format
 * @see LOGGER_IS_ENABLED
 * @see LOGGER_CONSOLE_FORCE
 */
fun log(input: Any?, prettyPrint: Boolean = true) {
    if (input != null && input is Exception) {
        logData(input.trace, false)
    } else {
        logData(input, prettyPrint)
    }
}

/**
 * ### If is logger enabled transfer input into json and write into console / android logger
 * @see writeConsole
 * @see getCurrentThreadTraceLine
 * @see toJson
 * @see LOGGER_IS_ENABLED
 * @see LOGGER_CONSOLE_FORCE
 */
private fun logData(input: Any?, prettyPrint: Boolean) {
    var obj = input
    if (!LOGGER_IS_ENABLED) {
        return
    }
    if (obj == null) {
        obj = "data null"
    }
    val item = try {
        if (obj is String) {
            obj
        } else {
            obj.toJson(prettyPrint)
        }
    } catch (e: Exception) {
        obj.toString()
    }

    val traceLine = getCurrentThreadTraceLine()
    writeConsole("${traceLine[0]} ${traceLine[1]}", item)

}

/**
 * ### just print input into console / android logger output
 * @see isAndroid
 */
private fun writeConsole(key: String, value: String) {
    if (!isAndroid()) {
        println("$key $value")
    } else {
        try {
            loggerMethod?.invoke(null, key, value)
        } catch (e: Exception) {
            println("$key $value")
        }
    }

}

/**
 * ### extract info about source code line
 *
 * @return trace line info of structure
 * - index [0] source file name and line in code
 * - index [1] name of function
 */
fun getCurrentThreadTraceLine(): Array<String> = try {

    val data = Thread.currentThread().stackTrace
    val indexLL = data.indexOfLast { it.fileName == "LogLine.kt" }
    val element = data[indexLL + 1]

    arrayOf("(${element.fileName}:${element.lineNumber})", "${element.methodName}-->")
} catch (e: Exception) {
    arrayOf("log", "")
}

/**
 * ### Transfer stack trace into String
 */
val Throwable?.trace: String
    get() {

        if (this == null) {
            return ""
        }

        // This is to reduce the amount of log spew that apps do in the non-error
        // condition of the network being unavailable.
        var t = this
        while (t != null) {
            if (t is UnknownHostException) {
                return ""
            }
            t = t.cause
        }

        return StringWriter().use { sw ->
            PrintWriter(sw).use { pw ->
                printStackTrace(pw)
                pw.flush()
            }
        }.toString()
    }

/**
 * ### transfer any object into json
 * @param prettyPrint enable /disable nice formatted output
 */
private fun Any?.toJson(prettyPrint: Boolean = false): String =
    GsonBuilder().apply {
        if (prettyPrint)
            setPrettyPrinting()
    }.create().toJson(this)
