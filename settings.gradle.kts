@file:Suppress("UnstableApiUsage")

pluginManagement {
    repositories {
        google()
        gradlePluginPortal()
        mavenCentral()
        maven("https://maven.pkg.jetbrains.space/public/p/compose/dev")
        maven("https://jitpack.io")
    }
    plugins {
//        kotlin("multiplatform").version(extra["version.kotlin"] as String)
//        kotlin("jvm").version(extra["version.kotlin"] as String)
//        kotlin("android").version(extra["version.kotlin"] as String)
//        id("com.android.application").version(extra["version.agp"] as String)
//        id("com.android.library").version(extra["version.agp"] as String)

        kotlin("multiplatform").version("1.8.20")
        kotlin("jvm").version("1.8.20")
        kotlin("android").version("1.8.20")
        id("com.android.application").version("7.3.0")
        id("com.android.library").version("7.3.0")
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.PREFER_SETTINGS)
    repositories {
        google()
        mavenCentral()
        maven("https://maven.pkg.jetbrains.space/public/p/compose/dev")
        maven("https://jitpack.io")
    }
}
rootProject.name = "log"
//include(":test:android")
//include(":test:desktop")
