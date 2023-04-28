import org.gradle.api.*
import org.gradle.api.plugins.*
import java.util.Properties

class Toolkit private constructor(
    private val propertiesExt: ExtraPropertiesExtension,
    private val properties: Properties
) {

    companion object {

        private lateinit var instance: Toolkit


        fun get(project: Project): Toolkit {
            if (!::instance.isInitialized) {

                val properties = Properties()
                project.rootProject.file("local.properties")
                    .takeIf { it.exists() }
                    ?.reader()
                    ?.use { properties.load(it) }

                instance = Toolkit(project.extensions.extraProperties, properties)
            }
            return instance
        }
    }

    operator fun getValue(thisRef: Any?, property: kotlin.reflect.KProperty<*>): String? = get(property.name)

    operator fun get(key: String): String? {
        val keys = listOf(
            key,
            key.replace("_", "."),
            key.replace(".", "_")
        )

        for (k in keys) {
            if (propertiesExt.has(k)) return propertiesExt[k] as String
            if (properties.containsKey(k)) return properties[k] as String
        }
        return null
    }
}
