package tk.mallumo.log

/**
 * ### just print input into console / android logger output
 */
internal actual fun writeConsole(key: String, value: String, level: Level) {
    val msg = "${level.name}: $key $value"
    when(level){
        Level.VERBOSE,
        Level.DEBUG -> console.log(msg)
        Level.INFO ->  console.info(msg)
        Level.WARN ->  console.warn(msg)
        Level.ERROR ,
        Level.WTF ->  console.error(msg)
    }
}

/**
 * ### transfer any object into json
 * @param prettyPrint enable /disable nice formatted output
 */
internal actual fun Any?.toJson(prettyPrint: Boolean): String = this?.toString()?:"null"

internal actual fun getCurrentThreadTraceLine(offset: Int): Array<String> =  arrayOf("log", "")
