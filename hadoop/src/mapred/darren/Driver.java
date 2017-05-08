package mapred.darren;

import mapred.util.EasyJob;
import mapred.util.SimpleParser;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.Text;

/**
 * Created by Darren on 4/27/2017.
 */
public class Driver {

    public static void main(String args[]) throws Exception {
        SimpleParser parser = new SimpleParser(args);

        String input = parser.get("input");
        String output = parser.get("output");
        String tmpdir = parser.get("tmpdir");

        //run the two jobs to get reddit neighborhood
        getSubs(input, tmpdir + "/subs");
        getNeighborhood(tmpdir + "/subs", output);
    }

    private static void getSubs(String input, String output) throws Exception {
        EasyJob ejob = new EasyJob(new Configuration(), input, output, "Get Subreddit <User,Ascore> Pairs");
        ejob.setClasses(SubMapper.class, SubReducer.class, null);
        ejob.setMapOutputClasses(Text.class, Text.class);
        ejob.run();
    }

    private static void getNeighborhood(String input, String output) throws Exception {
        EasyJob ejob = new EasyJob(new Configuration(), input, output, "Get Neighborhood of User pairs");
        ejob.setClasses(NeighborMapper.class, NeighborReducer.class, null);
        ejob.setMapOutputClasses(Text.class, Text.class);
        ejob.run();
    }

}
