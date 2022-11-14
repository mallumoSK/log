plugins {
    kotlin("multiplatform")
    id("com.android.library")
    id("maven-publish")
}

group = "tk.mallumo"
version = "1.7.20-12.0.2"

val gson = "com.google.code.gson:gson:2.9.1"

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

    sourceSets {
        @Suppress("UNUSED_VARIABLE") val commonMain by getting {
            dependencies {
                implementation(gson)
            }
        }

        @Suppress("UNUSED_VARIABLE") val jvmMain by getting
        @Suppress("UNUSED_VARIABLE") val androidMain by getting

    }
}

android {
    compileSdk = 31
    sourceSets["main"].manifest.srcFile("src/androidMain/AndroidManifest.xml")

    defaultConfig {
        minSdkVersion(21)
        targetSdkVersion(31)
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }
    lintOptions.isAbortOnError = false
    lintOptions.isCheckReleaseBuilds = false
    lintOptions.disable("TypographyFractions", "TypographyQuotes")
}
apply("secure.gradle")

java {
    toolchain.languageVersion.set(JavaLanguageVersion.of(8))
}
