package mapred.darren;

import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

/**
 * Created by Darren on 5/1/2017.
 */
public class NeighborReducer extends Reducer<Text, DoubleWritable, Text, DoubleWritable>{

    /**
     * We sum the partial distances and calculate the actual distance between users
     * @param key
     * @param value
     * @param context
     * @throws IOException
     * @throws InterruptedException
     */
    @Override
    protected void reduce(Text key, Iterable<DoubleWritable> value, Context context)
            throws IOException, InterruptedException {

        double distance = 0.0;
        //Sum the partial distance scores
        for(DoubleWritable val: value) {
            distance += val.get();
        }

        //Use sqrt for Euclidian distance
        distance = Math.sqrt(distance);
        context.write(key, new DoubleWritable(distance));
    }

}
