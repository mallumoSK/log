package tk.mallumo.log

import android.util.Log
/**
 * ### just print input into console / android logger output
 * @see isAndroid
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