package ex08

class Foo {
    var counter = 0
        set(value) {
            println("setが呼ばれる： $value")
            if (value >= 0) {
                field = value
            }
        }
        get() {
            println("getが呼ばれる：　$field")
            return field
        }
}

fun main() {
    val foo = Foo()
    foo.counter = -1
    println(foo.counter)
    foo.counter = 10
    println(foo.counter)
}