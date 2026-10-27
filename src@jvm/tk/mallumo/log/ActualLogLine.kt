package tk.mallumo.log

import com.google.gson.*

/**
 * ### just print input into console / android logger output
 */
internal actual fun writeConsole(key: String, value: String, level: Level) {
    if (level in arrayOf(Level.ERROR, Level.WTF, Level.WARN)) {
        System.err.println("${level.name}: $key $value")
    } else {
        println("${level.name}: $key $value")
    }
}

/**
 * ### transfer any object into json
 * @param prettyPrint enable /disable nice formatted output
 */
internal actual fun Any?.toJson(prettyPrint: Boolean): String = GsonBuilder().apply {
    if (prettyPrint) setPrettyPrinting()
}.create().toJson(this)

internal actual fun getCurrentThreadTraceLine(offset: Int): Array<String> = try {
    val data = Thread.currentThread().stackTrace
    val indexLL = data.indexOfLast { it.fileName?.contains("LogLine.kt") == true }
    val element = (indexLL + 1 + offset).let { stackindex ->
        if (stackindex > data.lastIndex) {
            data.last()
        } else {
            data[stackindex]
        }
    }

    arrayOf("(${element.fileName}:${element.lineNumber})", "${element.methodName}-->")
} catch (e: Exception) {
    arrayOf("log", "")
}
