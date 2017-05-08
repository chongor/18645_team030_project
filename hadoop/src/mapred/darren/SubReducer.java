package mapred.darren;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;
import java.math.BigDecimal;
import java.util.HashMap;
import java.util.Map;

/**
 * Created by Darren on 5/6/2017.
 */
public class SubReducer extends Reducer<Text, Text, Text, Text>{


    /**
     * Outputting subreddits with a list of users and their ascore for that sub
     * We are serializing them in a triangle like format writing out each time a new user is appended
     * This is to increase the number of mappers to increase processing speed
     *
     * @param key
     * @param value
     * @param context
     * @throws IOException
     * @throws InterruptedException
     */
    @Override
    protected void reduce(Text key, Iterable<Text> value, Context context)
            throws IOException, InterruptedException{

        Map<String, BigDecimal> ascores = new HashMap<String, BigDecimal>();

        //value = <sub,ascore> pairs
        for(Text v : value) {
            String[] data = v.toString().split(",");
            String user = data[0];
            BigDecimal ascore = new BigDecimal(data[1]);

            ascores.put(user, ascore);
        }

        /**
         * Serializing users with same subreddit subscriptions count as a string in following form:
         *
         * subreddit1 user1,ascore1;
         * subreddit1 user1,ascore1;user2,ascore2;
         * subreddit1 user1,ascore1;user2,ascore2;...;user3,ascore3;
         *
         * Creates larger intermediate files and as a result more map-tasks run by hadoop
         */
        StringBuilder builder = new StringBuilder();
        for (Map.Entry<String, BigDecimal> e : ascores.entrySet()){
            builder.append(e.getKey() + "," + e.getValue().toPlainString() + ";");
            context.write(key, new Text(builder.toString()));
        }

    }

}
