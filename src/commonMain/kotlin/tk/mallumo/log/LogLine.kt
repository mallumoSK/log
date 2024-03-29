package tk.mallumo.log

import kotlin.native.concurrent.*

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
@Suppress("unused")
fun logVERBOSE(input: Any?, prettyPrint: Boolean = true) =
    logWithOffsetVERBOSE(input, 0, prettyPrint)

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
fun logDEBUG(input: Any?, prettyPrint: Boolean = true) =
    logWithOffsetDEBUG(input, 0, prettyPrint)

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
@Suppress("unused")
fun logINFO(input: Any?, prettyPrint: Boolean = true) =
    logWithOffsetINFO(input, 0, prettyPrint)

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
fun logWARN(input: Any?, prettyPrint: Boolean = true) =
    logWithOffsetWARN(input, 0, prettyPrint)

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
fun logERROR(input: Any?, prettyPrint: Boolean = true) =
    logWithOffsetERROR(input, 0, prettyPrint)

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
fun logWTF(input: Any?, prettyPrint: Boolean = true) =
    logWithOffsetWTF(input, 0, prettyPrint)


/**
 * ### Write into console / android logger serialized input with params:
 * - name of sourcecode class entry
 * - number of line in sourcecode
 * - name of function where is this function used
 *
 * @param input any object that can be serialized using the GSON library
 * @param offset if is logging used inside nested lambda, or inside library this is useful tool for logging upper level
 * @param prettyPrint if is true serialized input will has "pretty" format
 * @see LOGGER_IS_ENABLED
 * @see LOGGER_CONSOLE_FORCE
 */
fun logWithOffsetVERBOSE(input: Any?, offset: Int, prettyPrint: Boolean = true) {
    logWithOffset(input, offset, prettyPrint, level = Level.VERBOSE)
}

/**
 * ### Write into console / android logger serialized input with params:
 * - name of sourcecode class entry
 * - number of line in sourcecode
 * - name of function where is this function used
 *
 * @param input any object that can be serialized using the GSON library
 * @param offset if is logging used inside nested lambda, or inside library this is useful tool for logging upper level
 * @param prettyPrint if is true serialized input will has "pretty" format
 * @see LOGGER_IS_ENABLED
 * @see LOGGER_CONSOLE_FORCE
 */
fun logWithOffsetDEBUG(input: Any?, offset: Int, prettyPrint: Boolean = true) {
    logWithOffset(input, offset, prettyPrint, level = Level.DEBUG)
}

/**
 * ### Write into console / android logger serialized input with params:
 * - name of sourcecode class entry
 * - number of line in sourcecode
 * - name of function where is this function used
 *
 * @param input any object that can be serialized using the GSON library
 * @param offset if is logging used inside nested lambda, or inside library this is useful tool for logging upper level
 * @param prettyPrint if is true serialized input will has "pretty" format
 * @see LOGGER_IS_ENABLED
 * @see LOGGER_CONSOLE_FORCE
 */
fun logWithOffsetINFO(input: Any?, offset: Int, prettyPrint: Boolean = true) {
    logWithOffset(input, offset, prettyPrint, level = Level.INFO)
}

/**
 * ### Write into console / android logger serialized input with params:
 * - name of sourcecode class entry
 * - number of line in sourcecode
 * - name of function where is this function used
 *
 * @param input any object that can be serialized using the GSON library
 * @param offset if is logging used inside nested lambda, or inside library this is useful tool for logging upper level
 * @param prettyPrint if is true serialized input will has "pretty" format
 * @see LOGGER_IS_ENABLED
 * @see LOGGER_CONSOLE_FORCE
 */
fun logWithOffsetWARN(input: Any?, offset: Int, prettyPrint: Boolean = true) {
    logWithOffset(input, offset, prettyPrint, level = Level.WARN)
}

/**
 * ### Write into console / android logger serialized input with params:
 * - name of sourcecode class entry
 * - number of line in sourcecode
 * - name of function where is this function used
 *
 * @param input any object that can be serialized using the GSON library
 * @param offset if is logging used inside nested lambda, or inside library this is useful tool for logging upper level
 * @param prettyPrint if is true serialized input will has "pretty" format
 * @see LOGGER_IS_ENABLED
 * @see LOGGER_CONSOLE_FORCE
 */
fun logWithOffsetERROR(input: Any?, offset: Int, prettyPrint: Boolean = true) {
    logWithOffset(input, offset, prettyPrint, level = Level.ERROR)
}

/**
 * ### Write into console / android logger serialized input with params:
 * - name of sourcecode class entry
 * - number of line in sourcecode
 * - name of function where is this function used
 *
 * @param input any object that can be serialized using the GSON library
 * @param offset if is logging used inside nested lambda, or inside library this is useful tool for logging upper level
 * @param prettyPrint if is true serialized input will has "pretty" format
 * @see LOGGER_IS_ENABLED
 * @see LOGGER_CONSOLE_FORCE
 */
fun logWithOffsetWTF(input: Any?, offset: Int, prettyPrint: Boolean = true) {
    logWithOffset(input, offset, prettyPrint, level = Level.WTF)
}

private fun logWithOffset(input: Any?, offset: Int, prettyPrint: Boolean = true, level: Level) {
    if (input != null && input is Exception) {
        logData(input.stackTraceToString(), false, offset, level)
    } else {
        logData(input, prettyPrint, offset, level)
    }
}

/**
 * ### If is logger enabled transfer input into json and write into console / android logger * @param offset = if is logger used inside nested lambda, or inside library this is useful tool for logging upper level
 * @param offset = if is logging used inside nested lambda, or inside library this is useful tool for logging upper level
 * @see writeConsole
 * @see getCurrentThreadTraceLine
 * @see toJson
 * @see LOGGER_IS_ENABLED
 * @see LOGGER_CONSOLE_FORCE
 */
private fun logData(input: Any?, prettyPrint: Boolean, offset: Int = 0, level: Level) {

    if (!LOGGER_IS_ENABLED) {
        return
    }

    val traceLine = getCurrentThreadTraceLine(offset)
    writeConsole(
        key = "${traceLine[0]} ${traceLine[1]}",
        value = input.extractMessage(prettyPrint),
        level = level
    )

}

/**
 * ### transfer any object to readable string, in critical situations as OutOfMemory is only converted into class signature
 */
private fun Any?.extractMessage(prettyPrint: Boolean): String {
    this ?: return "data null"

    return when (this) {
        is String -> {
            if (isBlank() || isEmpty()) "EMPTY / BLANK STRING"
            else this
        }

        else -> try {
            this.toJson(prettyPrint)
        } catch (e: Throwable) {
            toString()
        }
    }
}

/**
 * ### extract info about source code line
 *
 * @param offset = if is logger used inside nested lambda, or inside library this is useful tool for logging upper level
 * @return trace line info of structure
 * - index [0] source file name and line in code
 * - index [1] name of function
 */
internal expect fun getCurrentThreadTraceLine(offset: Int): Array<String>

/**
 * ### transfer any object into json
 * @param prettyPrint enable /disable nice formatted output
 */
internal expect fun Any?.toJson(prettyPrint: Boolean): String

/**
 * ### just print input into console / android logger output
 */
internal expect fun writeConsole(key: String, value: String, level: Level)

