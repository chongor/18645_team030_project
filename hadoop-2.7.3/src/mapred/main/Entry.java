package mapred.main;

import mapred.util.SimpleParser;

/**
 * Created by Darren on 4/26/2017.
 */
public class Entry {
    public static void main(String args[]) throws Exception {
        SimpleParser parser = new SimpleParser(args);
        String program = parser.get("program");

        long start = System.currentTimeMillis();

        if(program.equals("processData"))
            mapred.processdata.Driver.main(args);

        else if(program.equals("allPairs"))
            mapred.allPairs.Driver.main(args);

        else {
            System.out.println("Unknown program!");
            System.exit(1);
        }

        long end = System.currentTimeMillis();
        System.out.println(String.format("Runtime for program %s: %d ms", program, end - start));
    }
}