plugins {
    kotlin("jvm")
    application
}

val toolkit by lazy {
    Toolkit.get(extensions = extensions.extraProperties)
}

kotlin {
    sourceSets.main {
        kotlin.srcDir("src/jvmMain/kotlin")
    }
}

dependencies {
//    implementation(project(":log"))
}

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(8))
    }
}

tasks.withType<org.jetbrains.kotlin.gradle.tasks.KotlinCompile> {
    kotlinOptions.jvmTarget = "1.8"
}

application {
    mainClass.set("MainKt")
}
