pluginManagement {
    repositories {
        google()
        gradlePluginPortal()
        maven("https://maven.pkg.jetbrains.space/public/p/compose/dev")
    }
    plugins {
        val kotlinVersion = extra["version.kotlin"] as String
        val agpVersion = extra["version.agp"] as String

        kotlin("multiplatform") version kotlinVersion
        kotlin("jvm") version kotlinVersion
        kotlin("android") version kotlinVersion
        id("com.android.library") version agpVersion
    }
}

rootProject.name = "log"
