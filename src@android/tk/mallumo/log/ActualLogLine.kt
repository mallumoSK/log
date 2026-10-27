package tk.mallumo.log

import android.util.*
import com.google.gson.*

/**
 * ### just print input into console / android logger output
 */
internal actual fun writeConsole(key: String, value: String, level: Level) {
    if (LOGGER_CONSOLE_FORCE) println("${level.key}: $key $value")
    else when (level) {
        Level.VERBOSE -> Log.v(key, value)
        Level.DEBUG -> Log.d(key, value)
        Level.INFO -> Log.i(key, value)
        Level.WARN -> Log.w(key, value)
        Level.ERROR -> Log.e(key, value)
        Level.WTF -> Log.wtf(key, value)
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
    val indexLL = data.indexOfLast { it.fileName.contains("LogLine.kt") }
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
