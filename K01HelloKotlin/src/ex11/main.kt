package ex11

// Lazy プロパティのサンプル
fun main() {
    val foo = Foo()
    println(foo.bar)
    println(foo.bar)
}

class Foo {
    var counter = 5.0

    val bar: Double by lazy {
        println("computed!")
        counter + 1
    }
}