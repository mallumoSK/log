import android.annotation.*

plugins {
    kotlin("multiplatform")
    id("com.android.library")
    id("maven-publish")
}

val toolkit by lazy {
    Toolkit.get(project)
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

    sourceSets["main"].manifest.srcFile("src/androidMain/AndroidManifest.xml")

    defaultConfig {
        namespace = "${Deps.lib.group}.${Deps.lib.artifact}"
        minSdk = 21
        targetSdk = 31
        compileSdk = 31
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_11
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

@Suppress("LocalVariableName")
publishing {
    val jfrog_name by toolkit
    val jfrog_key by toolkit
    val gpr_name = toolkit["gpr.name"] ?: System.getenv("GITHUB_USERNAME")
    val gpr_key = toolkit["gpr.key"] ?: System.getenv("GITHUB_TOKEN")

    repositories {
        if (jfrog_name != null && jfrog_key != null) {
            maven {
                name = "mallumo.jfrog.io"
                url = uri("https://mallumo.jfrog.io/artifactory/gradle-dev-local/")
                credentials {
                    username = jfrog_name
                    password = jfrog_key
                }
            }
        }
        println(gpr_name)
        println(gpr_key)
        if (gpr_name != null && gpr_key != null) {
            maven {
                name = "github"
                url = uri("https://maven.pkg.github.com/mallumosk/log")
                credentials {
                    username = gpr_name
                    password = gpr_key
                }
            }
        }
    }
    publications {
        register<MavenPublication>("gpr") {
            groupId = Deps.lib.group
            artifactId = Deps.lib.artifact
            version = Deps.lib.version
        }
    }
}
java {
    toolchain. languageVersion.set(JavaLanguageVersion.of(11))
}
