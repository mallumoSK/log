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
        log("---")
        LOGGER_IS_ENABLED = true
        println("enabled:")
        log("---")
        println("enableDisable()\n")
    }

    @Test
    fun timeStamp() {
        println("\ntimeStamp()")
        logTimeSpendStampStart()
        Thread.sleep(200)
        logTimeSpendStamp()
        println("timeStamp()\n")
    }

    @Test
    fun line() {
        println("\nline()")
        log("---")
        println("line()\n")
    }

    @Test
    fun nestedFunctions() {
        println("\nnestedFunctions()")
        fun nested2() {
            logWithOffset("---", 2, prettyPrint = false)
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
        log(Input(), false)
        println("data()\n")
    }

    @Test
    fun dataNice() {
        println("\ndataNice()")
        log(Input())
        println("dataNice()\n")
    }
}
