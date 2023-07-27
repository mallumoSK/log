plugins {
    kotlin("multiplatform")
    id("com.android.library")
    id("maven-publish")
}

group = Deps.lib.group
version = Deps.lib.version

kotlin {

    androidTarget {
        publishLibraryVariants("release")
        publishLibraryVariantsGroupedByFlavor = true
    }

    jvm {
        compilations.all {
            kotlinOptions.jvmTarget = "11"
        }
    }

    js(IR)

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

repositories {
    google()
    mavenCentral()
    maven("https://maven.pkg.jetbrains.space/public/p/compose/dev")
}

@Suppress("UnstableApiUsage", "OldTargetApi")
android {

    sourceSets["main"].manifest.srcFile("src/androidMain/AndroidManifest.xml")

    defaultConfig {
        namespace = "${Deps.lib.group}.${Deps.lib.artifact}"
        minSdk = 21
        compileSdk = 31
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
        maven {
            name = "repsy.io"
            url = uri("https://repo.repsy.io/mvn/${rName}/public")
            credentials {
                username = rName
                password = rKey
            }
        }
    }
    publications {
        create<MavenPublication>("maven") {
            groupId = Deps.lib.group
            artifactId = Deps.lib.artifact
            version = Deps.lib.version
        }
    }
}

java {
    toolchain.languageVersion.set(JavaLanguageVersion.of(11))
}
