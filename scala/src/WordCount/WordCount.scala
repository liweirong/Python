package WordCount
import scala.io.Source
object WordCount {

  def main(args:Array[String]):Unit= {

    val lines = Source.fromFile("DataMining/1_MapReduce/wordCount/The_Man_of_Property.txt").getLines().toList

    System.out.print(lines.flatMap(_.split(" ")) // 按空格切开 -> List(Preface, “The, Forsyte, Saga”, was, the, ......)
      .map(x=>(x,1)) //进行map -> List((End,1), (The,1), (,1), (door.,1), (the,1), (slammed,1), (he,1)....)
      .groupBy(_._1).map(x=>(x._1,x._2.map(_._2).sum))
      .toList.sortBy(_._2)
      .reverse.slice(0,10)
     )
//总输出： List((the,5144), (of,3407), (to,2782), (and,2573), (a,2543), (he,2139), (his,1912), (was,1702), (in,1694), (had,1526))
  }
}
