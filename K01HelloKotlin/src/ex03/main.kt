package ex03

fun main() {
    val ret = sum(1, 2)
    println(ret)
    sum2(1, 2)
}

fun sum(a: Int, b: Int): Int {
    return a + b
}

fun sum2(a: Int, b: Int) {
    println(a + b)
}