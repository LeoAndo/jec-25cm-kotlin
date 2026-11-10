package ex11

// Lazy プロパティのサンプル
fun main() {
    val foo = Foo()
    foo.counter = 10.0
    println(foo.bar)
    foo.counter = 20.0
    println(foo.bar)
}

class Foo {
    var counter = 5.0

    val bar: Double by lazy {
        println("computed!")
        counter + 1
    }
}