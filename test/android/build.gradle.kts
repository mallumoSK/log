plugins {
    id("org.jetbrains.compose")
    id("com.android.application")
    kotlin("android")
}

val toolkit by lazy {
    Toolkit.get(extensions = extensions.extraProperties)
}


group = "tk.mallumo"
version = "1.0"

val lifecycle_version = "2.5.1"
dependencies {
    implementation(project(":test:common"))

    implementation("androidx.core:core-ktx:1.9.0")
    implementation("androidx.appcompat:appcompat:1.5.1")
//    implementation("com.google.android.material:material:1.7.0")

//    implementation("androidx.lifecycle:lifecycle-viewmodel-ktx:$lifecycle_version")

    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:${toolkit["version.coroutines"]}")
    implementation("androidx.compose.ui:ui:${toolkit["version.compose.android"]}")
    implementation("androidx.compose.material:material:${toolkit["version.compose.android"]}")
//    implementation("androidx.compose.ui:ui-tooling-preview:${toolkit["version.compose"]}")
    implementation("androidx.activity:activity-compose:${toolkit["version.compose.android.activity"]}")

    implementation("tk.mallumo:log:${toolkit["version.log"]}")
    implementation("tk.mallumo:utils:${toolkit["version.utils"]}")

    implementation("tk.mallumo:navigation:${toolkit["version.navigation"]}")

    androidTestImplementation("androidx.test.ext:junit:1.1.3")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.4.0")
    androidTestImplementation("androidx.compose.ui:ui-test-junit4:${toolkit["version.compose.android"]}")
    androidTestImplementation("androidx.test:core:1.4.0")
    androidTestImplementation("androidx.appcompat:appcompat:1.5.1")

    debugImplementation("androidx.compose.ui:ui-test-manifest:${toolkit["version.compose.android"]}")
}

@Suppress("UnstableApiUsage")
android {
    compileSdk = 33
    defaultConfig {

        applicationId = "tk.mallumo.android"
        minSdk = 24
        targetSdk = 33
        versionCode = 1
        versionName = "1.0"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"

    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
    buildFeatures.compose = true
    composeOptions.kotlinCompilerExtensionVersion = toolkit["version.compose.android.compiller"]

    namespace = "tk.mallumo.android"
    @Suppress("UnstableApiUsage")
    buildTypes {
        release {
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
            signingConfig = signingConfigs.create("release") {
                keyAlias = "sampledata"
                keyPassword = "sampledata"
                storeFile = file("${projectDir.absolutePath}/../sampledata/store.keystore")
                storePassword = "sampledata"
            }
        }
    }
    sourceSets {
//        getByName("debug") {
//            java.srcDirs("../common/build/generated/ksp/common/commonMain/kotlin")
//        }
    }
    packagingOptions {
        resources {
            excludes.add("/META-INF/{AL2.0,LGPL2.1}")
        }
    }
}
