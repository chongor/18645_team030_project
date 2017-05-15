package mapred.allPairs;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;
import java.math.BigDecimal;

/**
 * Created by Darren on 5/1/2017.
 */
public class NeighborReducer extends Reducer<Text, Text, Text, Text>{

    /**
     * We sum the partial distances and calculate the actual distance between users
     * @param key
     * @param value
     * @param context
     * @throws IOException
     * @throws InterruptedException
     */
    @Override
    protected void reduce(Text key, Iterable<Text> value, Context context)
            throws IOException, InterruptedException {

        double distance = 0.0;
        //Sum the partial distance scores
        for(Text val : value) {
            distance += Double.parseDouble(val.toString());
        }

        //Use sqrt for Euclidian distance
        distance = Math.sqrt(distance);
        context.write(key, new Text(new BigDecimal(distance).toPlainString()));
    }

}
