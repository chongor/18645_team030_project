package mapred.util;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

import java.io.IOException;
import java.net.URI;
import java.util.LinkedList;
import java.util.List;

/**
 * Created by Darren on 4/29/2017.
 *
 * A class that wraps around Job and makes it easier to setup
 * It is reminiscent of the OptimizedJob from MiniProject 3, but for Hadoop 2.7.3
 *
 */
public class EasyJob{

    public Job job;
    private List<String> inputs;
    private String output;

    public EasyJob(Configuration conf, String input, String output, String jobName) throws IOException {

        this.job = job.getInstance(conf, jobName);
        this.inputs = new LinkedList<String>();
        this.inputs.add(input);
        this.output = output;
    }

    /**
     * Makes creating a job easier
     *
     * @throws IOException
     */
    private void setup() throws IOException {

        this.job.setJarByClass(EasyJob.class);

        //IO Format
        this.job.setInputFormatClass(TextInputFormat.class);
        this.job.setOutputFormatClass(TextOutputFormat.class);

        // Input file/dir
        for (String input : inputs) {
            TextInputFormat.addInputPath(this.job, new Path(input));
        }
        TextOutputFormat.setOutputPath(this.job, new Path(output));

        FileSystem fs = FileSystem.get(URI.create(output), this.job.getConfiguration());
        fs.delete(new Path(output), true);

        this.job.setJarByClass(EasyJob.class);

    }

    /**
     * Sets classes for mapper, reducer, and the combiner
     *
     * The reducer and combiner can be null, but there must be a mapper class
    */
    public void setClasses(Class<? extends Mapper<?, ?, ?, ?>> mapperClass,
                           Class<? extends Reducer<?, ?, ?, ?>> reducerClass,
                           Class<? extends Reducer<?, ?, ?, ?>> combinerClass) {
        this.job.setMapperClass(mapperClass);

        if (reducerClass != null)
            this.job.setReducerClass(reducerClass);

        if (combinerClass != null)
            this.job.setCombinerClass(combinerClass);
    }

    /**
     * Sets the output format of the map step.  Is usually Text or IntWritables
     * @param mapOutputKeyClass
     * @param mapOutputValueClass
     */
    public void setMapOutputClasses(Class<?> mapOutputKeyClass, Class<?> mapOutputValueClass) {
        this.job.setMapOutputKeyClass(mapOutputKeyClass);
        this.job.setMapOutputValueClass(mapOutputValueClass);
    }

    /**
     * Runs the job
     * @throws IOException
     * @throws InterruptedException
     * @throws ClassNotFoundException
     */
    public void run() throws IOException, InterruptedException, ClassNotFoundException {
        setup();

        long start = System.currentTimeMillis();
        this.job.waitForCompletion(true);
        long end = System.currentTimeMillis();

        System.out.println(String.format("Runtime for Job %s: %d ms", this.job.getJobName(), end - start));
    }

}
