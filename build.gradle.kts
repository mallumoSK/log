plugins {
    kotlin("multiplatform")
    id("com.android.library")
    id("maven-publish")
}

group = "tk.mallumo"
version = "1.7.20-12.0.0"

val gson = "com.google.code.gson:gson:2.9.1"

kotlin {

    android {
        publishLibraryVariants("release", "debug")
        publishLibraryVariantsGroupedByFlavor = true
    }
    jvm {
        compilations.all {
            kotlinOptions.jvmTarget = "11"
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
//        minSdk = 24
//        targetSdk = 33

        minSdkVersion(24)
        targetSdkVersion(31)
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
    lintOptions.isAbortOnError = false
    lintOptions.isCheckReleaseBuilds = false
    lintOptions.disable("TypographyFractions", "TypographyQuotes")
}
apply("secure.gradle")

