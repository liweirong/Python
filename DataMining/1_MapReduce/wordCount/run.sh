HADOOP_CMD="/usr/local/src/hadoop-2.8.4/bin/hadoop"
STREAM_JAR_PATH="/usr/local/src/hadoop-2.8.4/share/hadoop/tools/lib/hadoop-streaming-2.8.4.jar"

#hadoop上的路径
INPUT_FILE_PATH_1="/The_Man_of_Property.txt"
OUTPUT_PATH="/output/wc"

#$HADOOP_CMD fs -rmr -skipTrash $OUTPUT_PATH

# Step 1.
$HADOOP_CMD jar $STREAM_JAR_PATH \
    -input $INPUT_FILE_PATH_1 \
    -output $OUTPUT_PATH \
    -mapper "python map.py" \
    -reducer "python red.py" \
    -file ./map.py \
    -file ./red.py