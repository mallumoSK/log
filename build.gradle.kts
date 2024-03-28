plugins {
    kotlin("multiplatform") version Deps.kotlin
    id("com.android.library") version Deps.agp
    id("maven-publish")
}

group = Deps.lib.group
version = Deps.lib.version

kotlin {

    js(IR)

    jvm {
        compilations.all {
            kotlinOptions.jvmTarget = "11"
        }
    }
    androidTarget {
        publishLibraryVariants("release")
        publishLibraryVariantsGroupedByFlavor = true
    }

    sourceSets {
        val commonMain by getting
        val jsMain by getting
        val jvmMain by getting {
            dependencies {
                implementation(Deps.gson)
            }
        }
        val androidMain by getting {
            dependencies {
                implementation(Deps.gson)
            }
        }
    }
}

@Suppress("UnstableApiUsage", "OldTargetApi")
android {

    sourceSets["main"].manifest.srcFile("src/androidMain/AndroidManifest.xml")

    defaultConfig {
        namespace = "${Deps.lib.group}.${Deps.lib.artifact}"
        compileSdk = 31
        minSdk = 21
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
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

publishing {
    val rName = propertiesLocal["repsy.name"]
    val rKey = propertiesLocal["repsy.key"]
    repositories {
        mavenLocal()
        maven {
            name = "repsy.io"
            url = uri("https://repo.repsy.io/mvn/${rName}/public")
            credentials {
                username = rName
                password = rKey
            }
        }
    }
}

repositories {
    google()
    mavenCentral()
    maven("https://maven.pkg.jetbrains.space/public/p/compose/dev")
    maven("https://repo.repsy.io/mvn/mallumo/public")
    gradlePluginPortal()
}

java {
    toolchain.languageVersion.set(JavaLanguageVersion.of(11))
}
