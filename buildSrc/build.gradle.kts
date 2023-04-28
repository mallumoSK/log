import org.jetbrains.kotlin.gradle.tasks.*

plugins {
    `kotlin-dsl`
    `java-gradle-plugin`
}

dependencies {
    implementation("org.jetbrains.kotlin:kotlin-gradle-plugin-api:1.8.0")
}

repositories {
    mavenCentral()
}

tasks.withType<KotlinCompile> {
    kotlinOptions.jvmTarget = "11"
}

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(11))
    }
}
