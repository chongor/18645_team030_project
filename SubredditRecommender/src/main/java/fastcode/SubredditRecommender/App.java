package fastcode.SubredditRecommender;

import java.io.File;
import java.io.IOException;
import java.util.List;

import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.impl.model.file.FileDataModel;
import org.apache.mahout.cf.taste.impl.neighborhood.ThresholdUserNeighborhood;
import org.apache.mahout.cf.taste.impl.recommender.GenericUserBasedRecommender;
import org.apache.mahout.cf.taste.impl.similarity.PearsonCorrelationSimilarity;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.neighborhood.UserNeighborhood;
import org.apache.mahout.cf.taste.recommender.RecommendedItem;
import org.apache.mahout.cf.taste.recommender.UserBasedRecommender;
import org.apache.mahout.cf.taste.similarity.UserSimilarity;

/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args )
    {
    	DataModel model = null;
		try {
			model = new FileDataModel(new File("data/votes_100.csv"));
		} catch (IOException e2) {
			// TODO Auto-generated catch block
			e2.printStackTrace();
		}
    	UserSimilarity similarity = null;
		try {
			similarity = new PearsonCorrelationSimilarity(model);
		} catch (TasteException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		System.out.println("Similarity");
    	UserNeighborhood neighborhood = new ThresholdUserNeighborhood(0.1, similarity, model);
    	UserBasedRecommender recommender = new GenericUserBasedRecommender(model, neighborhood, similarity);
    	List<RecommendedItem> recommendations = null;
		try {
			recommendations = recommender.recommend(100, 10);
		} catch (TasteException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    	for (RecommendedItem recommendation : recommendations) {
    	  System.out.println(recommendation);
    	}
    	System.out.println("Finished");
    }
}
