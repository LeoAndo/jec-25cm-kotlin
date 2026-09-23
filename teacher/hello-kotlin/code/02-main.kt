package ex02

fun main() {
    val name1: String = "Saito"
    println(name1.count())

    var name2: String? = null
    println(name2?.count())
    name2 = "Tanaka"
    println(name2?.count())
}