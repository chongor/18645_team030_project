package mapred.util;

import org.apache.commons.cli.BasicParser;
import org.apache.commons.cli.ParseException;

import java.util.ListIterator;

/**
 * Created by Darren on 4/26/2017.
 */
public class Parser extends BasicParser {

    private boolean ignoreUnrecognizedOption;

    public Parser(final boolean ignoreUnrecognizedOption) {
        this.ignoreUnrecognizedOption = ignoreUnrecognizedOption;
    }

    @Override
    protected void processOption(final String arg, final ListIterator iter) throws ParseException{
        boolean hasOption = getOptions().hasOption(arg);

        if(hasOption || !ignoreUnrecognizedOption) {
            super.processOption(arg, iter);
        }
    }
}
