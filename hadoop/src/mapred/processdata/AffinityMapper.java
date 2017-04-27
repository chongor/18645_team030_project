package mapred.processdata;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;
import java.util.Map;

/**
 * Created by Darren on 4/27/2017.
 */
public class AffinityMapper extends Mapper<Text, Text, Text, Text> {

    String[] subTotalComments;

    /*
     * Obtain list of subreddits with total number of comments posted in that subreddit
     */
    @Override
    protected void setup(Context context) throws IOException, InterruptedException {
        super.setup(context);
        Configuration config = context.getConfiguration();
        subTotalComments = config.get("subTotalComments").split("\n");
    }

    /*
     * Input:
     * Output:
     */
    @Override
    protected void map(Text key, Text value, Context context) throws IOException, InterruptedException {

    }

}
