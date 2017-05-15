package mapred.darren;

import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

/**
 * Created by Darren on 5/6/2017.
 */
public class SubMapper extends Mapper<LongWritable, Text, Text, Text>{

    /**
     * Iterate over affinity score data
     * Map out subreddit to user,ascore pairs
     *
     * @param key
     * @param value
     * @param context
     * @throws IOException
     * @throws InterruptedException
     */
    @Override
    protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException{

        String[] data = value.toString().split(",");
        String user = data[0];
        String sub = data[1];
        String ascore = data[2];

        StringBuilder builder = new StringBuilder();
        builder.append(user + "," + ascore);

        context.write(new Text(sub), new Text(builder.toString()));
    }

}
