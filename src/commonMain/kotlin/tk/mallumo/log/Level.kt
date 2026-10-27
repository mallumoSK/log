package tk.mallumo.log

internal enum class Level(val key: String) {

    VERBOSE("v"),

    /**
     * Priority constant for the println method; use Log.d.
     */
    DEBUG("d"),

    /**
     * Priority constant for the println method; use Log.i.
     */
    INFO("i"),

    /**
     * Priority constant for the println method; use Log.w.
     */
    WARN("w"),

    /**
     * Priority constant for the println method; use Log.e.
     */
    ERROR("e"),

    /**
     * Priority constant for the println method.
     */
    WTF("wtf")
}