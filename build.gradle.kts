import android.annotation.*

plugins {
    kotlin("multiplatform")
    id("com.android.library")
    id("maven-publish")
}

group = "tk.mallumo"
version = "1.8.10-13.0.0"

kotlin {

    android {
        publishLibraryVariants("release")
        publishLibraryVariantsGroupedByFlavor = true
    }
    jvm {
        compilations.all {
            kotlinOptions.jvmTarget = "1.8"
        }
    }
    js(IR)

    sourceSets {
        @Suppress("UNUSED_VARIABLE") val commonMain by getting
        @Suppress("UNUSED_VARIABLE") val jsMain by getting
        @Suppress("UNUSED_VARIABLE") val jvmMain by getting {
            dependencies {
                implementation("com.google.code.gson:gson:${extra["version.gson"]}")
            }
        }
        @Suppress("UNUSED_VARIABLE") val androidMain by getting {
            dependencies {
                implementation("com.google.code.gson:gson:${extra["version.gson"]}")
            }
        }
    }
}

@Suppress("UnstableApiUsage", "OldTargetApi")
android {
    compileSdk = 31
    sourceSets["main"].manifest.srcFile("src/androidMain/AndroidManifest.xml")

    defaultConfig {
        namespace = "tk.mallumo.log"
        minSdk = 21
        targetSdk = 31
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }
    lintOptions {
        isCheckReleaseBuilds = false
        isAbortOnError = false
        disable("TypographyFractions", "TypographyQuotes")
    }
    lint {
        abortOnError = false
        checkReleaseBuilds = false
        disable += setOf("TypographyFractions", "TypographyQuotes")
    }
    buildFeatures {
        buildConfig = false
    }
}
apply("secure.gradle")

java {
    toolchain.languageVersion.set(JavaLanguageVersion.of(8))
}
