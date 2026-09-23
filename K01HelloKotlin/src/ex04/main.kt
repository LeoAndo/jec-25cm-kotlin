package ex04

fun main() {
    val yamada = Person("Yamada", 20)
    println(yamada.name)
    println(yamada.age)
}

class Person(val name: String, val age: Int)