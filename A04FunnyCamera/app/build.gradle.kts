plugins {
    alias(libs.plugins.android.application)
}

android {
    namespace = "jp.ac.jec.a04funnycamera"
    compileSdk {
        version = release(37)
    }

    defaultConfig {
        applicationId = "jp.ac.jec.a04funnycamera"
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
    implementation(libs.androidx.core.ktx)
    implementation(libs.material)
    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.espresso.core)
    androidTestImplementation(libs.androidx.junit)

    // TODO STEP01: cameraxライブラリを追加する - START
    implementation(libs.camera.core)
    implementation(libs.camera.camera2) // これ追加しないと、実行時エラーになる
    implementation(libs.camera.lifecycle)
    implementation(libs.camera.view)
    // END
}