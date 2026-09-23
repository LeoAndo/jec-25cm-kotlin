plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlinxSerialization)
}

android {
    namespace = "jp.ac.jec.a03githubsearch"
    compileSdk {
        version = release(37)
    }

    defaultConfig {
        applicationId = "jp.ac.jec.a03githubsearch"
        minSdk = 31
        targetSdk = 37
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            optimization {
                enable = false
            }
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
}

dependencies {
    implementation(libs.androidx.activity.ktx)
    implementation(libs.androidx.appcompat)
    implementation(libs.androidx.constraintlayout)
    implementation(libs.androidx.recyclerview)
    implementation(libs.androidx.cardview)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.core.ktx)
    implementation(libs.material)
    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.espresso.core)
    androidTestImplementation(libs.androidx.junit)

    // Kotlin Multiplatformのアプリ用テンプレートプロジェクトのktor依存関係を参考にした
    // https://github.com/Kotlin/KMP-App-Template/blob/main/composeApp/build.gradle.kts#L52-L54
    // https://github.com/Kotlin/KMP-App-Template/blob/main/composeApp/build.gradle.kts#L35
    implementation(libs.ktor.client.okhttp)
    implementation(libs.ktor.client.core)
    implementation(libs.ktor.client.content.negotiation)
    implementation(libs.ktor.serialization.kotlinx.json)
}