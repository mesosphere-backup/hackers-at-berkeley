name := "micstream_spark"

resolvers ++= Seq(
  "Maven central" at "http://repo1.maven.org/maven2/",
  "Typesafe Releases" at "http://repo.typesafe.com/typesafe/releases/",
  "Sonatype OSS Releases" at "https://oss.sonatype.org/content/repositories/releases",
  "Java.net Maven2 Repository" at "http://download.java.net/maven/2/"
)

libraryDependencies ++= Seq(
  "org.apache.spark" % "spark-core_2.10" % "1.5.0",
  "org.apache.spark" % "spark-streaming_2.10" % "1.5.0",
  "org.apache.spark" % "spark-streaming-kafka_2.10" % "1.5.0",
  "com.datastax.cassandra" % "cassandra-driver-core" % "2.1.7"
)
