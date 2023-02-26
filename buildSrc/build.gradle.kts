import org.jetbrains.kotlin.gradle.tasks.*

plugins {
    `kotlin-dsl`
    `java-gradle-plugin`
}


repositories {
    mavenCentral()
}

tasks.withType<KotlinCompile> {
    kotlinOptions.jvmTarget = "11"
}
