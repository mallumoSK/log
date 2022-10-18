package tk.mallumo.log

/**
 * ### just print input into console / android logger output
 * @see isAndroid
 */
internal actual fun writeConsole(key: String, value: String, level: Level) {
    if (level == Level.ERROR) {
        System.err.println("${level.name}: $key $value")
    } else {
        println("${level.name}: $key $value")
    }
}
