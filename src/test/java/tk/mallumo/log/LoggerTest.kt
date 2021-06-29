package tk.mallumo.log

import org.junit.Test

class LoggerTest {

    init {
        LOGGER_IS_ENABLED = true
        LOGGER_CONSOLE_FORCE = true
    }

    data class Input(var itemx: String = "x")

    @Test
    fun enableDisable() {
        LOGGER_IS_ENABLED = false
        println("\nenableDisable()")
        println("disabled:")
        logDEBUG("---")
        LOGGER_IS_ENABLED = true
        println("enabled:")
        logERROR("---")
        println("enableDisable()\n")
    }

    @Test
    fun line() {
        println("\nline()")
        logWARN("---")
        println("line()\n")
    }

    @Test
    fun nestedFunctions() {
        println("\nnestedFunctions()")
        fun nested2() {
            logWithOffsetDEBUG("---", 2, prettyPrint = false)
        }

        fun nested1() {
            nested2()
        }
        nested1()
        println("\nnestedFunctions()")
    }

    @Test
    fun data() {
        println("\ndata()")
        logWARN(Input(), false)
        println("data()\n")
    }

    @Test
    fun dataNice() {
        println("\ndataNice()")
        logWTF(Input())
        println("dataNice()\n")
    }
}
