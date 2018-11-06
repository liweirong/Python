package main

import Array._
import math._

object LCS {

  def main(args:Array[String]):Unit= {
    val A:String = "ABCBDAB"
    val B:String = "BDCABA"
    System.out.print(A, B)
    System.out.print("最长字串的长度是: "+lcs(A,B))
  }

  def lcs( a:String, b:String ) : Int = {
    val myMatrix = ofDim[Int](a.length+1,b.length+1)

    for (i <- 1 until a.length+1) {
      for (j <- 1 until b.length+1)
        if(a(i-1) == b(j-1)) {
          myMatrix(i)(j) = myMatrix(i-1)(j-1) + 1
        }else{
          myMatrix(i)(j) = max(myMatrix(i-1)(j), myMatrix(i)(j-1))
        }
    }

    /*for (i <- 0 until a.length+1){
      for (j <- 0 until b.length+1)
        print(myMatrix(i)(j)+"\t")
      println()
    }*/
    myMatrix(a.length)(b.length)
  }


}
