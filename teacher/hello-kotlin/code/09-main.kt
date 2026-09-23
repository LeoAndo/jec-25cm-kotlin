package ex09

// data classのサンプル
fun main() {
    val yamada = Person("yamada", 20) // data classで定義
    val yamada2 = Person("yamada", 20) // data classで定義
    val tanaka = Person2("tanaka", 20) // classで定義
    val tanaka2 = Person2("tanaka", 20) // classで定義

    // equalsの比較
    val yamadaEquals = yamada.equals(yamada2)
    val tanakaEquals = tanaka.equals(tanaka2)
    println("yamada.equals(yamada2): $yamadaEquals , tanaka.equals(tanaka2): $tanakaEquals")

    // hashCodeの比較
    val yamadaHash = yamada.hashCode()
    val yamada2Hash = yamada2.hashCode()
    println("yamada.hashCode(): $yamadaHash , yamada2.hashCode(): $yamada2Hash")

    val tanakaHash = tanaka.hashCode()
    val tanaka2Hash = tanaka2.hashCode()
    println("tanaka.hashCode(): $tanakaHash , tanaka2.hashCode(): $tanaka2Hash")

    // toStringの比較
    val yamadaString = yamada.toString()
    val yamada2String = yamada2.toString()
    println("yamada.toString(): $yamadaString , yamada2.toString(): $yamada2String")

    val tanakaString = tanaka.toString()
    val tanaka2String = tanaka2.toString()
    println("tanaka.toString(): $tanakaString , tanaka2.toString(): $tanaka2String")

    // componentN（プロパティの分解）
    val name = yamada.component1()
    val age = yamada.component2()
    println("name: $name, age: $age")

    // copy（年齢だけ変更）
    val copyYamada = yamada.copy(age = 25)
    println("copyYamada $copyYamada")

    val copyYamadaHash = copyYamada.hashCode()
    println("copyYamada.hashCode: $copyYamadaHash")
}

data class Person(val name: String, val age: Int)

class Person2(val name: String, val age: Int)