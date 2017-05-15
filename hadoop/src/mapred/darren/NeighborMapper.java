package mapred.darren;

import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by Darren on 5/1/2017.
 */
public class NeighborMapper extends Mapper<LongWritable, Text, Text, Text>{

    /**
     * Compute partial distances between user pairs
     * @param key
     * @param value
     * @param context
     * @throws IOException
     * @throws InterruptedException
     */
    @Override
    protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {

        String line = value.toString();
        String[] userAscores = line.split("\\s+", 2);
        List<UserObject> parsedScores = parseUserScores(userAscores[1]);

        int lastIndex = parsedScores.size()-1;
        UserObject userOne = parsedScores.get(lastIndex);
        String fName = userOne.getUser();
        String finalKey = null;
        double firstScore = userOne.getAscore();
        for (int i = 0; i < lastIndex; i++) {
            UserObject userTwo = parsedScores.get(i);
            String sName = userTwo.getUser();
            double secondScore = userTwo.getAscore();

            // Order the user pairs
            finalKey = fName + " " + sName;
            if (sName.compareTo(fName) < 0)
                finalKey = sName + " " + fName;

            // Partial distance calculation
            double sum = firstScore + secondScore;
            double distance = sum * sum;
            String distString = new BigDecimal(distance).toPlainString();

            // Write the finalKey and partial distance
            context.write(new Text(finalKey), new Text(distString));
        }



    }

    private List<UserObject> parseUserScores(String line) {
        List<UserObject> parsedScores = new ArrayList<UserObject>();
        String[] userAscores = line.split(";");

        for (String pair : userAscores) {
            String[] userAscore = pair.split(",");
            parsedScores.add(new UserObject(userAscore[0], Double.parseDouble(userAscore[1])));
        }

        return parsedScores;
    }

}
