package mapred.processdata;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

/**
 * Created by Darren on 4/27/2017.
 */
public class SubCountReducer extends Reducer<Text, IntWritable, Text, IntWritable> {

    /**
     * Inputs: subreddit 1
     * Outputs: subreddit total_count
     */
    @Override
    protected void reduce(Text key, Iterable<IntWritable> value, Context context) throws IOException, InterruptedException {
        int count = 0;
        for (IntWritable v : value)
            count ++;

        context.write(key, new IntWritable(count));
    }

}
