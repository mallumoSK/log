plugins {
    `kotlin-dsl`
    `java-gradle-plugin`
}

dependencies {
    implementation("org.jetbrains.kotlin:kotlin-gradle-plugin-api:1.9.0")
}

repositories {
    mavenCentral()
}

java {
    toolchain.languageVersion.set(JavaLanguageVersion.of(11))
}
