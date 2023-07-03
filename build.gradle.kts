import java.util.*

plugins {
    kotlin("multiplatform")
    id("com.android.library")
    id("maven-publish")
}

group = Deps.lib.group
version = Deps.lib.version

kotlin {

    android {
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
        @Suppress("UNUSED_VARIABLE") val commonMain by getting
        @Suppress("UNUSED_VARIABLE") val jsMain by getting
        @Suppress("UNUSED_VARIABLE") val jvmMain by getting {
            dependencies {
                implementation(Deps.gson)
            }
        }
        @Suppress("UNUSED_VARIABLE") val androidMain by getting {
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
        minSdk = 21
        targetSdk = 31
        compileSdk = 31
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
    @Suppress("DEPRECATION")
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
val prop = Properties().apply {
    project.rootProject.file("local.properties").reader().use {
        load(it)
    }
}

publishing {
    val rName = prop["repsy.name"] as String
    val rKey = prop["repsy.key"] as String
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
