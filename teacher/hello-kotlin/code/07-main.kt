package ex07

fun main() {
    val result = 5.plusTen()
    println(result)
}

fun Int.plusTen(): Int {
    return this + 10
}