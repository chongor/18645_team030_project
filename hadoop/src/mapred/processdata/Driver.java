package mapred.processdata;

import mapred.util.SimpleParser;

/**
 * Created by Darren on 4/28/2017.
 */
public class Driver {

    public static void main(String args[]) throws Exception {
        SimpleParser parser = new SimpleParser(args);

        String input = parser.get("input");
        String output = parser.get("output");

    }

}
